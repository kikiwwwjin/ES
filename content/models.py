from django.db import models

# Create your models here.

class Model_result(models.Model):
    title = models.TextField() # 타이틀
    option_name = models.TextField() # 옵션명
    manufacturer = models.TextField() # 분류 제조사
    brand = models.TextField() # 분류 브랜드
    model_name = models.TextField() # 분류 모델명
    unit_count = models.TextField() # 모델 개수




# class Item_master_upload_log(models.Model):
#     user_id = models.TextField() # USER ID
#     site = models.TextField() # 사이트(프로젝트)명
#     table_nm = models.TextField() # 테이블명
#     backup_table_nm = models.TextField() # 백업 테이블명
#     reg_date = models.TextField() # 등록날짜
#     reg_time = models.TextField() # 등록시간