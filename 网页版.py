import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import colorsys
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="冷暖调判断器", page_icon="🎨")
st.title("🎨 冷暖调判断器")
st.write("上传一张照片，点击图片上的位置，立刻判断颜色的冷暖调。")

st.warning("💡 重要提示：点击图片后，结果会在图片正下方显示，请向下滑动查看！")

def judge_temperature(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    hue_deg = h * 360

    # 1. 黑白灰优先判断
    if v < 0.25: return "深黑（偏冷/暖）"
    if v > 0.80 and s < 0.20: return "净白（偏冷/暖）"
    if s < 0.20: return "柔灰（偏冷/暖）"

    # 2. 判断色彩三要素
    temp = "暖调" if hue_deg < 180 else "冷调"
    
    # 深浅（明度V）—— 过滤掉中等
    if v > 0.75: lightness = "轻浅"
    elif v < 0.40: lightness = "深沉"
    else: lightness = "" 
    
    # 柔艳（饱和度S）—— 过滤掉适中
    if s > 0.60: satur = "鲜艳"
    elif s < 0.30: satur = "柔和"
    else: satur = ""

    # 3. 色相具体名称
    if hue_deg < 30 or hue_deg >= 330: color_name = "红"
    elif hue_deg < 60: color_name = "橙"
    elif hue_deg < 90: color_name = "黄"
    elif hue_deg < 120: color_name = "黄绿"
    elif hue_deg < 150: color_name = "绿"
    elif hue_deg < 180: color_name = "青绿"
    elif hue_deg < 210: color_name = "青"
    elif hue_deg < 240: color_name = "蓝"
    elif hue_deg < 270: color_name = "蓝紫"
    elif hue_deg < 300: color_name = "紫"
    else: color_name = "紫红"

    # 4. 拼接（过滤掉空字符串）
    prefix = f"{lightness}{satur}"
    if prefix: 
        return f"{prefix}的{temp}{color_name}"
    else:       
        return f"{temp}{color_name}"

uploaded_file = st.file_uploader("选择一张图片", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    # ★★★ 修复点1：自动纠正手机照片的旋转方向 ★★★
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)  # 这句代码解决了90%的“点哪偏哪”问题
    
    # 压缩图片到400像素宽
    if max(img.size) > 400:
        ratio = 400 / max(img.size)
        img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.Resampling.LANCZOS)

    st.write("👇 点击图片上的位置取色：")
    value = streamlit_image_coordinates(img, key="click", width=400)

    if value is not None:
        x, y = value["x"], value["y"]
        
        # 修复点2：防止点边缘崩溃
        x = max(0, min(x, img.width - 1))
        y = max(0, min(y, img.height - 1))
        
        r, g, b = img.getpixel((x, y))[:3]
        result = judge_temperature(r, g, b)

        st.markdown("---")
        
        # 截取局部放大图
        crop_size = 40
        left = max(0, x - crop_size)
        top = max(0, y - crop_size)
        right = min(img.width, x + crop_size)
        bottom = min(img.height, y + crop_size)
        
        crop_img = img.crop((left, top, right, bottom))
        crop_img = crop_img.resize((100, 100), Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(crop_img)
        center_x = x - left
        center_y = y - top
        draw.line((center_x, 0, center_x, 100), fill="red", width=2)
        draw.line((0, center_y, 100, center_y), fill="red", width=2)
        draw.ellipse((center_x-5, center_y-5, center_x+5, center_y+5), outline="red", width=2)

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(crop_img, caption="📍 点此")
        with col2:
            st.markdown(
                f"<h2 style='text-align: center; color: #d32f2f; margin-bottom: 0;'>🎯 结果：{result}</h2>", 
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p style='text-align: center; color: #666;'>坐标：({x}, {y})  |  RGB：({r}, {g}, {b})</p >", 
                unsafe_allow_html=True
            )

st.divider()
st.write("📧 如有建议，请联系：**2037076846@qq.com**")
st.caption("📌 免责声明：本工具仅提供色彩美学参考。您的照片仅用于实时像素计算，服务器不会保存您的原图。")