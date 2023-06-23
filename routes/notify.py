from flask import Blueprint, request, jsonify
from query import notify as Notify

bp = Blueprint("notify", __name__, url_prefix="/notify")

@bp.route("/getall", methods=["GET"])
def get_all_notify():
    try:
        notify = Notify.Notify()
        notify_array = notify.get_all_notify()
        return jsonify(notify_array), 200
    except Exception as e:
        return jsonify({"err": e}), 404

@bp.route("/add", methods=["POST"])
def add_notify():
    try:
        notify = Notify.Notify()
        data = request.get_json()
        mess = data["mess"]
        notify.add_notify(mess)
        return jsonify({"code": 0}), 200
    except Exception as e:
        return jsonify({"err": e}), 404

@bp.route("/delete", methods=["DELETE"])
def delete_notify():
    try:
        notify = Notify.Notify()
        data = request.get_json()
        id = data["id"]
        notify.delete_notify(id)
        return jsonify({"code": 0}), 200
    except Exception as e:
        return jsonify({"err": e}), 404