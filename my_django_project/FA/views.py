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

        # image = Image.open(save_path)
        # image_np = np.array(image)
        image_np = face_recognition.load_image_file(request.FILES['file'])

        #读取图片
        image = face_recognition.load_image_file(save_path)
        #人脸识别
        face_locations = face_recognition.face_locations(image)
        return JsonResponse(
            {'message': '人脸位置信息', 'face_locations': face_locations,'save_path':save_path}
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
    if request.method == 'POST':
        try:
            # 从请求中获取人脸编码和姓名
            data = json.loads(request.body)
            face_locations = data.get('face_locations')
            names = data.get('names')
            image_path = data.get('path')

            # 检查必需的字段是否存在
            if not face_locations or not names or not image_path:
                return JsonResponse({'error': 'Missing face_locations, names, or image_path'}, status=400)
            # load image
            image = face_recognition.load_image_file(image_path)
            for face_location, name in zip(face_locations, names):
                # 通过face_location来从image_path中加载图片，然后通过face_recognition获得对应人脸的编码,编码的格式为    # 存储人脸编码，BLOB 类型
                #     encoding = models.BinaryField()
                # 讲人脸编码和对应姓名保存到数据库

                # extract the encoding of the current face
                encodings = face_recognition.face_encodings(image,[face_location])
                if encodings:
                    # 取第一个编码（通常只检测一个人脸）
                    encoding_binary = encodings[0].tobytes()  # 转为字节格式存储
                    # 创建数据库对象并保存
                    face_encoding = FaceEncoding(name=name, encoding=encoding_binary)
                    face_encoding.save()
                else:
                    # 如果没有检测到编码，跳过并记录日志
                    print(f"No encoding found for face at location: {face_location}")
            return JsonResponse({'message': 'Face encoding saved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
