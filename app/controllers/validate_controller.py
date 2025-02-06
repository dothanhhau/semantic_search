from flask import Blueprint, request, jsonify
from app.utils.json_validator import validate_json

validate_bp = Blueprint('validate', __name__, url_prefix='/validate')

# Định nghĩa schema JSON mong muốn
JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "age", "email"],
    "additionalProperties": False  # Không cho phép các trường khác ngoài schema
}

@validate_bp.route('/file/json', methods=['POST'])
def validate_json_file():
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400

    data = request.json
    is_valid, message = validate_json(data, JSON_SCHEMA)

    if is_valid:
        return jsonify({"success": message}), 200
    else:
        return jsonify({"error": message}), 400
