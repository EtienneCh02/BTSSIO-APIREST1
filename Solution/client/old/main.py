import tkinter as tk
from tkinter import messagebox
from login import LoginWindow
from api import get_livres

def start_app(auth):
    app = tk.Tk()
    app.title("Catalogue des livres")

    listbox = tk.Listbox(app, width=50)
    listbox.pack(padx=10, pady=10)

    def refresh():
        listbox.delete(0, tk.END)
        try:
            livres = get_livres(auth)
            for livre in livres:
                listbox.insert(
                    tk.END,
                    f"{livre['id']} - {livre['titre']} ({livre['auteur']})"
                )
        except Exception as e:
            messagebox.showerror("Erreur API", str(e))

    tk.Button(app, text="Rafraîchir", command=refresh).pack()
    refresh()
    app.mainloop()

# Lancement
root = tk.Tk()
LoginWindow(root, start_app)
root.mainloop()
