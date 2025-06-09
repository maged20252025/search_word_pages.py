
import streamlit as st
import fitz  # PyMuPDF
import io
from PyPDF2 import PdfWriter, PdfReader

def extract_matching_pages_from_pdf(pdf_file, keyword):
    file_bytes = pdf_file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    matching_pages = []
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        if keyword in page.get_text():
            matching_pages.append(page_number)
    return matching_pages, file_bytes

def create_new_pdf_from_pages(file_bytes, page_numbers):
    reader = PdfReader(io.BytesIO(file_bytes))
    writer = PdfWriter()
    for i in page_numbers:
        writer.add_page(reader.pages[i])
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream

st.title("🔍 استخراج صفحات PDF التي تحتوي على كلمة (مع التذييل)")

uploaded_pdf = st.file_uploader("📤 ارفع ملف PDF", type=["pdf"])
keyword = st.text_input("🔎 أدخل الكلمة التي تبحث عنها")

if uploaded_pdf and keyword:
    matching_pages, original_bytes = extract_matching_pages_from_pdf(uploaded_pdf, keyword)

    if matching_pages:
        output_pdf = create_new_pdf_from_pages(original_bytes, matching_pages)
        st.success(f"تم العثور على {len(matching_pages)} صفحة تحتوي على '{keyword}'.")

        st.download_button(
            label="📥 تحميل الصفحات المستخرجة (PDF)",
            data=output_pdf,
            file_name=f"نتائج_{keyword}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("لم يتم العثور على الكلمة في أي صفحة.")
