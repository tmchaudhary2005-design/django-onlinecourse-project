from django.contrib import admin
# CRITERIA: 7 imported classes
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# CRITERIA: ChoiceInline
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

# CRITERIA: QuestionInline
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# CRITERIA: LessonAdmin
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'content']

# CRITERIA: QuestionAdmin
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']

class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['name', 'pub_date']

# Registering all models
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
