import tkinter as tk
from tkinter import messagebox
from user import User
from book import Book
from borrow import Borrow
from user_manage import UserManage
from tkinter import ttk

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

    global right_content_frame
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
        "Afficher Livres": lambda: display_books_view(),
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

    global right_content_label
    right_content_label = tk.Label(right_content_frame, text="Sélectionnez une option dans le menu de gauche.")
    right_content_label.pack()

def clear_right_content_frame():
    # Destroy all widgets in right_content_frame
    for widget in right_content_frame.winfo_children():
        widget.destroy()

def display_books_view():
    clear_right_content_frame()  # Clear existing widgets

    books_to_show = Book.get_books()

    tree = ttk.Treeview(right_content_frame, columns=("ID", "Titre", "Auteur", "Éditeur", "ISBN", "Exemplaires", "Année"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Titre", text="Titre")
    tree.heading("Auteur", text="Auteur")
    tree.heading("Éditeur", text="Éditeur")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Exemplaires", text="Exemplaires")
    tree.heading("Année", text="Année")

    for book in books_to_show:
        tree.insert("", tk.END, values=(
            book.get('book_id', ''),
            book.get('title', ''),
            book.get('author', ''),
            book.get('publisher', ''),
            book.get('isbn', ''),
            book.get('num_copies', ''),
            book.get('year', '')
        ))

    tree.pack(expand=True, fill=tk.BOTH)
    tree.column("ID", width=50)
    tree.column("Titre", width=150)
    tree.column("Auteur", width=100)
    tree.column("Éditeur", width=100)
    tree.column("ISBN", width=100)
    tree.column("Exemplaires", width=50)
    tree.column("Année", width=50)

# ... (your other code remains unchanged)
