import streamlit as st
import requests
import base64
import os
from deep_translator import GoogleTranslator

# -------------------- TRANSLATIONS --------------------
translations = {
    "English": {
        "title": "🌿 Crop Suraksha",
        "subtitle": "Automated Plant Disease Analysis",
        "upload": "Upload Plant Leaf Image",
        "select_file": "Select a leaf photo",
        "result": "Diagnosis Results",
        "button": "Begin Analysis",
        "healthy": "Healthy Plant",
        "invalid": "Invalid Specimen",
        "invalid_msg": "Upload a clear leaf image",
        "low_conf": "Low Confidence",
        "disease": "Disease Detected",
        "confidence": "Confidence",
        "cause": "Cause",
        "action": "Treatment",
        "plant": "Plant",
        "scientific": "Scientific Name",
        "processing": "Processing...",
        "upload_msg": "Upload image to start"
    },
    "Hindi": {
        "title": "🌿 Crop Suraksha",
        "subtitle": "स्वचालित पौधा रोग विश्लेषण",
        "upload": "पत्ते की छवि अपलोड करें",
        "select_file": "फोटो चुनें",
        "result": "परिणाम",
        "button": "विश्लेषण शुरू करें",
        "healthy": "स्वस्थ पौधा",
        "invalid": "अमान्य छवि",
        "invalid_msg": "साफ पत्ते की छवि अपलोड करें",
        "low_conf": "कम विश्वास स्तर",
        "disease": "रोग पाया गया",
        "confidence": "विश्वास स्तर",
        "cause": "कारण",
        "action": "उपचार",
        "plant": "पौधा",
        "scientific": "वैज्ञानिक नाम",
        "processing": "प्रोसेसिंग...",
        "upload_msg": "शुरू करने के लिए छवि अपलोड करें"
    },
    "Marathi": {
        "title": "🌿 Crop Suraksha",
        "subtitle": "स्वयंचलित वनस्पती रोग विश्लेषण",
        "upload": "पानाची प्रतिमा अपलोड करा",
        "select_file": "फोटो निवडा",
        "result": "निदान परिणाम",
        "button": "विश्लेषण सुरू करा",
        "healthy": "निरोगी वनस्पती",
        "invalid": "अवैध प्रतिमा",
        "invalid_msg": "स्पष्ट प्रतिमा अपलोड करा",
        "low_conf": "कमी खात्री",
        "disease": "रोग आढळला",
        "confidence": "विश्वास टक्केवारी",
        "cause": "कारण",
        "action": "उपाय",
        "plant": "वनस्पती",
        "scientific": "शास्त्रीय नाव",
        "processing": "प्रक्रिया सुरू आहे...",
        "upload_msg": "सुरू करण्यासाठी प्रतिमा अपलोड करा"
    }
}

PLANT_ID_API_KEY = "ux5raFUDZ3ZCTr8HhMPyxRTIKGqOo1X4ECG3WAIUftMsrqnxKs"

st.set_page_config(page_title="Crop Health Detector", page_icon="🌿", layout="wide")

# -------------------- FUNCTIONS --------------------
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def translate_text(text, lang):
    if lang == "English" or not text:
        return text
    try:
        code = "hi" if lang == "Hindi" else "mr"
        return GoogleTranslator(source='auto', target=code).translate(text)
    except:
        return text

def identify_and_diagnose(image_bytes_base64):
    url = "https://api.plant.id/v2/identify"
    
    payload = {
        "images": [image_bytes_base64],
        "modifiers": ["crops_fast", "health_all"],
        "plant_details": ["common_names", "taxonomy"],
        "disease_details": ["cause", "treatment", "description"]
    }

    headers = {
        "Content-Type": "application/json",
        "Api-Key": PLANT_ID_API_KEY
    }

    try:
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code != 200:
            return None, res.text
        return res.json(), None
    except Exception as e:
        return None, str(e)

