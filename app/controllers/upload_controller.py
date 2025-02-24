import os
import json
from datetime import datetime
import uuid
from flask import Blueprint, render_template, request
from app.models.document_parts_model import DocumentParts
from app.models.document_model import Document
from app.services.ocr_service import extract_text
from app.services.tokenizer_service import vectorize_text
from app.utils.file_util import is_pdf_file, is_json_file, is_txt_file
from app.utils.data_processing import TextProcessor
from app.utils.convert_data import array2json
from app.utils.constant import Constants 
from dotenv import load_dotenv
load_dotenv()

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/pdf', methods=['GET', 'POST'])
def upload_pdf():
    message = ''
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename and is_pdf_file(file.filename):
            filePath = os.path.join(os.getenv('UPLOAD_FOLDER'), 'pdf', file.filename)
            try:
                file.save(filePath)

                # lấy text
                filename = file.filename
                text = extract_text(filePath)

                documents = TextProcessor.split_documents(text, Constants.DOC_SEPARATOR)
                # clean text
                for i in range(1, len(documents)):
                    document_name = ''
                    extracted_content = TextProcessor.extract_content(documents[i], Constants.RE_CONTENT_EXTRACTOR)
                            
                    doc_id = str(uuid.uuid4())
                    doc_name = TextProcessor.clean(document_name)
                    doc_vector = vectorize_text(doc_name)

                    if Document.load_collection():
                        Document.insert_one({
                            "id": doc_id,
                            "name": doc_name,
                            "vector": doc_vector,
                            "file_name": filename
                        })
                        Document.release_collection()

                        if DocumentParts.load_collection():
                            DocumentParts.create_partition(doc_id)
                            DocumentParts.insert_many([], doc_id)
                            DocumentParts.release_collection()

                message = 'Save db success'
            except Exception as e:
                message = e
        else:
            message = 'Invalid file. Please upload a PDF.'
    return render_template('upload_pdf.html', message=message)

@upload_bp.route('/json', methods=['GET', 'POST'])
def upload_json():
    if request.method == 'POST':
        # send file
        file = request.files.get('file')
        if file and file.filename and is_json_file(file.filename):
            try:
                content = json.load(file.stream)
                if validate_json_structure(content):
                    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
                    file_path = save_json_content(content, filename)
                    
                    doc_id = str(uuid.uuid4())
                    doc_name = TextProcessor.clean(filename)
                    doc_vector = vectorize_text(doc_name)

                    # Xử lý dữ liệu để insert vào db

                    if Document.load_collection():
                        Document.insert_one({
                            "id": doc_id,
                            "name": doc_name,
                            "vector": doc_vector,
                            "file_name": filename
                        })
                        Document.release_collection()

                        if DocumentParts.load_collection():
                            DocumentParts.create_partition(doc_id)
                            DocumentParts.insert_many([], doc_id)
                            DocumentParts.release_collection()

                    return f'JSON file is valid and saved as {filename}'
                else:
                    return 'Invalid JSON structure!'
            except json.JSONDecodeError:
                return 'Invalid JSON file!'
            
        # send text
        else:
            content = request.form['text'].strip()
            try:
                data = json.loads(content)
                if validate_json_structure(data):
                    
                    json_to_database(file_path)

                    doc_id = str(uuid.uuid4())
                    doc_name = TextProcessor.clean(request.form["doc_name"])
                    doc_vector = vectorize_text(doc_name)
                    file_name = f"{doc_name}.json"
                    file_path = save_json_content(content, file_name)

                    if Document.load_collection():
                        Document.insert_one({
                            "id": doc_id,
                            "name": doc_name,
                            "vector": doc_vector,
                            "file_name": file_name
                        })
                        Document.release_collection()

                        if DocumentParts.load_collection():
                            DocumentParts.create_partition(doc_id)
                            DocumentParts.insert_many([], doc_id)
                            DocumentParts.release_collection()

                    return f'JSON text is valid and saved as {filename}'
                else:
                    return 'Invalid JSON structure!'
            except json.JSONDecodeError:
                return 'Invalid JSON text!'

    return render_template('upload_json.html')

@upload_bp.route('/txt', methods=['GET', 'POST'])
def upload_txt():
    message = ''
    
    if request.method == 'POST':
        files = request.files.getlist('files[]')  # Nhận tất cả các file với name="files[]"
        processed_files = []  # Danh sách lưu trữ các file đã được lưu

        # Kiểm tra nếu không có file nào được upload
        if not files:
            message = "Vui lòng chọn ít nhất một file để tải lên."
            return render_template('upload_txt.html', message=message)
        
        # Duyệt qua từng file được upload
        for file in files:
            if file and file.filename and is_txt_file(file.filename):
                # Lưu file vào thư mục mong muốn
                filename = file.filename
                file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), 'txt', filename)
                file.save(file_path)

                # Đọc nội dung file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Xử lý nội dung file (ví dụ: phân tách theo dấu phân cách '\n\n')
                arr = content.split('\n\n')

                # Bạn có thể xử lý `arr` ở đây nếu cần

                
                processed_files.append(filename)

        # Nếu tất cả các file đã được xử lý
        message = f"Đã tải lên {len(processed_files)} file thành công."

    return render_template('upload_txt.html', message=message)