"""es URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import Sub
# CSS 관련 패키지 임포트
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', Sub.as_view()), # main 페이지(자기소개/특장점)
    # path('main/ajax_test', UploadData.as_view()), # main 페이지(포트폴리오) 보여준다
    # path('main/ajax_test', UploadData.as_view()), # main 페이지(모델결과) 보여준다

    # 모델 메인 페이지(모델을 선택할 수 있음)
    path('model_main/', Sub.as_view()), # 모델 메인 페이지

    # 모델별 페이지
    path('content/', include('content.urls')),
    # 로그인 페이지
    path('user/', include('user.urls'))
]

print('STATIC URL 세팅 :', settings.STATIC_URL)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
