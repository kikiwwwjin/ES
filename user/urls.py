from django.urls import path, include
# view
from .views import Join, Login

urlpatterns = [
    path('join', Join.as_view()),
    path('login', Login.as_view()),
]
