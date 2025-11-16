#!/bin/bash

echo "🚀 Starting AI Product Defect Detection App..."
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được cài đặt!"
    exit 1
fi

# Kiểm tra pip
if ! command -v pip3 &> /dev/null; then
    echo "📦 Đang cài đặt pip..."
    python3 -m ensurepip --upgrade
fi

# Cài đặt dependencies
echo "📦 Đang cài đặt dependencies..."
pip3 install -r requirements.txt

# Tạo ảnh mẫu nếu chưa có
if [ ! -f "sample_ok.png" ]; then
    echo "🖼️ Đang tạo ảnh mẫu..."
    python3 create_sample_image.py
fi

# Kiểm tra model
if [ ! -f "defect_detection_casting.h5" ]; then
    echo "⚠️ Cảnh báo: File model 'defect_detection_casting.h5' không tồn tại!"
    echo "   Vui lòng đặt file model vào thư mục hiện tại."
    echo ""
fi

# Chạy app
echo "✨ Đang khởi động ứng dụng..."
echo ""
streamlit run app.py
