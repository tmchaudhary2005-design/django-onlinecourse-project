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


# CRITERIA: show_exam_result function
def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    
    # Get the latest submission for this user and course
    submission = Submission.objects.filter(enrollment=enrollment).last()
    
    # Logic to calculate score
    total_questions = course.question_set.count()
    correct_answers = 0
    
    if submission:
        for choice in submission.choices.all():
            if choice.is_correct:
                correct_answers += 1
                
    # Calculate percentage score
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    passed = score >= 80  # Assume 80 is the passing grade
    
    context = {
        'course': course,
        'score': score,
        'passed': passed,
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
