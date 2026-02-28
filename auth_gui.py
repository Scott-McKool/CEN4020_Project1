import tkinter as tk
from tkinter import messagebox
from auth import login, register, database_connection
from game import Level1
from gui import gameWindow


class AuthWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login/Register")
        self.geometry("400x300")


        # for username
        tk.Label(self, text= "Username:").pack() # text label on the window that says Username:, pack() places the text on the window
        self.username_entry = tk.Entry(self) # input field for username
        self.username_entry.pack() 

        # for password
        tk.Label(self, text = "Password").pack()
        self.password_entry = tk.Entry(self, show = "*") # password input field hidden with *
        self.password_entry.pack()

        # buttons
        tk.Button(self, text = "Login", command = self.login).pack() # login button
        tk.Button(self, text = "Register", command = self.register).pack() # register button


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        db_login = login(username, password)

        if db_login == "Login successful":
            self.destroy()
            newGame = Level1(username, 5)
            gameWindow(newGame)

        else:
            messagebox.showerror("Error", "Invalid credentials")



    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db_register = register(username, password)

        if db_register == "Account created successfully":
            messagebox.showinfo("Success, account was created", "Now Login")

        else:
            messagebox.showerror("Error, username is taken")


if __name__ == "__main__":
    database_connection
    game = AuthWindow()
    game.mainloop()