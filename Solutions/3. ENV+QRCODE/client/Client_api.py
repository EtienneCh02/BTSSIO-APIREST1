import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pyotp
import qrcode
from PIL import Image, ImageTk
import io
import json
import os

# ==============================
# CONFIGURATION
# ==============================
API_URL = "http://127.0.0.1:8000/v_livres"
API_KEY = "tp-secret-key"
SECRET_FILE = "totp_secrets.json"

UTILISATEURS = {
    "admin": "admin123",
    "user": "user123"
}

# ==============================
# GESTION DES SECRETS TOTP
# ==============================
def load_secrets():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as f:
            return json.load(f)
    return {}

def save_secrets(secrets):
    with open(SECRET_FILE, "w") as f:
        json.dump(secrets, f)

secrets = load_secrets()

# ==============================
# APPLICATION
# ==============================
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client API - Gestion des livres")
        self.geometry("800x500")
        self.resizable(False, False)
        self.current_user = None
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
        if user in UTILISATEURS and UTILISATEURS[user] == pwd:
            self.current_user = user
            if user in secrets:
                # Clé déjà existante → passer directement à saisie 2FA
                self.frame_2fa_input()
            else:
                # Première connexion → générer QR code
                self.frame_2fa_qr()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    # ==========================
    # ÉCRAN QR CODE (première fois)
    # ==========================
    def frame_2fa_qr(self):
        self.clear_window()
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Scanner le QR Code avec Google Authenticator", font=("Arial", 14)).pack(pady=10)

        # Génération TOTP et QR Code
        secret = pyotp.random_base32()
        secrets[self.current_user] = secret
        save_secrets(secrets)  # sauvegarde dans le fichier

        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=self.current_user, issuer_name="MonApp")
        qr = qrcode.make(uri)

        # Convertir QR Code pour tkinter
        bio = io.BytesIO()
        qr.save(bio, format="PNG")
        bio.seek(0)
        qr_image = Image.open(bio)
        qr_image = qr_image.resize((200, 200))
        self.qr_photo = ImageTk.PhotoImage(qr_image)
        ttk.Label(frame, image=self.qr_photo).pack(pady=10)

        ttk.Button(frame, text="Continuer", command=self.frame_2fa_input).pack(pady=10)

    # ==========================
    # ÉCRAN SAISIE CODE 2FA
    # ==========================
    def frame_2fa_input(self):
        self.clear_window()
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Saisir le code 2FA généré par Google Authenticator", font=("Arial", 14)).pack(pady=10)
        self.entry_2fa = ttk.Entry(frame)
        self.entry_2fa.pack(pady=5)
        ttk.Button(frame, text="Valider", command=self.verify_2fa).pack(pady=10)

    def verify_2fa(self):
        code = self.entry_2fa.get()
        secret = secrets.get(self.current_user)
        totp = pyotp.TOTP(secret)
        if totp.verify(code):
            self.frame_recherche()
        else:
            messagebox.showerror("Erreur", "Code 2FA invalide")

    # ==========================
    # ÉCRAN RECHERCHE
    # ==========================
    def frame_recherche(self):
        self.clear_window()
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", pady=10)
        ttk.Label(search_frame, text="Mot-clé :").pack(side="left")
        self.entry_search = ttk.Entry(search_frame)
        self.entry_search.pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(search_frame, text="Rechercher", command=self.rechercher).pack(side="left")

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
        headers = {"X-API-Key": API_KEY}
        try:
            response = requests.get(API_URL, headers=headers)
            response.raise_for_status()
            livres = response.json()
        except Exception as e:
            messagebox.showerror("Erreur API", str(e))
            return

        for item in self.tree.get_children():
            self.tree.delete(item)
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
