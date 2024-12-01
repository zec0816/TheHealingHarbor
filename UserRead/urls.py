from django.urls import path
from . import views

app_name = "UserRead"

urlpatterns = [
    path('read/',views.ReadView, name="read"),
    path('read/1', views.Book1View, name="book1"),
    path('read/2', views.Book2View, name="book2"),
    path('read/3', views.Book3View, name="book3"),
    path('read/4', views.Book4View, name="book4"),
    path('read/5', views.Book5View, name="book5"),
]
