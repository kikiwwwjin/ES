from django.db import models

# Create your models here.

class Model_result(models.Model):
    title = models.TextField() # 타이틀
    option_name = models.TextField() # 옵션명
    manufacturer = models.TextField() # 분류 제조사
    brand = models.TextField() # 분류 브랜드
    model_name = models.TextField() # 분류 모델명
    unit_count = models.TextField() # 모델 개수