from django.contrib import admin
from django.urls import path
from customer_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Customer360 paths
    path('', views.index, name="index"),
    path('create/', views.create_customer, name='create_customer'),
    path('interact/<int:cid>/', views.interact, name='interact'),
    path('summary/', views.summary, name='summary'),

    # Exam paths
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/results/', views.show_exam_result, name='show_exam_result'),

    # Optional: temporary mock exam page for Task 7 screenshot
    path('mock_exam/', views.mock_exam_result, name='mock_exam_result'),
]
