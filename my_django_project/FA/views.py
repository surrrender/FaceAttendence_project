import io
import traceback

from PIL import Image
import face_recognition
import numpy as np

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

import base64

from rest_framework.utils import json
from .models import FaceEncoding
from django.core.files.uploadedfile import InMemoryUploadedFile

@csrf_exempt
def detect_face(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')  # 前端传递的文件字段名是 'file'
        if not uploaded_file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # 验证文件类型和大小
        if uploaded_file.content_type not in ['image/jpeg', 'image/png']:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        # 保存文件
        save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
        print(save_path)
        # 确保目标目录存在，创建不存在的目录
        dir_name = os.path.dirname(save_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # 读取图片
        image = face_recognition.load_image_file(save_path)
        # 人脸识别
        face_locations = face_recognition.face_locations(image)
        print("发送之前的location", face_locations)
        return JsonResponse(
            {'message': '人脸位置信息', 'face_locations': face_locations, 'save_path': save_path}
        )
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    #     #获取所有人脸编码
    #     face_encodings = face_recognition.face_encodings(image_np)
    #     print(face_encodings[0])
    #
    #     # 将每个面部编码转换为 Base64 编码
    #     # encodings_list = [encoding.tolist() for encoding in face_encodings]
    #     encodings_list = [base64.b64encode(encoding).decode('utf-8')for encoding in face_encodings]
    #     # 返回文件路径或其他需要的信息
    #     return JsonResponse(
    #         {'message': 'File uploaded successfully', 'face_encodings': encodings_list})
    # else:
    #     return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def save_face_encoding(request):
    """
    接收前端请求，提取并存储人脸编码到数据库。
    """
    print("进入函数")
    if request.method == 'POST':
        try:
            # 从请求中获取人脸编码和姓名
            data = json.loads(request.body)
            face_locations = data.get('face_locations')
            names = data.get('names')
            image_path = data.get('save_path')

            print("location from frontend", face_locations)
            print(names)
            print(image_path)
            # 检查必需的字段是否存在
            if not face_locations or not names or not image_path:
                return JsonResponse({'error': 'Missing face_locations, names, or image_path'}, status=400)
            # load image
            image = face_recognition.load_image_file(image_path)
            for face_location, name in zip(face_locations, names):
                # 通过face_location来从image_path中加载图片，然后通过face_recognition获得对应人脸的编码,编码的格式为    # 存储人脸编码，BLOB 类型
                #     encoding = models.BinaryField()
                # 讲人脸编码和对应姓名保存到数据库
                print(face_location, name)
                # extract the encoding of the current face
                encodings = face_recognition.face_encodings(image, [tuple(face_location)])
                # print("encodings的数据",encodings)
                if encodings:
                    # 取第一个编码（通常只检测一个人脸）
                    # print("encodings[0]的数据", encodings[0])
                    encoding_binary = encodings[0].tobytes()  # 转为字节格式存储
                    # print(encoding_binary)
                    # 创建数据库对象并保存
                    face_encoding = FaceEncoding(name=name, encoding=encoding_binary)
                    # print(face_encoding.encoding)
                    face_encoding.save()

                else:
                    # 如果没有检测到编码，跳过并记录日志
                    print(f"No encoding found for face at location: {face_location}")
            return JsonResponse({'message': 'Face encoding saved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def convert_uploaded_file_to_bytes(uploaded_file: InMemoryUploadedFile) -> bytes:
    # 检查上传的文件是否存在
    if uploaded_file:
        # 读取文件内容并返回字节数据
        byte_data = uploaded_file.read()  # 这将是一个字节串
        return byte_data
    return None

@csrf_exempt
def check_attendance(request):
    """
    接收前端发送来的照片，使用face_recognition来提取出所有的人脸编码
    讲数据库中face_encodings这张table所有的人名（不同名）提取出来作为一个集合
    将每一个人脸编码与数据库中的所有人脸一一比对，辨认出当前人脸，从集合中剔除
    最终将集合剩余的人名再次存储在数据库中一个信息的table attendance中，然后发送给前端
    """
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')  # 前端传递的文件字段名是 'file'
        if not uploaded_file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # 验证文件类型和大小
        if uploaded_file.content_type not in ['image/jpeg', 'image/png']:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        print("正确请求了视图")
        try:
            print(type(uploaded_file))
            # 讲上传文件读取为字节数据
            image_bytes = uploaded_file.read()
            # 讲PIL图像转换为numpy数组（face_recognition需要这种格式）
            image_np = face_recognition.load_image_file(io.BytesIO(image_bytes))

            face_encodings = face_recognition.face_encodings(image_np)
            if not face_encodings:
                return JsonResponse({'message': 'No faces found in the image'}, status=200)

            # 从数据库中获取所有人名和对应的编码
            all_register_faces = FaceEncoding.objects.all()
            name_set = set(face.name for face in all_register_faces)

            # 比对人脸编码，识别出席人员
            identified_names = set()
            for encoding in face_encodings:
                for face in all_register_faces:
                    stored_encoding = face.encoding
                    stored_encoding_np = np.frombuffer(stored_encoding, dtype=np.float64)
                    match = face_recognition.compare_faces([stored_encoding_np], encoding, tolerance=0.4)
                    if match[0]:
                        identified_names.add(face.name)
                        print("检测到人脸", face.name)

            absent_names = name_set - identified_names
            absent_names = list(absent_names)
            print(absent_names)
            return JsonResponse(
                {'message': '人脸位置信息', 'absent_names': absent_names}
            )

        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
