import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import io
import os
import textwrap

# --- 1. HELPER FUNCTION: WRAP TEXT ---
# This function calculates line breaks so text fits inside the image width
def wrap_text(text, font, max_width):
    """
    Wraps text to fit within max_width. 
    Returns a list of lines.
    """
    lines = []
    # If there are newlines in the input, handle them paragraph by paragraph
    paragraphs = text.split('\n')
    
    for paragraph in paragraphs:
        if paragraph.strip() == "":
            lines.append("") # Preserve empty lines
            continue
            
        # Current line buffer
        current_line = ""
        words = paragraph.split(' ') # Split by space (works well for English)
        
        # Note: Chinese text wrapping is complex because it lacks spaces. 
        # For simplicity, this basic wrapper works if Chinese sentences have some punctuation or if we treat the whole string carefully.
        # For a mixed approach, we check pixel length directly.
        
        accumulated_line = ""
        for word in words:
            test_line = accumulated_line + word + " "
            # Check width of this test line
            left, top, right, bottom = font.getbbox(test_line)
            text_width = right - left
            
            if text_width <= max_width:
                accumulated_line = test_line
            else:
                lines.append(accumulated_line)
                accumulated_line = word + " "
        
        lines.append(accumulated_line) # Append the last part
    
    return lines

# --- 2. LANGUAGE CONFIGURATION ---
st.set_page_config(page_title="Safety Portal / 安全门户", page_icon="🦺")

language = st.sidebar.radio("Select Language / 选择语言", ("English", "中文"))

# --- 3. TEXT CONTENT ---
t = {
    "English": {
        "title": "🦺 Contractor Safety Agreement",
        "instruction": "Please review the safety instructions below before signing in.",
        "rules_title": "SAFETY RULES AND REGULATIONS",
        "rules_text": """
1. PPE REQUIREMENT: All contractors must wear appropriate Personal Protective Equipment (PPE) at all times while on site. This includes hard hats, safety glasses, high-visibility vests, and steel-toed boots.

2. HAZARD REPORTING: Any unsafe conditions, defective equipment, or risky practices must be reported to the Site Supervisor immediately. Do not attempt to fix electrical faults yourself.

3. EMERGENCY PROCEDURES: Contractors must familiarize themselves with the site emergency evacuation plan. In case of an alarm, proceed immediately to the designated Assembly Point.

4. TOOLS & EQUIPMENT: All tools brought onto the site must be in good working condition, inspected, and meet safety standards. makeshift repairs are prohibited.

5. SUBSTANCE POLICY: There is a zero-tolerance policy for drugs and alcohol. Anyone found under the influence will be removed from the site immediately and permanently banned.
        """,
        "checkbox": "✅ I acknowledge that I have read and understood the Safety Agreement.",
        "success_msg": "Thank you. Please fill in your details below.",
        "lbl_name": "Full Name",
        "lbl_company": "Company Name",
        "lbl_date": "Date of Signing",
        "sign_here": "**Sign Below:**",
        "btn_download": "📥 Download Signed Document",
        "warning_fill": "⚠️ Please fill in your Name and Company.",
        "warning_tick": "👆 Please tick the box above to proceed.",
        "doc_declaration": "DECLARATION: I hereby confirm that I have read, understood, and agree to comply with the safety rules listed above.",
        "doc_sign_label": "Signature:"
    },
    "中文": {
        "title": "🦺 承包商安全协议",
        "instruction": "请在签到前阅读以下安全说明。",
        "rules_title": "安全规则与规定",
        "rules_text": """
1. 个人防护装备 (PPE): 所有承包商在现场必须始终佩戴适当的个人防护装备。这包括安全帽、护目镜、高能见度背心和钢头靴。

2. 危险报告: 任何不安全状况、有缺陷的设备或危险操作必须立即向现场主管报告。请勿尝试自行修理电气故障。

3. 紧急程序: 承包商必须熟悉现场紧急疏散计划。如果发生警报，请立即前往指定的集合点。

4. 工具和设备: 带入现场的所有工具必须处于良好的工作状态，经过检查并符合安全标准。严禁临时凑合的修理。

5. 药物和酒精政策: 对毒品和酒精实行零容忍政策。任何被发现受其影响的人将被立即逐出现场并永久禁止进入。
        """,
        "checkbox": "✅ 我确认已阅读并理解安全协议。",
        "success_msg": "谢谢。请在下方填写您的详细信息。",
        "lbl_name": "全名",
        "lbl_company": "公司名称",
        "lbl_date": "签署日期",
        "sign_here": "**请在下方签名：**",
        "btn_download": "📥 下载已签署文件",
        "warning_fill": "⚠️ 请填写您的姓名和公司。",
        "warning_tick": "👆 请先勾选上方选框以继续。",
        "doc_declaration": "声明：本人特此确认已阅读、理解并同意遵守上述安全规则。",
        "doc_sign_label": "签名："
    }
}

