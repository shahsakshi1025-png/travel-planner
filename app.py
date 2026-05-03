import streamlit as st
import base64
from agents import TravelCoordinator

st.set_page_config(layout="wide")

# ---------------- BACKGROUND IMAGE ----------------

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 👉 change filename if needed
bg_image = get_base64("background.jpeg")

# ---------------- CSS ----------------

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

/* Dark overlay */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
}}

/* Ensure content is visible */
.main {{
    position: relative;
    z-index: 1;
}}

/* Hero */
.hero {{
    text-align: center;
    padding: 60px;
}}

.hero h1 {{
    font-size: 60px;
    font-weight: bold;
    color: white;
}}

/* Section titles */
.section-title {{
    font-size: 30px;
    margin-top: 40px;
    color: white;
}}

/* Cards */
.card {{
    background-color: rgba(0,0,0,0.6);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
}}

/* Button */
div.stButton > button {{
    background-color: #ffcc00;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------

st.markdown("""
<div class="hero">
    <h1>🌍 Get Ready For Your Dream Journey</h1>
    <p>Plan your perfect trip with AI-powered multi-agent system</p>
</div>
""", unsafe_allow_html=True)

# ---------------- OVERVIEW ----------------

st.markdown('<div class="section-title">📌 Overview</div>', unsafe_allow_html=True)

st.write("""
This platform helps you plan your entire trip using AI.
Flights, hotels, activities, and budget are handled by different agents.
""")

# ---------------- DESTINATIONS ----------------

st.markdown('<div class="section-title">✨ Explore Destinations</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">🏝 Goa<br>Beaches & Nightlife</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">🏔 Manali<br>Mountains & Snow</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">🏙 Dubai<br>Luxury & Shopping</div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------

st.markdown('<div class="section-title">🧾 Plan Your Trip</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    city = st.text_input("Destination")

with col2:
    budget = st.number_input("Budget (INR)", min_value=1000)

with col3:
    days = st.slider("Days", 1, 10)

# ---------------- BUTTON ----------------

generate = st.button("✨ Generate Plan")

planner = TravelCoordinator()

# ---------------- RESULTS ----------------

# ---------------- RESULTS ----------------
if generate:
    if city == "":
        st.warning("Enter destination")
    else:
        with st.spinner("AI agents are planning your trip..."):
            result = planner.execute(city, budget, days)

        if any(isinstance(value, str) and value.startswith(("API", "HTTP", "Unexpected", "Error")) for value in result.values()):
            st.error("AI request failed. Check your API token or model.")
            st.write(result)
        else:
            st.markdown('<div class="section-title">✈️ Your Travel Plan</div>', unsafe_allow_html=True)

            # 🔹 ROW 1 → Flights & Hotels side by side
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✈️ Flights")
                st.markdown(result["flights"])

            with col2:
                st.markdown("### 🏨 Hotels")
                st.markdown(result["hotels"])

            # 🔹 ROW 2 → Full width Itinerary
            st.markdown("### 📍 Itinerary")
            st.markdown(result["activities"])

            # 🔹 ROW 3 → Full width Final Budget
            st.markdown("### 💰 Final Budget Plan")
            st.markdown(result["final"])