from django.contrib import admin
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from exams import views

# Protect the admin site — only superusers can enter
admin.site.has_permission = lambda request: request.user.is_active and request.user.is_superuser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exam/<str:language>/', views.take_exam, name='take_exam'),
    path('submit-exam/', views.submit_exam, name='submit_exam'),
    path('result/<int:attempt_id>/', views.result_page, name='result_page'),
    path('scores/', views.view_scores, name='view_scores'),
    path('add-question/', views.add_question, name='add_question'),
    path('db-test/', views.db_test, name='db_test'),
    path('force-admin/', views.force_admin, name='force_admin'),
    path('run-seed/', views.run_seed, name='run_seed'),

]