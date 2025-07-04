
import time
from threading import Thread
from django.core.mail import send_mail

queue = []

def process_queue():
    from .models import Employee 

    while True:
        if queue:
            task = queue.pop(0)
            employee_id, action = task
            employee = Employee.objects.get(id=employee_id)

            if action == "onboard":
                send_mail(
                    "Welcome to the Company",
                    f"Hi {employee.name}, welcome onboard!",
                    "your_email@gmail.com",
                    [employee.email],
                )
                employee.status = "onboarded"
                employee.save()
            elif action == "offboard":
                send_mail(
                    "Goodbye from the Company",
                    f"Hi {employee.name}, goodbye and good luck!",
                    "your_email@gmail.com",
                    [employee.email],
                )
                employee.status = "offboarded"
                employee.save()
        time.sleep(2)  

def start_worker():
    t = Thread(target=process_queue)
    t.daemon = True
    t.start()
