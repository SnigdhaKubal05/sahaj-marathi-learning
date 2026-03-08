import streamlit as st
from gtts import gTTS
import base64
from database import create_tables, insert_default_data, get_sentences_by_category

# ---------- DB INIT ----------
create_tables()
insert_default_data()

st.set_page_config(page_title="SAHAJ", layout="centered")

# ---------- CUSTOM BACKGROUND ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.stApp {
    background:
        radial-gradient(ellipse 70% 60% at 15% 15%, rgba(200,60,100,0.30) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 85% 85%, rgba(170,40,80,0.25)  0%, transparent 55%),
        radial-gradient(ellipse 80% 70% at 50% 50%, rgba(120,20,50,0.15)  0%, transparent 70%),
        linear-gradient(160deg, #1e0810, #2a0d16, #180609);
}

.block-container {
    max-width: 780px !important;
    margin: 2rem auto !important;
    padding: 2.5rem 3rem !important;
    border-radius: 26px;
    background: #1a0d12 !important;
    border: 1px solid rgba(220,90,130,0.25);
    box-shadow: 0 25px 60px rgba(0,0,0,0.75), 0 0 40px rgba(180,50,90,0.08), inset 0 1px 0 rgba(255,200,210,0.06);
    position: relative;
}

.block-container::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(230,100,140,0.7), transparent);
}

