from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.accounts_model import AccountModel
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import uuid

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

    if not email or not password:
        return jsonify({"status": 400, "message": "Email và mật khẩu là bắt buộc"}), 400
    
    if AccountModel.find_by_email(email):
        return jsonify({"status": 409, "message": "Email đã tồn tại"}), 409
    
    hashed_password = generate_password_hash(password)
    print(f" Hashed Password: {hashed_password}")
    new_account = {
       "id": str(uuid.uuid1()),    
        "email": email,
        "password": hashed_password,
        "role": 1,
    }
    
    if AccountModel.create_account(new_account):
        return jsonify({"status": 201, "message": "Đăng ký thành công"}), 201
    return jsonify({"status": 500, "message": "Lỗi máy chủ"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = AccountModel.find_by_email(email)
    if user and check_password_hash(user["password"], password):
        access_token = create_access_token(identity={"id": user["id"], "email": user["email"], "role": user["role"]})
        return jsonify({"status": 200, "message": "Đăng nhập thành công", "access_token": access_token})

    return jsonify({"status": 401, "message": "Email hoặc mật khẩu không đúng"}), 401


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"status": 200, "message": "Đăng xuất thành công"})


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()  # Dùng jwt_required thay vì login_required
def profile():
    user = get_jwt_identity()  # Lấy thông tin user từ token

    return jsonify({
        "status": 200,
        "user": user  # Trả về thông tin từ JWT
    })

