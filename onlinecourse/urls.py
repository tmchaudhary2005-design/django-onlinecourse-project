from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # ... (Keep your existing paths here, like index and course_details) ...

    # CRITERIA: paths for submit and show_exam_result
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/exam_result/', views.show_exam_result, name='show_exam_result'),
]