h1 { font-size: 46px !important; font-weight: 700; color: #ffffff !important; text-align: center; letter-spacing: 1.5px; }
h2 { font-size: 22px !important; font-weight: 600; color: #ffccd8 !important; text-align: center; }
h3 { font-size: 28px !important; font-weight: 600; color: #ffffff !important; text-align: center; }
p, label, .stMarkdown { color: #e8a0b0 !important; text-align: center; line-height: 1.75; }

.stButton,
div[data-testid="stVerticalBlock"] .stButton,
div[data-testid="column"] .stButton {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

.stButton > button {
    background: linear-gradient(135deg, #c73d5e, #e05575, #cf4a68);
    color: #ffffff !important;
    font-weight: 700;
    font-size: 18px !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none; border-radius: 14px;
    height: 56px; padding: 0 2.5rem; width: 260px !important;
    box-shadow: 0 6px 22px rgba(200,60,90,0.4);
    transition: all 0.25s ease;
    margin: 0 auto;
    text-shadow: 0 1px 4px rgba(0,0,0,0.5);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(200,60,90,0.6);
}

div[data-testid="column"],
div[data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
}

.stTextInput > div > input, .stTextArea > div > textarea {
    background: #2a1018 !important;
    border: 1px solid rgba(210,90,130,0.3) !important;
    border-radius: 11px !important; color: #ffffff !important;
}

#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(210,90,130,0.4); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ---------- AUDIO FUNCTION ----------
def play_audio(text):
    tts = gTTS(text=text, lang='mr')
    tts.save("temp.mp3")
    audio_file = open("temp.mp3", "rb")
    audio_bytes = audio_file.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


# ---------- REUSABLE SENTENCE PAGE HELPER ----------
# ✅ Defined BEFORE the if/elif chain so Python can find it
def show_sentence_page(header_text, category_key, audio_intro):
    st.header(header_text)

    if st.button("🔊 ऐका "):
        play_audio(audio_intro)

    sentences = get_sentences_by_category(category_key)

    if not sentences:
        st.warning("कोणतीही वाक्ये सापडली नाहीत.")
    else:
        for idx, sentence in enumerate(sentences):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"### {sentence}")
            with col2:
                if st.button("🔊", key=f"{category_key}_{idx}"):
                    play_audio(sentence)

    if st.button("🔙 वाक्यांच्या प्रकारांवर जा"):
        st.session_state.page = "sentences"
        st.rerun()

    if st.button("🏡 मुख्यपृष्ठावर जा"):
        st.session_state.page = "home"
        st.rerun()


# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "home_spoken" not in st.session_state:
    st.session_state.home_spoken = False


# ============================================================
# HOME
# ============================================================
if st.session_state.page == "home":

    st.title("SAHAJ - ऐका, शिका, बोला")
    st.subheader("Simple Marathi Learning for elders - आजी आजोबांसाठी")

    if not st.session_state.home_spoken:
        play_audio("सहज ऐका, शिका, बोला मध्ये आपले स्वागत आहे")
        st.session_state.home_spoken = True

    if st.button("🔤 मुळाक्षरे"):
        play_audio("मुळाक्षरे विभाग")
        st.session_state.page = "letters"
        st.rerun()

    if st.button("📖 शब्द"):
        play_audio("शब्द विभाग")
        st.session_state.page = "words"
        st.rerun()

    if st.button("📝 वाक्ये"):
        play_audio("वाक्य विभाग")
        st.session_state.page = "sentences"
        st.rerun()


# ============================================================
# LETTERS
# ============================================================
elif st.session_state.page == "letters":

    st.header("मुळाक्षरे")

    if st.button("🔊 ऐका "):
        play_audio("मुळाक्षरे")

    letters = [
        "अ", "आ", "इ", "ई", "उ", "ऊ",
        "ए", "ऐ", "ओ", "औ", "अं", "अः", "ॲ", "ऑ",
        "क", "ख", "ग", "घ", "ङ",
        "च", "छ", "ज", "झ", "ञ",
        "ट", "ठ", "ड", "ढ", "ण",
        "त", "थ", "द", "ध", "न",
        "प", "फ", "ब", "भ", "म",
        "य", "र", "ल", "व",
        "श", "ष", "स", "ह", "ळ", "क्ष", "ज्ञ"
    ]

    for letter in letters:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"### {letter}")
        with col2:
            if st.button("🔊", key=letter):
                play_audio(letter)

    if st.button("🔙 मुख्यपृष्ठावर जा"):
        play_audio("मुख्यपृष्ठावर जात आहोत")
        st.session_state.page = "home"
        st.rerun()

    if st.button("➡️ पुढे - शब्द"):
        st.session_state.page = "words"
        st.rerun()


# ============================================================
# WORDS
# ============================================================
elif st.session_state.page == "words":

    st.header("दैनंदिन वापरातील शब्द")

    if st.button("🔊 ऐका शब्द"):
        play_audio("दैनंदिन वापरातील शब्द")

    words = [
        "नमस्कार", "धन्यवाद", "कृपया", "पाणी", "चहा",
        "जेवण", "औषध", "घर", "मुलगा", "मुलगी",
        "भाऊ", "बहीण", "आई", "वडील", "बस",
        "दूध", "भाजी", "फळे", "डॉक्टर", "मदत",
        "हो", "नाही", "थांबा", "या", "जा"
    ]

    for word in words:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"### {word}")
        with col2:
            if st.button("🔊", key=word):
                play_audio(word)

    if st.button("🔙 मुख्यपृष्ठावर जा"):
        play_audio("मुख्यपृष्ठावर जात आहोत")
        st.session_state.page = "home"
        st.rerun()

    if st.button("➡️ पुढे - वाक्ये"):
        st.session_state.page = "sentences"
        st.rerun()


# ============================================================
# SENTENCES — Category picker
# ============================================================
elif st.session_state.page == "sentences":

    st.header("वाक्यांचे प्रकार")

    if st.button("🔊 ऐका "):
        play_audio("वाक्यांचे प्रकार निवडा")

    if st.button("🏠 घरगुती"):
        play_audio("घरगुती वाक्ये")
        st.session_state.page = "home_sentences"
        st.rerun()

    if st.button("🏥 रुग्णालय"):
        play_audio("रुग्णालय वाक्ये")
        st.session_state.page = "hospital_sentences"
        st.rerun()

    if st.button("🛒 बाजार"):
        play_audio("बाजार वाक्ये")
        st.session_state.page = "market_sentences"
        st.rerun()

    if st.button("🆘 मदत"):
        play_audio("मदत वाक्ये")
        st.session_state.page = "help_sentences"
        st.rerun()

    if st.button("🔙 मुख्यपृष्ठावर जा"):
        play_audio("मुख्यपृष्ठावर जात आहोत")
        st.session_state.page = "home"
        st.rerun()


# ============================================================
# 🏠 GHARGUTI SENTENCES
# ============================================================
elif st.session_state.page == "home_sentences":
    show_sentence_page("🏠 घरगुती वाक्ये", "gharguti", "घरगुती वाक्ये")


# ============================================================
# 🏥 HOSPITAL SENTENCES
# ============================================================
elif st.session_state.page == "hospital_sentences":
    show_sentence_page("🏥 रुग्णालय वाक्ये", "hospital", "रुग्णालय वाक्ये")


# ============================================================
# 🛒 MARKET SENTENCES
# ============================================================
elif st.session_state.page == "market_sentences":
    show_sentence_page("🛒 बाजार वाक्ये", "market", "बाजार वाक्ये")


# ============================================================
# 🆘 HELP SENTENCES
# ============================================================
elif st.session_state.page == "help_sentences":
    show_sentence_page("🆘 मदत वाक्ये", "help", "मदत वाक्ये")