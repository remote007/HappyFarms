from django.urls import path
from . import views


urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('environment_data', views.environment_data, name='environment_data'),

]