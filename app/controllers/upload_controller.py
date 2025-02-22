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
from app.utils.convert_data import preProcess, chuong_dieu_khoan_diem_to_json, convertJsonDataSourceToArray
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
                            
                    arr = preProcess(extracted_content) # Clear một vài dữ liệu thừa

                    finalJson = convert_to_json(arr) # Chuyển từ mảng sang json với cấu trúc định sẵn

                    finalJson['tailieu'] = filename
                    data = convertJsonDataSourceToArray(finalJson)

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

        files = request.files
        processed_files = []

        # Kiểm tra và xử lý các file upload từ các ô input
        for key, file in files.items():
            if file and file.filename and is_txt_file(file.filename):
                file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), 'txt', file.filename)
                file.save(file_path)
                processed_files.append(file_path)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                arr = content.split('\n\n')

                # Xử lý theo từng loại file
                if key == 'chuong_dieu_khoan_diem':
                    res = chuong_dieu_khoan_diem_to_json(arr)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(res, f, ensure_ascii=False, indent=4)
                    print('# do something 1')
                elif key == 'dieu_khoan_diem':


                    print('# do something 2')
                elif key == 'khoan':


                    print('# do something 3')
                elif key == 'bang':


                    print('# do something 4')

    return render_template('upload_txt.html', message=message)