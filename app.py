import streamlit as st
import plotly.graph_objects as go
import data_engine as de  # מנוע הנתונים שלנו

# --- PAGE CONFIG (wide, institutional layout) ---
st.set_page_config(
    page_title="ProTrade מתקדם",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded",
)

# --- GLOBAL STYLING: Futuristic glassmorphism fintech theme ---
st.markdown(
    """
<style>
/* Global app background & typography */
.stApp {
    background:
      radial-gradient(circle at top left, rgba(56,189,248,0.14) 0, transparent 45%),
      radial-gradient(circle at bottom right, rgba(168,85,247,0.16) 0, transparent 50%),
      radial-gradient(circle at top right, #050816 0, #02030a 55%, #01010a 100%);
    color: #e5e7eb;
    font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent;
    border-bottom: none;
}

/* Remove default padding and stretch content edge-to-edge */
main .block-container {
    padding-top: 0.6rem;
    padding-bottom: 0.6rem;
    padding-left: 0.6rem;
    padding-right: 0.6rem;
    max-width: 100%;
}

/* Top page title styling */
.protrade-title h1 {
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-size: 1.4rem;
}
.protrade-subtitle {
    color: #9aa4c1;
    font-size: 0.85rem;
}

/* Sidebar: minimalist glass navigation rail */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15,23,42,0.9) 0%, rgba(15,23,42,0.8) 100%);
    border-right: 1px solid rgba(31,41,55,0.9);
    backdrop-filter: blur(22px) saturate(170%);
    -webkit-backdrop-filter: blur(22px) saturate(170%);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem;
}
.sidebar-header {
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #e6edf7;
}
.sidebar-badge {
    font-size: 0.68rem;
    color: #9ca3af;
}

/* Navigation radio - make it feel like a terminal menu */
div[data-testid="stRadio"] > label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9ca3af;
}
div[data-testid="stRadio"] > div {
    background: rgba(15,23,42,0.6);
    border-radius: 999px;
    border: 1px solid rgba(31,41,55,0.9);
    padding: 0.25rem;
}
div[data-testid="stRadio"] input:checked + div {
    background: radial-gradient(circle at 0 0, rgba(56,189,248,0.35), transparent 55%);
    border-image: linear-gradient(90deg, #38bdf8, #a855f7) 1;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: radial-gradient(circle at top left, rgba(56,189,248,0.21), rgba(15,23,42,0.8));
    border-radius: 18px;
    padding: 16px 18px;
    border: 1px solid rgba(148,163,184,0.6);
    box-shadow:
      0 24px 80px rgba(15,23,42,0.95),
      0 0 0 1px rgba(15,23,42,0.8);
    backdrop-filter: blur(22px) saturate(170%);
    -webkit-backdrop-filter: blur(22px) saturate(170%);
}
div[data-testid="metric-container"] > label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #cbd5f5;
}

/* Tabs styling */
button[data-baseweb="tab"] {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding-top: 0.4rem;
    padding-bottom: 0.4rem;
    color: #9ca3af;
    border-radius: 999px 999px 0 0;
    background: transparent;
}
button[data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 2px solid transparent;
    background: radial-gradient(circle at 0 0, rgba(56,189,248,0.32), rgba(88,28,135,0.55));
    color: #f9fafb;
}

/* Plotly charts: glassmorphism card */
div[data-testid="stPlotlyChart"] {
    border-radius: 22px;
    border: 1px solid rgba(148,163,184,0.75);
    box-shadow:
      0 32px 120px rgba(15,23,42,0.98),
      0 0 0 1px rgba(15,23,42,0.8);
    background: radial-gradient(circle at top left, rgba(59,130,246,0.16), rgba(15,23,42,0.9));
    padding: 6px 6px 0 6px;
    backdrop-filter: blur(24px) saturate(200%);
    -webkit-backdrop-filter: blur(24px) saturate(200%);
}

/* News cards */
.news-card {
    background: radial-gradient(circle at top left, rgba(59,130,246,0.16), rgba(15,23,42,0.85));
    border: 1px solid rgba(148,163,184,0.75);
    padding: 13px 14px;
    margin-bottom: 10px;
    border-radius: 16px;
    border-left: 3px solid #38bdf8;
    transition: transform 0.16s ease-out, border-color 0.16s ease-out, box-shadow 0.16s ease-out;
}
.news-card:hover {
    transform: translateX(4px) translateY(-1px);
    border-color: #a855f7;
    box-shadow: 0 18px 55px rgba(15,23,42,0.95);
}
.news-title {
    color: #bfdbfe;
    font-weight: 500;
    text-decoration: none;
    font-size: 0.92rem;
}
.news-title:hover { color: #bfdbfe; }

/* Primary buttons */
.stButton>button {
    background: linear-gradient(120deg, #38bdf8, #a855f7);
    color: #f9fafb;
    border: none;
    font-weight: 600;
    border-radius: 999px;
    padding: 0.4rem 0.9rem;
    font-size: 0.82rem;
}
.stButton>button:hover {
    filter: brightness(1.08);
    box-shadow: 0 0 0 1px rgba(59,130,246,0.65);
}

/* Generic glass widget containers */
.glass-widget {
    background: radial-gradient(circle at top left, rgba(56,189,248,0.18), rgba(15,23,42,0.9));
    border-radius: 22px;
    border: 1px solid rgba(148,163,184,0.7);
    box-shadow:
      0 32px 120px rgba(15,23,42,0.97),
      0 0 0 1px rgba(15,23,42,0.85);
    padding: 16px 18px;
    backdrop-filter: blur(26px) saturate(210%);
    -webkit-backdrop-filter: blur(26px) saturate(210%);
}
</style>
""",
    unsafe_allow_html=True,
)

