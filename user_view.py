import tkinter as tk
from book import Book
from borrow import Borrow
from user import User

def show_user_view(root, user_id, logout_callback):
    user_window = tk.Toplevel(root)
    user_window.title("Vue Utilisateur")
    user_window.attributes('-zoomed', 1)

    logged_in_user_id = user_id

    # Create global variables for frames
    left_menu_frame = tk.Frame(user_window, bg="#f5f4f2")
    left_menu_frame.pack(side=tk.LEFT, fill=tk.Y)

    global right_content_frame
    right_content_frame = tk.Frame(user_window, bg="white")
    right_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def logout():
        user_window.destroy()
        logout_callback()

    def display_main_menu():
        def execute_action(action):
            # Access the global right_content_frame
            global right_content_frame
            right_content_frame.destroy()  # Clear the right content frame
            right_content_frame = tk.Frame(user_window, bg="white")
            right_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            action()

        user_buttons = {
            "Afficher Livres": lambda: display_books_view(logged_in_user_id),
            "Emprunter Livre": lambda: Borrow.borrow_book(logged_in_user_id, input("ID du livre à emprunter : ")),
            "Afficher Livres Empruntés": lambda: Borrow.display_borrowed_books(),
            "Retourner Livre": lambda: Borrow.return_book(logged_in_user_id, input("ID du livre à retourner : ")),
            "Afficher Livres Disponibles": lambda: Book.available_books(),
            "Afficher Livres Empruntés par Vous": lambda: Borrow.books_taken_by(logged_in_user_id),
            "Déconnexion": logout,
        }

        for label, action in user_buttons.items():
            button_text = f"→ {label}"
            button = tk.Button(left_menu_frame, text=button_text, command=lambda a=action: execute_action(a), relief=tk.FLAT, width=22, bg="white")
            if label == "Déconnexion":
                button.config(fg="red")
            button.pack()
            button.config(anchor=tk.W)

    display_main_menu()

def display_books_view(user_id):
    books_to_show = Book.get_books()

    for book in books_to_show:
        book_label = tk.Label(right_content_frame, text=f"Book ID: {book['book_id']}, Title: {book['title']}")
        book_label.pack()

# Add your other code here if needed
