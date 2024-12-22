from django.test import TestCase

# Create your tests here.
import os

path = r"D:\石卓\数据库实践\DB_Project\my_django_project\venv\Lib\site-packages\face_recognition_models\models\shape_predictor_68_face_landmarks.dat"
if not os.path.exists(path):
    print("文件不存在")

with open(r"D:\石卓\数据库实践\DB_Project\my_django_project\venv\Lib\site-packages\face_recognition_models\models\shape_predictor_68_face_landmarks.dat", 'rb') as file:
    data = file.read()
    print(data)
