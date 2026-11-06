from django.contrib import admin
from .models import Profile, Question, ExamAttempt, StudentAnswer

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(ExamAttempt)
admin.site.register(StudentAnswer)

admin.site.site_header = "School Exam Portal Admin"
admin.site.site_title = "Exam Portal"
admin.site.index_title = "Welcome to the Exam Portal"