import tkinter as tk
from tkinter import messagebox
from user import User
from admin_view import show_admin_view
from user_view import show_user_view

logged_in_user_id = None
is_admin = False
ADMIN_PASSWORD = "admin"
ADMIN_LOGIN = "admin"
ADMIN = "__ID__ADMIN__"


def main():
    root = tk.Tk()
    root.title("Système de Gestion de Bibliothèque")
    root.configure(bg="white")

    role_frame = tk.Frame(root, bg="white")
    root.minsize(width=640, height=480)
    root.configure(bg="white")


    def choose_login_role(role):
        role_frame.pack_forget()

        global login_label, login_entry, password_label, password_entry, login_button
        login_label = tk.Label(
            root, text=f"Saisissez le login {role} :", bg="white", fg="black"
        )
        login_label.pack()
        login_entry = tk.Entry(root, bg="white")
        login_entry.pack()

        if role == "admin":
            password_label = tk.Label(
                root, text="Saisissez le mot de passe admin :", bg="white", fg="black"
            )
            password_label.pack()
            password_entry = tk.Entry(root, show="*", bg="white")
            password_entry.pack()

        login_button = tk.Button(
            root, text="Connexion", command=lambda: login(role), bg="blue", fg="white"
        )
        login_button.pack()

    def login(role):
        global logged_in_user_id, is_admin
        user_login = login_entry.get()
        user_password = password_entry.get() if role == "admin" else None

        if user_login:
            if (
                role == "admin"
                and user_login == ADMIN_LOGIN
                and (not user_password or user_password == ADMIN_PASSWORD)
            ):
                logged_in_user_id = ADMIN
                is_admin = True
                messagebox.showinfo(
                    "Connexion Réussie", "Connecté en tant qu'administrateur."
                )
                clear_login_view()
                show_admin_view(root, logged_in_user_id, logout_callback)
            elif role == "user":
                users = (
                    User.get_users()
                )
                for user in users:
                    if user["login"] == user_login and (
                        not user_password or user["password"] == user_password
                    ):
                        logged_in_user_id = user["user_id"]
                        messagebox.showinfo(
                            "Connexion Réussie", "Connecté en tant qu'utilisateur."
                        )
                        clear_login_view()
                        show_user_view(root, logged_in_user_id, logout_callback)
                        return

                messagebox.showerror(
                    "Échec de la Connexion", "Identifiants de connexion invalides."
                )
            else:
                messagebox.showerror(
                    "Échec de la Connexion", "Rôle de connexion invalide."
                )
        else:
            messagebox.showerror("Échec de la Connexion", "Veuillez saisir un login.")

    def clear_login_view():
        login_label.destroy()
        login_entry.destroy()
        if "password_label" in globals():
            password_label.destroy()
        if "password_entry" in globals():
            password_entry.destroy()
        login_button.destroy()

    def logout_callback():
        global logged_in_user_id, is_admin
        logged_in_user_id = None
        is_admin = False
        root.destroy()
        main()

    role_label = tk.Label(
        role_frame, text="Sélectionnez un rôle de connexion :", bg="white", fg="black"
    )
    role_label.pack()

    admin_button = tk.Button(
        role_frame,
        text="Connexion Admin",
        command=lambda: choose_login_role("admin"),
        bg="blue",
        width=15,
        relief=tk.FLAT,
        fg="white",
    )
    admin_button.pack()

    user_button = tk.Button(
        role_frame,
        text="Connexion Utilisateur",
        command=lambda: choose_login_role("user"),
        width=15,
        bg="blue",
        relief=tk.FLAT,
        fg="white",
    )
    user_button.pack()

    role_frame.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
