
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Employee, Department
from .queue_worker import queue




# ------------------ DASHBOARD ------------------


@login_required
def dashboard(request):
    employees = Employee.objects.select_related('department')
    departments = Department.objects.all()

    # queue with employee name
    live_queue = []
    for emp_id, action in queue:
        try:
            emp = Employee.objects.get(id=emp_id)
            live_queue.append({
                'id': emp.id,
                'name': emp.name,
                'action': action
            })
        except Employee.DoesNotExist:
            continue

    context = {
        'total_employees': employees.count(),
        'total_departments': departments.count(),
        'onboarded': employees.filter(status='onboarded').count(),
        'offboarded': employees.filter(status='offboarded').count(),
        'employees': employees,
        'queue': live_queue,  
    }
    return render(request, 'management/dashboard.html', context)


# ------------------ EMPLOYEE LIST ------------------
@login_required
def employee_list(request):
    dept_id = request.GET.get('department')
    status = request.GET.get('status')

    employees = Employee.objects.select_related('department')

    if dept_id:
        employees = employees.filter(department_id=dept_id)
    if status:
        employees = employees.filter(status=status)

    employees = employees.order_by('-id')  

    departments = Department.objects.all()

    return render(request, 'management/employees.html', {
        'employees': employees,
        'departments': departments
    }
    )
# ------------------ ADD EMPLOYEE ------------------

@login_required
def add_or_edit_employee(request, emp_id=None):
    employee = get_object_or_404(Employee, id=emp_id) if emp_id else None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        doj = request.POST.get('doj')
        dept_id = request.POST.get('department')

        try:
            if employee:
                employee.name = name
                employee.email = email
                employee.date_of_joining = doj
                employee.department_id = dept_id
                employee.save()
                messages.success(request, "Employee updated successfully.")
            else:
                employee = Employee.objects.create(
                    name=name,
                    email=email,
                    date_of_joining=doj,
                    department_id=dept_id
                )
                messages.success(request, "Employee added successfully.")
                queue.append((employee.id, 'onboard'))  # Only for new employees

            return redirect('dashboard')
        except IntegrityError:
            messages.error(request, "An employee with this email already exists.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    departments = Department.objects.all()
    return render(request, 'management/add_employee.html', {
        'employee': employee,
        'departments': departments
    })


# DELETE EMPLOYEE
@login_required
def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    try:
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting employee: {str(e)}")

    return redirect('employee_list')

# ------------------ ONBOARD EMPLOYEE ------------------

@login_required
def onboard_employee(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    emp.status = 'onboarded'
    emp.date_of_exit = None 
    emp.save()
    queue.append((emp.id, 'onboard'))  
    messages.success(request, f"{emp.name} has been onboarded.")
    return redirect('dashboard')
    


# ------------------ OFFBOARD EMPLOYEE ------------------
@login_required
def offboard_employee(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    emp.date_of_exit = timezone.now().date()
    emp.save()
    queue.append((emp.id, 'offboard'))  
    return redirect('dashboard')




# ------------------ DEPARTMENT LIST ------------------
@login_required
def department_list(request):
    departments = Department.objects.all().order_by('-id')  
    return render(request, 'management/departments.html', {
        'departments': departments
    })


# ------------------ ADD / UPDATE DEPARTMENT ------------------
@login_required
def add_or_update_department(request, dept_id=None):
    department = get_object_or_404(Department, id=dept_id) if dept_id else None

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')

        try:
            if department:
                department.name = name
                department.location = location
                department.save()
                messages.success(request, "Department updated successfully.")
            else:
                Department.objects.create(name=name, location=location)
                messages.success(request, "Department added successfully.")

            return redirect('department_list')
        except IntegrityError:
            messages.error(request, "A department with this name already exists.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'management/add_department.html', {
        'department': department
    })


# ------------------ DELETE DEPARTMENT ------------------
@login_required
def delete_department(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)

    try:
        department.delete()
        messages.success(request, "Department deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting department: {str(e)}")

    return redirect('department_list')


# ------------------ FALLBACK REDIRECT ------------------
def redirect_to_login(request):
    return redirect('login')
