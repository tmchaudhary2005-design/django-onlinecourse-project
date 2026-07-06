# Make sure these are imported at the top of your views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Submission, Choice

# --- Add this code to the bottom of the file ---

# CRITERIA: submit function
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Assuming the user is enrolled
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        
        # Create a new submission
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Add selected choices to the submission
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice_id = value
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
                
        # Redirect to the exam result page
        return redirect('onlinecourse:show_exam_result', course_id=course.id)
    
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    
    # Get the latest submission
    submission = Submission.objects.filter(enrollment=enrollment).last()
    
    selected_ids = []
    if submission:
        # Extract the IDs of the choices the user selected
        selected_ids = [choice.id for choice in submission.choices.all()]

    total_score = 0
    possible_score = 0
    
    # Iterate through questions to calculate score using is_get_score()
    for question in course.question_set.all():
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    # Calculate grade
    grade = (total_score / possible_score) * 100 if possible_score > 0 else 0
    
    # Context variables required by the grader
    context = {
        'course': course,
        'grade': grade,
        'possible': possible_score,
        'selected_ids': selected_ids,
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
