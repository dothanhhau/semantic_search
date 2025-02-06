from jsonschema import validate, ValidationError, SchemaError

def validate_json(data, schema):
    """
    Kiểm tra JSON có hợp lệ với schema không.

    Args:
        data (dict): Dữ liệu JSON cần kiểm tra.
        schema (dict): Schema định nghĩa cấu trúc JSON.

    Returns:
        bool: True nếu JSON hợp lệ, False nếu không hợp lệ.
        str: Thông báo lỗi nếu không hợp lệ.
    """
    try:
        validate(instance=data, schema=schema)
        return True, "JSON is valid"
    except ValidationError as e:
        return False, f"Validation Error: {e.message}"
    except SchemaError as e:
        return False, f"Schema Error: {e.message}"
