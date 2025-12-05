import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Digital Sign-Off Form", page_icon="📝")

st.title("📝 Customer Sign-Off Form")
st.markdown("Please fill in your details and sign below.")

# --- FORM INPUTS ---
# We use columns to make it look professional
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name")
    
with col2:
    company = st.text_input("Company Name")

# Date Selector
date = st.date_input("Date of Signing")

st.write("---")
st.write("**Sign Here:**")

# --- SIGNATURE CANVAS ---
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

# --- PROCESSING ---
if canvas_result.image_data is not None:
    # Check if the user has actually drawn something (by checking opacity or logic)
    # Here we just check if they entered a name to enable the button
    if name and company:
        
        # 1. Convert Canvas to Image
        img_data = canvas_result.image_data.astype('uint8')
        signature_img = Image.fromarray(img_data)
        
        # 2. Create a blank white "Paper" image to combine text + signature
        # Size: 600px wide, 400px tall
        final_document = Image.new("RGB", (600, 400), "white")
        draw = ImageDraw.Draw(final_document)
        
        # 3. Draw the Text info onto the "Paper"
        # (We use default font for simplicity, but you can load .ttf files if needed)
        draw.text((20, 20), f"Name: {name}", fill="black")
        draw.text((20, 50), f"Company: {company}", fill="black")
        draw.text((20, 80), f"Date: {date}", fill="black")
        draw.line((20, 110, 580, 110), fill="black", width=2) # A separator line
        
        # 4. Paste the Signature Image at the bottom
        # We assume the signature canvas is transparent/white. 
        # We paste it starting at y=120
        final_document.paste(signature_img, (0, 120))
        
        # 5. Prepare for Download
        buffer = io.BytesIO()
        final_document.save(buffer, format="PNG")
        btn_data = buffer.getvalue()
        
        # Create a specific filename
        filename = f"Signed_{name.replace(' ', '_')}_{date}.png"

        st.success("Form ready! Download your signed slip below.")
        
        # Show the result on screen so they can see it
        st.image(final_document, caption="Preview of your signed document", use_column_width=True)
        
        st.download_button(
            label="📥 Download Signed Form",
            data=btn_data,
            file_name=filename,
            mime="image/png"
        )
    else:
        st.info("Please enter your Name and Company to generate the download.")
