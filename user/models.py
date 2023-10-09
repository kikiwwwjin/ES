from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.
class User(AbstractBaseUser):
    '''
    ○ 사용자
    필드 정의
        username(사용자 이름) : 본인 이름
        userid(아이디) : 고유 ID
        password(비밀번호) : 비밀번호(Default로 존재)
    '''
    username = models.CharField(max_length=50, unique=True, null=True, default='')
    # username = models.CharField(max_length=50, unique=True)
    userid = models.CharField(max_length=50, unique=True, null=True, default='')
    # userid = models.CharField(max_length=50, unique=True)
    USERNAME_FIELD = 'userid'
    # password = models.CharField() # Default로 쓰자

    class Meta: # 우리가 원하는 테이블명을 정의할 수 있음 기본(auth_user)
        db_table = 'user'
