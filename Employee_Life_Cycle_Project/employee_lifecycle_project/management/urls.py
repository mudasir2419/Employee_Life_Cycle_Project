from django.urls import path
from . import views


urlpatterns = [
    path('', views.redirect_to_login, name='home'),  
    path('dashboard/', views.dashboard, name='dashboard'),

    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_or_edit_employee, name='add_employee'),
    path('employees/edit/<int:emp_id>/', views.add_or_edit_employee, name='edit_employee'),
    path('employees/delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),

    path('employees/<int:emp_id>/onboard/', views.onboard_employee, name='onboard_employee'),   
    path('employees/<int:emp_id>/offboard/', views.offboard_employee, name='offboard_employee'),

    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_or_update_department, name='add_department'),
    path('departments/edit/<int:dept_id>/', views.add_or_update_department, name='update_department'),
    path('departments/delete/<int:dept_id>/', views.delete_department, name='delete_department'),
]
