import os
import json
from datetime import datetime
import uuid
from flask import Blueprint, render_template, request
from app.models.document_parts_model import DocumentParts
from app.models.document_model import Document
from app.services.ocr_service import extract_text
from app.services.tokenizer_service import vectorize_text
from app.utils.file_util import is_pdf_file, is_txt_file, read_file, write_file
from app.utils.data_processing import TextProcessor
from app.utils.convert_data import array2json, add_fields_vector_and_position, format_type_of_filename, json2array, add_fields_doc_id, select_fields_to_save_array, datetime2string
from app.utils.constant import Constants 
from dotenv import load_dotenv
load_dotenv()

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/pdf', methods=['POST'])
def upload_pdf():
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

@upload_bp.route('/txt', methods=['POST'])
def upload_txt():
    files = request.files.getlist('files')  # Nhận tất cả các file với name="files[]"
    processed_files = []  # Danh sách lưu trữ các file đã được lưu

    # Kiểm tra nếu không có file nào được upload
    if not files:
        return {"status": 500, "message": "Không có file nào gửi lên"}
    
    # Duyệt qua từng file được upload
    for file in files:
        if file and file.filename and is_txt_file(file.filename):
            # Lưu file vào thư mục mong muốn
            filename = file.filename
            filename += f"_{datetime2string(datetime.now())}"
            folder_path = os.path.join(str(os.getenv('UPLOAD_FOLDER')), 'txt')
            filename = format_type_of_filename(filename, 'txt')
            file.save(os.path.join(folder_path, filename))
            content = read_file(folder_path, filename, 'txt')

            # Xử lý nội dung file (ví dụ: phân tách theo dấu phân cách '\n\n')
            arr = content.split('\n\n')

            # Thiếu trường vector và position
            json_structer = array2json(arr)
            # Thêm trường vector và position
            final_json = add_fields_vector_and_position(json_structer)

            # Thiếu trường doc_id
            array = json2array(final_json)

            # Tạo entity mới 
            doc_id = str(uuid.uuid4()).replace("-", "_")
            doc_name = TextProcessor.clean(format_type_of_filename(file.filename))
            doc_vector = vectorize_text(doc_name)

            # Thêm trường doc_id
            final_array = add_fields_doc_id(array, doc_id)

            Document.insert([{
                "id": doc_id,
                "name": doc_name,
                "vector": doc_vector,
                "file_name": format_type_of_filename(file.filename) # Sau này chỉnh sửa lại thành filename
            }])
            
            if DocumentParts.create_partition(doc_id):
                DocumentParts.insert(final_array, doc_id)
            
            processed_files.append({
                'file': file.filename,
                'status': 'Thành công'
            })
        else:
            if file:
                processed_files.append({
                    'file': file.filename,
                    'status': 'Thất bại'
                })
            else:
                processed_files.append({
                    'file': '',
                    'status': 'Thất bại'
                })

    return {"status": 200, "message": processed_files}
