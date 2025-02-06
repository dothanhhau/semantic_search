import re

class TextProcessor:
    @staticmethod
    def clean(text):
        return re.sub(r'\s+', ' ', text).strip()
    
    @staticmethod
    def standardize(text):
        standardizedText = text.replace("~", "").replace("“", "") \
                                .replace(":", ".").replace("”", "") \
                                .replace('"', "").replace("'", "") \
                                .replace("!", ".").replace("?", ".") \
                                .replace("+", "").replace(",", "") \
                                .replace("(", "").replace(")", "") \
                                .replace("-", "")
        return standardizedText.lower()

    
    @staticmethod
    def extract_content(text, re_extractor):
        pattern = re.compile(re_extractor, re.DOTALL)
        matches = pattern.findall(text)

        parts = []
        for match in matches:
            part_type = match[0].strip()
            content = match[1].strip()

            parts.append(f"{part_type} {content}")

        if './.' in parts[-1]:
            parts[-1] = parts[-1].split('./.')[0] + '.'
        
        return parts
    
    @staticmethod
    def split_documents(text, separator):
        parts = text.split(separator)
        documents = [part.strip() for part in parts if part.strip()]
        documents = [separator + " " + doc for doc in documents]
        return documents