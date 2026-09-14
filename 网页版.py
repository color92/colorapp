import streamlit as st
from PIL import Image, ImageDraw
import colorsys
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="冷暖调判断器", page_icon="🎨")
st.title("🎨 冷暖调判断器")
st.write("上传一张照片，点击图片上的位置，立刻判断颜色的冷暖调。")

def judge_temperature(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    hue_deg = h * 360
    if hue_deg < 180: tendency = "暖"
    else: tendency = "冷"
    if hue_deg < 30 or hue_deg >= 330: detail = "红"
    elif hue_deg < 60: detail = "橙"
    elif hue_deg < 90: detail = "黄"
    elif hue_deg < 120: detail = "黄绿"
    elif hue_deg < 150: detail = "绿"
    elif hue_deg < 180: detail = "青绿"
    elif hue_deg < 210: detail = "青"
    elif hue_deg < 240: detail = "蓝"
    elif hue_deg < 270: detail = "蓝紫"
    elif hue_deg < 300: detail = "紫"
    else: detail = "紫红"
    if v < 0.25: return f"{tendency}黑（偏{tendency}{detail}）"
    if v > 0.80 and s < 0.20: return f"{tendency}白（偏{tendency}{detail}）"
    if s < 0.20: return f"{tendency}灰（偏{tendency}{detail}）"
    if 0 <= hue_deg < 30: return "暖调红 / 暖调橙（暖）"
    elif 30 <= hue_deg < 60: return "暖调黄 / 暖调橙（暖）"
    elif 60 <= hue_deg < 90: return "冷调黄 / 暖调绿（冷暖交界）"
    elif 90 <= hue_deg < 120: return "暖调绿（暖）"
    elif 120 <= hue_deg < 150: return "冷绿（冷）"
    elif 150 <= hue_deg < 180: return "暖调青 / 冷调绿（冷暖交界）"
    elif 180 <= hue_deg < 210: return "冷调青 / 暖调蓝（冷暖交界）"
    elif 210 <= hue_deg < 240: return "冷调蓝（冷）"
    elif 240 <= hue_deg < 270: return "暖调蓝 / 冷调紫（冷暖交界）"
    elif 270 <= hue_deg < 300: return "冷紫（冷）"
    elif 300 <= hue_deg < 330: return "暖调紫（暖）"
    elif 330 <= hue_deg < 360: return "冷调红 / 暖调紫（冷暖交界）"
    else: return "角度异常"

uploaded_file = st.file_uploader("选择一张图片", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    # ★★★ 图片压缩（解决大图卡顿）★★★
    if max(img.size) > 800:
        ratio = 800 / max(img.size)
        img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.Resampling.LANCZOS)

    st.write("👇 点击图片上的位置取色：")
    value = streamlit_image_coordinates(img, key="click")

    # ★★★ 侧边栏 + 放大镜功能 ★★★
    with st.sidebar:
        st.header("🎯 取色结果")
        if value is not None:
            x, y = value["x"], value["y"]
            r, g, b = img.getpixel((x, y))[:3]
            result = judge_temperature(r, g, b)

            # 画放大镜（带红色准星）
            crop_size = 80
            left = max(0, x - crop_size)
            top = max(0, y - crop_size)
            right = min(img.size[0], x + crop_size)
            bottom = min(img.size[1], y + crop_size)
            crop_img = img.crop((left, top, right, bottom))
            crop_img = crop_img.resize((160, 160), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(crop_img)
            center_x = x - left
            center_y = y - top
            draw.line((center_x, 0, center_x, 160), fill="red", width=2)
            draw.line((0, center_y, 160, center_y), fill="red", width=2)
            draw.ellipse((center_x-5, center_y-5, center_x+5, center_y+5), outline="red", width=2)

            st.image(crop_img, caption="📍 您点击的位置（已放大）")
            st.markdown(f"**坐标：** ({x}, {y})")
            st.markdown(f"**RGB：** ({r}, {g}, {b})")
            st.markdown(f"**判断结果：** {result}")
            st.markdown(f'<div style="width:60px;height:60px;background:rgb({r},{g},{b});border:2px solid #333;border-radius:8px;"></div>', unsafe_allow_html=True)
        else:
            st.info("👈 请在图片上点击一个位置")

st.divider()

# ★★★ 反馈邮箱 ★★★
st.write("📧 如有建议，请联系：**2037076846@qq.com**")

st.caption("📌 免责声明：本工具仅提供色彩美学参考。您的照片仅用于实时像素计算，服务器不会保存您的原图。")