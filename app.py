import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import os

# ========================
# CẤU HÌNH GIAO DIỆN
# ========================
st.set_page_config(page_title="AI Kiểm Tra Lỗi Sản Phẩm", layout="centered")

# ========================
# CSS TUỲ CHỈNH
# ========================
st.markdown("""
<style>

html, body, [class*="css"]  {
    background: linear-gradient(135deg, #021526 0%, #043A66 50%, #6A0DAD 75%, #FF4500 100%) !important;
    animation: gradientShift 10s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* TIÊU ĐỀ */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 0 0 12px #FFA500, 0 0 20px #FF6347;
    margin-bottom: 5px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 12px #FFA500, 0 0 20px #FF6347; }
    to { text-shadow: 0 0 20px #FFA500, 0 0 30px #FF6347; }
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #B8E4FF;
    margin-bottom: 30px;
}

/* HỘP UPLOAD GỌN ĐẸP */
.upload-area {
    background: rgba(138, 43, 226, 0.5);
    border: 2px dashed #FFD700;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 0 18px rgba(255, 215, 0, 0.25);
    backdrop-filter: blur(6px);
    width: 70%;
    margin-left: auto;
    margin-right: auto;
    transition: transform 0.3s ease;
}

.upload-area:hover {
    transform: scale(1.05);
}

/* CARD KẾT QUẢ */
.result-card {
    background: rgba(34, 139, 34, 0.75);
    padding: 20px;
    border-radius: 16px;
    margin-top: 20px;
    box-shadow: 0 0 25px rgba(50, 205, 50, 0.35);
    border: 1px solid #32CD32;
    width: 70%;
    margin-left: auto;
    margin-right: auto;
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ========================
# LOAD MODEL
# ========================
model = load_model("defect_detection_casting.h5")
labels = ["def_front", "ok_front"]

# ========================
# TIÊU ĐỀ
# ========================
st.markdown('<p class="title">🔍 AI KIỂM TRA LỖI SẢN PHẨM</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Công nghệ AI phát hiện lỗi sản phẩm theo thời gian thực</p>', unsafe_allow_html=True)

# ========================
# HIỂN THỊ ẢNH MẪU
# ========================
sample_image_path = "sample_ok.png"
if os.path.exists(sample_image_path):
    st.image(sample_image_path, caption="Ảnh mẫu minh họa", use_container_width=True)

# ========================
# HỘP UPLOAD
# ========================
st.markdown("<div class='upload-area'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Tải ảnh sản phẩm lên để kiểm tra", type=["jpg", "jpeg", "png"])
st.markdown("</div>", unsafe_allow_html=True)

# ========================
# HÀM DỰ ĐOÁN
# ========================
def predict_image(img):
    img_resized = img.resize((300, 300))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    index = np.argmax(prediction[0])
    confidence = prediction[0][index]
    return labels[index], confidence

# ========================
# HIỂN THỊ KẾT QUẢ
# ========================
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Ảnh đã tải lên", use_container_width=True)

    label, confidence = predict_image(img)

    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.subheader("⭐ KẾT QUẢ DỰ ĐOÁN")

    if label == "def_front":
        st.error(f"❌ SẢN PHẨM BỊ LỖI — Độ tin cậy: {confidence:.2f}")
    else:
        st.success(f"✔️ SẢN PHẨM OK — Độ tin cậy: {confidence:.2f}")

    st.markdown("</div>", unsafe_allow_html=True)

# ========================
# FOOTER
# ========================
st.write("---")
st.caption("© 2025 - Hệ thống kiểm định AI | Blue Neon UI | Streamlit + TensorFlow")