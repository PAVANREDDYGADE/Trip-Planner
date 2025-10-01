import streamlit as st
from ai_client import AIClient
from planner import validate_inputs, build_prompt

# Step 1: Set page title and favicon icon.
# Place your favicon.ico file in the app folder.
st.set_page_config(
    page_title="Student AI Travel Planner",
    page_icon="favicon.ico",
    layout="wide"
)

# Main app title
st.title("🎒 Student AI Travel Planner")

# Input form for trip details
with st.form("planner_form"):
    destination = st.text_input("Destination", placeholder="e.g., Ooty, Goa, Jaipur")
    start_date = st.date_input("Start date (optional)", value=None)
    duration_days = st.number_input("Duration (days)", min_value=1, max_value=14, value=3)
    budget_level = st.selectbox("Budget level", ["tight", "moderate", "flexible"])
    transport = st.selectbox("Preferred transport", ["bus/train", "shared cab", "flight"])
    stay_type = st.selectbox("Preferred stay", ["hostel", "homestay", "budget hotel"])
    interests = st.text_input("Interests (comma-separated)", placeholder="nature, food, culture, hiking")
    submitted = st.form_submit_button("Generate Itinerary")

# Handle submission
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
        with st.spinner("Generating itinerary, please wait..."):
            st.write("Sending prompt to AI...")
            client = AIClient()
            prompt = build_prompt(normalized)
            result = client.generate_itinerary(prompt)
            st.write("Received response from AI.")
        st.markdown("### Itinerary")
        st.text(result)

# Step 2: Inform users about sharing app URL
st.markdown("""
---
### Share this app
Send this link to your friends so they can use the trip planner:

`https://your-app-name.streamlit.app`
""")
