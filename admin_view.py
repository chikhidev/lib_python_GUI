import tkinter as tk
from tkinter import messagebox
from user import User
from book import Book
from borrow import Borrow
from user_manage import UserManage

MAX_BOOKS_PER_STUDENT = 3

def show_admin_view(root, user_id, logout_callback):
    admin_window = tk.Toplevel(root)
    admin_window.title("Vue Admin")

    admin_window.geometry("+100+100")
    admin_window.attributes('-zoomed', 1)


    logged_in_user_id = user_id

    main_paned_window = tk.PanedWindow(admin_window, orient=tk.HORIZONTAL)
    main_paned_window.pack(fill=tk.BOTH, expand=True)
    main_paned_window.configure(bg="white")

    left_menu_frame = tk.Frame(main_paned_window)
    left_menu_frame.configure(bg="#f5f4f2")
    main_paned_window.add(left_menu_frame)

    right_content_frame = tk.Frame(main_paned_window)
    right_content_frame.configure(bg="white")
    main_paned_window.add(right_content_frame)

    def logout():
        admin_window.destroy()
        logout_callback()

    admin_buttons = {
        "Ajouter Utilisateur": lambda: User.add_user(),
        "Afficher Utilisateurs": lambda: User.display_users(),
        "Ajouter Livre": lambda: Book.add_book(),
        "Afficher Livres": lambda: Book.display_books(),
        "Emprunter Livre": lambda: Borrow.borrow_book(logged_in_user_id, input("ID du livre à emprunter : ")),
        "Afficher Livres Empruntés": lambda: Borrow.display_borrowed_books(),
        "Gérer Comptes Utilisateur": lambda: UserManage.manage_user_accounts(),
        "Gérer Livres Empruntés": lambda: Borrow.manage_borrowed_books(),
        "Afficher Livres en Retard": lambda: Borrow.display_late_returning_books(),
        "Marquer Livre comme\nrendu": lambda: Borrow.return_book(logged_in_user_id, input("ID du livre à marquer comme rendu : ")),
        "Afficher LivresDisponiles": lambda: Book.available_books(),
        "Afficher Utilisateurs qui\nont Emprunté un Livre": lambda: Borrow.books_taken_by(logged_in_user_id),
        "Déconnexion": logout
    }

    for label, action in admin_buttons.items():
        button_text = f"→ {label}"
        button = tk.Button(left_menu_frame, text=button_text, command=action, relief=tk.FLAT, width=22, bg="white")
        if label == "Déconnexion":
          button.config(fg="red")
        button.pack()
        button.config(anchor=tk.W)

    right_content_label = tk.Label(right_content_frame, text="Sélectionnez une option dans le menu de gauche.")
    right_content_label.pack()

