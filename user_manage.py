from user import User

class UserManage:
    def manage_user_accounts():
        user_id = input("ID de l'utilisateur : ")
        user = User.get_user(user_id)
        if not user:
            print("Utilisateur introuvable.")
            return

        suspended_users = UserManage.read_suspended_users_from_file()
        if user_id in suspended_users:
            action = input("Réactiver (R) le compte d'utilisateur ? ")
            if action.lower() == "r":
                UserManage.reactivate_user_account(user_id)
                print("Compte d'utilisateur réactivé.")
            else:
                print("Action invalide. Veuillez sélectionner une action valide.")
        else:
            action = input("Suspendre (S) le compte d'utilisateur ? ")
            if action.lower() == "s":
                suspended_users.append(user_id)
                UserManage.write_suspended_users_to_file(suspended_users)
                print("Compte d'utilisateur suspendu.")
            else:
                print("Action invalide. Veuillez sélectionner une action valide.")

    def read_suspended_users_from_file():
        with open("suspended_users.txt", "r") as file:
            suspended_users = file.readlines()
            suspended_users = [user.strip() for user in suspended_users]
            return suspended_users

    def write_suspended_users_to_file(suspended_users):
        with open("suspended_users.txt", "w") as file:
            for user_id in suspended_users:
                file.write(user_id + "\n")

    def suspend_user_account(user_id):
        user = User.get_user(user_id)
        if user:
            suspended_users = UserManage.read_suspended_users_from_file()
            suspended_users.append(user_id)
            UserManage.write_suspended_users_to_file(suspended_users)

    def reactivate_user_account(user_id):
        user = User.get_user(user_id)
        if user:
            suspended_users = UserManage.read_suspended_users_from_file()
            if user_id in suspended_users:
                suspended_users.remove(user_id)
                UserManage.write_suspended_users_to_file(suspended_users)