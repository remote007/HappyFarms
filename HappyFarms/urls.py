from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib import admin
from Farms import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/city_envcomponents/<str:city>/', views.city_envcomponents),
    path('', include('Farms.urls'))
]