current_text = t[language]

# --- 4. UI DISPLAY ---
st.title(current_text["title"])
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
                    # Different sizes for Header, Body, and Small text
                    font_header = ImageFont.truetype(font_path, 40)
                    font_body = ImageFont.truetype(font_path, 20)
                    font_bold = ImageFont.truetype(font_path, 24)
                else:
                    font_header = ImageFont.load_default()
                    font_body = ImageFont.load_default()
                    font_bold = ImageFont.load_default()
                    if language == "中文":
                        st.warning("⚠️ Font file missing. Text will look wrong.")
            except Exception:
                font_header = ImageFont.load_default()
                font_body = ImageFont.load_default()
                font_bold = ImageFont.load_default()

            # --- B. PREPARE CONTENT ---
            # Define image width (A4-ish ratio, but pixel based)
            IMG_WIDTH = 800
            MARGIN = 50
            CONTENT_WIDTH = IMG_WIDTH - (MARGIN * 2)
            
            # 1. Wrap the long rules text
            wrapped_rules = wrap_text(current_text["rules_text"], font_body, CONTENT_WIDTH)
            
            # 2. Calculate Height Needed
            # Start with some padding
            cursor_y = 50 
            
            # Add Header height
            cursor_y += 60 
            
            # Add Rules height (number of lines * line height)
            line_height = 30
            rules_height = len(wrapped_rules) * line_height
            cursor_y += rules_height + 40 # +40 for spacing
            
            # Add Form Details height
            cursor_y += 150 
            
            # Add Signature height
            cursor_y += 150 
            
            TOTAL_HEIGHT = cursor_y + 50 # Bottom margin

            # --- C. DRAW THE IMAGE ---
            final_document = Image.new("RGB", (IMG_WIDTH, TOTAL_HEIGHT), "white")
            draw = ImageDraw.Draw(final_document)
            black = (0, 0, 0)
            
            # Reset Cursor
            y = 50
            
            # 1. Draw Title
            draw.text((MARGIN, y), current_text["rules_title"], fill=black, font=font_header)
            y += 60
            draw.line((MARGIN, y, IMG_WIDTH - MARGIN, y), fill=black, width=2)
            y += 30
            
            # 2. Draw Rules (Line by Line)
            for line in wrapped_rules:
                draw.text((MARGIN, y), line, fill=black, font=font_body)
                y += line_height
            
            y += 40 # Space before declaration
            
            # 3. Draw Declaration & Details
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
            
            # 4. Paste Signature
            draw.text((MARGIN, y), current_text["doc_sign_label"], fill=black, font=font_bold)
            
            # Convert canvas data to image
            sig_data = canvas_result.image_data.astype('uint8')
            signature_img = Image.fromarray(sig_data)
            
            # Resize signature if needed? Let's keep it original size but center it or put it below
            # Paste signature at (Margin, y + 30)
            final_document.paste(signature_img, (MARGIN, y + 30), signature_img)
            
            # --- D. DOWNLOAD ---
            buffer = io.BytesIO()
            final_document.save(buffer, format="PNG")
            btn_data = buffer.getvalue()
            
            filename = f"Safety_Contract_{name}_{date}.png"

            st.write("---")
            st.image(final_document, caption="Final Document Preview", width=600)
            
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
