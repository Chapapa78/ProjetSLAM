import numpy as np
import os
import cv2

CHEMIN_COLMAP = '/Users/iliesse/Documents/ProjetSLAM/TEST/'
CHEMIN_IMAGES = '/Users/iliesse/Documents/ProjetSLAM/Imagendirect/'


def charger_donnees_colmap(chemin_colmap):
    cameras = {}
    with open(os.path.join(chemin_colmap, 'cameras.txt'), 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            data = line.split()
            try:
                camera_id = int(data[0])
            except ValueError:
                print(f"Ignorant la ligne invalide dans 'cameras.txt': {line}")
                continue
            camera_type = data[1]
            cameras[camera_id] = {'type': camera_type, 'params': data[2:]}

    images = []
    with open(os.path.join(chemin_colmap, 'images.txt'), 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            data = line.split()
            try:
                image_id = int(data[0])
                camera_id = int(data[1])
            except ValueError:
                print(f"Ignorant la ligne invalide dans 'images.txt': {line}")
                continue
            image_path = os.path.join(chemin_colmap, 'images', data[2])  # Modifier le chemin de l'image
            image_pose = np.array(list(map(float, data[3:]))) if len(data) > 3 else None
            images.append({'id': image_id, 'camera_id': camera_id, 'path': image_path, 'pose': image_pose})

    points3D = {}
    with open(os.path.join(chemin_colmap, 'points3D.txt'), 'r') as file:
        for line in file:
            if line.startswith('#'):
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


def charger_images(chemin_images):
    images = []
    for filename in os.listdir(chemin_images):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(chemin_images, filename)
            images.append({'path': image_path})
    return images


def charger_image(image_path):
    return cv2.imread(image_path)


def comparer_image_colmap(image, carte, seuil_distance=10):
    orb = cv2.ORB_create()
    kp_image, des_image = orb.detectAndCompute(image, None)

    if not kp_image:
        print("Aucun point d'intérêt détecté dans l'image.")
        return []

    correspondances = []
    for point_id, coordinates in carte.items():
        distance = np.linalg.norm(coordinates[:2] - np.array([kp.pt for kp in kp_image]), axis=1)
        if np.min(distance) < seuil_distance:
            correspondances.append((point_id, kp_image[np.argmin(distance)].pt))

    return correspondances


cameras, _, points3D = charger_donnees_colmap(CHEMIN_COLMAP)
images = charger_images(CHEMIN_IMAGES)

for image_data in images:
    image_path = image_data['path']
    image = charger_image(image_path)
    correspondances = comparer_image_colmap(image, points3D)
    image_with_correspondences = cv2.drawKeypoints(image, [cv2.KeyPoint(x=pt[1][0], y=pt[1][1], _size=10) for pt in
                                                           correspondances], None, color=(0, 255, 0), flags=0)
    cv2.imshow("Image avec correspondances COLMAP", image_with_correspondences)
    cv2.waitKey(0)

cv2.destroyAllWindows()