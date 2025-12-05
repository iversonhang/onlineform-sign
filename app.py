import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Signature App", page_icon="✍️")

st.title("✍️ Sign & Download")
st.markdown("Draw your signature below and click the download button.")

# 1. Create the Canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)", 
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    height=200,
    width=600,
    drawing_mode="freedraw",
    key="signature_canvas",
)

# 2. Process the input
if canvas_result.image_data is not None:
    # Convert the numpy array (from canvas) into a standard image
    img_data = canvas_result.image_data.astype('uint8')
    image = Image.fromarray(img_data)

    # 3. Create a buffer to hold the image data in memory (Cloud friendly)
    # This replaces saving to the hard drive
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    btn_data = buffer.getvalue()

    # 4. Show a download button
    # Only show if the user has actually drawn something (not just a blank canvas)
    # (A simple check is to see if the bytes are different from a blank canvas, 
    # but for simplicity, we just show the button always)
    st.download_button(
        label="📥 Download Signature",
        data=btn_data,
        file_name="signature.png",
        mime="image/png"
    )
