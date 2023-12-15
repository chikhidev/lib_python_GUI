import file
import re

USERS_FILE_NAME = "users.txt"


class User:
    def __init__(self, id, name, nickname, email, login, password):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.email = email
        self.login = login
        self.password = password

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', nickname='{self.nickname}', email='{self.email}', login='{self.login}', password='{self.password}')"

    def create_user(self):
        user_data = f"{self.id},{self.name},{self.nickname},{self.email},{self.login},{self.password}"
        file.write_to_file(USERS_FILE_NAME, user_data)

    def add_user():
        user_id = input("ID utilisateur : ")
        user_check = User.get_user(user_id)
        if user_check:
            print("L'ID utilisateur existe déjà.")
            return
        name = input("nom : ")
        nickname = input("prenom : ")
        mail_valide = False
        while not mail_valide:
            mail = input("email : ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", mail):
                mail_valide = True
            elif mail == 0:
                return
            else:
                print(
                    "Format d'email non valide. Veuillez saisir une adresse e-mail valide, ex: example@mail.com"
                )

        login = input("login : ")
        password = input("mot de passe : ")
        if user_id and name and nickname and mail and login and password:
            user = User(user_id, name, nickname, mail, login, password)
            user.create_user()
            print("Utilisateur ajouté avec succès.")
        else:
            print("Veuillez renseigner tous les champs.")

    def get_users():
        users = []
        lines = file.read_from_file(USERS_FILE_NAME)

        if not lines:
            print("Aucun utilisateur trouvé (fichier vide).")
            return

        for line in lines:
            user_data = line.strip().split(",")
            if len(user_data) == 6:
                user = {
                    "user_id": user_data[0],
                    "name": user_data[1],
                    "nickname": user_data[2],
                    "mail": user_data[3],
                    "login": user_data[4],
                    "password": user_data[5],
                    "borrowed_books": [],
                }
                users.append(user)

        return users



    def get_user(user_id):
        users = User.get_users()
        for user in users:
            if user["user_id"] == user_id:
                return user
        return None

    def display_users():
        users = User.get_users()
        if not users:
            print("\nAucun utilisateur trouvé.\n")
        else:
            print("\nUtilisateurs:\n")
            for user in users:
                print(
                    f"ID: {user['user_id']}, nom: {user['name']}, prenom: {user['nickname']}, email: {user['mail']}, login: {user['login']}, mot de passe: {user['password']}"
                )