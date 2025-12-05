import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw, ImageFont
import io

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Contractor Safety Portal", page_icon="🦺")

# --- 2. THE SAFETY AGREEMENT TEXT ---
# You can edit the text inside the quotes below to fit your specific needs.
SAFETY_AGREEMENT_TEXT = """
**1. Personal Protective Equipment (PPE):** All contractors must wear appropriate PPE at all times while on site. This includes, but is not limited to, hard hats, safety glasses, high-visibility vests, and steel-toed boots.

**2. Hazard Reporting:** Any unsafe conditions, equipment, or practices must be reported to the Site Supervisor immediately.

**3. Emergency Procedures:** Contractors must familiarize themselves with the site emergency evacuation plan and assembly points upon arrival.

**4. Tools and Equipment:** All tools brought onto the site must be in good working condition and meet safety standards.

**5. Drug and Alcohol Policy:** Zero tolerance policy for drugs and alcohol. Anyone found under the influence will be removed from the site immediately.
"""

# --- 3. UI LAYOUT ---
st.title("🦺 Contractor Safety Agreement")
st.markdown("Please review the safety instructions below before signing in.")

# Display the agreement in a scrollable box or clearly on screen
with st.container(border=True):
    st.markdown(SAFETY_AGREEMENT_TEXT)

# The "I have read" Tick Box
agreed = st.checkbox("✅ I acknowledge that I have read and understood the Safety Agreement and Instructions.")

# --- 4. CONDITIONAL FORM (Only shows if they tick the box) ---
if agreed:
    st.success("Thank you. Please fill in your details below.")
    st.write("---")

    # Form Inputs
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
    with col2:
        company = st.text_input("Company Name")

    date = st.date_input("Date of Signing")

    st.write("**Sign Below:**")

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

    # --- 5. IMAGE GENERATION & DOWNLOAD ---
    if canvas_result.image_data is not None:
        # We check if Name and Company are filled before allowing download
        if name and company:
            
            # Convert canvas data to an image
            img_data = canvas_result.image_data.astype('uint8')
            signature_img = Image.fromarray(img_data)
            
            # Create a blank white "Paper" (600px wide x 500px tall)
            final_document = Image.new("RGB", (600, 500), "white")
            draw = ImageDraw.Draw(final_document)
            
            # Draw the Text Info
            # (In a real app, you might want to load a .ttf font, but default is fine here)
            black = (0, 0, 0)
            draw.text((20, 20), "CONTRACTOR SAFETY ACKNOWLEDGEMENT", fill=black)
            draw.line((20, 35, 580, 35), fill=black, width=2)
            
            draw.text((20, 60), f"I, {name}, representing {company},", fill=black)
            draw.text((20, 80), f"hereby confirm that I have read and agree to the", fill=black)
            draw.text((20, 100), f"Contractor Safety Agreement instructions on {date}.", fill=black)
            
            draw.text((20, 150), f"Name: {name}", fill=black)
            draw.text((20, 170), f"Company: {company}", fill=black)
            draw.text((20, 190), f"Date: {date}", fill=black)
            
            draw.text((20, 240), "Signature:", fill=black)

            # Paste the signature image at the bottom
            # We resize it slightly to fit nicely if needed, or paste directly
            final_document.paste(signature_img, (0, 260))
            
            # Save to Memory Buffer
            buffer = io.BytesIO()
            final_document.save(buffer, format="PNG")
            btn_data = buffer.getvalue()
            
            filename = f"Safety_Agreement_{name.replace(' ', '_')}_{date}.png"

            st.write("---")
            st.image(final_document, caption="Document Preview", width=400)
            
            st.download_button(
                label="📥 Download Signed Agreement",
                data=btn_data,
                file_name=filename,
                mime="image/png"
            )
        else:
            # If signature exists but details are missing
            if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
                 st.warning("⚠️ Please fill in your Name and Company to finish.")

else:
    # This shows if the box is NOT ticked
    st.info("👆 Please tick the box above to proceed to the signature form.")
