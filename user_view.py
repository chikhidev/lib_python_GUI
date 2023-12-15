import tkinter as tk
from book import Book
from borrow import MAX_DAYS_ALLOWED, Borrow
from user import User
from tkinter import ttk
from tkinter import messagebox
import datetime

MAX_DAYS_ALLOWED = 7

def show_user_view(root, user_id, logout_callback):
    global logged_in_user_id, user_window, user
    user_window = tk.Toplevel(root)
    user_window.title("Vue Utilisateur")
    user_window.attributes("-zoomed", 1)

    logged_in_user_id = user_id
    user = User.get_user(user_id)

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
            global right_content_frame
            clear_right_content_frame()
            action()

        user_buttons = {
            "Afficher Livres": lambda: display_books_view(),
            "Emprunter Livre": lambda: borrow_book(),
            "Afficher Livres deja\nempruntés (non disponibles)": lambda: display_unval_books(),
            "Afficher Livres Disponibles": lambda: display_available_books(),
            "Afficher Livres Empruntés\npar vous | retourner": lambda: display_borrowed_books(),
            "Déconnexion": logout,
        }

        header_label = tk.Label(
            left_menu_frame,
            text=f"Profile: {user['name']}",
            font=("Helvetica", 10, "bold"),
            bg="#f5f4f2",
            padx=5,
            pady=10,
        )
        header_label.pack(anchor=tk.W)

        for label, action in user_buttons.items():
            button_text = f"→ {label}"
            button = tk.Button(
                left_menu_frame,
                text=button_text,
                command=lambda a=action: execute_action(a),
                relief=tk.FLAT,
                width=22,
                bg="white",
            )
            if label == "Déconnexion":
                button.config(fg="red")
            button.pack()
            button.config(anchor=tk.W)

    display_main_menu()

def clear_right_content_frame():
    for widget in right_content_frame.winfo_children():
        widget.destroy()

def display_books_view():
    clear_right_content_frame()

    def search_books():
        search_term = search_entry.get().strip()
        if search_term:
            loading_label.config(text="╾ Recherche en cours...", fg="#21675e")
            user_window.update()
            books_to_show = Book.search_books(search_term)
            populate_treeview(tree, books_to_show)
            count_label.config(text=f"{len(books_to_show)} Livres trouvés")
            loading_label.config(text="", fg="white")

    search_frame = tk.Frame(right_content_frame, bg="white")
    search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    search_entry = tk.Entry(search_frame, font=("Helvetica", 10), width=30)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(
        search_frame,
        text="Rechercher",
        command=search_books,
        relief=tk.FLAT,
        bg="#21675e",
        fg="#ffffff",
    )
    search_button.pack(side=tk.LEFT, padx=5)

    loading_label = tk.Label(search_frame, text="", font=("Helvetica", 10), bg="white")
    loading_label.pack(side=tk.LEFT, padx=5)

    count_label = tk.Label(search_frame, text="", font=("Helvetica", 10), bg="white")
    count_label.pack(side=tk.RIGHT, padx=5)

    tree = ttk.Treeview(
        right_content_frame,
        columns=("ID", "Titre", "Auteur", "Éditeur", "ISBN", "Exemplaires", "Année"),
        show="headings",
    )
    tree.heading("ID", text="ID")
    tree.heading("Titre", text="Titre")
    tree.heading("Auteur", text="Auteur")
    tree.heading("Éditeur", text="Éditeur")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Exemplaires", text="Exemplaires")
    tree.heading("Année", text="Année")

    populate_treeview(tree, Book.get_books())

    tree.pack(expand=True, fill=tk.BOTH)
    tree.column("ID", width=50)
    tree.column("Titre", width=150)
    tree.column("Auteur", width=100)
    tree.column("Éditeur", width=100)
    tree.column("ISBN", width=100)
    tree.column("Exemplaires", width=50)
    tree.column("Année", width=50)

def populate_treeview(tree, books):
    tree.delete(*tree.get_children())

    for book in books:
        tree.insert(
            "",
            tk.END,
            values=(
                book.get("book_id", ""),
                book.get("title", ""),
                book.get("author", ""),
                book.get("editor", ""),
                book.get("isbn", ""),
                book.get("num_copies", ""),
                book.get("year", ""),
            ),
        )

