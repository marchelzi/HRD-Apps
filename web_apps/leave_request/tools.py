from core.requester import mblast_sender
from leave_request import messages as leave_request_messages
from leave_request.models import LeaveRequest
from core import utils as core_utils


def send_document_to_pic(obj, absolute_url):

    approve_shorter = core_utils.shorten_url(
        absolute_url + obj.get_approve_url(LeaveRequest.APPROVED))

    cancel_shorter = core_utils.shorten_url(
        absolute_url + obj.get_approve_url(LeaveRequest.CANCELED))

    reject_shorter = core_utils.shorten_url(
        absolute_url + obj.get_approve_url(LeaveRequest.REJECTED))

    messages = leave_request_messages.CREATED_LEAVE_REQUEST.format(
        obj.employee.full_name,
        obj.employee.position.name,
        ' '.join([obj.leave_details.start_date.strftime("%d %B %Y"),
                 obj.leave_details.end_date.strftime("%d %B %Y")]),
        obj.leave_details.duration,
        obj.leave_details.reason,
        approve_shorter,
        cancel_shorter,
        reject_shorter

    )

    mblast_sender(messages, obj.employee.branch.person_in_charge.phone)
