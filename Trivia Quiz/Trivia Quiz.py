import requests
import json
import random
import pprint as pp
import html

# GET CATEGORY RESPONSE 
cat_response = requests.get("https://opentdb.com/api_category.php")
#print(cat_response.status_code)
#print(f"cat_response = {cat_response}")
categories = cat_response.json()
#print(f'categories = {categories}')
cat_options = categories['trivia_categories']
#print(f'cat_options = {cat_options}')

SET GAME CATEGORY & GET RESPONSE
def set_game_cat():
    while True:
        game_cat = input('Pick a number from 10-20 to choose the quiz category: ')
        try:
            game_cat = int(game_cat)
        except:
            print("<ERROR> Please pick a number from 10-20 to choose the quiz category \n")
            continue
        if game_cat < 10 or game_cat > 20:
            print("<ERROR> Please pick a number from 10-20 to choose the quiz category \n")
            continue
        break
    
    for i in cat_options:
        if i['id'] == game_cat:
            print(f'You are in category {i['id']} < {i['name']} >\n')
            cat_name = i['name']

    q_response = requests.get(f'https://opentdb.com/api.php?amount=10&category={game_cat}&type=multiple')
    #print(q_response.status_code)
    questions = q_response.json()
    question_bank = questions['results']

    return (game_cat, cat_name, question_bank)


TEMPLATE MESSAGES
success_messages = [
    "Spot on! That's the rights answer!",
    "Brillant! You nailed it!",
    "Great job! That's the correct answer!",
    "You got it! Good job!",
    "You are right! Nice work!",
    "That's the one! Well done!",
    "Fantastic! That's the correct answer"
] 

incorrect_messages = [
    "Unfortunately, that's not the right answer.",
    "Opps, that's the wrong answer.", 
    "Not quite right. Better luck next time!",
    "That's not it. Good effort!",
    "That's not it. Nice try!",
    "Not the answer we were looking for." 
]

## FEATURE: HINTS 50/50
## Input >> 4 display_options 
## Output >> 2 remaining_options (the correct answer + 1 randomised item from the incorrect answers)
def hint(correct_answer, incorrect_answers):
    remaining_options = {}
    # pick a random choice among the incorrect answers
    random_key = random.choice(list(incorrect_answers.keys()))
    random_value = incorrect_answers[random_key]
    random_option = {random_key:random_value}

    remaining_options.update(random_option)
    remaining_options.update(correct_answer)
    sorted_remaining_options = dict(sorted(remaining_options.items()))

    return sorted_remaining_options

## PRINT DECODE TEXT
def print_decode(x):
    print(html.unescape(x))

## PRINT DISPLAY OPTIONS WITHOUT BRACKET
def print_options(display_options):
    for k, v in display_options.items():
        print_decode(f"{k}: {v}")
    return

# MAIN GAME
def main(question_bank):
    global hint_used
    global question_correct
    global question_wrong
  

    active_question = random.choice(question_bank)

    for i in range(10):
        active_question = random.choice(question_bank)    
        answer_list = active_question['incorrect_answers'] + [active_question['correct_answer']]
        random.shuffle(answer_list)
        
        # Add option_label A, B, C, D to answers 
        
        display_options = dict(zip(option_labels, answer_list))

        print_decode(f'\nQuestion {i+1}: {active_question['question']}\n')
        print_options(display_options) 

        # Make a libraries to store correct answer and incorrect answer
        for k, v in display_options.items():
            if v == active_question["correct_answer"]:
                correct_answer = {k:v}
            else:
                new_item = {k:v}
                incorrect_answers.update(new_item)
        print()

        # User input answer
        print("Select A-D, or type HINT to elimiate answers")
        user_input = input('Answer or HINT >> ').upper()
        
        # Check user answer
        
        if user_input == "HINT":
            while hint_used < hint_quota:
                hint_used += 1
                print(f"\n**** Two answers left. ****            Hints used:[{hint_used}/{hint_quota}]")
                sorted_remaining_options = hint(correct_answer, incorrect_answers)
                print_options(sorted_remaining_options)
                user_input = input ("\nAnswer >> ").upper()
                break
            else: 
                print('You have used all your hints.')
                user_input = input ("Answer >> ").upper()
            
        if user_input not in option_labels:
            print('\n<ERROR!> Select A-D, or type HINT to elimiate answers')
            user_input = input('Answer or HINT >> ').upper()

        if [user_input] == list(correct_answer.keys()):
            print()
            print(random.choice(success_messages), '\n')
            question_correct += 1
        else:
            print()
            print(random.choice(incorrect_messages),"\n") 
            print('The correct answer is', end = " ") 
            print_options(correct_answer)
            question_wrong += 1

        question_bank.remove(active_question)       #remove the question asked from the question bank to avoid repetition 
        display_options.clear()         #clear display_options to store answers for the next quesitons
        incorrect_answers.clear()

        next = input('\n[Press <ENTER> to continue]')

        print("-------------------------------------------------")
    return (question_correct, question_wrong, hint_used)

# WARM-UP GAME
def warmup():
    print("\nIf the STRESSED splled backward is DESSERT,")
    print(f'What is {'HINTS'[::-1]} spelled backward?')
    warm_up_answer = input("").upper()

    if warm_up_answer == 'HINTS':
        print("\nYou've got it!")
        print(f'You will have {hint_quota} hints in this quiz.\nJust type HINT when you need one! USE IT WISELY!\n')
    else: 
        print('Not quite....The answer is HINTS!')
        print(f'You will have {hint_quota} hints in this quiz.\nJust type HINT when you need one! USE IT WISELY!\n')  

    next = input('Press <ENTER> when you are ready')
    return

# SCORECARD
def scorecard(user_name, game_cat, cat_name, question_correct, question_wrong, hint_used):
    score = question_correct *10
    print(f"\nWell done {user_name}!")
    print("You've completed all 10 questions!\n")
    print("Here is your scorecard:")
    print(f'Category: {game_cat} < {cat_name} >')
    print(f"Correct answers: {question_correct} (10 points each)")
    print(f"Incorrect answers: {question_wrong}")
    print(f"Total points: {score} points")
    print(f"Hints used: {hint_used}/{hint_quota}")
    log_msg = f"user_name:{user_name}, game_cat:{game_cat}, cat_name:{cat_name}, question_correct:{question_correct}, question_wrong:{question_wrong}, score:{score}, hint_used:{hint_used}, hint_quota:{hint_quota}"
    return log_msg

## GLOBAL VARIABLE
display_options = {}
option_labels = ['A', 'B', 'C', 'D']
incorrect_answers = {}
elim_list = []
hint_quota = 3
hint_used = 0
question_correct = 0
question_wrong = 0

## WELCOME MESSAGE & SET GAME CATEGORY
print('WELCOME TO TRIVIA QUIZ CHALLENGE!\n')
user_name = input("What's your name? ").capitalize()

print(f'\nHello {user_name}!\n')

game_cat, cat_name, question_bank = set_game_cat()

print('There are 10 multiple choice questions in this quiz, each one carries 10 points.')
print('You will have 3 HINTS. Each hint will eliminate 2 incorrects answers for you.\n')

print("\nBefore we start, let's do a warm up test! \n")
input("Press <ENTER> when you are ready!")

warmup()
main(question_bank)
log_msg = scorecard(user_name, game_cat, cat_name, question_correct, question_wrong, hint_used)

# CREATE A SCOREBOARD AND LOG USERS' SCORES
with open("Assignment_2/trivia_challenge_scoreboard.txt","a") as log:
    log.write(log_msg + "\n")