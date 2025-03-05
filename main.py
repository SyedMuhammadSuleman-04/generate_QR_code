
# import streamlit as st
# import qrcode
# from PIL import Image
# import io
# import cv2
# import numpy as np

# st.set_page_config(page_title="QR Code Generator & Reader", layout='wide')
# st.title('📲 QR Code Generator & Reader')
# st.write('Generate QR codes from text or URLs and scan QR codes to extract information!')

# # QR Code Generator
# st.subheader("Generate QR Codes")
# qr_texts = st.text_area("Enter multiple texts or URLs (one per line) to generate QR codes:")

# qr_text_list = qr_texts.splitlines()

# # Editable list of QR code entries
# if qr_text_list:
#     st.subheader("Review & Edit QR Codes")
#     edited_texts = []
#     for i, text in enumerate(qr_text_list):
#         col1, col2 = st.columns([4, 1])
#         new_text = col1.text_input(f"Edit text for QR Code {i + 1}", text)
#         if not col2.button(f"❌ Delete {i + 1}", key=f"delete_{i}"):
#             edited_texts.append(new_text)
#     qr_text_list = edited_texts

# if st.button("Generate QR Codes"):
#     if qr_text_list:
#         for i, qr_text in enumerate(qr_text_list, start=1):
#             if qr_text.strip():
#                 qr = qrcode.make(qr_text.strip())
#                 img_bytes = io.BytesIO()
#                 qr.save(img_bytes, format='PNG')
#                 img_bytes.seek(0)
#                 st.image(Image.open(img_bytes), caption=f"QR Code {i}", use_column_width=False)
#                 st.download_button(f"Download QR Code {i}", img_bytes, file_name=f"qr_code_{i}.png", mime="image/png")
#     else:
#         st.error("Please enter at least one text or URL")

# # QR Code Reader
# st.subheader("Read QR Code")
# uploaded_files = st.file_uploader("Upload QR Code images (multiple allowed):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
#         img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
#         detector = cv2.QRCodeDetector()
#         data, bbox, _ = detector.detectAndDecode(img)
#         if bbox is not None and data:
#             st.image(Image.open(io.BytesIO(cv2.imencode('.png', img)[1].tobytes())), caption=f"Uploaded QR Code: {uploaded_file.name}", use_column_width=False)
#             st.success(f"Decoded Data: {data}")
#         else:
#             st.error(f"No QR code detected in {uploaded_file.name}. Please upload a valid QR code image.")


import streamlit as st
import qrcode
from PIL import Image
import io
import cv2
import numpy as np

st.set_page_config(page_title="QR Code Generator & Reader", layout='wide')
st.title('📲 QR Code Generator & Reader')
st.write('Generate QR codes from text or URLs and scan QR codes to extract information!')

# Initialize session state for QR codes
if "qr_text_list" not in st.session_state:
    st.session_state.qr_text_list = []

# QR Code Generator
st.subheader("Generate QR Codes")
qr_texts = st.text_area("Enter multiple texts or URLs (one per line) to generate QR codes:")

if st.button("Add QR Codes"):
    if qr_texts.strip():
        st.session_state.qr_text_list.extend(qr_texts.splitlines())

# Editable list of QR code entries
if st.session_state.qr_text_list:
    st.subheader("Review & Edit QR Codes")
    updated_texts = []
    for i, text in enumerate(st.session_state.qr_text_list):
        col1, col2 = st.columns([4, 1])
        new_text = col1.text_input(f"Edit text for QR Code {i + 1}", text, key=f"text_{i}")
        if col2.button(f"❌ Delete {i + 1}", key=f"delete_{i}"):
            st.session_state.qr_text_list.pop(i)
            st.rerun()
        else:
            updated_texts.append(new_text)
    st.session_state.qr_text_list = updated_texts

# Generate QR codes
if st.button("Generate QR Codes"):
    if st.session_state.qr_text_list:
        for i, qr_text in enumerate(st.session_state.qr_text_list, start=1):
            if qr_text.strip():
                qr = qrcode.make(qr_text.strip())
                img_bytes = io.BytesIO()
                qr.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                st.image(Image.open(img_bytes), caption=f"QR Code {i}", use_column_width=False)
                st.download_button(f"Download QR Code {i}", img_bytes, file_name=f"qr_code_{i}.png", mime="image/png")
    else:
        st.error("Please enter at least one text or URL")

# QR Code Reader
st.subheader("Read QR Code")
uploaded_files = st.file_uploader("Upload QR Code images (multiple allowed):", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)
        if bbox is not None and data:
            st.image(Image.open(io.BytesIO(cv2.imencode('.png', img)[1].tobytes())), caption=f"Uploaded QR Code: {uploaded_file.name}", use_column_width=False)
            st.success(f"Decoded Data: {data}")
        else:
            st.error(f"No QR code detected in {uploaded_file.name}. Please upload a valid QR code image.")
