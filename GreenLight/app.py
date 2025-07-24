import streamlit as st

def calculate_score(floors, lighting, hvac, solar, panels, building_type, area, appliances, green_roof, rainwater, ventilation, wall_insulation, green_area):
    score = 100
    score -= floors * 1.5
    lighting_scores = {"LED": 0, "CFL": 5, "Incandescent": 10, "Filament": 8}
    score -= lighting_scores.get(lighting, 10)

    if hvac == "Yes":
        score -= 20
    if solar == "Yes":
        score += 10 + (panels * 0.05)

    if building_type == "Industrial":
        score -= 10
    elif building_type == "Commercial":
        score -= 5

    if appliances > 20:
        score -= 5

    if green_roof == "Yes":
        score += 5
    if rainwater == "Yes":
        score += 5

    ventilation_scores = {"Always": 5, "Often": 2, "Rarely": -2, "Never": -5}
    score += ventilation_scores.get(ventilation, 0)

    insulation_scores = {"High": 5, "Medium": 2, "Low": -5}
    score += insulation_scores.get(wall_insulation, 0)

    green_ratio = min(green_area / area, 1.0)
    score += green_ratio * 10

    return max(0, min(score, 100))

def estimate_energy_emissions(floors, lighting, hvac, solar, panels, area, appliances, wall_insulation, green_area):
    base_energy = area * 20
    lighting_factors = {"LED": 0.8, "CFL": 1.0, "Incandescent": 1.3, "Filament": 1.2}
    hvac_factor = 1.2 if hvac == "Yes" else 1.0
    solar_reduction = 1 - (min(panels, 1000) * 0.001)
    appliance_energy = appliances * 300
    insulation_factor = {"High": 0.9, "Medium": 1.0, "Low": 1.1}.get(wall_insulation, 1.0)
    green_factor = 1.0 - min(green_area / area, 1.0) * 0.1

    energy = (base_energy * lighting_factors.get(lighting, 1.3) * hvac_factor + appliance_energy) * insulation_factor * green_factor * solar_reduction
    emissions = energy * 0.0007
    return round(energy, 2), round(emissions, 2)

st.set_page_config(page_title="GreenLight – Building Estimator", layout="centered")

st.markdown("""
<style>
body {
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(135deg, #e8f5e9, #81c784);
    color: #2e7d32;
    margin: 0;
    padding: 0;
}

.main {
    max-width: 900px;
    margin: 80px auto;
    background: #f2f2f2;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.main:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

h1 {
    font-size: 2.5rem;
    color: #69c227;
    text-align: center;
    border: solid black 2px;
    border-radius: 40px;
    background: #2f2f2f;
    margin-bottom: 20px;
    font-weight: bold;
}
h1::after {
    content: '';
    display: block;
    width: 50px;
    height: 4px;
    background: #66bb6a;
    margin: 10px auto 0;
    border-radius: 2px;
}

.stTextInput label {
    font-size: 1.2rem;
    color: #2e7d32;
    font-weight: bold;
    margin-bottom: 8px;
    display: inline-block;
}
.stTextInput input {
    padding: 12px;
    border-radius: 8px;
    border: 2px solid #a5d6a7;
    font-size: 1rem;
    color: #2e7d32;
    background: #f9fbe7;
    transition: border-color 0.3s ease;
}
.stTextInput input:focus {
    border-color: #388e3c;
    outline: none;
    box-shadow: 0 0 8px rgba(56, 142, 60, 0.3);
}

.stButton button {
    background: #66bb6a;
    color: white;
    font-size: 1rem;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    transition: background-color 0.3s ease, transform 0.2s ease;
    cursor: pointer;
    box-shadow: 0 5px 15px rgba(102, 187, 106, 0.3);
}
.stButton button:hover {
    background: #ffffff;
    transform: translateY(-3px);
}

.stSpinner > div {
    color: #388e3c;
    animation: spin 1s infinite linear;
}

.response-box {
    background: #f1f8e9;
    border-left: 4px solid #81c784;
    padding: 15px;
    border-radius: 8px;
    font-size: 1rem;
    line-height: 1.6;
    color: #2e7d32;
    margin-top: 20px;
}

.stInfo {
    background: #e8f5e9;
    color: #1b5e20;
    border-radius: 8px;
    padding: 15px;
    font-size: 0.9rem;
    margin-top: 10px;
}

.stWarning {
    background: #fffde7;
    color: #f57c00;
    border-radius: 8px;
    padding: 15px;
    font-size: 0.9rem;
    margin-top: 10px;
}

.stError {
    background: #ffcdd2;
    color: #c62828;
    border-radius: 8px;
    padding: 15px;
    font-size: 0.9rem;
    margin-top: 10px;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

.stApp {
    background-image: url('https://i.postimg.cc/KzpDVv8X/Untitled-design.png');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

html, body, [class*="css"] {
    background-color: rgba(0, 0, 0, 0.6);
    color: #f2f2f2;
    font-family: 'Helvetica Neue', sans-serif;
}

h1, h2, h3, h4 {
    color: white;
}

.stMarkdown a {
    color: #90ee90;
}

.st-emotion-cache-8fjoqp {
    background-color: black;
    border-radius: 50px;
    padding: 20px;
    max-width: 700px;
    width: 90%;
    margin: 0 auto;
    min-height: 800px;
    height: auto !important;
    overflow: hidden;
}

/* Bottom Button Styling */
.bottom-btn {
    display: block;
    width: fit-content;
    margin: 30px auto 10px;
    padding: 12px 24px;
    background-color: #66bb6a;
    color: white;
    font-weight: bold;
    font-size: 1rem;
    text-align: center;
    text-decoration: none;
    border-radius: 10px;
    transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
    box-shadow: 0 5px 15px rgba(102, 187, 106, 0.3);
}

.bottom-btn:hover {
    background-color: #ffffff;
    color: #388e3c;
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(102, 187, 106, 0.4);
}
</style>
""", unsafe_allow_html=True)

