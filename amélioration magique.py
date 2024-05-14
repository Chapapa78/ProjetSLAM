import numpy as np
import cv2
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Fonction pour charger les données extraites de COLMAP à partir des fichiers texte
def charger_donnees_colmap():
    cameras = {}
    with open('C:/Users/qiful/Desktop/COLMAP-3.9.1-windows-no-cuda/Projet_industriel_RnBi_-Cartographie_et_Localisation/TEST/cameras.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):  # Ignorer les lignes commençant par #
                continue
            data = line.split()
            try:
                camera_id = int(data[0])
            except ValueError:
                print(f"Ignorant la ligne invalide dans 'cameras.txt': {line}")
                continue
            camera_type = data[1]
            # Stocker les paramètres de la caméra dans un dictionnaire
            cameras[camera_id] = {'type': camera_type, 'params': data[2:]}
    
    images = []
    with open('C:/Users/qiful/Desktop/COLMAP-3.9.1-windows-no-cuda/Projet_industriel_RnBi_-Cartographie_et_Localisation/TEST/images.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):  # Ignorer les lignes commençant par #
                continue
            data = line.split()
            try:
                image_id = int(data[0])
                camera_id = int(data[1])
            except ValueError:
                print(f"Ignorant la ligne invalide dans 'images.txt': {line}")
                continue
            image_path = data[2]
            images.append({'id': image_id, 'camera_id': camera_id, 'path': image_path, 'pose': None})  # Ajout de la clé 'pose'

    points3D = {}
    with open('C:/Users/qiful/Desktop/COLMAP-3.9.1-windows-no-cuda/Projet_industriel_RnBi_-Cartographie_et_Localisation/TEST/points3D.txt', 'r') as file:
        for line in file:
            if line.startswith('#'):  # Ignorer les lignes commençant par #
                continue
            data = line.split()
            try:
                point_id = int(data[0])
                coordinates = list(map(float, data[1:]))
            except ValueError:
                print(f"Ignorant la ligne invalide dans 'points3D.txt': {line}")
                continue
            points3D[point_id] = coordinates

    return cameras, images, points3D

# Fonction pour initialiser la carte 3D
def initialiser_carte(points3D):
    carte = []  # Liste pour stocker les points 3D de la carte
    for point_id, coordinates in points3D.items():
        carte.append(np.array(coordinates))
    return np.array(carte)  # Convertir la liste en un tableau numpy

# Fonction pour estimer le mouvement de la caméra entre deux images
def estimer_mouvement(image1, image2):
    # Implémenter une méthode pour estimer le mouvement de la caméra, par exemple, en utilisant des descripteurs d'image et une correspondance de points.
    # Retourner la matrice de transformation de la pose de la caméra entre les deux images.
    return np.eye(4)  # Retourner une matrice d'identité pour l'exemple

# Fonction pour obtenir de nouveaux points 3D entre deux poses de caméra
def obtenir_nouveaux_points(pose1, pose2):
    # Simuler la recherche de correspondances de points entre deux images
    correspondances = [(1, 2), (3, 4), (5, 6)]  # Exemple de correspondances de points

    nouveaux_points = []
    for correspondance in correspondances:
        # Simuler la triangulation des correspondances de points pour obtenir de nouveaux points 3D
        point_3D = {
            'id': correspondance[0],  # ID du point 3D simulé
            'xyz': np.random.rand(3)  # Coordonnées 3D simulées
        }
        nouveaux_points.append(point_3D)

    return nouveaux_points

# Fonction pour mettre à jour la carte 3D
def mettre_a_jour_carte(carte, nouveaux_points):
    # Mettre à jour la carte avec de nouveaux points 3D
    for point in nouveaux_points:
        carte[point['id']] = point['xyz']
    return carte

# Fonction pour afficher la localisation d'une image dans la carte 3D
def afficher_localisation_image(image_path, carte, cameras, images):
    # Lire l'image
    image = cv2.imread(image_path)
    
    # Récupérer la pose de la caméra pour l'image donnée
    image_id = None
    for img in images:
        if img['path'] == image_path:
            image_id = img['id']
            camera_id = img['camera_id']
            break
    if image_id is None:
        print(f"Image '{image_path}' non trouvée dans les données.")
        return

    pose_camera = None
    for camera in cameras.values():
        if camera['type'] == 'PINHOLE':
            pose_camera = np.array(camera['params'], dtype=np.float64).reshape(3, 4)
            break
    if pose_camera is None:
        print("Aucune caméra PINHOLE trouvée dans les données.")
        return

    # Afficher la localisation de l'image dans la carte 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(carte[:, 0], carte[:, 1], carte[:, 2], c='b', marker='o', label='Points 3D')
    
    # Calculer la position de l'image dans la carte 3D
    pose_image = np.dot(pose_camera, np.linalg.inv(np.eye(3, 4)))  # Assumant que la pose de la caméra est déjà en coordonnées 3D
    ax.scatter(pose_image[0], pose_image[1], pose_image[2], c='r', marker='x', label='Position de l\'image')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.show()

# Fonction principale SLAM
def slam():
    # Charger les données extraites de COLMAP
    cameras, images, points3D = charger_donnees_colmap()

    # Initialiser la carte 3D
    carte = initialiser_carte(points3D)

    # Boucle principale pour traiter chaque paire d'images successives
    for i in range(len(images) - 1):
        # Estimer le mouvement de la caméra entre deux images consécutives
        transformation_pose = estimer_mouvement(images[i], images[i + 1])

        # Mettre à jour la pose de la caméra dans la carte
        nouvelle_pose = np.dot(transformation_pose, images[i]['pose'])
        images[i + 1]['pose'] = nouvelle_pose

        # Mettre à jour la carte avec de nouveaux points 3D
        nouveaux_points = obtenir_nouveaux_points(images[i]['pose'], images[i + 1]['pose'])
        carte = mettre_a_jour_carte(carte, nouveaux_points)

    return carte

# Exécuter l'algorithme SLAM
carte_3D = slam()

# Écrire la carte 3D dans un fichier texte
with open('carte_3D.txt', 'w') as file:
    for point_id, coordinates in carte_3D.items():
        file.write(f"Point {point_id}: {coordinates}\n")

print("La carte 3D a été enregistrée dans le fichier 'carte_3D.txt'.")

# Exemple d'utilisation : spécifiez le chemin de l'image que vous voulez afficher
image_path = 'C:/Users/qiful/Desktop/COLMAP-3.9.1-windows-no-cuda/Projet_industriel_RnBi_-Cartographie_et_Localisation/couloir 1/test-00019.jpg'
afficher_localisation_image(image_path, carte_3D, cameras, images)
