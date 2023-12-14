import tkinter as tk
from book import Book
from borrow import Borrow

def show_user_view(root, user_id, logout_callback):
    user_window = tk.Toplevel(root)
    user_window.title("Vue Utilisateur")

    user_window.attributes('-zoomed', 1)

    logged_in_user_id = user_id

    def display_main_menu():
        user_frame = tk.Frame(user_window)
        user_frame.pack()

        def logout():
            user_window.destroy()
            logout_callback()

        user_buttons = {
            "Afficher Livres": lambda: Book.display_books(),
            "Emprunter Livre": lambda: Borrow.borrow_book(logged_in_user_id, input("ID du livre à emprunter : ")),
            "Afficher Livres Empruntés": lambda: Borrow.display_borrowed_books(),
            "Retourner Livre": lambda: Borrow.return_book(logged_in_user_id, input("ID du livre à retourner : ")),
            "Afficher Livres\nDisponibles": lambda: Book.available_books(),
            "Afficher Livres\nEmpruntés par Vous": lambda: Borrow.books_taken_by(logged_in_user_id),
            "Déconnexion": logout,
        }

        for label, action in user_buttons.items():
            button_text = f"→ {label}"
            button = tk.Button(user_frame, text=button_text, command=action, relief=tk.FLAT, width=22)
            if label == "Déconnexion":
                button.config(fg="red")
            button.pack()
            button.config(anchor=tk.W)

    display_main_menu()
