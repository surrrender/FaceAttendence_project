from django.db import models


# Create your models here.
# A model is the single, definitive source of information about your data.
# It contains the essential fields and behaviors of the data you’re storing.
class FaceEncoding(models.Model):
    # 自动生成 ID 字段
    id = models.AutoField(primary_key=True)
    # 存储名字字段，最多 255 个字符
    name = models.CharField(max_length=255)
    # 存储人脸编码，BLOB 类型
    encoding = models.BinaryField()

    # 在模型中可以定义 __str__ 方法，方便输出对象时查看相关信息
    def __str__(self):
        return self.name


class AbsentPerson(models.Model):
    time = models.TimeField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
