import streamlit as st
from ai_client import AIClient
from planner import validate_inputs, build_prompt

st.set_page_config(page_title="Student AI Travel Planner", layout="wide")

WELCOME_BG = "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=1500&q=80"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{WELCOME_BG}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    .welcome-card {{
        background: rgba(8, 44, 68, 0.75);
        border-radius: 30px;
        padding: 2.2rem 2rem 1.6rem 2rem;
        max-width: 530px;
        margin: 60px auto 0 auto;
        box-shadow: 0 8px 36px rgba(18,40,110,0.30);
        text-align: center;
    }}
    .welcome-title {{
        font-size: 2.7rem;
        color: #fbfbf4;
        font-weight: 900;
        letter-spacing: .12em;
        margin-bottom: 1.1em;
        text-shadow: 2px 2px 24px #0e2539b7;
    }}
    .welcome-desc {{
        color: #dbeaf7;
        font-size: 1.14rem;
        margin-bottom: 1.7em;
        text-shadow: 0 1px 9px #1d2d48;
    }}
    .stButton>button {{
        background: rgba(255,255,255,0.25);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        color: #063451 !important;
        font-size: 1.2rem;
        font-weight: 800;
        border-radius: 16px;
        padding: 0.97rem 2.5rem;
        box-shadow: 0 8px 40px rgba(71,219,240,0.16), 0 1.5px 12px rgba(100,120,200,0.10);
        border: 1.5px solid rgba(200,220,255,0.30);
        letter-spacing: 0.06em;
        transition: background .19s, color .19s, box-shadow 0.13s;
        outline: none;
    }}
    .stButton>button:hover {{
        background: rgba(255,255,255,0.39);
        box-shadow: 0 12px 30px rgba(44,200,240,0.22), 0 4px 18px rgba(255,255,255,0.13);
        color: #156c97 !important;
        border: 1.8px solid rgba(115,210,255,0.38);
    }}
    .glass-card {{
        background: rgba(8, 44, 68, 0.92);
        border-radius: 24px;
        box-shadow: 0 6px 30px rgba(57, 80, 200, 0.13);
        border: 2px solid rgba(255,255,255,0.15);
        max-width: 480px;
        margin: 32px auto 0 auto;
        padding: 1.1rem 1.3rem 0.9rem 1.3rem;
        text-align: left;
        color: white;
    }}
    .main-title {{
        color: white;
        font-size: 2.08rem;
        font-weight: 900;
        letter-spacing: 0.10em;
        text-align: center;
        margin-bottom: 1em;
        text-shadow: 0 1px 8px #142a4baa;
    }}
    .destinations-section {{
        background: rgba(255, 255, 255, 0.11);
        border-radius: 20px;
        padding: 8px 18px 7px 18px;
        margin-bottom: 12px;
        margin-top: 3px;
        box-shadow: 0 3px 16px rgba(255,255,255,0.17);
        text-align: center;
        font-weight: 900;
        letter-spacing: 0.09em;
        font-size: 1.15rem;
        color: #fff;
        border: 1px solid rgba(255,255,255,0.28);
    }}
    label {{
        color: #fff !important;
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        letter-spacing: 0.06em;
        margin-bottom: 5px !important;
        margin-top: 8px !important;
        display: block;
    }}
    .stTextInput>div>input, .stNumberInput>div>input, .stSelectbox>div>div, .stDateInput>div>input {{
        background: rgba(255,255,255,0.93) !important;
        border-radius: 7px !important;
        font-size: 1.06rem;
        border: 1px solid #4ebde7 !important;
        margin-bottom: 4px !important;
        color: #1a1a23 !important;
        text-align: left;
    }}
    </style>
""", unsafe_allow_html=True)

if "has_started" not in st.session_state:
    st.session_state.has_started = False

if not st.session_state.has_started:
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-title">🌏 Welcome to Student AI Travel Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-desc">Dream. Plan. Explore.<br>Let our AI craft your journey in seconds.<br>Click below to get started!</div>', unsafe_allow_html=True)
    if st.button("Start Planning Your Trip 🚀"):
        st.session_state.has_started = True
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="main-title">🎒 Student AI Travel Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="destinations-section">Explore Popular Destinations</div>', unsafe_allow_html=True)
    with st.form("planner_form"):
        destination = st.text_input("Destination", placeholder="e.g., Ooty, Goa, Jaipur")
        start_date = st.date_input("Start date (optional)", value=None)
        duration_days = st.number_input("Duration (days)", min_value=1, max_value=14, value=3)
        budget_level = st.selectbox("Budget level", ["tight", "moderate", "flexible"])
        transport = st.selectbox("Preferred transport", ["bus/train", "shared cab", "flight"])
        stay_type = st.selectbox("Preferred stay", ["hostel", "homestay", "budget hotel"])
        interests = st.text_input("Interests (Including-comma)", placeholder="nature, food, culture, hiking")
        submitted = st.form_submit_button("Generate Itinerary")
    if submitted:
        ok, msg, normalized = validate_inputs({
            "destination": destination,
            "start_date": str(start_date) if start_date else "",
            "duration_days": int(duration_days),
            "budget_level": budget_level,
            "interests": interests,
            "transport": transport,
            "stay_type": stay_type,
            "currency": "INR",
        })
        if not ok:
            st.error(msg)
        else:
            st.info("Preparing your custom itinerary, please wait...")
            client = AIClient()
            prompt = build_prompt(normalized)
            result = client.generate_itinerary(prompt)
            st.markdown("### Your Travel Itinerary")
            st.markdown(
                f'<div style="color:#fff; font-size:1.17rem; font-weight:600; white-space:pre-line;">{result}</div>',
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)
