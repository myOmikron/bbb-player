import json

from django import views
from django.http import JsonResponse

from rc_protocol.rc_protocol import validate_checksum

from bbb_player import settings


def check_params(request, salt):
    try:
        decoded = json.loads(request)
    except json.JSONDecodeError:
        return {"success": False, "message": "JSON could not be decoded", "status": 400}
    if "checksum" not in decoded:
        return {"success": False, "message": "Missing checksum parameter", "status": 400}
    if not validate_checksum(decoded, settings.RCP_SECRET, salt, time_delta=settings.RCP_TIMEDELTA):
        return {"success": False, "message": "Checksum was not correct", "status": 401}
    if "recordings" not in decoded:
        return {"success": False, "message": "Missing recordings parameter", "status": 400}
    if not isinstance(decoded["recordings"], list):
        return {"success": False, "message": "Parameter recordings is not a list", "status": 400}
    return {"success": True, **decoded}


class GetRecordingsView(views.View):
    def post(self, request, *args, **kwargs):
        decoded = check_params(request, "getRecordings")
        if not decoded["success"]:
            return JsonResponse({"success": False, "message": decoded["message"]}, status=decoded["status"])
        # TODO:
        # If empty: Return all
        # If one: Gather metadata from one
        # If multiple: Gather metadata from those, concatenate


class DeleteRecordingsView(views.View):
    def post(self, request, *args, **kwargs):
        decoded = check_params(request, "deleteRecordings")
        if not decoded["success"]:
            return JsonResponse({"success": False, "message": decoded["message"]}, status=decoded["status"])
        if len(decoded["recordings"]) == 0:
            return JsonResponse({"success": False, "message": "Parameters recordings has to contain an element"})
        # TODO: Try deleting all recordings
