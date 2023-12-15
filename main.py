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

login_frame = None  # Global variable to track the login frame

def main():
    root = tk.Tk()
    root.title("Système de Gestion de Bibliothèque")
    root.configure(bg="white")

    root.minsize(width=640, height=480)
    root.configure(bg="white")
    root.attributes('-zoomed', 1)

    frame = tk.Frame(root, bg="white")
    frame.pack(pady=10)

    role_frame = tk.Frame(frame, bg="white")
    role_frame.grid(row=0, column=0, padx=10)

    def choose_login_role(role):
      global login_frame

      # Hide the role frame
      role_frame.grid_remove()

      # Create the login frame
      login_frame = tk.Frame(frame, bg="white")
      login_frame.grid(row=0, column=1, padx=10, pady=20)

      global login_label, login_entry, password_label, password_entry, login_button, return_button, button_frame

      title_font = ("Arial", 14, "bold")  # Set the desired font size and style for the title
      label_font = ("Arial", 8)  # Set the desired font size for labels

      title_label = tk.Label(
          login_frame, text=f"Login en tant que\n{'administrateur' if role == 'admin' else 'utilisateur'}!", bg="white", fg="black", font=title_font
      )
      title_label.grid(row=0, column=0, columnspan=2, pady=10)

      login_label = tk.Label(
          login_frame, text=f"Login ⤵", bg="white", fg="black", font=label_font
      )
      login_label.grid(row=1, column=0, sticky='w', padx=5, columnspan=2, pady=5)

      login_entry = tk.Entry(login_frame, bg="white", font=("Arial", 10), highlightthickness=0)
      login_entry.grid(row=2, column=0, padx=5, sticky='w', columnspan=2)

      password_label = tk.Label(
          login_frame, text=f"Mot de passe ⤵", bg="white", fg="black", font=label_font
      )
      password_label.grid(row=3, column=0, sticky='w', padx=5, columnspan=2, pady=5)

      password_entry = tk.Entry(login_frame, show="*", bg="white", font=("Arial", 10), highlightthickness=0)
      password_entry.grid(row=4, column=0, padx=5, sticky='w', columnspan=2)

      button_frame = tk.Frame(login_frame, bg="white")
      button_frame.grid(row=5, column=0, padx=5, pady=12, sticky='w', columnspan=2)

      login_button = tk.Button(
          button_frame, text="Connexion", command=lambda: login(role), bg="blue", fg="white", font=("Arial", 10), relief="flat"
      )
      login_button.grid(row=0, column=0)

      return_button = tk.Button(
          button_frame, text="⏎ Retour", command=return_to_role_selection, font=("Arial", 10), relief="flat"
      )
      return_button.grid(row=0, column=1, padx=5)




    def return_to_role_selection():
        login_frame.grid_remove()
        role_frame.grid()

    def login(role):
      global logged_in_user_id, is_admin
      user_login = login_entry.get()
      user_password = password_entry.get()

      if user_login:
          if role == "admin":
              if user_login == ADMIN_LOGIN and (not user_password or user_password == ADMIN_PASSWORD):
                  logged_in_user_id = ADMIN
                  is_admin = True
                  messagebox.showinfo("Connexion Réussie", "Connecté en tant qu'administrateur.")
                  clear_login_view()
                  show_admin_view(root, logged_in_user_id, logout_callback)
              else:
                  messagebox.showerror("Échec de la Connexion", "Identifiants de connexion admin invalides.")
          elif role == "user":
              users = User.get_users()
              for user in users:
                  if user["login"] == user_login and "password" in user and user["password"] == user_password:
                      logged_in_user_id = user["user_id"]
                      messagebox.showinfo("Connexion Réussie", "Connecté en tant qu'utilisateur.")
                      clear_login_view()
                      show_user_view(root, logged_in_user_id, logout_callback)
                      return

              messagebox.showerror("Échec de la Connexion", "Identifiants de connexion utilisateur invalides.")
          else:
              messagebox.showerror("Échec de la Connexion", "Rôle de connexion invalide.")
      else:
          messagebox.showerror("Échec de la Connexion", "Veuillez saisir un login.")



    def clear_login_view():
      global login_label, login_entry, password_label, password_entry, login_button

      # Check if each widget exists before attempting to destroy it
      widgets_to_destroy = [widget for widget in [login_label, login_entry, password_label, password_entry, login_button] if widget is not None]

      for widget in widgets_to_destroy:
          if widget.winfo_exists():
              widget.destroy()

      # Reset the global variables to None
      login_label, login_entry, password_label, password_entry, login_button = (None, None, None, None, None)




    def logout_callback():
        global logged_in_user_id, is_admin
        logged_in_user_id = None
        is_admin = False
        root.destroy()
        main()

    role_label = tk.Label(
      role_frame, text="Sélectionnez un rôle de connexion  ⤵", bg="white", fg="black"
    )
    role_label.grid(row=0, columnspan=2, pady=20)

    admin_button = tk.Button(
      role_frame,
      text="➤ Connexion Admin",
      command=lambda: choose_login_role("admin"),
      bg="white", fg="black",
      width=22,
      relief=tk.FLAT,
    )
    admin_button.grid(row=1, column=0, pady=5)

    user_button = tk.Button(
      role_frame,
      text="➤ Connexion Utilisateur",
      command=lambda: choose_login_role("user"),
      width=22,
      bg="white", fg="black",
      relief=tk.FLAT,
    )
    user_button.grid(row=1, column=1, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
