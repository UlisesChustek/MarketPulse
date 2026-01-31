import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from engine import MarketEngine

st.set_page_config(page_title="MarketPulse | Terminal", layout="wide")
st.title("🧠 MarketPulse: Global Sentiment Terminal")

# --- 1. The Flexible Asset Selector ---
universe = MarketEngine.get_asset_universe()

# Create a flattened "All Assets" dictionary for the global autofill
all_assets = {}
for category, assets in universe.items():
    for name, ticker in assets.items():
        # We add the category to the name for better context in the global search
        # e.g., "Petrobras (Brazil Market)"
        all_assets[f"{name} ({category.split()[1]})"] = ticker

# Define the menu options
menu_options = ["🌐 Search All (Autofill)", "✍️ Manual Ticker Entry"] + sorted(list(universe.keys()))

col1, col2 = st.columns([1, 2])

with col1:
    selected_category = st.selectbox("📂 Market Filter", menu_options)

# Variables to hold selection
selected_ticker = None
selected_asset_name = None

with col2:
    if selected_category == "🌐 Search All (Autofill)":
        # MODE 1: Global Dropdown with Autofill
        selected_asset_name = st.selectbox("🔍 Search Global Universe", sorted(all_assets.keys()))
        selected_ticker = all_assets[selected_asset_name]
        
    elif selected_category == "✍️ Manual Ticker Entry":
        # MODE 2: Free Text Input
        user_input = st.text_input("⌨️ Enter Ticker Symbol", value="EURUSD=X", help="E.g., PBR, BTC-USD, GC=F").upper()
        selected_ticker = user_input.strip()
        selected_asset_name = f"{selected_ticker} (Manual)"
        
    else:
        # MODE 3: Category Filter
        category_assets = universe[selected_category]
        selected_asset_name = st.selectbox("📍 Select Asset", sorted(category_assets.keys()))
        selected_ticker = category_assets[selected_asset_name]

# --- 2. Execution & Visualization ---
if selected_ticker:
    engine = MarketEngine(selected_ticker)
    df = engine.get_historical_data(period="1y")

    if not df.empty:
        latest_price = df['Close'].iloc[-1]
        latest_emotion = df['Emotional_Score'].iloc[-1]
        
        # Determine currency/unit
        currency = "ARS" if ".BA" in selected_ticker else "USD"
        
        # Header Stats
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Price ({currency})", f"${latest_price:,.2f}")
        c2.metric("Sentiment Score (RSI)", f"{latest_emotion:.1f}")
        
        # Mood Logic
        if latest_emotion > 70:
            status = "🔥 Extreme Greed (Risk)"
            color = "#FF4B4B" # Red
        elif latest_emotion < 30:
            status = "❄️ Extreme Fear (Opp)"
            color = "#00CC96" # Green
        else:
            status = "😐 Neutral Zone"
            color = "#FFAA00" # Yellow
            
        c3.markdown(f"### <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)

        # --- 3. The Pro Chart ---
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Background: Price
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['Close'], name=f"Price ({currency})",
                fill='tozeroy',
                line=dict(color='rgba(255, 255, 255, 0.1)', width=1),
                fillcolor='rgba(255, 255, 255, 0.05)'
            ),
            secondary_y=False
        )

        # Foreground: Sentiment
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['Emotional_Score'], name="Sentiment",
                line=dict(color=color, width=3) # Line color matches the mood
            ),
            secondary_y=True
        )

        # Reference Zones
        fig.add_hrect(y0=70, y1=100, fillcolor="red", opacity=0.1, secondary_y=True)
        fig.add_hrect(y0=0, y1=30, fillcolor="green", opacity=0.1, secondary_y=True)

        fig.update_layout(
            title=f"Sentiment Analysis: {selected_asset_name}",
            template="plotly_dark",
            height=550,
            hovermode="x unified",
            legend=dict(orientation="h", y=1.1)
        )
        
        fig.update_yaxes(showgrid=False, secondary_y=False) 
        fig.update_yaxes(range=[0, 100], showgrid=True, gridcolor='rgba(128,128,128,0.2)', secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Data unavailable for '{selected_ticker}'. Market might be closed or ticker invalid.")