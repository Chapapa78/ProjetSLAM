import subprocess
import os
import shutil

def run_command(command):
    """Exécute une commande dans le shell et attend qu'elle se termine."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    try:
        if process.returncode != 0:
            print(f"Erreur: {stderr.decode('utf-8')}")
        else:
            print(stdout.decode('utf-8'))
    except UnicodeDecodeError:
        print(f"Erreur: Impossible de décoder le message d'erreur. Message d'erreur brut: {stderr}")

def create_project(project_path):
    """Crée un nouveau projet COLMAP."""
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    images_path = os.path.join(project_path, "images")
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    run_command(f'colmap feature_extractor --database_path {os.path.join(project_path, "database.db")} --image_path {images_path}')

def add_image_to_project(image_path, project_path):
    """Ajoute une image au projet COLMAP."""
    images_dir = os.path.join(project_path, "images")
    os.makedirs(images_dir, exist_ok=True)
    if os.path.isdir(image_path):
        for filename in os.listdir(image_path):
            shutil.copy(os.path.join(image_path, filename), images_dir)
    else:
        shutil.copy(image_path, images_dir)

def feature_extraction(project_path):
    """Exécute l'extraction des caractéristiques."""
    run_command(f'colmap feature_extractor --database_path {os.path.join(project_path, "database.db")} --image_path {os.path.join(project_path, "images")}')

def import_project(base_project, project_path):
    """Importe un autre projet dans le projet actuel."""
    cameras_file = os.path.join(base_project, "cameras.txt")
    images_file = os.path.join(base_project, "images.txt")
    points3D_file = os.path.join(base_project, "points3D.txt")
    if os.path.exists(cameras_file) and os.path.exists(images_file) and os.path.exists(points3D_file):
        shutil.copy(cameras_file, project_path)
        shutil.copy(images_file, project_path)
        shutil.copy(points3D_file, project_path)
    else:
        print("Erreur: Les fichiers de base du projet n'existent pas.")

def feature_matching(project_path):
    """Exécute la correspondance des caractéristiques."""
    run_command(f'colmap exhaustive_matcher --database_path {os.path.join(project_path, "database.db")}')

def run_model_reconstruction(project_path):
    """Exécute la reconstruction du modèle dans COLMAP."""
    run_command(f'colmap mapper --database_path {os.path.join(project_path, "database.db")}')

def export_data(project_path, output_path):
    """Exporte les données vers un nouveau dossier."""
    model_path = os.path.join(project_path, "sparses")
    if os.path.exists(model_path):
        run_command(f'colmap model_converter --input_path {model_path} --output_path {output_path} --output_type TXT')
    else:
        print(f"Erreur: Le chemin {model_path} n'existe pas.")


def compare_data(image_path, project_path):
    """Compare les données entre une image et le projet (fonction factice pour illustration)."""
    # Implémentez votre logique de comparaison ici
    pass

def find_nearest_camera_pose(image_path, project_path):
    """Trouve la pose de caméra la plus proche de l'image (fonction factice pour illustration)."""
    # Implémentez votre logique pour trouver la pose de caméra la plus proche ici
    pass

# Utilisation exemple
project_path = 'C:/Users/qiful/Desktop/COLMAP-3.9.1-windows-no-cuda/Projet_industriel_RnBi_-Cartographie_et_Localisation_FINALE/workspace'
base_project = 'C:/Users/qiful/Desktop/COLMAP-3.9.1-windows-no-cuda/Projet_industriel_RnBi_-Cartographie_et_Localisation_FINALE/cartographe'
image_path = 'C:/Users/qiful/Desktop/COLMAP-3.9.1-windows-no-cuda/Projet_industriel_RnBi_-Cartographie_et_Localisation_FINALE/workspace/prise robot'
output_path = 'C:/Users/qiful/Desktop/COLMAP-3.9.1-windows-no-cuda/Projet_industriel_RnBi_-Cartographie_et_Localisation_FINALE/workspace/sparses'

create_project(project_path)
add_image_to_project(image_path, project_path)
feature_extraction(project_path)
import_project(base_project, project_path)
feature_matching(project_path)
export_data(project_path, output_path)
compare_data(image_path, project_path)
find_nearest_camera_pose(image_path, project_path)
