import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import io
import os

# --- 1. LANGUAGE CONFIGURATION ---
st.set_page_config(page_title="Safety Portal / 安全门户", page_icon="🦺")

# Language Selector in Sidebar
language = st.sidebar.radio("Select Language / 选择语言", ("English", "中文"))

# --- 2. TRANSLATION DICTIONARY ---
# This holds all the text for both languages
t = {
    "English": {
        "title": "🦺 Contractor Safety Agreement",
        "instruction": "Please review the safety instructions below before signing in.",
        "rules_title": "Safety Rules:",
        "rules_text": """
        **1. PPE:** Wear hard hats, safety glasses, and boots at all times.
        **2. Reporting:** Report unsafe conditions to the Supervisor immediately.
        **3. Emergency:** Know the evacuation plan and assembly points.
        **4. Tools:** Use only tools that are in good working condition.
        **5. Substance:** Zero tolerance for drugs and alcohol.
        """,
        "checkbox": "✅ I acknowledge that I have read and understood the Safety Agreement.",
        "success_msg": "Thank you. Please fill in your details below.",
        "lbl_name": "Full Name",
        "lbl_company": "Company Name",
        "lbl_date": "Date of Signing",
        "sign_here": "**Sign Below:**",
        "btn_download": "📥 Download Signed Agreement",
        "warning_fill": "⚠️ Please fill in your Name and Company.",
        "warning_tick": "👆 Please tick the box above to proceed.",
        "doc_header": "CONTRACTOR SAFETY ACKNOWLEDGEMENT",
        "doc_body": "I hereby confirm that I have read and agree to the safety instructions.",
        "doc_sign_label": "Signature:"
    },
    "中文": {
        "title": "🦺 承包商安全协议",
        "instruction": "请在签到前阅读以下安全说明。",
        "rules_title": "安全规则：",
        "rules_text": """
        **1. 个人防护装备 (PPE):** 必须始终佩戴安全帽、护目镜和安全靴。
        **2. 报告:** 发现任何不安全状况立即向主管报告。
        **3. 紧急情况:** 熟悉紧急疏散计划和集合点。
        **4. 工具:** 仅使用状况良好的工具。
        **5. 违禁品:** 严禁携带毒品和酒精进场。
        """,
        "checkbox": "✅ 我确认已阅读并理解安全协议。",
        "success_msg": "谢谢。请在下方填写您的详细信息。",
        "lbl_name": "全名",
        "lbl_company": "公司名称",
        "lbl_date": "签署日期",
        "sign_here": "**请在下方签名：**",
        "btn_download": "📥 下载已签署协议",
        "warning_fill": "⚠️ 请填写您的姓名和公司。",
        "warning_tick": "👆 请先勾选上方选框以继续。",
        "doc_header": "承包商安全确认书",
        "doc_body": "本人特此确认已阅读并同意遵守上述安全指示。",
        "doc_sign_label": "签名："
    }
}

# Select the dictionary based on language choice
current_text = t[language]

# --- 3. UI LAYOUT ---
st.title(current_text["title"])
st.markdown(current_text["instruction"])

# Display Rules
with st.container(border=True):
    st.markdown(f"### {current_text['rules_title']}")
    st.markdown(current_text["rules_text"])

# Acknowledgement Checkbox
agreed = st.checkbox(current_text["checkbox"])

# --- 4. CONDITIONAL FORM ---
if agreed:
    st.success(current_text["success_msg"])
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(current_text["lbl_name"])
    with col2:
        company = st.text_input(current_text["lbl_company"])

    date = st.date_input(current_text["lbl_date"])

    st.write(current_text["sign_here"])

    # Signature Canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#ffffff",
        height=150,
        width=600,
        drawing_mode="freedraw",
        key="signature_canvas",
    )

    # --- 5. IMAGE GENERATION ---
    if canvas_result.image_data is not None:
        if name and company:
            
# A. LOAD FONT (Crucial for Chinese)
            try:
                font_path = "font.ttf" 
                if os.path.exists(font_path):
                    custom_font = ImageFont.truetype(font_path, 20)
                    header_font = ImageFont.truetype(font_path, 28)
                else:
                    # Fallback if file not found
                    custom_font = ImageFont.load_default()
                    header_font = ImageFont.load_default()
                    if language == "中文":
                        st.warning("⚠️ Font file 'font.ttf' not found. Chinese text will appear as squares.")
            except Exception as e:
                # Fallback if any error occurs during font loading
                custom_font = ImageFont.load_default()
                header_font = ImageFont.load_default()  # <--- This line was missing!

            # B. CREATE IMAGE
            img_data = canvas_result.image_data.astype('uint8')
            signature_img = Image.fromarray(img_data)
            
            final_document = Image.new("RGB", (600, 500), "white")
            draw = ImageDraw.Draw(final_document)
            black = (0, 0, 0)
            
            # C. DRAW TEXT
            # Header
            draw.text((20, 20), current_text["doc_header"], fill=black, font=header_font)
            draw.line((20, 55, 580, 55), fill=black, width=2)
            
            # Body
            draw.text((20, 70), f"{current_text['lbl_name']}: {name}", fill=black, font=custom_font)
            draw.text((20, 100), f"{current_text['lbl_company']}: {company}", fill=black, font=custom_font)
            draw.text((20, 130), f"{current_text['lbl_date']}: {date}", fill=black, font=custom_font)
            
            # Statement
            draw.text((20, 170), current_text["doc_body"], fill=black, font=custom_font)
            
            # Signature Label
            draw.text((20, 240), current_text["doc_sign_label"], fill=black, font=custom_font)

            # Paste Signature
            final_document.paste(signature_img, (0, 260), signature_img) # Use signature_img as mask if transparent
            
            # Save to buffer
            buffer = io.BytesIO()
            final_document.save(buffer, format="PNG")
            btn_data = buffer.getvalue()
            
            filename = f"Signed_{name}_{date}.png"

            st.write("---")
            st.image(final_document, caption="Preview", width=400)
            
            st.download_button(
                label=current_text["btn_download"],
                data=btn_data,
                file_name=filename,
                mime="image/png"
            )
        else:
             if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
                 st.warning(current_text["warning_fill"])

else:
    st.info(current_text["warning_tick"])
