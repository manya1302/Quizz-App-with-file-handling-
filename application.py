# app.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models import User, Quiz

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("600x400")
        self.root.configure(bg='#e1bee7')  # Light purple background
        self.users_dict = User.load_users()
        self.quiz = Quiz()
        self.current_user = None
        self.create_styles()
        self.create_home_page()

    def create_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 12), background='#9575cd', foreground='white')
        style.map('TButton', background=[('active', '#7e57c2')])
        style.configure('TLabel', background='#e1bee7', foreground='#4a148c', font=('Helvetica', 12))
        style.configure('Header.TLabel', background='#d1c4e9', foreground='#4a148c', font=('Helvetica', 16, 'bold'))
        style.configure('TEntry', background='#fff', foreground='#4a148c', font=('Helvetica', 12))

    def create_home_page(self):
        self.clear_window()
        ttk.Label(self.root, text="Welcome to the Quiz Application", style='Header.TLabel').pack(pady=20)
        ttk.Button(self.root, text="Register", command=self.create_register_page, width=20).pack(pady=10)
        ttk.Button(self.root, text="Login", command=self.create_login_page, width=20).pack(pady=10)

    def create_register_page(self):
        self.clear_window()
        ttk.Label(self.root, text="Register", style='Header.TLabel').pack(pady=20)
        ttk.Label(self.root, text="Username").pack(pady=5)
        username_entry = ttk.Entry(self.root)
        username_entry.pack(pady=5)
        ttk.Label(self.root, text="Password").pack(pady=5)
        password_entry = ttk.Entry(self.root, show='*')
        password_entry.pack(pady=5)
        ttk.Button(self.root, text="Register", command=lambda: self.register(username_entry.get(), password_entry.get())).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_home_page).pack(pady=10)

    def create_login_page(self):
        self.clear_window()
        ttk.Label(self.root, text="Login", style='Header.TLabel').pack(pady=20)
        ttk.Label(self.root, text="Username").pack(pady=5)
        username_entry = ttk.Entry(self.root)
        username_entry.pack(pady=5)
        ttk.Label(self.root, text="Password").pack(pady=5)
        password_entry = ttk.Entry(self.root, show='*')
        password_entry.pack(pady=5)
        ttk.Button(self.root, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get())).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.create_home_page).pack(pady=10)

    def create_welcome_page(self):
        self.clear_window()
        ttk.Label(self.root, text=f"Welcome, {self.current_user.user_name}", style='Header.TLabel').pack(pady=20)
        ttk.Button(self.root, text="DBMS Quiz", command=lambda: self.create_quiz_page("DBMS")).pack(pady=10)
        ttk.Button(self.root, text="DSA Quiz", command=lambda: self.create_quiz_page("DSA")).pack(pady=10)
        ttk.Button(self.root, text="Python Quiz", command=lambda: self.create_quiz_page("Python")).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def create_quiz_page(self, topic):
        self.clear_window()
        quiz_questions = self.quiz.get_questions(topic)
        total_score = [0]

        def next_question(index):
            if index < len(quiz_questions):
                self.clear_window()
                q = quiz_questions[index]
                ttk.Label(self.root, text=q["question"], font=("Helvetica", 14), background='#e1bee7', foreground='#4a148c').pack(pady=10, anchor='w')
                for i, option in enumerate(q["options"]):
                    ttk.Button(self.root, text=option, command=lambda i=i: check_answer(i, q["answer"], index+1)).pack(pady=5, anchor='w')
            else:
                self.create_result_page(total_score[0], len(quiz_questions), topic)

        def check_answer(selected, answer, next_index):
            if quiz_questions[next_index-1]["options"][selected] == answer:
                total_score[0] += 1
            next_question(next_index)

        next_question(0)

    def create_result_page(self, score, total, topic):
        self.clear_window()
        self.current_user.add_quiz_score(topic, score)
        User.save_users(self.users_dict)
        ttk.Label(self.root, text="Quiz Completed!", style='Header.TLabel').pack(pady=20)
        ttk.Label(self.root, text=f"Your score: {score}/{total}").pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def register(self, user_name, user_password):
        if user_name in self.users_dict:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            self.users_dict[user_name] = User(user_name, user_password)
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.create_login_page()

    def login(self, user_name, user_password):
        if user_name in self.users_dict and self.users_dict[user_name].user_password == user_password:
            self.current_user = self.users_dict[user_name]
            self.create_welcome_page()
        else:
            messagebox.showerror("Error", "Login failed. Check your username and/or password.")

    def logout(self):
        self.current_user = None
        self.create_home_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
