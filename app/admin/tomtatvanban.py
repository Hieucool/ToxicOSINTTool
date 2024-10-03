# -*- coding: UTF-8 -*-

import re
import nltk
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from underthesea import word_tokenize as vt_word_tokenize
# Tải dữ liệu cần thiết cho việc tách câu (nếu chưa tải)
nltk.download('punkt')

text_file = "copus_original.txt"

### Tiền xử lý văn bản
def XL_noidung_original(noidung):
    # # Mở file để đọc
    # with open(noidung, 'r', encoding='utf-8') as file:
    #     # Đọc nội dung từ file
    #     content = file.read()
    
    sentences = noidung.split(".")  # Split text into sentences

    unique_sentences = list(set(sentences)) 
    cleaned_text = ". ".join(unique_sentences)  
    # Chuyển đổi sang chữ thường
    output = cleaned_text.lower()  
    # Đổi các ký tự xuống dòng thành chấm câu
    output = output.replace('\n', '. ')  
    
    # Loại bỏ đi các khoảng trắng thừa
    output = output.strip()  
    # Xử lý dấu câu trùng lặp
    output = re.sub(r'([.!?])\1+', r'\1', output)  
    # Xóa ký tự không cần thiết
    output = re.sub(r'[\"\'‘’“”`‛‟«»„‹›「」『』()〝〞〟〰]', '', output)  
    return output

### Tiền xử lý tách văn bản thành câu
def tach_van_ban_thanh_cau(van_ban):
    return sent_tokenize(van_ban)

### Tiền xử lý ghép từ có nghĩa
def tien_xu_ly_ghep_tu_co_nghia(van_ban):
    return vt_word_tokenize(van_ban, format="text")

### Tính điểm cho từng câu
def tinh_diem_cau(cac_cau, tan_so_tu):
    diem_cau = {}
    for i, cau in enumerate(cac_cau):
        tu_ca_i = vt_word_tokenize(cau, format="text").split()  # Sử dụng thư viện Underthesea để tách từ
        diem_cau[i] = sum(tan_so_tu[tu] for tu in tu_ca_i)
    return diem_cau

### Tạo tóm tắt
def tao_tom_tat(cac_cau, so_cau_tom_tat=3):
    # Tính tần số xuất hiện của từng từ
    tan_so_tu = Counter(' '.join(cac_cau).split())
    # Tính điểm cho từng câu
    diem_cau = tinh_diem_cau(cac_cau, tan_so_tu)
    # Chọn các câu có điểm cao nhất
    cac_cau_tom_tat = sorted(diem_cau.keys(), key=lambda i: diem_cau[i], reverse=True)[:so_cau_tom_tat]
    # Sắp xếp lại các câu theo thứ tự xuất hiện ban đầu
    cac_cau_tom_tat.sort()
    # Gộp các câu đã chọn để tạo tóm tắt
    tom_tat = ' '.join(cac_cau[i] for i in cac_cau_tom_tat)
    return tom_tat

#Tiền xử lý thêm sau khi tóm tắt để có đoạn văn bản đẹp
def XL_output(kq_tomtat):
    formatted_text = kq_tomtat.replace("_", " ")
    formatted_text = re.sub(r'\s*([,\.])', r'\1', formatted_text)
    return formatted_text

def Summerizer(noidung, socau = 5):
    # Tiền xử lý văn bản
    ketquaXL = XL_noidung_original(noidung)
    # Ghép từ có nghĩa
    ketquaXL_gheptu = tien_xu_ly_ghep_tu_co_nghia(ketquaXL)
    # Tách câu
    ketquaXL_tachcau = tach_van_ban_thanh_cau(ketquaXL_gheptu)
    # kết quả tóm tắt với số lượng câu mong muốn, ở đây đang để là 5 câu.
    tom_tat = XL_output(tao_tom_tat(ketquaXL_tachcau, socau))
    return tom_tat

#test
# text = """
# Nhiều khách Việt cả nam lẫn nữ xúng xính diện Hanbok chụp ảnh trong lễ hội Con đường văn hoá Hàn Quốc được tổ chức bên ngoài sứ quán Hàn ở Hà Nội ngày 13/4. Lễ hội Con đường văn hoá Hàn Quốc 2024 do Đại sứ quán Hàn Quốc tại Việt Nam cùng Trung tâm Văn hoá Hàn Quốc tại Việt Nam tổ chức trong hai ngày 13 và 14/4. Sự kiện diễn ra phía ngoài tòa nhà Đại sứ quán Hàn Quốc ở Hà Nội. Tòa nhà Đại sứ quán và con đường đá bao quanh được đưa vào sử dụng từ năm 2019, trở thành địa điểm nổi tiếng thu hút người dân Hà Nội đến tham quan và chụp ảnh thường xuyên, theo Đại sứ quán Hàn Quốc tại Việt Nam. Lễ hội Con đường văn hoá Hàn Quốc 2024 do Đại sứ quán Hàn Quốc tại Việt Nam cùng Trung tâm Văn hoá Hàn Quốc tại Việt Nam tổ chức trong hai ngày 13 và 14/4. Sự kiện diễn ra phía ngoài tòa nhà Đại sứ quán Hàn Quốc ở Hà Nội. Tòa nhà Đại sứ quán và con đường đá bao quanh được đưa vào sử dụng từ năm 2019, trở thành địa điểm nổi tiếng thu hút người dân Hà Nội đến tham quan và chụp ảnh thường xuyên, theo Đại sứ quán Hàn Quốc tại Việt Nam. Đỗ Quyên, sinh viên năm nhất Học viện Báo chí và Tuyên truyền, nói mặc Hanbok rất "xúc động". Quyên thường tìm hiểu văn hoá của Hàn Quốc nên khi biết có lễ hội đã rủ bạn cùng đến tham dự. Đỗ Quyên, sinh viên năm nhất Học viện Báo chí và Tuyên truyền, nói mặc Hanbok rất "xúc động". Quyên thường tìm hiểu văn hoá của Hàn Quốc nên khi biết có lễ hội đã rủ bạn cùng đến tham dự. Lê Trong Toàn cùng vợ trải nghiệm mặc trang phục truyền thống của Hàn Quốc tại con đường đá nổi tiếng bên ngoài Đại sứ quán Hàn Quốc. Đại sứ quán Hàn Quốc cùng Trung tâm Văn hoá Hàn Quốc tại Việt Nam lên kế hoạch tổ chức lễ hội thường niên tại địa điểm này. Trong năm đầu tiên tổ chức vào 2023, lễ hội thu hút 20.000 người tham dự.  Lê Trong Toàn cùng vợ trải nghiệm mặc trang phục truyền thống của Hàn Quốc tại con đường đá nổi tiếng bên ngoài Đại sứ quán Hàn Quốc. Đại sứ quán Hàn Quốc cùng Trung tâm Văn hoá Hàn Quốc tại Việt Nam lên kế hoạch tổ chức lễ hội thường niên tại địa điểm này. Trong năm đầu tiên tổ chức vào 2023, lễ hội thu hút 20.000 người tham dự."""

# print(Summerizer(text))