PAGE_MAIN = "לוח בקרה ראשי"
PAGE_SCANNER = "סריקת שוק אמריקאי"
PAGE_MACRO = "סימולטור מאקרו"
PAGE_NEWS = "חדשות בזמן אמת"


# --- SIDEBAR: Institutional navigation & controls ---
with st.sidebar:
    st.markdown(
        '<div class="sidebar-header">טרמינל PROTRADE</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-badge">רב-נכסי | ניתוחים בזמן אמת</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    selected_page = st.radio(
        "ניווט מערכת",
        (
            PAGE_MAIN,
            PAGE_SCANNER,
            PAGE_NEWS,
            PAGE_MACRO,
        ),
        index=0,
    )

    st.markdown("### נכס נבחר")
    selected_ticker = st.selectbox(
        "בחר נכס",
        ["NVDA", "AAPL", "MSFT", "TSLA", "AMZN", "GOOGL", "META", "AMD", "BTC-USD"],
    )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 רענן נתונים"):
            st.rerun()
    with col_b:
        st.write("")  # spacer

    st.caption("מנוע נתונים: `data_engine.py` ✅")


# --- MAIN SHELL: Title bar ---
st.markdown(
    '<div class="protrade-title"><h1>⚡ PROTRADE | טרמינל מוסדי מתקדם</h1></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="protrade-subtitle">סביבת מסחר רב-נכסית עם ניתוחים טכניים ומודיעין חדשותי.</div>',
    unsafe_allow_html=True,
)
st.markdown("---")


# --- DATA FETCH (shared across pages where relevant) ---
df = None
if selected_page == PAGE_MAIN:
    with st.spinner("שואב נתוני שוק ממנוע האנליטיקה..."):
        df = de.get_stock_data(selected_ticker)


