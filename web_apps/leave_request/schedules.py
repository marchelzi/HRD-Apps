
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from employee.models import Employee
from leave_request.models import LeaveBalance


@shared_task(name="reset_leave")
def reset_leave_quota():
    dt_now = timezone.now().date()
    emloyees = Employee.objects.filter(
        joint_date__lte=dt_now - timedelta(days=365))
    for employee in emloyees:
        if not hasattr(employee, 'leave_balances'):
            LeaveBalance.objects.create(
                employee=employee,
                total_balance=12,
                balance=12
            )
        else:
            last_balance = employee.leave_balances.balance
            last_balance = 7 if last_balance > 7 else last_balance
            employee.leave_balances.total_balance = 12 + last_balance
            employee.leave_balances.balance = employee.leave_balances.total_balance
            employee.leave_balances.save()


@shared_task(name="check_user_join_date")
def add_leave_to_one_year_user():
    dt_now = timezone.now().date()

    employees = Employee.objects.filter(
        joint_date__lte=dt_now - timedelta(days=365),
        leave_balances__total_balance=0
    )

    for employee in employees:
        if not hasattr(employee, 'leave_balances'):
            LeaveBalance.objects.create(
                employee=employee,
                total_balance=12,
                balance=12
            )
        else:
            employee.leave_balances.total_balance = 12
            employee.leave_balances.balance = 12
            employee.leave_balances.save()
