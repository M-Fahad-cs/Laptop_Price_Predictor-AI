import streamlit as st
import pickle
import numpy as np
import pandas as pd

# --- 1. PAGE CONFIGURATION (Must be the very first Streamlit command) ---
st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="wide")

# --- 2. ADVANCED CSS & MOVING BACKGROUND ---
# This fixes the white-on-white text issue and adds smooth animations!
st.markdown("""
<style>
/* 1. Background Animation */
@keyframes pan {
    0% { background-position: 0% 0%; background-size: 100%; }
    50% { background-position: 50% 50%; background-size: 105%; }
    100% { background-position: 0% 0%; background-size: 100%; }
}

/* 2. Fade In Animation for the main container */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 3. Pulse Animation for the Predict Button */
@keyframes pulse {
    0% { box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4); }
    50% { box-shadow: 0 4px 25px rgba(255, 75, 75, 0.8); }
    100% { box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4); }
}

/* Apply background to the main Streamlit app */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=2071&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    animation: pan 40s infinite alternate ease-in-out;
}

/* Glassmorphism effect for the main container with fade-in animation */
.block-container {
    background: rgba(15, 23, 42, 0.75); 
    backdrop-filter: blur(12px); 
    -webkit-backdrop-filter: blur(12px);
    padding: 3rem 4rem !important;
    border-radius: 20px;
    margin-top: 3rem;
    margin-bottom: 3rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    animation: fadeIn 1.2s ease-out; /* Added fade-in animation here! */
}

/* Force text labels to be white */
h1, h2, h3, p, label, .stMarkdown {
    color: #f8fafc !important;
}

/* --- THE FIX: Make Inputs Dark with White Text --- */
/* Fix Selectboxes */
div[data-baseweb="select"] > div {
    background-color: #1e293b !important; /* Solid dark blue/gray */
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
}
div[data-baseweb="select"] span {
    color: white !important;
}

/* AGGRESSIVE FIX for Number Inputs (Weight & Screen Size) */
.stNumberInput input {
    color: white !important;
    -webkit-text-fill-color: white !important;
    background-color: #1e293b !important;
}
.stNumberInput div[data-baseweb="input"] {
    background-color: #1e293b !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}
.stNumberInput div[data-baseweb="base-input"] {
    background-color: #1e293b !important;
}

/* The Giant Gradient Predict Button */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #10b981, #059669); /* Changed to Money Green! */
    color: white;
    height: 3.5em;
    width: 100%;
    border-radius: 12px;
    font-size: 22px;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease-in-out;
    animation: pulse 2s infinite; 
}
div.stButton > button:hover {
    transform: scale(1.02);
}

/* Custom CSS for Money Rain Animation */
.money-emoji {
    position: fixed;
    top: -10vh;
    font-size: 3.5rem;
    z-index: 9999;
    animation: fall linear forwards;
}
@keyframes fall {
    100% { top: 110vh; transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# --- 3. COLORFUL HEADER ---
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);'>💻 Smart AI Laptop Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 2rem;'>Select your desired configurations below to get an instant AI-powered estimate!</p>", unsafe_allow_html=True)

# --- 4. LOAD THE AI BRAIN ---
pipe = pickle.load(open('pipe.pkl', 'rb'))
df = pickle.load(open('df.pkl', 'rb'))

# --- 5. ORGANIZE INPUTS INTO A 3-COLUMN GRID ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🛠️ Brand & Build")
    Company = st.selectbox('Brand', df['Company'].unique())
    Type = st.selectbox('Type', df['TypeName'].unique())
    Weight = st.number_input('Weight of the Laptop (kg)', value=1.5)
    OS = st.selectbox('Operating System', df['os'].unique())

with col2:
    st.subheader("🖥️ Display Specs")
    Screen_Size = st.number_input('Screen Size (in Inches)', value=15.6)
    Resolution = st.selectbox('Screen Resolution', ['1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800', '2880x1800', '2560x1600', '2560x1440', '2304x1440'])
    Touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
    IPS = st.selectbox('IPS Display', ['No', 'Yes'])

with col3:
    st.subheader("⚙️ Internal Hardware")
    Cpu = st.selectbox('CPU Brand', df['Cpu Brand'].unique())
    Ram = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
    Gpu = st.selectbox('GPU Brand', df['Gpu brand'].unique())
    HHD = st.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])
    SSD = st.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])

# --- 6. THE PREDICTION BUTTON ---
st.markdown("<br><br>", unsafe_allow_html=True) 

if st.button('🚀 Predict Price'):
    # Convert Yes/No to 1/0
    if Touchscreen == 'Yes':
        Touchscreen = 1
    else:
        Touchscreen = 0
        
    if IPS == 'Yes':
        IPS = 1
    else:
        IPS = 0
        
    # Calculate PPI
    x_res = int(Resolution.split('x')[0])
    y_res = int(Resolution.split('x')[1])
    ppi = ((x_res**2) + (y_res**2))**0.5 / Screen_Size
    
    # Create the DataFrame with the exact column names the AI expects!
    query_df = pd.DataFrame({
        'Company': [Company],
        'TypeName': [Type],
        'Ram': [Ram],
        'Weight': [Weight],
        'Touchscreen': [Touchscreen],
        'IPS': [IPS],        
        'ppi': [ppi],
        'Cpu Brand': [Cpu],
        'HHD': [HHD],        # STRICTLY HHD to match your AI model
        'SSD': [SSD],
        'Gpu brand': [Gpu],
        'os': [OS]
    })
    
    # Calculate Math
    predicted_price_euro = int(np.exp(pipe.predict(query_df)[0]))
    predicted_price_pkr = predicted_price_euro * 205
    
    # Format with commas (e.g., 250,000)
    formatted_pkr = "{:,}".format(predicted_price_pkr)
    
    # --- 7. STYLISH RESULT OUTPUT WITH MONEY RAIN ---
    # This custom HTML triggers the money falling animation
    money_rain_html = """
    <div class="money-emoji" style="left: 10%; animation-duration: 2s; animation-delay: 0s;">💸</div>
    <div class="money-emoji" style="left: 20%; animation-duration: 3s; animation-delay: 0.2s;">💵</div>
    <div class="money-emoji" style="left: 35%; animation-duration: 2.5s; animation-delay: 0.5s;">💰</div>
    <div class="money-emoji" style="left: 50%; animation-duration: 4s; animation-delay: 0.1s;">💸</div>
    <div class="money-emoji" style="left: 65%; animation-duration: 2.8s; animation-delay: 0.4s;">💵</div>
    <div class="money-emoji" style="left: 80%; animation-duration: 3.5s; animation-delay: 0.3s;">💰</div>
    <div class="money-emoji" style="left: 90%; animation-duration: 2.2s; animation-delay: 0.6s;">💸</div>
    """
    st.markdown(money_rain_html, unsafe_allow_html=True)
    
    st.success(f"### 💸 The predicted price of this LAPTOP is **Rs {formatted_pkr}**")