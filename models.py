# models.py

import os

class User:
    def __init__(self, user_name, user_password, quiz_scores=None):
        self.user_name = user_name
        self.user_password = user_password
        self.quiz_scores = quiz_scores if quiz_scores is not None else {}

    def add_quiz_score(self, quiz_topic, quiz_score):
        self.quiz_scores[quiz_topic] = quiz_score

    @staticmethod
    def load_users(file_name='users_data.txt'):
        users_dict = {}
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                for line in file:
                    user_name, user_password, scores_str = line.strip().split(',')
                    scores_dict = eval(scores_str)
                    users_dict[user_name] = User(user_name, user_password, scores_dict)
        return users_dict

    @staticmethod
    def save_users(users_dict, file_name='users_data.txt'):
        with open(file_name, 'w') as file:
            for user in users_dict.values():
                file.write(f"{user.user_name},{user.user_password},{user.quiz_scores}\n")

class Quiz:
    def __init__(self):
        self.quiz_questions = {
            "DBMS": [
                {"question": "What does DBMS stand for?", "options": ["Database Management System", "Data Mining System", "Database Maintenance System", "Data Management Software"], "answer": "Database Management System"},
                {"question": "Which of these is a database management system?", "options": ["Oracle", "Linux", "Python", "HTML"], "answer": "Oracle"},
                {"question": "SQL stands for?", "options": ["Structured Query Language", "Stylish Question Language", "Statement Query Language", "Standard Query Language"], "answer": "Structured Query Language"},
                {"question": "Which SQL command is used to remove a table?", "options": ["DELETE", "DROP", "REMOVE", "ERASE"], "answer": "DROP"},
                {"question": "A primary key can contain null values.", "options": ["True", "False"], "answer": "False"}
            ],
            "DSA": [
                {"question": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "LinkedList", "Array"], "answer": "Stack"},
                {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "answer": "O(log n)"},
                {"question": "In which data structure, elements are added and removed from only one end?", "options": ["Stack", "Queue", "Deque", "Array"], "answer": "Stack"},
                {"question": "Which of the following is a non-linear data structure?", "options": ["Array", "LinkedList", "Queue", "Tree"], "answer": "Tree"},
                {"question": "DFS stands for?", "options": ["Depth First Search", "Depth First Sort", "Data First Search", "Data First Sort"], "answer": "Depth First Search"}
            ],
            "Python": [
                {"question": "Who developed Python programming language?", "options": ["Dennis Ritchie", "Guido van Rossum", "James Gosling", "Bjarne Stroustrup"], "answer": "Guido van Rossum"},
                {"question": "Which keyword is used to define a function in Python?", "options": ["def", "function", "func", "define"], "answer": "def"},
                {"question": "What is the output of 3**2 in Python?", "options": ["6", "9", "3", "12"], "answer": "9"},
                {"question": "Which of the following is not a keyword in Python?", "options": ["pass", "eval", "assert", "nonlocal"], "answer": "eval"},
                {"question": "Python is a ____.", "options": ["Compiled language", "Interpreted language", "Both compiled and interpreted", "None of the above"], "answer": "Interpreted language"}
            ]
        }

    def get_questions(self, topic):
        return self.quiz_questions.get(topic, [])
