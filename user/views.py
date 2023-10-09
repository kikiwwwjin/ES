from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password # 단방향(비밀번호 생성)
from .models import User


# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        '''
        회원 가입
        '''
        username = request.data.get('username', None) # 사용자명
        userid = request.data.get('userid', None) # 사용자 ID
        password = request.data.get('password', None) # 패스워드

        # 결과 변수
        result_dict = dict()

        # 아이디 중복체크
        dup_userid = User.objects.filter(userid=userid)
        if dup_userid is None: # 아이디가 존재하지 않을 경우
            # INSERT
            User.objects.create(
                username=username,
                userid=userid,
                password=make_password(password),
            )
            result_dict['result'] = '회원가입 완료'
        else: # 아이디가 이미 존재할 경우
            result_dict['result'] = '아이디가 이미 존재합니다.'

        return JsonResponse(result_dict)




class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')