# -------------------- MAIN --------------------
def main():
    local_css("style.css")

    lang = st.selectbox("Language / भाषा / भाषा निवडा", ["English", "Hindi", "Marathi"])
    t = translations[lang]

    # -------- SIDEBAR --------
    st.sidebar.title("System Status")

    st.sidebar.success({
        "English": "Connected to AI, ready for analysis.",
        "Hindi": "AI से जुड़ा हुआ, विश्लेषण के लिए तैयार।",
        "Marathi": "AI शी जोडलेले, विश्लेषणासाठी तयार."
    }[lang])

 
    st.sidebar.write({
        "English": "This system uses AI to identify plant species and detect diseases.",
        "Hindi": "यह प्रणाली पौधों की पहचान और रोगों का पता लगाने के लिए AI का उपयोग करती है।",
        "Marathi": "ही प्रणाली वनस्पती ओळखण्यासाठी आणि रोग शोधण्यासाठी AI वापरते."
    }[lang])

 
    st.sidebar.subheader({
        "English": "👨‍💻 Developers",
        "Hindi": "👨‍💻 डेवलपर्स",
        "Marathi": "👨‍💻 विकसक"
    }[lang])

    st.sidebar.success("Prathamesh A Hon : FY BTech CSE")
    st.sidebar.success("Mayur B Gund : FY BTech CSE")
    st.sidebar.success("Abhishek A Shinde : FY BTech CSE")
    st.sidebar.success("Danish A Shaikh : FY BTech CSE")
    
    

    # -------- MAIN UI --------
    st.markdown(f'<h1 class="main-title">{t["title"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{t["subtitle"]}</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"### {t['upload']}")
        uploaded_file = st.file_uploader("", type=['jpg','jpeg','png'])
        st.caption(t["select_file"])

        if uploaded_file:
            st.image(uploaded_file, width="stretch")

    with col2:
        st.markdown(f"### {t['result']}")

        if uploaded_file:
            if st.button(t["button"]):
                with st.spinner(t["processing"]):

                    img = encode_image(uploaded_file)
                    data, error = identify_and_diagnose(img)

                    if error:
                        st.error(error)
                        return

                    if not data or "suggestions" not in data:
                        st.error("No result")
                        return

                    suggestions = data.get("suggestions", [])
                    if not suggestions:
                        st.error("No plant detected")
                        return

                    s = suggestions[0]
                    prob = s.get("probability", 0)

                    if prob < 0.01:
                        st.error(f"{t['invalid']} - {t['invalid_msg']}")
                        return

                    details = s.get("plant_details", {})
                    common = details.get("common_names", ["Unknown"])[0]
                    sci = details.get("scientific_name", "N/A")

                    st.markdown(f"""
                    <div class="result-card">
                        <b>{t['plant']}:</b> {translate_text(common, lang)}<br>
                        <i>{t['scientific']}: {sci}</i>
                    </div>
                    """, unsafe_allow_html=True)

                    health = data.get("health_assessment", {})

                    if health.get("is_healthy"):
                        st.success(f"✅ {t['healthy']}")
                        return

                    diseases = health.get("diseases", [])
                    if not diseases:
                        st.warning(t["low_conf"])
                        return

                    d = diseases[0]
                    conf = round(d.get("probability", 0) * 100, 1)

                    if conf < 5:
                        st.warning(t["low_conf"])
                        return

                    name = translate_text(d.get("name", ""), lang)
                    st.error(f"{t['disease']}: {name}")
                    st.write(f"{t['confidence']}: {conf}%")

                    with st.expander(t["action"]):
                        det = d.get("disease_details", {})
                        cause = translate_text(det.get("cause", ""), lang)

                        st.write(f"{t['cause']}: {cause}")

                        treatment = det.get("treatment", {}).get("biological", "")
                        if isinstance(treatment, list):
                            treatment = " ".join(treatment)

                        st.write(translate_text(treatment, lang))

        else:
            st.info(t["upload_msg"])
# -------- FOOTER --------
st.markdown("""
    <div class="footer-container">
        <div class="footer-line-1">Dedicated to <strong>Shetkari Raja</strong> | Plant Health Engine | By <strong>Bug Hunters</strong></div>
        <div class="footer-line-2"><footer>&copy; 2026 Bug Hunters. All rights reserved.</footer></div>
    </div>
""", unsafe_allow_html=True)
# --------------------
if __name__ == "__main__":
    main()