def borrow_book():
    clear_right_content_frame()

    def search_books():
        search_term = search_entry.get().strip()
        if search_term:
            loading_label.config(text="╾ Recherche en cours...", fg="#21675e")
            user_window.update()
            books_to_show = Book.search_books(search_term)
            populate_treeview(tree, books_to_show)
            count_label.config(text=f"{len(books_to_show)} Livres trouvés")
            loading_label.config(text="", fg="white")

    search_frame = tk.Frame(right_content_frame, bg="white")
    search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    search_entry = tk.Entry(search_frame, font=("Helvetica", 10), width=30)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_button = tk.Button(
        search_frame,
        text="Rechercher",
        command=search_books,
        relief=tk.FLAT,
        bg="#21675e",
        fg="#ffffff",
    )
    search_button.pack(side=tk.LEFT, padx=5)

    loading_label = tk.Label(search_frame, text="", font=("Helvetica", 10), bg="white")
    loading_label.pack(side=tk.LEFT, padx=5)

    count_label = tk.Label(search_frame, text="", font=("Helvetica", 10), bg="white")
    count_label.pack(side=tk.RIGHT, padx=5)

    books_to_show = Book.get_books()

    tree = ttk.Treeview(
        right_content_frame,
        columns=("ID", "Titre", "Auteur", "Éditeur", "ISBN", "Exemplaires", "Année"),
        show="headings",
    )
    tree.heading("ID", text="ID")
    tree.heading("Titre", text="Titre")
    tree.heading("Auteur", text="Auteur")
    tree.heading("Éditeur", text="Éditeur")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Exemplaires", text="Exemplaires")
    tree.heading("Année", text="Année")

    populate_treeview(tree, books_to_show)

    tree.pack(expand=True, fill=tk.BOTH)
    tree.column("ID", width=50)
    tree.column("Titre", width=150)
    tree.column("Auteur", width=100)
    tree.column("Éditeur", width=100)
    tree.column("ISBN", width=100)
    tree.column("Exemplaires", width=50)
    tree.column("Année", width=50)

    def borrow_selected_book():
      selected_item = tree.focus()
      if selected_item:
          selected_book = tree.item(selected_item, "values")
          book_id = selected_book[0]

          result = Borrow.borrow_book(logged_in_user_id, book_id)

          message_window = tk.Toplevel(right_content_frame)
          message_window.title("Envoyer un message")

          # Add UI elements to the new window
          if result["status"] == "success":
              message_label = tk.Label(
                  message_window,
                  text=result["message"],
                  font=("Helvetica", 12),
                  padx=20,
                  pady=20,
              )
          else:
              message_label = tk.Label(
                  message_window,
                  text=f"Erreur : {result['message']}",
                  font=("Helvetica", 12),
                  padx=20,
                  pady=20,
                  fg="red",
              )

          message_label.pack()

          close_button = tk.Button(
              message_window,
              text="Fermer",
              command=message_window.destroy,
              relief=tk.FLAT,
              width=20,
              bg="#21675e",
              fg="#ffffff",
          )
          close_button.pack(pady=10)


    container_frame = tk.Frame(right_content_frame, bg="white")
    container_frame.pack(pady=10, side=tk.LEFT)

    message_label = tk.Label(
        container_frame,
        text="✎ Sélectionnez le livre et cliquez ici pour traiter votre demande",
        font=("Helvetica", 10),
        bg="white",
    )
    message_label.pack(side=tk.LEFT, padx=10)

    borrow_button = tk.Button(
        container_frame,
        text="Emprunter ✔",
        command=borrow_selected_book,
        relief=tk.FLAT,
        width=15,
        bg="#21675e",
        fg="#ffffff",
    )
    borrow_button.pack(side=tk.LEFT)



def display_borrowed_books():
  clear_right_content_frame()

  # Top Section - Treeview displaying borrowed books
  tree = ttk.Treeview(
      right_content_frame,
      columns=("ID", "Titre", "Date Emprunt", "En Retard"),
      show="headings",
  )
  tree.heading("ID", text="ID")
  tree.heading("Titre", text="Titre")
  tree.heading("Date Emprunt", text="Date Emprunt")
  tree.heading("En Retard", text="En Retard")

  borrowed_books_to_show = Borrow.get_borrowed_books(logged_in_user_id)

  for book_info in borrowed_books_to_show:
      is_late = check_if_book_is_late(book_info["due_date"])
      color = "red" if is_late == "Oui" else "green"
      tree.insert(
          "",
          "end",
          values=(book_info["book_id"], book_info["title"], book_info["due_date"], is_late),
          tags=(color,),
      )

  tree.tag_configure("red", foreground="red")
  tree.tag_configure("green", foreground="green")

  tree.pack(expand=True, fill=tk.BOTH)
  tree.column("ID", width=50)
  tree.column("Titre", width=150)
  tree.column("Date Emprunt", width=150)
  tree.column("En Retard", width=100)  # Adjust the width as needed

  # Bottom Section - Policy, Return Button, and Warning Label
  bottom_frame = tk.Frame(right_content_frame, bg="white")
  bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=10, padx=10)

  # Container frame for additional sentence and button
  container_frame2 = tk.Frame(bottom_frame, bg="white")
  container_frame2.pack(side=tk.LEFT, padx=10, pady=5)

  additional_sentence_label = tk.Label(
      container_frame2,
      text="Sélectionnez un livre à retourner.",
      font=("Helvetica", 10),
      bg="white",
      padx=10,
  )
  additional_sentence_label.pack(side=tk.LEFT)

  return_button = tk.Button(
      container_frame2,
      text="Retourner le Livre ↺",
      command=lambda: return_selected_book(tree),
      relief=tk.FLAT,
      width=17,
      bg="#21675e",
      fg="#ffffff",
  )
  return_button.pack(side=tk.LEFT)


