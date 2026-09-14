import streamlit as st
from PIL import Image, ImageDraw
import colorsys
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="冷暖调判断器", page_icon="🎨")
st.title("🎨 冷暖调判断器")
st.write("上传一张照片，点击图片上的位置，立刻判断颜色的冷暖调。")

st.warning("💡 重要提示：点击图片上的位置后，结果会在图片的正下方显示，请向下滑动查看！")

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
    
    # 压缩图片（改回400，保证清晰度和点击精度）
    if max(img.size) > 400:
        ratio = 400 / max(img.size)
        img = img.resize((int(img.size[0] * ratio), int(img.size[1] * ratio)), Image.Resampling.LANCZOS)

    st.write("👇 点击图片上的位置取色：")
    value = streamlit_image_coordinates(img, key="click", width=400)

    if value is not None:
        x, y = value["x"], value["y"]
        
        x = max(0, min(x, img.width - 1))
        y = max(0, min(y, img.height - 1))
        
        r, g, b = img.getpixel((x, y))[:3]
        result = judge_temperature(r, g, b)

        marked_img = img.copy()
        draw = ImageDraw.Draw(marked_img)
        draw.ellipse((x-6, y-6, x+6, y+6), outline="red", width=3)
        draw.line((x-10, y, x+10, y), fill="red", width=2)
        draw.line((x, y-10, x, y+10), fill="red", width=2)
        
        st.image(marked_img, caption="📍 您点击的位置", width=400)

        st.markdown("---")
        st.markdown(
            f"<h2 style='text-align: center; color: #d32f2f; margin-bottom: 0;'>🎯 判定结果：{result}</h2>", 
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='text-align: center; color: #666;'>坐标：({x}, {y})  |  RGB：({r}, {g}, {b})</p >", 
            unsafe_allow_html=True
        )

st.divider()
st.write("📧 如有建议，请联系：**2037076846@qq.com**")
st.caption("📌 免责声明：本工具仅提供色彩美学参考。您的照片仅用于实时像素计算，服务器不会保存您的原图。")