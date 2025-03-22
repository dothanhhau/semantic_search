from flask import Blueprint, request, jsonify, render_template
from app.models.accounts_model import AccountModel
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/')

@auth_bp.route('/register', methods=['GET'])
def show_register_page():
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET'])
def show_login_page():
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if (not email) or (not password):
        return jsonify({"status": 400, "message": "Email và mật khẩu là bắt buộc"}), 400
    
    if AccountModel.find_by_email(email):
        return jsonify({"status": 409, "message": "Email đã tồn tại"}), 409
    
    new_account = {
        "email": email,
        "password": password,
        "role": 1,
    }
    
    if AccountModel.create_account(new_account):
        return jsonify({"status": 201, "message": "Đăng ký thành công"}), 201
    return jsonify({"status": 500, "message": "Lỗi máy chủ"}), 500

@auth_bp.route('/register_admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if (not email) or (not password):
        return jsonify({"status": 400, "message": "Email và mật khẩu là bắt buộc"}), 400
    
    if AccountModel.find_by_email(email):
        return jsonify({"status": 409, "message": "Email đã tồn tại"}), 409
    
    new_account = {
        "email": email,
        "password": password,
        "role": 0,
    }
    
    if AccountModel.create_account(new_account):
        return jsonify({"status": 201, "message": "Đăng ký thành công"}), 201
    return jsonify({"status": 500, "message": "Lỗi máy chủ"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"status": 400, "message": "Thiếu thông tin đăng nhập"}), 400
    
    user = AccountModel.verify_credentials(email,password)
    if user:
        access_token = create_access_token(identity=email, fresh=True, additional_claims={"role": user['role']})
        return jsonify(status=200, message='Đăng nhập thành công', role=user['role'], access_token=access_token) 
    return jsonify({"status": 401, "message": "Email hoặc mật khẩu không đúng"}), 401
