class Constants:
    RE_CONTENT_EXTRACTOR = r'(Điều \d+\.|Chương [IVXLCDM]+|\d+\.|[a-z]\))(.*?)(?=\n(Điều \d+\.|Chương [IVXLCDM]+|\d+\.|[a-z]\)|$)|$)'
    DOC_SEPARATOR = "BỘ GIÁO DỤC VÀ ĐÀO TẠO"