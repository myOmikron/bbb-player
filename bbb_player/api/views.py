import json
import os
import re
import shlex
import shutil
import subprocess

from django import views
from django.http import JsonResponse, HttpResponse

from rc_protocol.rc_protocol import validate_checksum

from bbb_player import settings


def check_params(request, salt, required_params):
    try:
        decoded = json.loads(request.body)
    except json.JSONDecodeError:
        return {"success": False, "message": "JSON could not be decoded", "status": 400}
    if "checksum" not in decoded:
        return {"success": False, "message": "Missing checksum parameter", "status": 400}
    if not validate_checksum(decoded, settings.RCP_SECRET, salt, time_delta=settings.RCP_TIMEDELTA):
        return {"success": False, "message": "Checksum was not correct", "status": 401}
    for entry in required_params:
        if entry not in decoded:
            return {"success": False, "message": f"Missing recordings {entry}", "status": 400}
    return {"success": True, **decoded}


class GetRecordingsView(views.View):
    def post(self, request, *args, **kwargs):
        decoded = check_params(request, "getRecordings", ["recordings"])
        if not decoded["success"]:
            return JsonResponse({"success": False, "message": decoded["message"]}, status=decoded["status"])
        if not isinstance(decoded["recordings"], list):
            return {"success": False, "message": "Parameter recordings is not a list", "status": 400}
        if len(decoded["recordings"]) == 0:
            files = [os.path.join("/var/bigbluebutton/published/presentation/", x, "recording.xml") for x in os.listdir("/var/bigbluebutton/published/presentation/")]
        else:
            files = [os.path.join("/var/bigbluebutton/published/presentation", x, "recording.xml") for x in decoded["recordings"]]
        try:
            response = ""
            for file in files:
                if os.path.exists(file) and os.path.isfile(file):
                    with open(file) as fh:
                        response += fh.read() + "\n"
            return HttpResponse(response)
        except Exception:
            return HttpResponse("")


class DeleteRecordingsView(views.View):
    def post(self, request, *args, **kwargs):
        decoded = check_params(request, "deleteRecordings", ["recordings"])
        if not decoded["success"]:
            return JsonResponse({"success": False, "message": decoded["message"]}, status=decoded["status"])
        if not isinstance(decoded["recordings"], list):
            return {"success": False, "message": "Parameter recordings is not a list", "status": 400}
        if len(decoded["recordings"]) == 0:
            return JsonResponse({"success": False, "message": "Parameters recordings has to contain an element"})
        for recording in decoded["recordings"]:
            if re.match(r"^[\w\d]+-[\w\d]+$", recording):
                shutil.rmtree(os.path.join("/var/bigbluebutton/published/presentation/", recording))
        return JsonResponse({"success": True, "message": "Reordings has been deleted"})


class UpdatePublishStateView(views.View):
    def post(self, request, *args, **kwargs):
        decoded = check_params(request, "updatePublishState", ["internalMeetingId"])
        if not decoded["success"]:
            return JsonResponse({"success": False, "message": decoded["message"]}, status=decoded["status"])
        internal_meeting_id = decoded["internalMeetingId"]
        cmd = shlex.split(f"python3 /home/bbb-player/bbb-player/bbb_player/worker/main.py -i {internal_meeting_id} -H {settings.HOSTNAME}")
        subprocess.Popen(cmd)
        return HttpResponse("200")
