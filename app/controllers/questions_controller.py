import uuid
import io
import pandas as pd
from flask import Blueprint, request, jsonify, send_file
from app.models.questions_model import Questions
from app.services.tokenizer_service import vectorize_text

questions_bp = Blueprint('questions', __name__, url_prefix='/api/questions')

@questions_bp.route('/', methods=['GET'])
def get_all():
    data = Questions.get_all()
    res = []
    for x in data:
        x.pop('vector')
        res.append(x)
    return jsonify(res)

@questions_bp.route('/<id>', methods=['GET'])
def get_question_by_id(id):
    data = Questions.find_by_id(id)
    res = None
    if data:
        res = data[0]
        res.pop('vector')
    return res

@questions_bp.route('/export_reviews', methods=['GET'])
def export_reviews():
    try:
        data = Questions.get_all()
        res = []
        columns = ['STT', 'Câu hỏi', 'Đánh giá', 'Nhận xét']
        for index, x in enumerate(data):
            x.pop('vector')
            res.append([index + 1, x['content'], x['rating'], x['feedback']])
        # Chuyển danh sách thành DataFrame
        df = pd.DataFrame(res, columns=columns)

        # Ghi dữ liệu vào bộ nhớ (không lưu vào file)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="DanhSachDanhGia")

        output.seek(0)  # Đặt lại con trỏ về đầu file

        # Gửi file về client mà không cần lưu trên ổ đĩa
        return send_file(output, as_attachment=True, 
                         download_name="DanhSachDanhGia.xlsx",
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@questions_bp.route('/create', methods=['POST'])
def create_question():
    data = request.get_json()
    Questions.insert({
        "id": str(uuid.uuid4()).replace('-', '_'),
        "content": data['content'],
        'vector': vectorize_text(data['content']),
        "rating": data['rating'],
        "feedback": data.get('feedback', '')
    })

@questions_bp.route('/update/<id>', methods=['PATCH'])
def update_question_by_id(id):
    id = str(id)
    data = request.get_json()
    res = Questions.find_by_id(id)
    if res:
        tmp = res[0]
        tmp['rating'] = int(data['rating'])
        tmp['feedback'] = data['feedback']
        Questions.upsert([tmp])
        return jsonify(status=200, message='Cập nhật thành công')
    else: 
        return jsonify(status=404, message='ID không tồn tại')

@questions_bp.route('/delete/<id>', methods=['DELETE'])
def delete_question_by_id(id):
    id = str(id)
    data = Questions.find_by_id(id)

    if data:
        Questions.delete_by_id(id)
        return {"status": 200, "message": "Xoá thành công"}
    else:
        return {"status": 404, "message": "ID không tồn tại"}

