import tkinter as tk
from tkinter import messagebox
from book import Book
from borrow import Borrow

def show_user_view(root, user_id, logout_callback):
    user_window = tk.Toplevel(root)
    user_window.title("Vue Utilisateur")

    # Initialize global variables for user login
    logged_in_user_id = user_id

    def display_main_menu():
        user_frame = tk.Frame(user_window)
        user_frame.pack()

        def logout():
            user_window.destroy()  # Destroy the user window
            logout_callback()  # Call the logout callback to return to the root window

        user_buttons = {
            "Afficher Livres": lambda: Book.display_books(),
            "Emprunter Livre": lambda: Borrow.borrow_book(logged_in_user_id, input("ID du livre à emprunter : ")),
            "Afficher Livres Empruntés": lambda: Borrow.display_borrowed_books(),
            "Retourner Livre": lambda: Borrow.return_book(logged_in_user_id, input("ID du livre à retourner : ")),
            "Afficher Livres Disponibles": lambda: Book.available_books(),
            "Afficher Livres Empruntés par Vous": lambda: Borrow.books_taken_by(logged_in_user_id),
            "Déconnexion": logout,
        }

        for label, action in user_buttons.items():
            button = tk.Button(user_frame, text=label, command=action)
            button.pack()

    display_main_menu()
