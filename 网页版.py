import streamlit as st
from PIL import Image
import colorsys
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="冷暖调判断器", page_icon="🎨")
st.title("🎨 冷暖调判断器")
st.write("上传一张照片，点击图片上的位置，立刻判断颜色的冷暖调。")

def judge_temperature(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    hue_deg = h * 360

    if hue_deg < 180:
        tendency = "暖"
    else:
        tendency = "冷"

    if hue_deg < 30 or hue_deg >= 330:
        detail = "红"
    elif hue_deg < 60:
        detail = "橙"
    elif hue_deg < 90:
        detail = "黄"
    elif hue_deg < 120:
        detail = "黄绿"
    elif hue_deg < 150:
        detail = "绿"
    elif hue_deg < 180:
        detail = "青绿"
    elif hue_deg < 210:
        detail = "青"
    elif hue_deg < 240:
        detail = "蓝"
    elif hue_deg < 270:
        detail = "蓝紫"
    elif hue_deg < 300:
        detail = "紫"
    else:
        detail = "紫红"

    if v < 0.25:
        return f"{tendency}黑（偏{tendency}{detail}）"
    if v > 0.80 and s < 0.20:
        return f"{tendency}白（偏{tendency}{detail}）"
    if s < 0.20:
        return f"{tendency}灰（偏{tendency}{detail}）"

    if 0 <= hue_deg < 30:
        return "暖调红 / 暖调橙（暖）"
    elif 30 <= hue_deg < 60:
        return "暖调黄 / 暖调橙（暖）"
    elif 60 <= hue_deg < 90:
        return "冷调黄 / 暖调绿（冷暖交界）"
    elif 90 <= hue_deg < 120:
        return "暖调绿（暖）"
    elif 120 <= hue_deg < 150:
        return "冷绿（冷）"
    elif 150 <= hue_deg < 180:
        return "暖调青 / 冷调绿（冷暖交界）"
    elif 180 <= hue_deg < 210:
        return "冷调青 / 暖调蓝（冷暖交界）"
    elif 210 <= hue_deg < 240:
        return "冷调蓝（冷）"
    elif 240 <= hue_deg < 270:
        return "暖调蓝 / 冷调紫（冷暖交界）"
    elif 270 <= hue_deg < 300:
        return "冷紫（冷）"
    elif 300 <= hue_deg < 330:
        return "暖调紫（暖）"
    elif 330 <= hue_deg < 360:
        return "冷调红 / 暖调紫（冷暖交界）"
    else:
        return "角度异常"

uploaded_file = st.file_uploader("选择一张图片", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.write("👇 点击图片上的位置取色：")

    value = streamlit_image_coordinates(img, key="click")

    if value is not None:
        x, y = value["x"], value["y"]
        r, g, b = img.getpixel((x, y))[:3]
        result = judge_temperature(r, g, b)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**坐标：** ({x}, {y})")
            st.markdown(f"**RGB：** ({r}, {g}, {b})")
        with col2:
            st.markdown(f"**判断结果：** {result}")
            st.markdown(
                f'<div style="width:60px;height:60px;background:rgb({r},{g},{b});border:2px solid #333;border-radius:8px;"></div>',
                unsafe_allow_html=True
            )

st.divider()
st.subheader("📝 反馈")
st.write("如果你在使用中遇到问题，或者有建议，欢迎填写反馈：")
st.markdown("[点这里填写反馈](https://v.wjx.cn/vm/eo23cWG.aspx)")