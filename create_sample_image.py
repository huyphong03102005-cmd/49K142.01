"""
Script để tạo ảnh mẫu nếu chưa có sample_ok.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_image():
    # Tạo ảnh 800x600 với gradient
    width, height = 800, 600
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Vẽ gradient background
    for y in range(height):
        r = int(100 + (155 * y / height))
        g = int(150 + (105 * y / height))
        b = int(200 + (55 * y / height))
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
    
    # Vẽ hình chữ nhật trung tâm (giả lập sản phẩm)
    product_rect = [(200, 150), (600, 450)]
    draw.rectangle(product_rect, fill=(220, 220, 220), outline=(100, 100, 100), width=5)
    
    # Vẽ text
    try:
        # Thử sử dụng font mặc định
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 60)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 30)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Text chính
    text1 = "SẢN PHẨM MẪU"
    text2 = "OK - Không lỗi"
    
    # Vẽ text với shadow
    draw.text((405, 285), text1, fill=(50, 50, 50), font=font_large, anchor="mm")
    draw.text((400, 280), text1, fill=(255, 255, 255), font=font_large, anchor="mm")
    
    draw.text((405, 345), text2, fill=(50, 50, 50), font=font_small, anchor="mm")
    draw.text((400, 340), text2, fill=(100, 200, 100), font=font_small, anchor="mm")
    
    # Vẽ checkmark
    check_points = [(350, 380), (370, 400), (410, 360)]
    draw.line(check_points, fill=(100, 200, 100), width=8)
    
    # Lưu ảnh
    image.save('sample_ok.png')
    print("✅ Đã tạo file sample_ok.png thành công!")

if __name__ == "__main__":
    if not os.path.exists('sample_ok.png'):
        create_sample_image()
    else:
        print("ℹ️ File sample_ok.png đã tồn tại!")
