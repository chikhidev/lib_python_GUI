import datetime
from user import User
from user_manage import UserManage
from book import Book

MAX_BOOKS_PER_STUDENT = 3
BORROWED_BOOKS_FILE = "borrowed_books.txt"
MAX_DAYS_ALLOWED = 7


class Borrow:
    @staticmethod
    def calculate_due_date():
        current_date = datetime.date.today()
        return current_date + datetime.timedelta(days=14)

    @staticmethod
    def borrow_book(user_id, book_id):
        borrowed_books = Borrow.read_borrowed_books_from_file(user_id)

        if len(borrowed_books) >= MAX_BOOKS_PER_STUDENT:
            print("Limite de livres empruntés atteinte.")
            return

        if Borrow.is_book_already_borrowed(user_id, book_id):
            print("Ce livre est déjà emprunté par l'utilisateur.")
            return

        all_borrowed_books = Borrow.read_all_borrowed_books()
        if any(entry["book_id"] == book_id for entry in all_borrowed_books):
            print("Ce livre est déjà emprunté par un autre utilisateur.")
            return

        book = Book.get_book_by_id(book_id)
        if book is None:
            print("Livre introuvable.")
            return

        due_date = Borrow.calculate_due_date()
        borrowed_books.append({"book_id": book_id, "due_date": due_date})
        Borrow.write_borrowed_books_to_file(user_id, borrowed_books)
        print("Livre emprunté avec succès.")

    @staticmethod
    def return_book(user_id, book_id):
        user = User.get_user(user_id)
        if user is None:
            print("Utilisateur introuvable.")
            return

        book = Book.get_book_by_id(book_id)
        if book is None:
            print("Livre introuvable.")
            return

        borrowed_books = Borrow.read_borrowed_books_from_file(user_id)
        found_book = next((b for b in borrowed_books if b["book_id"] == book_id), None)

        if found_book is None:
            print("L'utilisateur n'a pas emprunté ce livre.")
            return

        borrowed_books.remove(found_book)

        try:
            with open(BORROWED_BOOKS_FILE, "w") as file:
                for book in borrowed_books:
                    line = f"{user_id},{book['book_id']},{book['due_date']}\n"
                    file.write(line)

            print("Livre retourné avec succès.")
        except FileNotFoundError:
            print(f"Fichier {BORROWED_BOOKS_FILE} introuvable.")
        except Exception as e:
            print(f"Une erreur s'est produite lors du retour du livre : {e}")


    @staticmethod
    def read_all_borrowed_books():
        try:
            with open(BORROWED_BOOKS_FILE, "r") as file:
                content = []
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 3:
                        user_id, book_id, due_date = values
                        content.append({"user_id": user_id, "book_id": book_id, "due_date": due_date})
                        
                return content
        except FileNotFoundError:
            print(f"Fichier {BORROWED_BOOKS_FILE} introuvable.")
            return []



    @staticmethod
    def is_book_already_borrowed(user_id, book_id):
        borrowed_books = Borrow.read_borrowed_books_from_file(user_id)
        return any(b["book_id"] == book_id for b in borrowed_books)

    @staticmethod
    def write_borrowed_books_to_file(user_id, borrowed_books):
        try:
            with open(BORROWED_BOOKS_FILE, "r") as file:
                lines = file.readlines()

            with open(BORROWED_BOOKS_FILE, "w") as file:
                for line in lines:
                    if user_id not in line:
                        file.write(line)

                for book in borrowed_books:
                    line = f"{user_id},{book['book_id']},{book['due_date']}\n"
                    file.write(line)

            print("Livres empruntés enregistrés avec succès.")
        except FileNotFoundError:
            print(f"Fichier {BORROWED_BOOKS_FILE} introuvable.")

    @staticmethod
    def extend_borrow_duration(user_id, book_id):
        user = User.get_user(user_id)
        if user is None:
            print("Utilisateur introuvable.")
            return
        book = Book.get_book(book_id)
        if book is None:
            print("Livre introuvable.")
            return
        borrowed_books = user["borrowed_books"]
        for borrowed_book in borrowed_books:
            if borrowed_book["book_id"] == book_id:
                due_date = datetime.datetime.strptime(
                    borrowed_book["due_date"], "%Y-%m-%d"
                ).date()
                new_due_date = due_date + datetime.timedelta(days=7)
                borrowed_book["due_date"] = new_due_date.strftime("%Y-%m-%d")
                Borrow.write_borrowed_books_to_file(user_id, borrowed_books)
                print("Durée d'emprunt prolongée.")
                return
        print("L'utilisateur n'a pas emprunté ce livre.")

    @staticmethod
    def manage_borrowed_books():
        user_id = input("ID de l'utilisateur : ")
        user = User.get_user(user_id)

        if not user:
            print("Utilisateur introuvable.")
            return

        suspended_users = UserManage.read_suspended_users_from_file()

        if user_id in suspended_users:
            print(
                "Compte d'utilisateur suspendu. L'emprunt de livres n'est pas autorisé."
            )
            return

        user_borrowed_books = Borrow.read_borrowed_books_from_file(user_id)
        num_borrowed_books = len(user_borrowed_books)
        print("Nombre de livres empruntés par l'utilisateur :", num_borrowed_books)

        if num_borrowed_books >= MAX_BOOKS_PER_STUDENT:
            print("Nombre maximal de livres empruntés atteint.")
            return

        action = input(
            "Marquer comme rendu (R) ou Prolonger la durée (P) de l'emprunt ? "
        )

        if action.lower() == "r":
            book_id = input("ID du livre : ")
            Borrow.return_book(user_id, book_id)
        elif action.lower() == "p":
            book_id = input("ID du livre : ")
            Borrow.extend_borrow_duration(user_id, book_id)
        else:
            print("Action invalide. Veuillez sélectionner une action valide.")

    @staticmethod
    def display_borrowed_books():
        import os
        try:
            with open(BORROWED_BOOKS_FILE, "r") as file:
                if os.path.getsize(BORROWED_BOOKS_FILE) == 0:
                    print("Le fichier est vide. Aucun livre emprunté à afficher.")
                else:
                    for borrowed_book in file:
                        try:
                            user_id, book_id, due_date = borrowed_book.strip().split(",")
                            print(
                                f"Utilisateur : {user_id}\tLivre : {book_id}\tDate d'échéance : {due_date}"
                            )
                        except ValueError:
                            pass
        except FileNotFoundError:
            print("Fichier introuvable. Impossible d'afficher les livres empruntés.")


    @staticmethod
    def display_late_returning_books():
        try:
            current_date = datetime.date.today()
            with open(BORROWED_BOOKS_FILE, "r") as file:
                if file.tell() == 0:
                    print("Le fichier est vide. Aucun livre en retard à afficher.")
                else:
                    for borrowed_book in file:
                        try:
                            user_id, book_id, due_date = borrowed_book.strip().split(",")
                            due_date = datetime.datetime.strptime(
                                due_date, "%Y-%m-%d"
                            ).date()
                            days_diff = (current_date - due_date).days

                            if days_diff >= MAX_DAYS_ALLOWED:
                                print(
                                    f"Utilisateur : {user_id}\tLivre : {book_id}\tDate d'échéance : {due_date}"
                                )
                        except ValueError:
                            print(f"Données de livre emprunté incorrectes  {borrowed_book}")
        except FileNotFoundError:
            print("Fichier introuvable. Impossible d'afficher les livres en retard.")

    def books_taken_by(user_id):
        user_borrowed_books = Borrow.read_borrowed_books_from_file(user_id)
        if not user_borrowed_books:
            print(f"L'utilisateur avec l'ID {user_id} n'a emprunté aucun livre.")
        else:
            print(f"\nLivres empruntés par l'utilisateur avec l'ID {user_id}:")
            for borrowed_book in user_borrowed_books:
                book_id = borrowed_book["book_id"]
                due_date = borrowed_book["due_date"]
                book = Book.get_book_by_id(book_id)
                if book:
                    print(
                        f"ID: {book_id}\tTitle: {book['title']}\tDue Date: {due_date}"
                    )
                else:
                    print(f"Livre introuvable avec l'ID {book_id}.")

    @staticmethod
    def read_borrowed_books_from_file(user_id):
        try:
            with open(BORROWED_BOOKS_FILE, "r") as file:
                content = []
                for line in file:
                    try:
                        current_user_id, book_id, due_date = line.strip().split(",")
                        if current_user_id == user_id:
                            content.append({"user_id": current_user_id, "book_id": book_id, "due_date": due_date})
                    except ValueError:
                        pass
                return content
        except FileNotFoundError:
            print(f"Fichier {BORROWED_BOOKS_FILE} introuvable.")
            return []