from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# A model is the single, definitive source of information about your data.
# It contains the essential fields and behaviors of the data you’re storing.

class ClassInstance(models.Model):
    # 关联Djiango自带的User模型
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return self.lecture


class FaceEncoding(models.Model):
    # 关联Djiango自带的User模型
    # 可以在这里不加user属性，每次通过user选出对应的class_instance，然后用class_instance来取得这些数据
    # 课程实例
    class_instance = models.ForeignKey(ClassInstance, on_delete=models.CASCADE)
    # 课程名
    lecture = models.CharField(max_length=255)
    # 存储名字字段，最多 255 个字符
    name = models.CharField(max_length=255)
    # 存储人脸编码，BLOB 类型
    encoding = models.BinaryField()
    # 在模型中可以定义 __str__ 方法，方便输出对象时查看相关信息

    def __str__(self):
        return self.name


class AbsentPerson(models.Model):
    class_instance = models.ForeignKey(ClassInstance, on_delete=models.CASCADE)
    time = models.TimeField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



