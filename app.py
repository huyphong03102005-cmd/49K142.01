import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import os

# ========================
# CẤU HÌNH GIAO DIỆN
# ========================
st.set_page_config(
    page_title="AI Kiểm Tra Lỗi Sản Phẩm",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================
# CSS TUỲ CHỈNH - THIẾT KẾ MỚI
# ========================
st.markdown("""
<style>
/* BACKGROUND GRADIENT ĐẸP MẮT */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* CONTAINER CHÍNH */
.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* TIÊU ĐỀ */
.title {
    text-align: center;
    font-size: 56px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #ffd89b 50%, #19547b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
    text-shadow: 0 4px 20px rgba(255,255,255,0.3);
    animation: titleGlow 3s ease-in-out infinite;
}

@keyframes titleGlow {
    0%, 100% { filter: drop-shadow(0 0 20px rgba(255,255,255,0.5)); }
    50% { filter: drop-shadow(0 0 40px rgba(255,255,255,0.8)); }
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #ffffff;
    margin-bottom: 40px;
    font-weight: 300;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

/* CARD CONTAINER */
.card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255,255,255,0.5);
    margin-bottom: 30px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 70px rgba(0,0,0,0.4);
}

/* HỘP UPLOAD */
.upload-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    margin-bottom: 30px;
}

.upload-title {
    color: #ffffff;
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 20px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

/* BUTTON CUSTOM */
.stButton > button {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 15px 40px;
    font-size: 18px;
    font-weight: 600;
    box-shadow: 0 10px 30px rgba(245, 87, 108, 0.4);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(245, 87, 108, 0.6);
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    padding: 20px;
    border: 3px dashed #667eea;
}

[data-testid="stFileUploader"] label {
    color: #667eea !important;
    font-weight: 600;
    font-size: 18px;
}

/* RESULT CARDS */
.result-success {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    box-shadow: 0 15px 40px rgba(56, 239, 125, 0.4);
    margin: 20px 0;
    animation: slideIn 0.5s ease;
}

.result-error {
    background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    box-shadow: 0 15px 40px rgba(235, 51, 73, 0.4);
    margin: 20px 0;
    animation: slideIn 0.5s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* CONFIDENCE BAR */
.confidence-bar {
    background: rgba(255,255,255,0.3);
    border-radius: 50px;
    height: 30px;
    margin: 20px 0;
    overflow: hidden;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);
}

.confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #ffd89b 0%, #19547b 100%);
    border-radius: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    transition: width 1s ease;
    box-shadow: 0 0 20px rgba(255,255,255,0.5);
}

/* IMAGE DISPLAY */
.image-container {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    margin: 20px 0;
    border: 4px solid rgba(255,255,255,0.5);
}

/* STATS CARD */
.stats-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4);
    margin: 10px;
}

.stats-number {
    font-size: 36px;
    font-weight: 900;
    margin: 10px 0;
}

.stats-label {
    font-size: 14px;
    font-weight: 300;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* FOOTER */
.footer {
    text-align: center;
    color: white;
    padding: 30px;
    margin-top: 50px;
    font-size: 14px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

/* HIDE STREAMLIT BRANDING */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* CUSTOM SCROLLBAR */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.1);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* LOADING ANIMATION */
.loading {
    display: inline-block;
    width: 50px;
    height: 50px;
    border: 5px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top-color: #fff;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* FEATURE ICONS */
.feature-box {
    background: rgba(255,255,255,0.9);
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    margin: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}

.feature-box:hover {
    transform: translateY(-10px);
}

.feature-icon {
    font-size: 48px;
    margin-bottom: 15px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 10px;
}

.feature-desc {
    font-size: 14px;
    color: #666;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# ========================
# LOAD MODEL
# ========================
@st.cache_resource
def load_ai_model():
    try:
        model = load_model("defect_detection_casting.h5")
        return model
    except:
        st.error("⚠️ Không thể tải model AI. Vui lòng kiểm tra file defect_detection_casting.h5")
        return None

model = load_ai_model()
labels = ["def_front", "ok_front"]

# ========================
# TIÊU ĐỀ
# ========================
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="title">🔍 AI KIỂM TRA LỖI SẢN PHẨM</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ Công nghệ AI tiên tiến phát hiện lỗi sản phẩm với độ chính xác cao ✨</p>', unsafe_allow_html=True)

# ========================
# FEATURES SECTION
# ========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Nhanh Chóng</div>
        <div class="feature-desc">Phân tích hình ảnh trong vài giây</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Chính Xác</div>
        <div class="feature-desc">Độ chính xác lên đến 95%+</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Thông Minh</div>
        <div class="feature-desc">Học máy sâu với TensorFlow</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ========================
# MAIN CARD
# ========================
st.markdown('<div class="card">', unsafe_allow_html=True)

# ========================
# HIỂN THỊ ẢNH MẪU
# ========================
sample_image_path = "sample_ok.png"
if os.path.exists(sample_image_path):
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(sample_image_path, caption="📸 Ảnh mẫu minh họa sản phẩm", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========================
# HỘP UPLOAD
# ========================
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown('<div class="upload-title">📤 TẢI ẢNH SẢN PHẨM LÊN ĐỂ KIỂM TRA</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Chọn file ảnh (JPG, JPEG, PNG)",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

# ========================
# HÀM DỰ ĐOÁN
# ========================
def predict_image(img):
    img_resized = img.resize((300, 300))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array, verbose=0)
    index = np.argmax(prediction[0])
    confidence = prediction[0][index]
    return labels[index], confidence

# ========================
# HIỂN THỊ KẾT QUẢ
# ========================
if uploaded_file and model:
    img = Image.open(uploaded_file)
    
    # Hiển thị ảnh đã upload
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(img, caption="🖼️ Ảnh đã tải lên", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Thực hiện dự đoán
    with st.spinner('🔄 Đang phân tích ảnh...'):
        label, confidence = predict_image(img)
    
    # Hiển thị kết quả
    confidence_percent = confidence * 100
    
    if label == "def_front":
        st.markdown(f"""
        <div class="result-error">
            <div style="font-size: 48px; margin-bottom: 10px;">❌</div>
            <div>SẢN PHẨM BỊ LỖI</div>
            <div style="font-size: 16px; margin-top: 10px; opacity: 0.9;">Phát hiện khuyết tật trên bề mặt</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-success">
            <div style="font-size: 48px; margin-bottom: 10px;">✅</div>
            <div>SẢN PHẨM ĐẠT CHUẨN</div>
            <div style="font-size: 16px; margin-top: 10px; opacity: 0.9;">Không phát hiện lỗi</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Thanh độ tin cậy
    st.markdown(f"""
    <div class="confidence-bar">
        <div class="confidence-fill" style="width: {confidence_percent}%;">
            {confidence_percent:.1f}% Độ tin cậy
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Thống kê chi tiết
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">Kết Quả</div>
            <div class="stats-number">{"❌" if label == "def_front" else "✅"}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">Độ Tin Cậy</div>
            <div class="stats-number">{confidence_percent:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status_text = "LỖI" if label == "def_front" else "OK"
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-label">Trạng Thái</div>
            <div class="stats-number" style="font-size: 24px;">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========================
# HƯỚNG DẪN SỬ DỤNG
# ========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📋 Hướng Dẫn Sử Dụng")
st.markdown("""
1. **Tải ảnh lên**: Click vào khu vực upload và chọn ảnh sản phẩm cần kiểm tra
2. **Chờ phân tích**: Hệ thống AI sẽ tự động phân tích ảnh trong vài giây
3. **Xem kết quả**: Kết quả sẽ hiển thị ngay với độ tin cậy chi tiết
4. **Kiểm tra lại**: Bạn có thể tải lên nhiều ảnh khác để kiểm tra tiếp

**💡 Lưu ý**: Để có kết quả tốt nhất, hãy chụp ảnh rõ nét, đủ ánh sáng và tập trung vào bề mặt sản phẩm.
""")
st.markdown('</div>', unsafe_allow_html=True)

# ========================
# FOOTER
# ========================
st.markdown("""
<div class="footer">
    <div style="font-size: 18px; margin-bottom: 10px;">🚀 Powered by AI & Deep Learning</div>
    <div>© 2025 - Hệ thống kiểm định AI | TensorFlow + Streamlit</div>
    <div style="margin-top: 10px; opacity: 0.8;">Made with ❤️ for Quality Control</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
