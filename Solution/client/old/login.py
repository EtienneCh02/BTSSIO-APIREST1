import tkinter as tk
from tkinter import messagebox
from api import login

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Connexion API")

        tk.Label(root, text="Utilisateur").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(root, text="Mot de passe").grid(row=1, column=0, padx=5, pady=5)

        self.user_entry = tk.Entry(root)
        self.pwd_entry = tk.Entry(root, show="*")

        self.user_entry.grid(row=0, column=1)
        self.pwd_entry.grid(row=1, column=1)

        tk.Button(root, text="Connexion", command=self.try_login).grid(
            row=2, column=0, columnspan=2, pady=10
        )

    def try_login(self):
        user = self.user_entry.get()
        pwd = self.pwd_entry.get()

        auth = login(user, pwd)
        if auth:
            self.root.destroy()
            self.on_success(auth)
        else:
            messagebox.showerror("Erreur", "Identifiants invalides")
