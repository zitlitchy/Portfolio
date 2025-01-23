## Assignment 2 - Trivia Quiz Challenge
Each user can choose questions from 11 categories from the Open Trivia Database.
Each user have to answer 10 questions each time. 
They have 3 hints for each game, where 2 incorrect answer will be elimiated from the answers.
The game result will be logged in logged in trivia_challenge_scoreboard.txt

The game is dividied into four parts:
1. Welcome message
2. Warm-up game
3. Main game
4. Scorecard

## Details
Two APIs from Open Trivia Database are used here: 
1. ```cat_options```: The library of question category
2. ```question_bank```: The library of questions 

### 1. Welcome and set game category
This part is for collecting user name, and let user choose the game category

### 2. Warm-up game
A warm-up game to remind user of their three hints.

### 3. Main game logic
1. Questions are display randomly from question bank ```random.choice(question_bank) ```
2. Compile correct answer and incorrect answer into one list, then randomised the order of answer ```random.shuffle(answer_list)```
3. Add labels A-D to each answer for the ease of user input, the data will be stored in ```display_options```
4. Seprate all answer options into a ```correct_answer``` library and a ```incorrect_answer``` library
5. If user request a hint, ```hint()```will remove the first incorrect answer user first chose, then random choose one answer from the  ```incorrect_answer``` list and combine that with the ```correct_answer```. The two ```remaining_options``` will then be sorted by their label. User will have 50/50 chance to getting the right answer.
6. Counters are set to count the numebr of correct answer, incorrect answer and hint_requests in each loop
7. If the user's request hints more then the hint_quota, an error message will be displayed
7. A random choice of message will be selected from the template messages when user success or fail
8. ```display_options``` and ```ìncorrect_answer```will be clear in each question loop so to store new values as user enter a new question

### 4. Scorecard and logs
A scoredcard will be created at the end of the game.
User's performance will be logged in ```trivia_challenge_scoreboard.txt```

### 5. Formatting and display
Multiple functions were defined to format question and answer display
1. ```print_decode(x)```: change html code to normal display
2. ```print_options(display_options)```: print answer options without bracket