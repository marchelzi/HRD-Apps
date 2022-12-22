
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from leave_request.models import LeaveBalance,  LeaveDetail, LeaveRequest


@receiver(post_save, sender="employee.Employee")
def update_leave_balance(sender, instance, created, **kwargs):
    # get current date
    dt_now = timezone.now().date()
    if instance.joint_date:
        already_one_year = dt_now - instance.joint_date
        if not hasattr(instance, 'leave_balances'):
            if already_one_year.days >= 365:
                LeaveBalance.objects.create(
                    employee=instance,
                    total_balance=12,
                    balance=12
                )
            else:
                LeaveBalance.objects.create(
                    employee=instance,
                    total_balance=0,
                    balance=0
                )
        else:
            if already_one_year.days <= 365:
                instance.leave_balances.total_balance = 0
                instance.leave_balances.balance = 0
                instance.leave_balances.save()
            else:
                if instance.leave_balances.total_balance == 0:
                    instance.leave_balances.total_balance = 12
                    instance.leave_balances.balance = 12
                    instance.leave_balances.save()


@receiver(post_save, sender='leave_request.LeaveRequest')
def decrease_leave_balance_by_leave_request(sender, instance: LeaveRequest, created, **kwargs):
    instance.employee.leave_balances.recalculate_balance()
