import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import io
import os
import textwrap

# --- 1. HELPER FUNCTION: WRAP TEXT ---
def wrap_text(text, font, max_width):
    lines = []
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        if paragraph.strip() == "":
            lines.append("") 
            continue
        current_line = ""
        words = paragraph.split(' ')
        accumulated_line = ""
        for word in words:
            test_line = accumulated_line + word + " "
            left, top, right, bottom = font.getbbox(test_line)
            text_width = right - left
            if text_width <= max_width:
                accumulated_line = test_line
            else:
                lines.append(accumulated_line)
                accumulated_line = word + " "
        lines.append(accumulated_line)
    return lines

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="AISHK Safety Portal", page_icon="🏫")

# Logo in the web interface (Sidebar)
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)

language = st.sidebar.radio("Select Language / 选择语言", ("English", "中文"))

# --- 3. TEXT CONTENT (UPDATED FOR AISHK) ---
t = {
    "English": {
        "school_name": "Australian International School Hong Kong",
        "title": "Contractor Safety Agreement",
        "instruction": "Welcome to AISHK. Please review the safety instructions below before signing in.",
        "rules_title": "CAMPUS SAFETY RULES AND REGULATIONS",
        "rules_text": """
1. IDENTIFICATION: All contractors must wear the AISHK Visitor Pass at all times while on campus.

2. PPE REQUIREMENT: Appropriate Personal Protective Equipment (PPE) must be worn in designated work areas.

3. STUDENT SAFETY: Contractors must strictly maintain separation from students. Do not enter classrooms or student areas unless authorized and accompanied by staff.

4. EMERGENCY PROCEDURES: In the event of a fire alarm, stop work immediately and proceed to the designated assembly point on the sports field.

5. NO SMOKING: AISHK is a smoke-free campus. Smoking is strictly prohibited anywhere on school grounds.

6. PHOTOGRAPHY: Taking photos of students or staff is strictly prohibited.
        """,
        "checkbox": "✅ I acknowledge that I have read and understood the AISHK Safety Agreement.",
        "success_msg": "Thank you. Please fill in your details below.",
        "lbl_name": "Full Name",
        "lbl_company": "Company Name",
        "lbl_date": "Date of Signing",
        "sign_here": "**Sign Below:**",
        "btn_download": "📥 Download Signed Document",
        "warning_fill": "⚠️ Please fill in your Name and Company.",
        "warning_tick": "👆 Please tick the box above to proceed.",
        "doc_declaration": "DECLARATION: I hereby confirm that I have read, understood, and agree to comply with the school safety rules listed above.",
        "doc_sign_label": "Signature:"
    },
    "中文": {
        "school_name": "香港澳洲國際學校",
        "title": "承包商安全协议",
        "instruction": "欢迎来到香港澳洲國際學校 (AISHK)。请在签到前阅读以下安全说明。",
        "rules_title": "校园安全规则与规定",
        "rules_text": """
1. 身份识别: 所有承包商在校期间必须始终佩戴访客证。

2. 个人防护装备: 在指定工作区域必须佩戴适当的个人防护装备 (PPE)。

3. 学生安全: 承包商必须严格与学生保持距离。除非获得授权并由工作人员陪同，否则不得进入教室或学生活动区域。

4. 紧急程序: 如果发生火警，请立即停止工作并前往运动场的指定集合点。

5. 禁止吸烟: 本校为无烟校园。严禁在校园内任何地方吸烟。

6. 摄影: 严禁拍摄学生或教职员工的照片。
        """,
        "checkbox": "✅ 我确认已阅读并理解学校安全协议。",
        "success_msg": "谢谢。请在下方填写您的详细信息。",
        "lbl_name": "全名",
        "lbl_company": "公司名称",
        "lbl_date": "签署日期",
        "sign_here": "**请在下方签名：**",
        "btn_download": "📥 下载已签署文件",
        "warning_fill": "⚠️ 请填写您的姓名和公司。",
        "warning_tick": "👆 请先勾选上方选框以继续。",
        "doc_declaration": "声明：本人特此确认已阅读、理解并同意遵守上述学校安全规则。",
        "doc_sign_label": "签名："
    }
}

current_text = t[language]

# --- 4. UI DISPLAY ---
st.title(current_text["school_name"])
st.subheader(current_text["title"])
st.markdown(current_text["instruction"])

# Show Rules on Screen
with st.container(border=True):
    st.markdown(f"### {current_text['rules_title']}")
    st.markdown(current_text["rules_text"])

