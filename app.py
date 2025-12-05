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

current
