import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# 1. Analytical Engine
@st.cache_resource
def load_analyzer():
    # Explicitly download the lexicon before initializing the analyzer
    nltk.download('vader_lexicon', quiet=True)
    return SentimentIntensityAnalyzer()

analyzer = load_analyzer()
# 2. Page Configuration
st.set_page_config(page_title="Sentiment Analysis Tool", page_icon="📊", layout="centered")

# Consolidated CSS and HTML Banner
st.markdown("""
    <style>
        .banner { background:#f0f2f6; color:#31333F; padding:10px; text-align:center; border-radius:5px; border:1px solid #d1d5db; margin-bottom:25px; font-size:14px; font-weight:500; }
        .footer { display:flex; justify-content:space-between; color:#888; font-size:12px; margin-top:50px; }
        .lnk { color:#007BFF !important; text-decoration:underline !important; font-weight:500; }
    </style>
    <div class="banner">ℹ️ Planned update: LLM integration for advanced contextual reasoning is in development.</div>
    """, unsafe_allow_html=True)

# Callback function to reset the interface
def reset_interface():
    st.session_state.text_input = ""

# 3. Header Section
with st.container():
    st.markdown("<h1 style='text-align: center;'>Sentiment Analysis Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>VADER Lexicon v3.0 | Quantitative Linguistic Evaluation Using NLTK</p>", unsafe_allow_html=True)
    st.divider()

# 4. Input Interface
sentence = st.text_input("Text input for evaluation", placeholder="Enter the text you wish to analyze...", key="text_input")

if sentence:
    # Core Processing
    sentiment = analyzer.polarity_scores(sentence)
    compound = sentiment['compound']

    # Professional Classification Logic
    if compound >= 0.8: mood, icon, bg = "Highly positive", "📈", "success"
    elif compound >= 0.4: mood, icon, bg = "Positive", "✅", "success"
    elif compound >= 0.1: mood, icon, bg = "Slightly positive", "🔍", "info"
    elif compound > -0.1: mood, icon, bg = "Neutral", "⚖️", "secondary"
    elif compound > -0.4: mood, icon, bg = "Slightly negative", "📉", "warning"
    elif compound > -0.8: mood, icon, bg = "Negative", "⚠️", "error"
    else: mood, icon, bg = "Highly negative", "🚫", "error"

    # 5. Analysis Report
    with st.container(border=True):
        st.markdown(f"<h3 style='text-align: center;'>{icon} Result: {mood}</h3>", unsafe_allow_html=True)
        
        # Professional Status Indicators
        if bg == "success": st.success("The analyzed text contains constructive or positive sentiment.")
        elif bg == "warning": st.warning("The analyzed text contains elements of concern or minor negativity.")
        elif bg == "error": st.error("The analyzed text contains significant negative sentiment.")
        else: st.info("The analyzed text is balanced and objective.")

        # Progress Bar
        intensity = (compound + 1) / 2
        st.progress(intensity, text=f"Calculated sentiment score: {intensity:.0%}")

        # Metrics Dashboard
        st.write("")
        c1, c2, c3 = st.columns(3)
        c1.metric("Positive score", f"{sentiment['pos']:.2%}")
        c2.metric("Neutral score", f"{sentiment['neu']:.2%}")
        c3.metric("Negative score", f"{sentiment['neg']:.2%}")

    # 7. Supplementary Data
    st.write("")
    with st.expander("View raw data metrics"):
        st.json(sentiment)

    st.button("Reset analysis", use_container_width=True, on_click=reset_interface)

else:
    # Initial state
    st.info("Please enter text in the field above to generate a sentiment report.")

# 8. Footer
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

