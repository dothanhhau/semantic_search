from transformers import AutoTokenizer, AutoModel 
# Tải mô hình và tokenizer 
tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base') 
model = AutoModel.from_pretrained('vinai/phobert-base') 
# Lưu mô hình và tokenizer vào thư mục local 
path = './duong/dan/ban/muon/luu/phobert'
model.save_pretrained(path) 
tokenizer.save_pretrained(path)
