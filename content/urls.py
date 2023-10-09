from django.urls import path
from .views import Sk_magic # 사이트별
from .views import UploadData, Upload_item_master, Dupcheck_item_master, Filecheck_item_master # 기능별

# CSS 관련 패키지 임포트
from django.conf.urls.static import static
from django.conf import settings

# 모델별 상세페이지
urlpatterns = [
    # 모델별(content) 상세페이지
    path('sk_magic/', Sk_magic.as_view()),  # 아이템 마스터 파일 정보 확인

    # path('model_main/sk_magic/', Sk_magic.as_view()),  # SK MAGIC 모델(상세페이지)
    path('item_master_filecheck', Filecheck_item_master.as_view()),  # 아이템 마스터 파일 정보 확인
    path('item_master_dupcheck', Dupcheck_item_master.as_view()),  # 아이템 마스터 중복체크
    path('item_master_upload', Upload_item_master.as_view()),  # 아이템 마스터 업로드

    # 모델별 정제 결과
    # path('model_main/sk_magic/ajax_test', UploadData.as_view()), # SK MAGIC 정제 결과(상세페이지)
    # 모델별 아이템 마스터 등록하기
    path('add_item', UploadData.as_view()), # 아이템 마스터 등록하기
]
# # STATIC Default 경로 세팅
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)