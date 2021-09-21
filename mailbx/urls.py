from mailbx import views
from django.urls import path

urlpatterns = [
    path('main/',views.mainpage),
    path('logout/',views.logout),
    path('wemail/',views.wemail),

]