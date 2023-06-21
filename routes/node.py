from flask import Blueprint, request, jsonify
from query import node as Node

bp = Blueprint("node", __name__, url_prefix="/node")

@bp.route('/create', methods=["POST"])
def create_node():
    try:
        node = Node()
        body = request.get_json()
        name = body["name"]
        id = body["id"]
        query_code = node.insert_node(id, name, 1024)
        return jsonify({"code": str(query_code)}), 200
    except Exception as e:
        return jsonify({"err": e}), 404
    
@bp.route('/rename', methods=["PUT"])
def rename_node():
    try:
        node = Node()
        body = request.get_json()
        query_code = node.rename_node(body["id"], body["new_name"])
        return jsonify({"code": str(query_code)}), 200
    except Exception as e:
        return jsonify({"err": e}), 404

@bp.route('/delete', methods=["DELETE"])
def delete_node():
    try:
        node = Node()
        data = request.get_json()
        id = data["id"]
        node.delete_node(id)
        return jsonify({"code": 0}), 200
    except Exception as e:
        return jsonify({"err": e}), 404


