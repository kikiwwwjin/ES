from django.shortcuts import render
from rest_framework.views import APIView



class Sub(APIView):
    def get(self, request):
        print('get으로 호출')
        return render(request, 'cokkack/main.html')

    def post(self, request):
        print('post로 호출')
        return render(request, 'cokkack/main.html')


class Sk_magic(APIView):
    def get(self, request):
        print('sk magic 모델 get으로 호출')
        return render(request, 'models/sk_magic.html')

    def post(self, request):
        print('sk magic 모델 post로 호출')
        return render(request, 'models/sk_magic.html')