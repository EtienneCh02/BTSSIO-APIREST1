import tkinter as tk
from tkinter import ttk, messagebox
import requests

# ==============================
# CONFIGURATION
# ==============================
LOGIN_URL = "http://127.0.0.1:8000/login"
API_URL = "http://127.0.0.1:8000/v_livres"
API_KEY = "tp-secret-key"

#UTILISATEURS = {
#    "admin": "admin123",
#    "user": "user123"
#}

# ==============================
# APPLICATION
# ==============================
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client API - Gestion des livres")
        self.geometry("800x500")
        self.resizable(False, False)

        self.frame_login()

    # ==========================
    # ÉCRAN LOGIN
    # ==========================
    def frame_login(self):
        self.clear_window()

        frame = ttk.Frame(self, padding=30)
        frame.pack(expand=True)

        ttk.Label(frame, text="Connexion", font=("Arial", 16)).pack(pady=10)

        ttk.Label(frame, text="Utilisateur").pack(anchor="w")
        self.entry_user = ttk.Entry(frame)
        self.entry_user.pack(fill="x", pady=5)

        ttk.Label(frame, text="Mot de passe").pack(anchor="w")
        self.entry_password = ttk.Entry(frame, show="*")
        self.entry_password.pack(fill="x", pady=5)

        ttk.Button(frame, text="Se connecter", command=self.login).pack(pady=20)

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_password.get()

        try:
            response = requests.post(
                LOGIN_URL,
                data={
                    "username": user,
                    "password": pwd
                }
            )
            response.raise_for_status()
            data = response.json()
            self.token = data["access_token"]
            self.frame_recherche()

        except Exception as e:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    # ==========================
    # ÉCRAN RECHERCHE
    # ==========================
    def frame_recherche(self):
        self.clear_window()

        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        # Barre de recherche
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", pady=10)

        ttk.Label(search_frame, text="Mot-clé :").pack(side="left")
        self.entry_search = ttk.Entry(search_frame)
        self.entry_search.pack(side="left", padx=5, fill="x", expand=True)

        ttk.Button(search_frame, text="Rechercher", command=self.rechercher).pack(side="left")

        # Tableau de résultats
        columns = ("Auteurs", "Titre", "Genres", "Editeur", "Stock")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True, pady=10)

    # ==========================
    # RECHERCHE API
    # ==========================
    def rechercher(self):
        mot_cle = self.entry_search.get().lower()
        headers = {
            #"X-API-Key": API_KEY
            "Authorization": f"Bearer {self.token}"
        }
        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()
            livres = response.json()
        except Exception as e:
            messagebox.showerror("Erreur API", str(e))
            return

        # Nettoyage tableau
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filtrage local
        for livre in livres:
            titre = str(livre.get("Titre", "")).lower()
            if mot_cle in titre:
                self.tree.insert("", "end", values=(
                    livre.get("Auteurs"),
                    livre.get("Titre"),
                    livre.get("Genres"),
                    livre.get("Editeur"), 
                    livre.get("Stock")
                ))

    # ==========================
    # UTILITAIRE
    # ==========================
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


# ==============================
# LANCEMENT
# ==============================
if __name__ == "__main__":
    app = Application()
    app.mainloop()
