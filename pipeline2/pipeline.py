import os
import re
import json
from datetime import datetime

def load_sample(path: str):
    """On générateur pour lire le fichier ligne par ligne."""
    with open(path, 'r') as file:
        for line in file:
            yield line.strip()  # On retourne une ligne à la fois

def generate_json(data) -> list[dict]:
    """On transforme les données du générateur en une liste de dictionnaires."""
    result = {}
    for line in data:
        if not line:  # Ici on s'assure que la ligne n'est pas vide
            continue
        parts = line.split()
        name = parts[0]
        montant_str = parts[2]
        montant = float(re.sub(r'[^\d.]', '', montant_str))  # On enlever '€'

        if name not in result:
            result[name] = montant
        else:
            result[name] += montant

    json_result = []
    for name, total in result.items():
        json_result.append({"name": name, "total_sent": total})

    return json_result

def save_result(result: list[dict], sample_name: str):
    """Sauvegarde le résultat sous forme de fichier JSON."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'result_sample_{sample_name}_{timestamp}.json'
    output_path = os.path.join('result', filename)

    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)
    print(f'Results saved to {output_path}')

def process_files():
    """Traite tous les fichiers dans le dossier source."""
    source_dir = 'source'
    archived_dir = 'archived'

    if not os.path.exists(archived_dir):
        os.makedirs(archived_dir)

    # Traiter tous les fichiers dans le dossier source
    for filename in os.listdir(source_dir):
        if filename.endswith('.txt'):
            print(f'Processing file: {filename}')
            file_path = os.path.join(source_dir, filename)

            # Utiliser le générateur pour traiter le fichier ligne par ligne
            data_generator = load_sample(file_path)
            result = generate_json(data_generator)  # Passer le générateur à generate_json
            save_result(result, filename[:-4])  # Enlève .txt pour le nom

            # Déplacer le fichier traité vers le dossier archived
            os.rename(file_path, os.path.join(archived_dir, filename))
            print(f'File {filename} has been archived.')

if __name__ == "__main__":
    process_files()
