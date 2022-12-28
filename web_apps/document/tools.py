import os
from tempfile import TemporaryFile
from core.requester import mblast_sender
from document import messages as document_messages
from core import utils as core_utils
from document.models import Document
from docxtpl import DocxTemplate
from celery import shared_task

CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_spk(obj: Document):
    doc = DocxTemplate(os.path.join(CORE_DIR, "document/assets/SPK.docx"))
    context = {
        'doc_number': obj.representation,
        'director_name': obj.approved_by.full_name,
        'director_nik': obj.approved_by.id_number,
        'director_position': obj.approved_by.position,
        'employee_name': obj.employee.full_name,
        'employee_nik': obj.employee.id_number,
        'employee_position': obj.employee.position,
        'description': obj.description,
        'date': obj.created_at.strftime("%d %B %Y"),
    }
    doc.render(context)
    # save to buffer
    with TemporaryFile() as buffer:
        doc.save(buffer)
        buffer.seek(0)
        return buffer.read()


def build_sp(obj: Document):
    doc = DocxTemplate(os.path.join(CORE_DIR, "document/assets/SP.docx"))
    serial_sp = {
        1: 'Pertama',
        2: 'Kedua',
        3: 'Ketiga',
        4: 'Keempat',
        5: 'Kelima',
    }
    context = {
        'doc_number': obj.representation,
        'serial_sp': serial_sp[obj.serial_sp].upper(),
        'director_name': obj.approved_by.full_name,
        'employee_name': obj.employee.full_name,
        'employee_nik': obj.employee.id_number,
        'employee_position': obj.employee.position,
        'description': obj.description,
        'date': obj.created_at.strftime("%d %B %Y"),
    }
    doc.render(context)
    # save to buffer
    with TemporaryFile() as buffer:
        doc.save(buffer)
        buffer.seek(0)
        return buffer.read()


@shared_task(name='send_document_to_pic')
def send_document_to_pic(obj_id, absolute_url):
    obj = Document.objects.get(id=obj_id)
    approve_shorter = core_utils.shorten_url(
        absolute_url + obj.get_approve_url())
    reject_shorter = core_utils.shorten_url(
        absolute_url + obj.get_reject_url())
    messages = document_messages.DOCUMENT_CREATED_MESSAGES.format(
        obj.representation,
        obj.get_document_type_display(),
        obj.employee.full_name,
        obj.description,
        approve_shorter,
        reject_shorter
    )

    mblast_sender(messages, obj.employee.branch.person_in_charge.phone)
