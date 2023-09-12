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
from django.urls import path
from .views import Sub, Sk_magic
from content.views import Main, UploadData
# CSS 관련 패키지 임포트
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', Sub.as_view()), # main 페이지(자기소개/특장점)
    # path('main/ajax_test', UploadData.as_view()), # main 페이지(포트폴리오) 보여준다
    path('main/ajax_test', UploadData.as_view()), # main 페이지(모델결과) 보여준다

    # 포트폴리오 메인 페이지
    # path('portfolio/', Sub.as_view()), # portfolio(포트폴리오)
    # 모델 메인 페이지
    path('model_main/', Sub.as_view()), # 모델 메인 페이지

    # 모델별 상세페이지
    # path('portfolio/sk_magic/', Sk_magic.as_view()), # SK MAGIC 모델(상세페이지)
    # 모델별 상세페이지
    path('model_main/sk_magic/', Sk_magic.as_view()), # SK MAGIC 모델(상세페이지)

    # 모델별 정제 결과
    # path('portfolio/sk_magic/ajax_test', UploadData.as_view()), # SK MAGIC 정제 결과(상세페이지)
    # 모델별 정제 결과
    path('model_main/sk_magic/ajax_test', UploadData.as_view()), # SK MAGIC 정제 결과(상세페이지)


]
print(settings.STATIC_URL)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
