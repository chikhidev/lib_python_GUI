def write_to_file(file_name, data):
    try:
        with open(file_name, "a") as file:
            file.write(data + "\n")
        print("Données écrites avec succès.")
    except FileNotFoundError:
        print(f"Fichier {file_name} introuvable.")


def read_from_file(file_name):
  try:
      with open(file_name, "r") as file:
          content = file.readlines()
          return content
  except FileNotFoundError:
      print(f"Fichier {file_name} introuvable.")
      return []