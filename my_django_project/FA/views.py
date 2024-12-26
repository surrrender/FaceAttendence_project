import io
import traceback
from datetime import datetime

import face_recognition
import numpy as np

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from .models import FaceEncoding
from .models import AbsentPerson
from .models import ClassInstance


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detect_face(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')  # 前端传递的文件字段名是 'file'
        if not uploaded_file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        lecture_name = request.POST.get('lecture_name')
        if not lecture_name:
            return JsonResponse({'error': 'No lecture provided'}, status=400)
        # 验证文件类型和大小
        if uploaded_file.content_type not in ['image/jpeg', 'image/png']:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)

        # 保存文件
        save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

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
        return JsonResponse(
            {'message': '人脸位置信息', 'face_locations': face_locations, 'save_path': save_path}
        )
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
            lecture_name = data.get('lecture_name')
            # 检查必需的字段是否存在
            if not face_locations or not names or not image_path:
                return JsonResponse({'error': 'Missing face_locations, names, or image_path'}, status=400)
            # 创建对应的班级
            class_instance = ClassInstance(user=request.user, lecture=lecture_name, image_path=image_path)
            class_instance.save()
            # load image
            image = face_recognition.load_image_file(image_path)
            for face_location, name in zip(face_locations, names):
                encodings = face_recognition.face_encodings(image, [tuple(face_location)])
                if encodings:
                    encoding_binary = encodings[0].tobytes()  # 转为字节格式存储
                    class_instance = ClassInstance.objects.get(user=request.user, lecture=lecture_name)
                    # 创建数据库对象并保存
                    face_encoding = FaceEncoding(class_instance=class_instance, lecture=lecture_name, name=name,
                                                 encoding=encoding_binary)
                    face_encoding.save()

                else:
                    # 如果没有检测到编码，跳过并记录日志
                    print(f"No encoding found for face at location: {face_location}")
            return JsonResponse({'message': 'Face encoding saved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_attendance(request):
    """
    接收前端发送来的照片，使用face_recognition来提取出所有的人脸编码
    讲数据库中face_encodings这张table所有的人名（不同名）提取出来作为一个集合
    将每一个人脸编码与数据库中的所有人脸一一比对，辨认出当前人脸，从集合中剔除
    最终将集合剩余的人名再次存储在数据库中一个信息的table attendance中，然后发送给前端
    """
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')  # 前端传递的文件字段名是 'file'
        attendance_date = request.POST.get('time')
        lecture_name = request.POST.get('lecture_name')
        try:
            time_obj = datetime.strptime(attendance_date, '%Y/%m/%d %H:%M')  # 根据前端的格式解析时间
        except ValueError:
            return JsonResponse({'error': 'Invalid time format'}, status=400)

        if not uploaded_file:
            return JsonResponse({'error': 'No file provided'}, status=400)

        # 验证文件类型和大小
        if uploaded_file.content_type not in ['image/jpeg', 'image/png']:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)
        try:
            # 讲上传文件读取为字节数据
            image_bytes = uploaded_file.read()
            image_np = face_recognition.load_image_file(io.BytesIO(image_bytes))

            face_encodings = face_recognition.face_encodings(image_np)
            if not face_encodings:
                return JsonResponse({'message': 'No faces found in the image'}, status=200)

            # 从数据库中获取所有人名和对应的编码
            all_register_faces = FaceEncoding.objects.filter(lecture=lecture_name)
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
            # 如何将数组转为json格式的数据
            return_value = [{'name': name, 'time': attendance_date} for name in absent_names]
            print(return_value)

            class_instance = ClassInstance.objects.get(user=request.user, lecture=lecture_name)
            # 存储人名
            for name in absent_names:
                absent_person = AbsentPerson(class_instance=class_instance, time=time_obj, name=name)
                absent_person.save()
            return JsonResponse(
                {'message': '人脸位置信息', 'absent_names': return_value}
            )

        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def require_lectures(request):
    print("进入了获取课程信息的视图")
    try:
        class_instances = ClassInstance.objects.filter(user=request.user)
        lectures = list(class_instance.lecture for class_instance in class_instances)
        return_value = [{'value': lecture} for lecture in lectures]
        return JsonResponse(
            {'message': '课程信息', 'lectureNames': return_value}, status=200
        )
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def show_absent_information(request):
    try:
        class_instances = ClassInstance.objects.filter(user=request.user)
        class_instance = None
        time_obj = None
        # 获取前端发送来的课程和时间信息
        data = json.loads(request.body)

        if 'lectureName' in data and data['lectureName']:
            class_instance = ClassInstance.objects.get(user=request.user, lecture=data['lectureName'])
        if 'date' in data and data['date']:
            time_obj = datetime.strptime(data['date'], '%Y/%m/%d %H:%M')

        if class_instance is None and time_obj is None:# 发送过来的两个信息都为空
            absent_persons = AbsentPerson.objects.filter(class_instance__in=class_instances)
        else:# 一个为空和两个都不为空的情况
            if class_instance is not None:
                absent_persons = AbsentPerson.objects.filter(class_instance=class_instance)
            if time_obj is not None:
                absent_persons = AbsentPerson.objects.filter(time=time_obj)

        return_value = [{'lecture': person.class_instance.lecture, 'time': person.time, 'name': person.name} for person in absent_persons]
        return JsonResponse(
            {'message': '课程信息', 'tableData': return_value}, status=200
        )
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
