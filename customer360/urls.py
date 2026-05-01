from django.contrib import admin
from django.urls import path
from customer_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('create/', views.create_customer, name='create_customer'),
    path('interact/<int:cid>/', views.interact, name='interact'),
    path('summary/', views.summary, name='summary'),

    # Add these for Task 6
    path('submit/', views.submit, name='submit'),
    path('show_exam_result/', views.show_exam_result, name='show_exam_result'),
]
