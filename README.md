# MarketPulse 🧠 | Global Sentiment Terminal

**MarketPulse** is a real-time financial analytics dashboard designed to visualize the "emotional temperature" of the market. Unlike standard price charts, MarketPulse overlays a **Technical Sentiment Score** (0-100) onto historical price action, allowing investors to spot Overbought (Greed) and Oversold (Fear) zones instantly.

## 🚀 Key Features

- **🧠 The "Emotional Score":** A proprietary metric derived from 14-day RSI (Relative Strength Index) and Volatility smoothing.
    - **> 70 (Red):** Extreme Greed / Overbought Risk.
    - **< 30 (Green):** Extreme Fear / Buying Opportunity.
- **🌎 Multi-Market Support:** Dedicated engineered categories for:
    - **Brazil Market:** ADRs like Petrobras (PBR), Vale, Nubank.
    - **Commodities:** Gold, Silver, Oil, Copper (Clean names, technical tickers).
    - **Argentina CEDEARs:** Analysis of .BA tickers with FX awareness.
    - **Crypto & Big Tech:** BTC, ETH, NVDA, AAPL, etc.
- **🔍 Hybrid Search Engine:**
    - **Autofill Mode:** Browse curated categories.
    - **Manual Mode:** Type ANY ticker supported by Yahoo Finance (e.g., `EURUSD=X`, `^VIX`).
- **📊 Professional Visualization:** Interactive **Dual-Axis Plotly Charts** showing Price (Area) vs. Sentiment (Line) with dynamic color coding.
<img width="1794" height="787" alt="image" src="https://github.com/user-attachments/assets/53423b57-a862-4289-a321-d020bf27622a" />

## 🛠️ Technical Architecture

The project is built using a modular Python architecture:
- **Core Engine (`src/engine.py`):** Handles API requests via `yfinance`, calculates Technical Indicators (RSI, Volatility), and manages the Asset Universe dictionary.
- **Dashboard Interface (`src/dashboard.py`):** A responsive Streamlit application featuring dynamic filtering, metric cards, and advanced plotting logic.
- **Visualization:** Built with **Plotly Graph Objects** for high-precision financial charting (Dual Y-Axis).

## 📦 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/UlisesChustek/MarketPulse.git
   cd MarketPulse
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Terminal:**
   ```bash
   streamlit run src/dashboard.py
   ```

## 🧠 The Math Behind the Model

The **Emotional Score** is calculated using a smoothed Relative Strength Index logic:

1539 RSI = 100 - \frac{100}{1 + RS} 1539

Where $ is the average of upward price changes divided by the average of downward price changes over a 14-day window. The result is a normalized oscillator (0-100) that mathematically represents momentum.

---

*Developed by Ulises Chustek. Data Science Portfolio Project demonstrating Financial Engineering and Real-Time Data Visualization.*
