questions = [
    {
        "question": "What is the output of print(2 * 3)?",
        "options": ["5", "6", "9", "0"],
        "answer": "6"
    },
    {
        "question": "Which of the following is a mutable data type in Python?",
        "options": ["List", "Tuple", "String", "Integer"],
        "answer": "List"
    },
    {
        "question": "What is the correct way to create a function in Python?",
        "options": ["function myFunc():", "def myFunc():", "create myFunc():", "function:myFunc"],
        "answer": "def myFunc():"
    },
    {
        "question": "Which keyword is used to check for membership in a list?",
        "options": ["for", "while", "in", "if"],
        "answer": "in"
    },
    {
        "question": "Which of these is NOT a Python data type?",
        "options": ["float", "str", "char", "int"],
        "answer": "char"
    }
]

def run_quiz():
    score = 0
    total_questions = len(questions)
    user_answers = []

    i = 0
    for q in questions:
        i += 1
        print(f"Question {i}: {q['question']}")

        j = 1
        for option in q['options']:
            print(f"{j}. {option}")
            j += 1

        answer = input("Please enter the number corresponding to your answer: ")

        while not answer.isdigit() or int(answer) < 1 or int(answer) > len(q['options']):
            answer = input("Invalid input. Please enter a valid option number: ")

        selected_option = q['options'][int(answer) - 1]
        user_answers.append(selected_option)

        if selected_option == q['answer']:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect! The correct answer was: {q['answer']}\n")

    display_results(score, total_questions, user_answers)

def display_results(score, total_questions, user_answers):
    print(f"Your final score is {score}/{total_questions}.\n")
    print("Correct Answers:")
    i = 1
    for q in questions:
        print(f"{i}. {q['answer']} (Your answer: {user_answers[i - 1]})")
        i += 1

if __name__ == "__main__":
    run_quiz()
