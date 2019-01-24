import threading
import uuid
from threading import Thread

import time
from flask import Flask, request, jsonify, copy_current_request_context
from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_restplus import Namespace, Resource, fields, reqparse
import datetime as dt
from datetime import date

DEVICES = {
    "G030PT024426QFFT": {
        "patient_id": "w_miller",
        "name": "red",
    },
    "G030PT0222173RL7": {
        "patient_id": "w_miller",
        "name": "blue",
    },
}

api = Namespace("IOT", description="The generic api endpoints")


def generate_event(request, state):
    """
    {'serialNumber': 'G030PT0222173RL7', 'batteryVoltage': '1705mV', 'clickType': 'SINGLE'}

    :param request:
    :param state:
    :return:
    """
    if "serialNumber" in request:
        patient_id = DEVICES[request["serialNumber"]]["patient_id"]
        medi_name = DEVICES[request["serialNumber"]]["name"]
    else:
        patient_id = "w_miller"
        medi_name = "red"

    event = {}
    h = dt.datetime.now().hour
    now = ""
    if 5 <= h < 11:
        now = "morning"
    elif 10 <= h < 16:
        now = "noon"
    elif 16 <= h < 22:
        now = "evening"
    else:
        now = "night"
    event["time"] = now
    event["patientID"] = str(patient_id)
    event["date"] = str(date.today())
    event["medi"] = medi_name
    event["state"] = state
    event["key"] = event["patientID"] + "-" + event["date"] + "-" + event["medi"] + "-" + event["time"]
    return event


def process(request):
    request["action"] = "create"
    emit('medication', generate_event(request, "taken"), namespace="", broadcast=True)
    print("start")
    print("emit taken")
    request["action"] = "delete"
    time.sleep(10)
    print("emit totake")
    emit('medication', generate_event(request, "totake"), namespace="", broadcast=True)
    print("done")


@api.route("/medication")
class IOTMedication(Resource):
    @api.doc("Create a new medication event")
    def post(self):
        """
        Create iot event
        :return:
        """

        r = request.__copy__()
        content = r.get_json(silent=True)
        process(content)

        response = jsonify(content)
        response.status_code = 201
        return response