def check_if_book_is_late(due_date):
  try:
      current_date = datetime.date.today()
      due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
      days_diff = (current_date - due_date).days
      return "Oui" if days_diff > MAX_DAYS_ALLOWED else "Non"
  except ValueError:
      return "N/A"


def return_selected_book(tree):
  selected_item = tree.selection()
  if not selected_item:
      messagebox.showerror("Erreur", "Veuillez sélectionner un livre à retourner.")
      return

  book_id = tree.item(selected_item, "values")[0]
  result = Borrow.return_book(logged_in_user_id, book_id)

  message_window = tk.Toplevel(right_content_frame)
  message_window.title("Message")

  # Add UI elements to the new window
  message_label = tk.Label(
      message_window,
      text=result["message"],
      font=("Helvetica", 12),
      padx=20,
      pady=20,
  )
  message_label.pack()

  close_button = tk.Button(
      message_window,
      text="Fermer",
      command=lambda: on_close_return_window(message_window),
      relief=tk.FLAT,
      width=20,
      bg="#21675e",
      fg="#ffffff",
  )
  close_button.pack(pady=10)

def on_close_return_window(window):
  window.destroy()
  clear_right_content_frame()
  display_borrowed_books()

def display_available_books():
  clear_right_content_frame()

  available_books = Book.available_books()

  tree = ttk.Treeview(
      right_content_frame,
      columns=("ID", "Titre", "Auteur", "Éditeur", "ISBN", "Exemplaires", "Année"),
      show="headings",
  )
  tree.heading("ID", text="ID")
  tree.heading("Titre", text="Titre")
  tree.heading("Auteur", text="Auteur")
  tree.heading("Éditeur", text="Éditeur")
  tree.heading("ISBN", text="ISBN")
  tree.heading("Exemplaires", text="Exemplaires")
  tree.heading("Année", text="Année")

  populate_treeview(tree, available_books)

  tree.pack(expand=True, fill=tk.BOTH)
  tree.column("ID", width=50)
  tree.column("Titre", width=150)
  tree.column("Auteur", width=100)
  tree.column("Éditeur", width=100)
  tree.column("ISBN", width=100)
  tree.column("Exemplaires", width=50)
  tree.column("Année", width=50)

def display_unval_books():
  clear_right_content_frame()

  borrowed_book_ids = Borrow.read_all_borrowed_books()
  all_books = Book.get_books()

  unval_books = [
      book for book in all_books if book["book_id"] in borrowed_book_ids
  ]

  tree = ttk.Treeview(
      right_content_frame,
      columns=("ID", "Titre", "Auteur", "Éditeur", "ISBN", "Exemplaires", "Année", "Statut"),
      show="headings",
  )
  tree.heading("ID", text="ID")
  tree.heading("Titre", text="Titre")
  tree.heading("Auteur", text="Auteur")
  tree.heading("Éditeur", text="Éditeur")
  tree.heading("ISBN", text="ISBN")
  tree.heading("Exemplaires", text="Exemplaires")
  tree.heading("Année", text="Année")
  tree.heading("Statut", text="Statut")

  for book in unval_books:
      tree.insert("", "end", values=(book["book_id"], book["title"], book["author"],
                                     book["editor"], book["isbn"], book["num_copies"],
                                     book["year"], "déjà pris"), tags=("taken",))

  tree.tag_configure("taken", foreground="#80535b")  # Set the color for the "taken" tag

  tree.pack(expand=True, fill=tk.BOTH)
  tree.column("ID", width=50)
  tree.column("Titre", width=150)
  tree.column("Auteur", width=100)
  tree.column("Éditeur", width=100)
  tree.column("ISBN", width=100)
  tree.column("Exemplaires", width=50)
  tree.column("Année", width=50)
  tree.column("Statut", width=70)
