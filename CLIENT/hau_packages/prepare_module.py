import os
import shutil
import cv2
from preprocess_module import tracking_face
from get_data_module import get_msv_by_class, get_sv_by_msv

def reset_path(path_name, remake=True):
    if os.path.exists(path_name):
        shutil.rmtree(path_name)
    if remake:
        os.mkdir(path_name)

def download_dataset(dataset_path, download_urls):
    os.chdir(dataset_path)
    for down_url in download_urls:
        os.system(f'gdown --folder {down_url}')
    os.chdir('../')

def download_dataset_by_class(dataset_path, class_id):
    reset_path(dataset_path)
    student_msv = get_msv_by_class(class_id)

    students = []
    for msv in student_msv:
        students.append(get_sv_by_msv(msv))

    student_links = []
    for s in students:
        student_links.append(s['LinkAnh'])

    download_dataset(dataset_path, student_links)

def cleaning_dataset(dataset_path, haar_model):
    for fold in os.listdir(dataset_path):
        fold_dir = os.path.join(dataset_path, fold)
        if os.path.isdir(fold_dir):
            face_count = 0
            for img in os.listdir(fold_dir):
                oldPATH_img = os.path.join(fold_dir, img)
                img = cv2.imread(oldPATH_img)
                list_face = tracking_face(img, haar_model)
                for face in list_face:
                    fold_img = os.path.join(fold_dir, fold + "-" + str(face_count) + '.' + oldPATH_img.split(".")[-1])
                    cv2.imwrite(fold_img, face)
                    face_count += 1
                if '-' not in img:
                    os.remove(os.path.abspath(oldPATH_img))