import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# 1. BRAIN (Optimized)
@st.cache_resource
def load_analyzer():
    nltk.download('vader_lexicon', quiet=True)
    return SentimentIntensityAnalyzer()

analyser = load_analyzer()

# 2. PAGE CONFIG (Full Width / No Sidebar)
st.set_page_config(page_title="VibeScan AI", page_icon="📡", layout="centered")

# Callback function to clear the input
def clear_scanner():
    st.session_state.vibe_input = ""

# 3. HEADER SECTION
with st.container():
    st.markdown("<h1 style='text-align: center;'>📡 VibeScan AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>VADER Lexicon v3.0 | Real-time Sentiment Decoder</p>", unsafe_allow_html=True)
    st.divider()

# 4. INPUT AREA
sentence = st.text_input("ENTER SIGNAL TRANSMISSION", placeholder="Type your thoughts here...", key="vibe_input")

if sentence:
    # CORE ENGINE
    sentiment = analyser.polarity_scores(sentence)
    compound = sentiment['compound']

    # SPECTRUM LOGIC
    if compound >= 0.8: mood, icon, bg = "MAXIMUM JOY 🚀", "🔥", "success"
    elif compound >= 0.4: mood, icon, bg = "RADIANT VIBES ✨", "☀️", "success"
    elif compound >= 0.1: mood, icon, bg = "SOFT OPTIMISM 🕊️", "🌤️", "info"
    elif compound > -0.1: mood, icon, bg = "OBJECTIVE DATA 🤖", "⚙️", "secondary"
    elif compound > -0.4: mood, icon, bg = "MILD TENSION ⚡", "☁️", "warning"
    elif compound > -0.8: mood, icon, bg = "DISTRESSED 🔥", "💥", "error"
    else: mood, icon, bg = "TOXIC TURBULENCE ☢️", "☣️", "error"

    # 5. THE RESULTS "CARD"
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center;'>{icon} {mood}</h2>", unsafe_allow_html=True)
        
        # Color-coded Status
        if bg == "success": st.success("Positive Frequency Detected")
        elif bg == "warning": st.warning("Potential Turbulence Detected")
        elif bg == "error": st.error("Critical Negative Interference")
        else: st.info("Stable Signal")

        # Visual Intensity Bar
        strength = (compound + 1) / 2
        st.progress(strength, text=f"Signal Intensity: {strength:.0%}")

        # METRICS DASHBOARD
        st.write("")
        c1, c2, c3 = st.columns(3)
        c1.metric("✅ Positive", f"{sentiment['pos']:.2%}")
        c2.metric("⚪ Neutral", f"{sentiment['neu']:.2%}")
        c3.metric("❌ Negative", f"{sentiment['neg']:.2%}")

    # 6. FOOTER ACTIONS
    st.write("")
    with st.expander("🔍 Deep Telemetry Data"):
        st.json(sentiment)

    # Replaced st.rerun() with an on_click callback
    st.button("🔄 Reset Scanner", use_container_width=True, on_click=clear_scanner)

else:
    # Empty state message
    st.info("Scanner idle. Please enter a text transmission above to begin.")

# 7. FINAL MINIMALIST FOOTER WITH LINK TO GITHUB
st.markdown("---")
st.markdown(
    """
    <style>
        .footer-text {
            display: flex; 
            justify-content: space-between; 
            color: #888888; 
            font-size: 12px; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding-bottom: 20px;
        }
        .footer-link {
            color: inherit !important; 
            text-decoration: underline !important; 
            font-weight: 500;
        }
        .footer-link:hover {
            color: #333333 !important;
        }
    </style>
    
    <div class="footer-text">
        <div>VibeScan v3.0</div>
        <div>
            Built by 
            <a href='https://github.com/AryaBuwa ' target='_blank' class='footer-link'>
                Arya
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)