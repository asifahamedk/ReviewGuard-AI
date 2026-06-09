from django.urls import path

from .views import home
from .views import dashboard,history

urlpatterns = [
    path('',home,name='home'),
    path('dashboard/', dashboard, name='dashboard'),
]
    