# --- PAGE: MAIN DASHBOARD ---
if selected_page == PAGE_MAIN:
    st.subheader(f"📊 סקירה טכנית · {selected_ticker}")

    if df is None:
        st.error("שגיאה במשיכת הנתונים ממנוע המידע. ייתכן והבורסה סגורה.")
    else:
        curr = df["Close"].iloc[-1]
        prev = df["Close"].iloc[-2]
        change = ((curr - prev) / prev) * 100
        rsi = df["RSI"].iloc[-1]

        m1, m2, m3 = st.columns(3)
        m1.metric("מחיר סגירה אחרון", f"${curr:,.2f}", f"{change:.2f}%")
        m2.metric(
            "RSI (מומנטום)",
            f"{rsi:.1f}",
            "קניית יתר" if rsi > 70 else "מכירת יתר" if rsi < 30 else "ניטרלי",
        )
        m3.metric(
            "SMA 200 (מגמה)",
            f"${df['SMA200'].iloc[-1]:.2f}",
            "מגמה חיובית" if curr > df["SMA200"].iloc[-1] else "מגמה שלילית",
        )

        # --- Big Data Sentiment Engine widget (glass card) ---
        st.markdown("")
        sent_col, expl_col = st.columns([2, 1])

        # simple synthetic sentiment score based on price change & RSI
        sentiment_score = max(
            0.0,
            min(100.0, 50 + change * 1.2 + (rsi - 50) * 0.4),
        )

        with sent_col:
            st.markdown(
                '<div class="glass-widget"><strong>מנוע סנטימנט Big Data</strong></div>',
                unsafe_allow_html=True,
            )
            sent_fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=sentiment_score,
                    number={"suffix": " / 100"},
                    title={"text": "ציון סנטימנט שוק"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "#38bdf8"},
                        "bgcolor": "rgba(15,23,42,0.0)",
                        "borderwidth": 0,
                        "steps": [
                            {"range": [0, 40], "color": "rgba(248,113,113,0.35)"},
                            {"range": [40, 60], "color": "rgba(148,163,184,0.35)"},
                            {"range": [60, 100], "color": "rgba(52,211,153,0.45)"},
                        ],
                    },
                )
            )
            sent_fig.update_layout(
                template="plotly_dark",
                height=260,
                margin=dict(t=40, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(sent_fig, width="stretch")

        with expl_col:
            st.markdown(
                """
                **מודול סנטימנט AI**  
                הציון המשוכלל מחושב משילוב של תנודתיות יומית, מומנטום (RSI) והטיית כיוון לטווח קצר.  
                ניתן לחבר כאן מודלים מוסדיים מתקדמים (NLP, order book, זרמי ETF ועוד).
                """,
            )

        st.markdown("")
        tab_chart, tab_tech, tab_risk = st.tabs(
            ["גרף אינטראקטיבי", "ניתוח טכני", "סיכונים מוסדיים ונתוני יסוד"]
        )

        # --- TAB 1: Interactive Chart (candles + overlays) ---
        with tab_chart:
            fig = go.Figure()
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="מחיר",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SMA50"],
                    line=dict(color="cyan", width=1.5),
                    name="SMA 50",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["SMA200"],
                    line=dict(color="orange", width=2),
                    name="SMA 200",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BB_High"],
                    line=dict(color="gray", width=1, dash="dot"),
                    name="BB Upper",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["BB_Low"],
                    line=dict(color="gray", width=1, dash="dot"),
                    fill="tonexty",
                    fillcolor="rgba(255,255,255,0.03)",
                    name="BB Lower",
                )
            )

            fig.update_layout(
                template="plotly_dark",
                height=570,
                xaxis_rangeslider_visible=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=10, l=10, r=10),
            )
            st.plotly_chart(fig, width="stretch")

        # --- TAB 2: Technical Analysis (RSI & moving averages detail) ---
        with tab_tech:
            st.markdown("#### מבנה מומנטום ומגמה")

            col_left, col_right = st.columns([2, 1])
            with col_left:
                rsi_fig = go.Figure()
                rsi_fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df["RSI"],
                        line=dict(color="#22c55e", width=1.5),
                        name="RSI",
                    )
                )
                rsi_fig.add_hline(y=70, line=dict(color="#f97316", width=1, dash="dot"))
                rsi_fig.add_hline(y=30, line=dict(color="#3b82f6", width=1, dash="dot"))
                rsi_fig.update_layout(
                    template="plotly_dark",
                    height=260,
                    margin=dict(t=20, b=10, l=10, r=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(rsi_fig, width="stretch")

            with col_right:
                st.markdown("##### תמונת מצב טכנית עדכנית")
                st.write(
                    {
                        "מחיר סגירה אחרון": round(curr, 2),
                        "RSI": round(rsi, 1),
                        "SMA 50": round(df["SMA50"].iloc[-1], 2),
                        "SMA 200": round(df["SMA200"].iloc[-1], 2),
                    }
                )

        # --- TAB 3: Institutional Risk & Fundamentals ---
        with tab_risk:
            # simple proxy metrics based on historical volatility
            returns = df["Close"].pct_change().dropna()
            vol = float(returns.std() * (252**0.5)) if not returns.empty else 0.0
            stress_score = max(0.0, min(100.0, vol * 1500))
            liquidity_buffer = max(0.0, 100.0 - stress_score * 0.6)

            rcol1, rcol2 = st.columns(2)
            with rcol1:
                st.markdown("##### מדדי סיכון מוסדי")
                m_a, m_b, m_c = st.columns(3)
                m_a.metric("סטיית תקן שנתית משוערת", f"{vol*100:.1f}%")
                m_b.metric("מדד סטרס משוקלל", f"{stress_score:.1f} / 100")
                m_c.metric("כרית נזילות משוערת", f"{liquidity_buffer:.1f} / 100")

            with rcol2:
                st.markdown("##### בריאות מאזנית וכספית (דמו)")
                st.write(
                    """
                    אזור זה מיועד לחיבור מודלי קרדיט, תרחישי סטרס רגולטוריים
                    (Basel / Solvency), תזרימי מזומנים מוסדיים ומדדי כיסוי חוב.
                    ניתן למפות כאן מדדי DSCR, LCR, NSFR ועוד.
                    """
                )


# --- PAGE: US MARKET SCANNER ---
elif selected_page == PAGE_SCANNER:
    st.subheader("🔍 סריקת שוק המניות האמריקאי")
    st.caption("סריקה רוחבית של מאות/אלפי מניות בארה״ב על בסיס אותם אינדיקטורים טכניים.")

    col_u, col_n = st.columns([2, 1])
    with col_u:
        universe_label = st.selectbox(
            "יקום סריקה",
            options=[
                "מדד S&P 500 (חברות הגדולות)",
                "NASDAQ 100 (טק גדול)",
                "איחוד רשימות מרכזיות (עלול להיות איטי)",
            ],
        )
        if "S&P 500" in universe_label:
            universe_kind = "sp500"
        elif "NASDAQ" in universe_label:
            universe_kind = "nasdaq100"
        else:
            universe_kind = "all"
    with col_n:
        limit = st.slider(
            "מספר מקסימלי של מניות לסריקה",
            min_value=50,
            max_value=1500,
            value=400,
            step=50,
        )

    run_scan = st.button("🚀 הרץ סריקה על השוק האמריקאי")

    if run_scan:
        with st.spinner("מריץ סריקה רוחבית על השוק האמריקאי... זה עשוי לקחת מספר שניות."):
            scan_df = de.scan_us_market(universe_kind=universe_kind, limit=limit)

        if scan_df is None or scan_df.empty:
            st.error("לא התקבלו נתונים מהסריקה. ייתכן וקיימת בעיית חיבור או הגבלה ב-API.")
        else:
            st.success(f"נסרקו בהצלחה {len(scan_df)} מניות.")

            # תצוגת טבלה פשוטה ומהירה (ללא תלות ב-matplotlib)
            st.dataframe(
                scan_df,
                width="stretch",
            )


# --- PAGE: LIVE NEWS (existing news engine, full-width) ---
elif selected_page == PAGE_NEWS:
    st.subheader("📰 חדשות שוק בזמן אמת")

    news = de.get_market_news()
    if news:
        for item in news:
            st.markdown(
                f"""
            <div class="news-card">
                <a href="{item['link']}" target="_blank" class="news-title">{item['title']}</a>
                <div style="color: #8b949e; font-size: 11px; margin-top: 5px;">
                    {item['source']} · {item['published']}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
    else:
        st.info("אין חדשות זמינות כרגע ממנוע החדשות.")


# --- PAGE: MACRO-ECONOMIC SIMULATOR ---
elif selected_page == PAGE_MACRO:
    st.subheader("🧮 סימולטור מאקרו כלכלי לתיק")
    st.caption("בדוק את עמידות התיק לתרחישי ריבית, אינפלציה וצמיחה שונים.")

    c1, c2, c3 = st.columns(3)
    with c1:
        rate = st.slider("ריבית בסיס (%)", 0.0, 10.0, 3.0, 0.25)
    with c2:
        inflation = st.slider("אינפלציה צפויה (%)", -2.0, 15.0, 2.5, 0.25)
    with c3:
        growth = st.slider("צמיחת תוצר (%)", -5.0, 8.0, 2.0, 0.25)

    stress_index = max(
        0.0,
        min(
            100.0,
            50 + (rate - 3) * 4 + (inflation - 2) * 3 - (growth - 2) * 5,
        ),
    )

    g1, g2 = st.columns([2, 1])
    with g1:
        macro_fig = go.Figure(
            data=[
                go.Bar(
                    x=["מדד סטרס תיק"],
                    y=[stress_index],
                    marker=dict(
                        color=["#38bdf8" if stress_index < 60 else "#f97316" if stress_index < 80 else "#ef4444"]
                    ),
                )
            ]
        )
        macro_fig.update_yaxes(range=[0, 100])
        macro_fig.update_layout(
            template="plotly_dark",
            height=320,
            margin=dict(t=40, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(macro_fig, width="stretch")

    with g2:
        st.markdown(
            """
            **פירוש מהיר של הסימולטור**  
            - ריבית גבוהה ואינפלציה עקשנית מעלות את מדד הסטרס.  
            - צמיחת תוצר גבוהה מאזנת ומפחיתה סיכון מערכתי.  
            - ניתן לחבר כאן מנועי VaR, CVaR ותרחישי קיצון מוסדיים מותאמים.
            """
        )
