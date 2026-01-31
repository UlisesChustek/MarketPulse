import yfinance as yf
import pandas as pd
import numpy as np

class MarketEngine:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_historical_data(self, period="2y"):
        try:
            # Fetch data with auto-adjust
            df = yf.Ticker(self.ticker).history(period=period, auto_adjust=True)
            
            if df.empty:
                return pd.DataFrame()

            # --- Technical Indicators ---
            # 1. RSI (Relative Strength Index)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            # 2. Emotional Score (Smoothed RSI)
            df['Emotional_Score'] = df['RSI'].rolling(window=3).mean()
            
            return df.dropna()
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_asset_universe():
        """
        Returns a categorized dictionary mapping Human-Readable Names to Tickers.
        Includes Brazil, Crypto, Metals, and more.
        """
        return {
            "🇧🇷 Brazil Market (ADRs)": {
                "Petrobras": "PBR",
                "Vale S.A.": "VALE",
                "Itau Unibanco": "ITUB",
                "Bradesco": "BBD",
                "Ambev": "ABEV",
                "Embraer": "ERJ",
                "Nu Holdings (Nubank)": "NU",
                "Gerdau": "GGB"
            },
            "🛢️ Commodities & Metals": {
                "Gold (Ounce)": "GC=F",
                "Silver (Ounce)": "SI=F",
                "Crude Oil (WTI)": "CL=F",
                "Copper": "HG=F",
                "Natural Gas": "NG=F",
                "Corn": "ZC=F"
            },
            "🚀 Crypto": {
                "Bitcoin": "BTC-USD",
                "Ethereum": "ETH-USD",
                "Solana": "SOL-USD",
                "Binance Coin": "BNB-USD",
                "Ripple (XRP)": "XRP-USD"
            },
            "🇦🇷 CEDEARs (Argentina)": {
                "Apple (CEDEAR)": "AAPL.BA",
                "Mercado Libre": "MELI.BA",
                "Tesla (CEDEAR)": "TSLA.BA",
                "Coca-Cola": "KO.BA",
                "SPY (S&P 500)": "SPY.BA",
                "Vista Oil": "VIST.BA"
            },
            "🏢 US Big Tech": {
                "Apple": "AAPL",
                "Nvidia": "NVDA",
                "Tesla": "TSLA",
                "Microsoft": "MSFT",
                "Meta": "META",
                "Google": "GOOGL",
                "Amazon": "AMZN"
            },
            "🌎 Global ETFs": {
                "S&P 500": "SPY",
                "Nasdaq 100": "QQQ",
                "China Large-Cap": "FXI",
                "Emerging Markets": "EEM"
            }
        }