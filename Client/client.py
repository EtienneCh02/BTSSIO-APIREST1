import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_BASE_URL = "http://127.0.0.1:8001"  # URL de ton API FastAPI [file:3]

API_KEY = "tp-secret-key"

# --- "Base de données" utilisateurs locale (login/mot de passe) ---
USERS = {
    "admin": "admin",
    "user": "user123",
}

# --- Fonctions d'accès à l'API ------------------------------------------------


def get_livres_from_api():
    """
    Récupère la liste des livres via l'endpoint /v_livres.
    L'API renvoie une liste de dicts conformes au schéma V_LivresSchema. [file:3][file:7]
    """
    url = f"{API_BASE_URL}/v_livres"
    headers = {"X-API-Key": API_KEY}
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erreur API", f"Impossible de joindre l'API :\n{e}")
        return []


# --- Fenêtre principale (recherche + tableau) ---------------------------------


class MainWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Client Livres - Recherche")
        self.geometry("1100x600")

        # Frame recherche
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(search_frame, text="Mot clé (titre) :").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(
            side=tk.LEFT, padx=5
        )

        tk.Button(search_frame, text="Rechercher", command=self.search).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(search_frame, text="Rafraîchir", command=self.refresh).pack(
            side=tk.LEFT, padx=5
        )

        # Label info
        self.info_var = tk.StringVar(value="Aucun résultat pour l'instant.")
        tk.Label(self, textvariable=self.info_var).pack(anchor="w", padx=10)

        # Colonnes alignées avec la vue SQL V_Livres
        columns = (
            "Id_Livre",
            "Titre",
            "Résumé",
            "Prix",
            "Date_de_parution",
            "ISBN",
            "Stock",
            "Id_Editeur",
        )

        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.tree.heading("Id_Livre", text="Id_Livre")
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Résumé", text="Résumé")
        self.tree.heading("Prix", text="Prix")
        self.tree.heading("Date_de_parution", text="Date de parution")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Id_Editeur", text="Id_Editeur")

        self.tree.column("Id_Livre", width=70, anchor="center")
        self.tree.column("Titre", width=250, anchor="w")
        self.tree.column("Résumé", width=250, anchor="w")
        self.tree.column("Prix", width=80, anchor="e")
        self.tree.column("Date_de_parution", width=120, anchor="center")
        self.tree.column("ISBN", width=140, anchor="center")
        self.tree.column("Stock", width=60, anchor="center")
        self.tree.column("Id_Editeur", width=80, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Barre de défilement verticale
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Chargement initial
        self.all_livres = []
        self.refresh()

    def refresh(self):
        """Recharge tous les livres depuis l'API et affiche tout."""
        self.all_livres = get_livres_from_api()
        self.populate_table(self.all_livres)
        self.info_var.set(f"{len(self.all_livres)} livre(s) chargé(s) depuis l'API.")

    def search(self):
        """Filtre localement sur le titre en fonction du mot clé saisi."""
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.populate_table(self.all_livres)
            self.info_var.set(
                f"{len(self.all_livres)} livre(s) affiché(s) (sans filtre)."
            )
            return

        filtered = []
        for livre in self.all_livres:
            titre = str(livre.get("Titre", "") or "").lower()
            if keyword in titre:
                filtered.append(livre)

        self.populate_table(filtered)
        self.info_var.set(
            f"{len(filtered)} livre(s) trouvé(s) pour le mot clé '{keyword}'."
        )

    def populate_table(self, livres):
        """Vide le tableau et réinsère les lignes fournies."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for livre in livres:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    livre.get("Id_Livre", ""),
                    livre.get("Titre", ""),
                    livre.get("Résumé", ""),
                    livre.get("Prix", ""),
                    livre.get("Date_de_parution", ""),
                    livre.get("ISBN", ""),
                    livre.get("Stock", ""),
                    livre.get("Id_Editeur", ""),
                ),
            )


# --- Fenêtre de login ---------------------------------------------------------


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client Livres - Login")
        self.geometry("300x160")
        self.resizable(False, False)

        tk.Label(self, text="Identifiant :").pack(pady=(10, 0))
        self.username_var = tk.StringVar()
        tk.Entry(self, textvariable=self.username_var).pack()

        tk.Label(self, text="Mot de passe :").pack(pady=(10, 0))
        self.password_var = tk.StringVar()
        tk.Entry(self, textvariable=self.password_var, show="*").pack()

        tk.Button(self, text="Se connecter", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning(
                "Champs manquants", "Merci de remplir identifiant et mot de passe."
            )
            return

        # Vérification locale très simple
        if USERS.get(username) == password:
            # Login OK : ouvrir la fenêtre principale
            self.open_main_window()
        else:
            messagebox.showerror("Login échoué", "Identifiant ou mot de passe incorrect.")

    def open_main_window(self):
        self.withdraw()  # cacher la fenêtre de login
        main_win = MainWindow(self)
        main_win.protocol("WM_DELETE_WINDOW", self.on_main_close)

    def on_main_close(self):
        self.destroy()


# --- Point d'entrée -----------------------------------------------------------


if __name__ == "__main__":
    import subprocess
    import os
    import sys
    import atexit

    # Le chemin du projet racine (dossier parent)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    print("Démarrage de l'API en tâche de fond...")
    
    # On utilise sys.executable pour s'assurer qu'on utilise le même que pour ce script
    # On exécute le module uvicorn pour démarrer FastAPI sur le port 8001 (pour éviter le conflit avec Symfony)
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"],
        cwd=project_root
    )

    # Sécurité supplémentaire pour bien killer le process API si on quitte mal
    def kill_api():
        try:
            api_process.terminate()
        except:
            pass

    atexit.register(kill_api)

    app = LoginWindow()
    app.mainloop()

    # Quand le mainloop (la fenêtre tk) se termine, on arrête le sous-processus API
    print("Arrêt de l'API...")
    kill_api()
