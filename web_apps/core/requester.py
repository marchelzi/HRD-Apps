from django.conf import settings
import requests
from core.circuit_breaker import circuit_breaker


@circuit_breaker
def mblast_sender(message, nomor_telepon):
    AUTH_HEADERS = {"AUTHORIZATION": f"{settings.MBLAST_CLIENT_APIKEY}"}
    req_data = {"client_module": 0}
    req_data["to"] = str(nomor_telepon)
    req_data["client_code"] = settings.MBLAST_CLIENT_CODE
    req_data["message"] = message
    req_data["broadcast"] = True
    try:
        req = requests.post(
            f"{settings.MBLAST_CLIENT_ENDPOINT}/api/message/send/",
            json=req_data,
            headers=AUTH_HEADERS,
        )
        return True
    except Exception as e:
        return False
