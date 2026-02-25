import yfinance as yf
import pandas as pd
import ta
import feedparser
import streamlit as st


@st.cache_data(ttl=300)  # שומר נתונים ל-5 דקות כדי למנוע עומס על יאהו
def get_stock_data(ticker, period="1y"):
    """
    פונקציה שמושכת נתוני מניה מהבורסה ומחשבת אינדיקטורים טכניים.
    אם יש שגיאה, היא מחזירה None במקום להקריס את האתר.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

        if df.empty or len(df) < 50:
            return None

        # --- חישוב אינדיקטורים של בתי השקעות ---

        # ממוצעים נעים קלאסיים
        df["SMA50"] = ta.trend.sma_indicator(df["Close"], window=50)
        df["SMA200"] = ta.trend.sma_indicator(df["Close"], window=200)

        # מומנטום (RSI)
        df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

        # רצועות בולינגר (Bollinger Bands) לזיהוי תנודתיות
        indicator_bb = ta.volatility.BollingerBands(
            close=df["Close"], window=20, window_dev=2
        )
        df["BB_High"] = indicator_bb.bollinger_hband()
        df["BB_Low"] = indicator_bb.bollinger_lband()

        return df
    except Exception:
        return None


@st.cache_data(ttl=600)
def get_market_news():
    """
    פונקציה בטוחה למשיכת חדשות שוק ההון בעברית מגוגל ניוז.
    """
    url = "https://news.google.com/rss/search?q=שוק+ההון+וול+סטריט+מניות&hl=he&gl=IL&ceid=IL:he"
    try:
        feed = feedparser.parse(url)
        news_list = []
        for entry in feed.entries[:8]:  # לוקח את 8 הכתבות האחרונות
            news_list.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published[:16],  # תאריך נקי
                    "source": entry.source.title if "source" in entry else "Google News",
                }
            )
        return news_list
    except Exception:
        return []


@st.cache_data(ttl=3600)
def get_us_universe(kind="all"):
    """
    מחזיר רשימת מניות לשוק האמריקאי.
    kind:
        - 'sp500' : רק S&P 500
        - 'nasdaq100' : מדד נאסד\"ק 100 (אם זמין)
        - 'all' : איחוד רשימות עיקריות
    """
    sp = []
    nq = []

    # ניסיון ראשון: סריקה מוויקיפדיה (עצמאי מ-yfinance)
    try:
        sp_table = pd.read_html(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        )[0]
        sp = [str(s).replace(".", "-") for s in sp_table["Symbol"].tolist()]
    except Exception:
        try:
            sp = yf.tickers_sp500()
        except Exception:
            sp = []

    try:
        nasdaq_tables = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")
        for t in nasdaq_tables:
            for col in ("Ticker", "Symbol"):
                if col in t.columns:
                    nq = [str(s).replace(".", "-") for s in t[col].tolist()]
                    break
            if nq:
                break
    except Exception:
        try:
            nq = yf.tickers_nasdaq()
        except Exception:
            nq = []

    if kind == "sp500":
        return sp or nq  # אם S&P ריק, ניפול לנאסד"ק
    if kind == "nasdaq100":
        return nq or sp  # ואם נאסד"ק ריק, ניפול ל-S&P

    # 'all' – איחוד עיקרי
    combined = list(set(sp + nq))
    combined.sort()

    # אם משום מה לא הצלחנו לקבל רשימות – חזרה לרשימת ברירת מחדל
    if not combined:
        combined = [
            "AAPL",
            "MSFT",
            "AMZN",
            "GOOGL",
            "META",
            "TSLA",
            "NVDA",
            "JPM",
            "BAC",
            "XOM",
        ]

    return combined


@st.cache_data(ttl=300)
def scan_us_market(universe_kind="all", limit=300, period="3mo"):
    """
    סורק את שוק המניות האמריקאי לפי יקום שנבחר ומחזיר טבלת סקירה.
    כדי לא להעמיס יתר על המידה, ניתן להגביל את מספר המניות הנסרקות (limit).
    """
    tickers = get_us_universe(universe_kind)
    if not tickers:
        # ביטחון נוסף
        tickers = [
            "AAPL",
            "MSFT",
            "AMZN",
            "GOOGL",
            "META",
            "TSLA",
            "NVDA",
            "JPM",
            "BAC",
            "XOM",
        ]

    if limit is not None:
        tickers = tickers[: limit]

    rows: list[dict] = []
    for symbol in tickers:
        df = get_stock_data(symbol, period=period)
        if df is None:
            continue

        try:
            curr = float(df["Close"].iloc[-1])
            prev = float(df["Close"].iloc[-2])
            change_pct = (curr - prev) / prev * 100.0
            rsi = float(df["RSI"].iloc[-1])
            above_200 = curr > float(df["SMA200"].iloc[-1])
        except Exception:
            continue

        rows.append(
            {
                "Ticker": symbol,
                "Last": curr,
                "Change_%": change_pct,
                "RSI": rsi,
                "Above_SMA200": above_200,
            }
        )

    if not rows:
        return pd.DataFrame()

    df_scan = pd.DataFrame(rows)
    df_scan = df_scan.sort_values("Change_%", ascending=False)
    return df_scan.reset_index(drop=True)
