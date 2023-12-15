import file
BOOKS_FILE_NAME = "books.txt"

class Book:
    def __init__(self, book_id, title, author, editor, isbn, num_copies, year):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.editor = editor
        self.isbn = isbn
        self.num_copies = num_copies
        self.year = year

    def __str__(self):
        return f"ID: {self.book_id}, title: {self.title}, author: {self.author}, editor: {self.editor}, ISBN: {self.isbn}, num_copies: {self.num_copies}, year: {self.year}"

    def get_book(book_id):
        books = Book.get_books()
        for book in books:
            if book.book_id == book_id:
                return book
        return None

    def add_book():
        book_id = input("ID livre : ")
        title = input("titre : ")
        author = input("auteur : ")
        editor = input("editeur : ")
        isbn = input("ISBN : ")

        while True:
          try:
              num_copies = int(input("nombre de copies : "))
              break
          except ValueError:
              answer = input("Veuillez saisir un nombre entier\n")
        while True:
          try:
              year = int(input("année : "))
              break
          except ValueError:
              answer = input("Veuillez saisir un nombre entier\n")
        if book_id and title and author and editor and isbn and num_copies and year:
            book = Book(book_id, title, author, editor, isbn, num_copies, year)
            book.create_book()
            print("Livre ajouté avec succès.")
        else:
            print("Veuillez renseigner tous les champs.")

    def create_book(self):
        book_data = f"{self.book_id},{self.title},{self.author},{self.editor},{self.isbn},{self.num_copies},{self.year}"
        file.write_to_file(BOOKS_FILE_NAME, book_data)

    @staticmethod
    def get_books():
        try:
            lines = Book.read_from_file(BOOKS_FILE_NAME)
            books = []

            for line in lines:
                book_data = line.strip().split(",")

                if len(book_data) == 7:
                    book = {
                        "book_id": book_data[0],
                        "title": book_data[1],
                        "author": book_data[2],
                        "editor": book_data[3],
                        "isbn": book_data[4],
                        "num_copies": int(book_data[5]),
                        "year": int(book_data[6]),
                    }
                    books.append(book)

            return books
        except FileNotFoundError:
            print(f"Fichier {BOOKS_FILE_NAME} introuvable.")
            return []



    @staticmethod
    def get_book_by_id(book_id):
        books = Book.get_books()
        for book in books:
            if book['book_id'] == book_id:
                return book
        return None

    @staticmethod
    def display_books():
        books = Book.get_books()
        if not books:
            print("Aucun livre disponible.")
        else:
            print("\nListe des livres:")
            for book in books:
                print(
                    f"\tID: {book.get('book_id', '')}, titre: {book.get('title', '')}, auteur: {book.get('author', '')}, editeur: {book.get('editor', '')}, ISBN: {book.get('isbn', '')}, nombre de copies: {book.get('num_copies', '')}, année: {book.get('year', '')}"
                )

    def available_books():
        try:
            from borrow import Borrow

            borrowed_books = Borrow.read_all_borrowed_books()

            all_books = Book.get_books()
            available_books = []
            
            if not all_books:
                print("il n'y a aucun livre trouvé")
                return
            if not borrowed_books and all_books:
                available_books = all_books
            else:
                for book in all_books:
                    found = False
                    for borrowed_book in borrowed_books:
                        if borrowed_book["book_id"] == book["book_id"]:
                            found = True
                    if not found:
                        available_books.append(book)

            if not available_books:
                print("Plus aucun livre disponible!")
            else:
                print("\nAvailable Books:")
                for book in available_books:
                    print(
                        f"ID: {book['book_id']}\tTitle: {book['title']}\tAuthor: {book['author']}"
                    )
        except FileNotFoundError:
            print(f"Fichier {BORROWED_BOOKS_FILE} introuvable.")
        except ValueError as ve:
            print(f"Erreur!, peut-être parce que le fichier est vide")
        except Exception as e:
            print(f"Une erreur s'est produite: {e}")


    @staticmethod
    def read_from_file(file_name):
        try:
            with open(file_name, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"Fichier {file_name} introuvable.")
            return []