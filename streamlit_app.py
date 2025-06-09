
import streamlit as st
import fitz  # PyMuPDF
import io
from PyPDF2 import PdfWriter, PdfReader

def extract_matching_pages_from_pdf(pdf_file, keyword):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    matching_pages = []
    total_pages = doc.page_count

    for page_number in range(total_pages):
        page = doc.load_page(page_number)
        text = page.get_text()
        if keyword in text:
            matching_pages.append(page_number)

    return matching_pages, doc

def create_new_pdf_from_pages(doc, page_numbers):
    pdf_writer = PdfWriter()
    for page_number in page_numbers:
        pdf_bytes = doc.extract_pdf(page_numbers=[page_number])
        temp_reader = PdfReader(io.BytesIO(pdf_bytes))
        pdf_writer.add_page(temp_reader.pages[0])

    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)
    return output_stream

st.title("🔍 استخراج صفحات PDF التي تحتوي على كلمة (مع التذييل)")

uploaded_pdf = st.file_uploader("📤 ارفع ملف PDF", type=["pdf"])
keyword = st.text_input("🔎 أدخل الكلمة التي تبحث عنها")

if uploaded_pdf and keyword:
    matching_pages, doc = extract_matching_pages_from_pdf(uploaded_pdf, keyword)

    if matching_pages:
        output_pdf = create_new_pdf_from_pages(doc, matching_pages)
        st.success(f"تم العثور على {len(matching_pages)} صفحة تحتوي على '{keyword}'.")

        st.download_button(
            label="📥 تحميل الصفحات المستخرجة (PDF)",
            data=output_pdf,
            file_name=f"نتائج_{keyword}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("لم يتم العثور على الكلمة في أي صفحة.")