agreed = st.checkbox(current_text["checkbox"])

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

    # --- 5. IMAGE GENERATION LOGIC ---
    if canvas_result.image_data is not None:
        if name and company:
            
            # --- A. LOAD FONTS ---
            try:
                font_path = "font.ttf"
                if os.path.exists(font_path):
                    font_header = ImageFont.truetype(font_path, 36) # School Name
                    font_sub = ImageFont.truetype(font_path, 28)    # Title
                    font_body = ImageFont.truetype(font_path, 20)   # Text
                    font_bold = ImageFont.truetype(font_path, 24)   # Bold text
                else:
                    raise Exception("Font not found")
            except Exception:
                font_header = ImageFont.load_default()
                font_sub = ImageFont.load_default()
                font_body = ImageFont.load_default()
                font_bold = ImageFont.load_default()

            # --- B. PREPARE CONTENT ---
            IMG_WIDTH = 800
            MARGIN = 50
            CONTENT_WIDTH = IMG_WIDTH - (MARGIN * 2)
            
            # Wrap Rules
            wrapped_rules = wrap_text(current_text["rules_text"], font_body, CONTENT_WIDTH)
            
            # Calculate Height
            cursor_y = 50 
            
            # Add Logo Space if it exists
            has_logo = os.path.exists("logo.png")
            if has_logo:
                cursor_y += 100 # Reserve 100px height for logo
            
            cursor_y += 50 # School Name
            cursor_y += 40 # Title
            cursor_y += 30 # Spacer
            
            # Rules Height
            line_height = 30
            rules_height = len(wrapped_rules) * line_height
            cursor_y += rules_height + 40 
            
            # Form & Signature Height
            cursor_y += 150 # Form details
            cursor_y += 150 # Signature
            
            TOTAL_HEIGHT = cursor_y + 50

            # --- C. DRAW THE IMAGE ---
            final_document = Image.new("RGB", (IMG_WIDTH, TOTAL_HEIGHT), "white")
            draw = ImageDraw.Draw(final_document)
            black = (0, 0, 0)
            
            # Reset Cursor
            y = 50
            
            # 1. Draw Logo
            if has_logo:
                logo_img = Image.open("logo.png")
                # Resize logo to max height 80px, maintain aspect ratio
                logo_img.thumbnail((400, 80)) 
                # Paste logo (using itself as mask if transparent)
                if logo_img.mode == 'RGBA':
                    final_document.paste(logo_img, (MARGIN, y), logo_img)
                else:
                    final_document.paste(logo_img, (MARGIN, y))
                y += 100 # Move down past logo

            # 2. Draw Headers
            draw.text((MARGIN, y), current_text["school_name"], fill="#003366", font=font_header) # AISHK Blue-ish color
            y += 45
            draw.text((MARGIN, y), current_text["title"], fill=black, font=font_sub)
            y += 40
            draw.line((MARGIN, y, IMG_WIDTH - MARGIN, y), fill=black, width=2)
            y += 30
            
            # 3. Draw Rules
            draw.text((MARGIN, y), current_text["rules_title"], fill=black, font=font_bold)
            y += 30
            for line in wrapped_rules:
                draw.text((MARGIN, y), line, fill=black, font=font_body)
                y += line_height
            
            y += 40
            
            # 4. Draw Declaration & Details
            draw.line((MARGIN, y, IMG_WIDTH - MARGIN, y), fill=black, width=1)
            y += 20
            draw.text((MARGIN, y), current_text["doc_declaration"], fill=black, font=font_bold)
            y += 50
            
            draw.text((MARGIN, y), f"{current_text['lbl_name']}: {name}", fill=black, font=font_body)
            y += 30
            draw.text((MARGIN, y), f"{current_text['lbl_company']}: {company}", fill=black, font=font_body)
            y += 30
            draw.text((MARGIN, y), f"{current_text['lbl_date']}: {date}", fill=black, font=font_body)
            y += 50
            
            # 5. Paste Signature
            draw.text((MARGIN, y), current_text["doc_sign_label"], fill=black, font=font_bold)
            
            sig_data = canvas_result.image_data.astype('uint8')
            signature_img = Image.fromarray(sig_data)
            
            # Resize signature slightly if it's too big
            signature_img.thumbnail((400, 150))
            
            # Paste
            final_document.paste(signature_img, (MARGIN, y + 30), signature_img)
            
            # --- D. DOWNLOAD ---
            buffer = io.BytesIO()
            final_document.save(buffer, format="PNG")
            btn_data = buffer.getvalue()
            
            filename = f"AISHK_Safety_{name}_{date}.png"

            st.write("---")
            st.image(final_document, caption="Signed Document Preview", width=600)
            
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