st.title("GreenSnap – Building Energy Estimator")
st.markdown("<h4 style='text-align: center;'>Estimate your building's energy consumption, emissions, and sustainability score.</h4>", unsafe_allow_html=True)

building_type = st.selectbox("🏠 What type of building is it?", ["Residential", "Commercial", "Industrial", "Educational", "Hospital"])
area = st.number_input("📐 Total floor area (in m²)", min_value=10, max_value=100000, step=10)
floors = st.number_input("🏢 Number of floors", min_value=1, max_value=1000)
lighting = st.selectbox("🔦 What kind of lighting type does your building have?", ["LED", "CFL", "Incandescent", "Filament"])
hvac = st.radio("❄️ Is HVAC (Heating, ventilation, and air conditioning) installed?", ["Yes", "No"])
solar = st.radio("☀️ Solar Panels Installed?", ["Yes", "No"])
panels = st.number_input("🔋 Number of Solar Panels", min_value=0, max_value=1000, step=1, value=0)
appliances = st.number_input("⚙️ Approximate number of heavy electrical appliances", min_value=0, max_value=1000)
green_area = st.number_input("🌿 How much area (in m²) is covered by greenery?", min_value=0, max_value=100000, step=10)
green_roof = st.radio("🏡 Is there a green roof or rooftop garden?", ["Yes", "No"])
rainwater = st.radio("💧 Is rainwater harvesting implemented?", ["Yes", "No"])
ventilation = st.selectbox("🌬️ How often do you use natural ventilation?", ["Always", "Often", "Rarely", "Never"])
wall_insulation = st.selectbox("🧱 Wall Insulation Quality", ["High", "Medium", "Low"])

if st.button("Calculate"):
    score = calculate_score(floors, lighting, hvac, solar, panels, building_type, area, appliances, green_roof, rainwater, ventilation, wall_insulation, green_area)
    energy, emissions = estimate_energy_emissions(floors, lighting, hvac, solar, panels, area, appliances, wall_insulation, green_area)

    st.markdown("### Results", unsafe_allow_html=True)
    st.write(f"Estimated Annual Energy Usage: **{energy} kWh**")
    st.write(f"Estimated Annual CO₂ Emissions: **{emissions} tons**")
    st.write(f"Sustainability Score: **{score}/100**")
    st.progress(score / 100)

    if score >= 80:
        st.success("Excellent! Your building is highly sustainable.")
    elif score >= 50:
        st.info("Good! Some improvements can boost your sustainability.")
    else:
        st.warning("Consider optimizing energy usage and adopting greener practices.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Made with ❤️ for Code Green Challenge by Anshuman Verma | SDG 7 & SDG 13")

# ✅ Bottom Button
st.markdown("""
                <a href="https://greenpillar.pythonanywhere.com" class="bottom-btn">Back to home </a>
            """, unsafe_allow_html=True)
