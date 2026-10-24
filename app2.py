
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Retail Intelligence | Executive",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).parent

# ==================================================
# EXECUTIVE DARK THEME
# ==================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #080F1F;
        --panel: #101B30;
        --panel2: #14213A;
        --border: #243550;
        --text: #F1F5F9;
        --muted: #91A3BC;
        --cyan: #38BDF8;
        --green: #34D399;
        --red: #FB7185;
        --amber: #FBBF24;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(8, 15, 31, 0.95);
    }

    [data-testid="stSidebar"] {
        background: #0B1426;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.4px;
    }

    p, label, [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    .hero {
        padding: 24px 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #142744 0%, #101B30 60%, #10283C 100%);
        border: 1px solid #29415F;
        margin-bottom: 24px;
    }

    .eyebrow {
        color: #38BDF8;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #F8FAFC;
        font-size: clamp(26px, 3vw, 38px);
        font-weight: 800;
        letter-spacing: -1.2px;
        line-height: 1.2;
        margin: 0;
    }

    .hero-subtitle {
        color: #A9BAD0;
        font-size: 14px;
        margin-top: 10px;
        line-height: 1.7;
    }

    .section-label {
        color: #E2E8F0;
        font-size: 19px;
        font-weight: 750;
        margin-top: 14px;
        margin-bottom: 4px;
    }

    .section-note {
        color: #91A3BC;
        font-size: 12px;
        margin-bottom: 15px;
    }

    .kpi-card {
        background: linear-gradient(145deg, #13223A, #0E192C);
        border: 1px solid #263A56;
        border-radius: 15px;
        padding: 19px 20px;
        min-height: 142px;
    }

    .kpi-label {
        color: #9FB0C7;
        font-size: 12px;
        font-weight: 650;
        margin-bottom: 13px;
    }

    .kpi-value {
        color: #F8FAFC;
        font-size: clamp(23px, 2.2vw, 32px);
        font-weight: 800;
        letter-spacing: -0.8px;
        line-height: 1.2;
        overflow-wrap: anywhere;
    }

    .kpi-foot {
        color: #91A3BC;
        font-size: 11px;
        margin-top: 12px;
    }

    .kpi-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        margin-right: 6px;
    }

    .panel {
        background: #101B30;
        border: 1px solid #243550;
        border-radius: 16px;
        padding: 18px 20px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #243550;
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stDownloadButton"] button {
        border: 1px solid #287CB0;
        border-radius: 9px;
        background: #123452;
        color: #E0F2FE;
        font-weight: 650;
        width: 100%;
    }

    div[data-testid="stDownloadButton"] button:hover {
        background: #19496B;
        border-color: #38BDF8;
        color: white;
    }

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stMultiSelect"] > div {
        border-radius: 8px;
    }

    hr {
        border-color: #243550;
    }

    .footer {
        text-align: center;
        color: #647994;
        font-size: 11px;
        padding-top: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# DATA LOADING
# ==================================================
@st.cache_data
def load_data():
    filenames = [
        "rfm_segmentleri.csv",
        "churn_risk_analizi.csv",
        "churn_kampanya_listesi.csv",
    ]

    loaded = {}
    for filename in filenames:
        path = DATA_DIR / filename
        if not path.exists():
            raise FileNotFoundError(filename)

        loaded[filename] = pd.read_csv(path)

    rfm = loaded["rfm_segmentleri.csv"]
    risk = loaded["churn_risk_analizi.csv"]
    campaign = loaded["churn_kampanya_listesi.csv"]

    for frame in (rfm, risk, campaign):
        if "kesit_tarihi" in frame.columns:
            frame["kesit_tarihi"] = pd.to_datetime(
                frame["kesit_tarihi"], errors="coerce"
            )

        if "churn_riski" in frame.columns:
            frame["churn_riski"] = pd.to_numeric(
                frame["churn_riski"], errors="coerce"
            )

        if "kayip" in frame.columns:
            frame["kayip"] = pd.to_numeric(
                frame["kayip"], errors="coerce"
            )

    return rfm, risk, campaign


try:
    rfm_all, risk_all, campaign_all = load_data()
except (FileNotFoundError, pd.errors.ParserError) as exc:
    st.error(f"Veri dosyaları yüklenemedi: {exc}")
    st.info(
        "Üç CSV dosyasının app2.py ile aynı klasörde olduğunu "
        "ve dosyaların doğru dışa aktarıldığını kontrol et."
    )
    st.stop()

if risk_all.empty:
    st.error("Churn risk dosyasında görüntülenecek kayıt bulunamadı.")
    st.stop()

# ==================================================
# HEADER
# ==================================================
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">RETAIL INTELLIGENCE · EXECUTIVE OVERVIEW</div>
        <div class="hero-title">Customer Analytics</div>
        <div class="hero-subtitle">
            Müşteri segmentasyonu, kayıp riski ve kampanya önceliklendirme
            tek bir ekranda.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# SIDEBAR FILTERS
# ==================================================
st.sidebar.markdown("## 📊 Control Center")
st.sidebar.caption("Analiz görünümünü özelleştir.")
st.sidebar.divider()

risk_view = risk_all.copy()
campaign_view = campaign_all.copy()

if "kesit_tarihi" in risk_view.columns:
    dates = sorted(risk_view["kesit_tarihi"].dropna().unique())

    if dates:
        chosen_date = st.sidebar.selectbox(
            "Analiz tarihi",
            dates,
            format_func=lambda d: pd.Timestamp(d).strftime("%d %B %Y"),
        )

        risk_view = risk_view[
            risk_view["kesit_tarihi"] == chosen_date
        ].copy()

        if "kesit_tarihi" in campaign_view.columns:
            campaign_view = campaign_view[
                campaign_view["kesit_tarihi"] == chosen_date
            ].copy()

if "segment" in risk_view.columns:
    all_segments = sorted(
        risk_view["segment"].dropna().unique().tolist()
    )
    chosen_segments = st.sidebar.multiselect(
        "RFM segmentleri",
        options=all_segments,
        default=all_segments,
    )

    risk_view = risk_view[
        risk_view["segment"].isin(chosen_segments)
    ].copy()

    if "segment" in campaign_view.columns:
        campaign_view = campaign_view[
            campaign_view["segment"].isin(chosen_segments)
        ].copy()

risk_filter_options = ["Tümü", "Düşük", "Orta", "Yüksek"]
chosen_risk = st.sidebar.selectbox(
    "Churn risk seviyesi",
    risk_filter_options,
    index=0,
)

risk_labels = {
    "Düşük": "Dusuk",
    "Orta": "Orta",
    "Yüksek": "Yuksek",
}

if chosen_risk != "Tümü" and "risk_seviyesi" in risk_view.columns:
    risk_view = risk_view[
        risk_view["risk_seviyesi"].astype(str)
        == risk_labels[chosen_risk]
    ].copy()

st.sidebar.divider()
st.sidebar.caption("Model: Random Forest")
st.sidebar.caption("Risk eşikleri: %30 / %60")

if st.sidebar.button("🔄 Filtreleri sıfırla", use_container_width=True):
    st.rerun()

# ==================================================
# KPI CALCULATIONS
# ==================================================
customer_count = (
    risk_view["musteri_id"].nunique()
    if "musteri_id" in risk_view.columns
    else len(risk_view)
)

if "churn_riski" in risk_view.columns and not risk_view.empty:
    average_risk = risk_view["churn_riski"].mean()
    high_risk_count = int((risk_view["churn_riski"] > 0.60).sum())
else:
    average_risk = None
    high_risk_count = 0

actual_churn = (
    risk_view["kayip"].mean()
    if "kayip" in risk_view.columns and not risk_view.empty
    else None
)

campaign_count = len(campaign_view)

def kpi_card(label, value, foot, color):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-foot">
                <span class="kpi-dot" style="background:{color};"></span>
                {foot}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="section-label">Executive Summary</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Seçili filtrelere göre temel performans göstergeleri</div>',
    unsafe_allow_html=True,
)

k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    kpi_card(
        "MÜŞTERİ KAYDI",
        f"{customer_count:,}",
        "Filtrelenmiş müşteri grubu",
        "#38BDF8",
    )

with k2:
    kpi_card(
        "YÜKSEK RİSK",
        f"{high_risk_count:,}",
        "Tahmini risk > %60",
        "#FB7185",
    )

with k3:
    kpi_card(
        "ORTALAMA CHURN RİSKİ",
        f"{average_risk:.1%}" if average_risk is not None else "N/A",
        "Modelin ortalama risk skoru",
        "#FBBF24",
    )

with k4:
    kpi_card(
        "KAMPANYA ADAYLARI",
        f"{campaign_count:,}",
        "Seçili kampanya listesindeki kayıtlar",
        "#34D399",
    )

st.write("")

if actual_churn is not None:
    st.caption(
        f"Seçili kayıtların gözlenen kayıp oranı: {actual_churn:.1%}. "
        "Bu değer model tahmini değil, veri setindeki kayıp etiketinin oranıdır."
    )

st.divider()


# ==============================
# YONETICI DASHBOARD
# ==============================
import pandas as pd
import streamlit as st
from pathlib import Path

st.markdown("---")
st.header("📊 Yönetici Dashboard'u")
st.caption("RFM müşteri segmentleri ve genel müşteri görünümü")

rfm_path = Path(__file__).parent / "rfm_segmentleri.csv"

if rfm_path.exists():
    rfm_df = pd.read_csv(rfm_path)

    toplam_musteri = rfm_df["musteri_id"].nunique()
    toplam_segment = rfm_df["segment"].nunique()
    ortalama_recency = rfm_df["recency_gun"].mean()
    toplam_ciro = rfm_df["toplam_tutar"].sum()

    # Üst KPI kartları
    col1, col2 = st.columns(2)

    col1.metric("👥 Toplam Müşteri", f"{toplam_musteri:,}")
    col2.metric("🏷️ Segment Sayısı", f"{toplam_segment}")

    col3, col4 = st.columns(2)

    col3.metric(
        "📅 Ortalama Son Alışveriş Aralığı",
        f"{ortalama_recency:.0f} gün"
    )
    col4.metric(
        "💰 Toplam İşlem Tutarı",
        f"{toplam_ciro:,.2f}"
    )

    st.markdown("### 🧩 Müşteri Segmentlerinin Dağılımı")

    segment_sayilari = (
        rfm_df["segment"]
        .value_counts()
        .rename_axis("Segment")
        .reset_index(name="Müşteri Sayısı")
    )

    st.bar_chart(
        segment_sayilari.set_index("Segment")["Müşteri Sayısı"]
    )

    st.markdown("### 📋 Segment Detayları")

    segment_ozet = (
        rfm_df.groupby("segment", dropna=False)
        .agg(
            Musteri_Sayisi=("musteri_id", "nunique"),
            Ortalama_Recency=("recency_gun", "mean"),
            Toplam_Tutar=("toplam_tutar", "sum")
        )
        .reset_index()
        .rename(columns={
            "segment": "Müşteri Segmenti",
            "Musteri_Sayisi": "Müşteri Sayısı",
            "Ortalama_Recency": "Ort. Son Alışveriş Aralığı (gün)",
            "Toplam_Tutar": "Toplam İşlem Tutarı"
        })
        .sort_values("Müşteri Sayısı", ascending=False)
    )

    segment_ozet["Ort. Son Alışveriş Aralığı (gün)"] = (
        segment_ozet["Ort. Son Alışveriş Aralığı (gün)"].round(1)
    )

    st.dataframe(
        segment_ozet,
        use_container_width=True,
        hide_index=True
    )

else:
    st.error("rfm_segmentleri.csv dosyası bulunamadı.")


# ==================================================
# CHARTS
# ==================================================
st.markdown(
    '<div class="section-label">Customer Portfolio</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Segment büyüklüğü ve tahmini müşteri kayıp riski</div>',
    unsafe_allow_html=True,
)

chart_left, chart_right = st.columns(2, gap="large")

plot_layout = dict(
    paper_bgcolor="#101B30",
    plot_bgcolor="#101B30",
    font=dict(color="#DCE7F5", family="Arial"),
    margin=dict(l=20, r=20, t=45, b=65),
    height=350,
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#C3D1E3"),
    ),
)

if "segment" in risk_view.columns and not risk_view.empty:
    segment_counts = (
        risk_view.groupby("segment", as_index=False)
        .size()
        .rename(columns={"size": "musteri_sayisi"})
        .sort_values("musteri_sayisi", ascending=True)
    )

    with chart_left:
        st.markdown("#### RFM Segment Dağılımı")
        fig = px.bar(
            segment_counts,
            x="musteri_sayisi",
            y="segment",
            orientation="h",
            text="musteri_sayisi",
            color_discrete_sequence=["#38BDF8"],
        )
        fig.update_traces(
            textposition="outside",
            textfont=dict(color="#E2E8F0"),
            cliponaxis=False,
        )
        fig.update_layout(**plot_layout)
        fig.update_layout(
            height=max(330, len(segment_counts) * 48),
            showlegend=False,
            xaxis_title="Müşteri sayısı",
            yaxis_title="",
        )
        fig.update_xaxes(
            gridcolor="#263750",
            zeroline=False,
        )
        fig.update_yaxes(
            gridcolor="#263750",
            automargin=True,
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    with chart_left:
        st.info("Segment grafiği için veri bulunamadı.")

if (
    {"segment", "churn_riski"}.issubset(risk_view.columns)
    and not risk_view.empty
):
    segment_risk = (
        risk_view.groupby("segment", as_index=False)
        .agg(
            ortalama_risk=("churn_riski", "mean"),
            kayit_sayisi=("churn_riski", "size"),
        )
        .sort_values("ortalama_risk", ascending=True)
    )

    with chart_right:
        st.markdown("#### Segment Bazında Ortalama Risk")
        fig = px.bar(
            segment_risk,
            x="ortalama_risk",
            y="segment",
            orientation="h",
            text="ortalama_risk",
            color="ortalama_risk",
            color_continuous_scale=[
                [0, "#34D399"],
                [0.5, "#FBBF24"],
                [1, "#FB7185"],
            ],
            range_color=[0, 1],
            hover_data={"kayit_sayisi": True, "ortalama_risk": ":.1%"},
        )
        fig.update_traces(
            texttemplate="%{x:.1%}",
            textposition="outside",
            textfont=dict(color="#E2E8F0"),
            cliponaxis=False,
        )
        fig.update_layout(**plot_layout)
        fig.update_layout(
            height=max(330, len(segment_risk) * 48),
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Ortalama tahmini risk",
            yaxis_title="",
        )
        fig.update_xaxes(
            tickformat=".0%",
            range=[0, min(1.15, max(0.25, segment_risk["ortalama_risk"].max() * 1.25))],
            gridcolor="#263750",
            zeroline=False,
        )
        fig.update_yaxes(automargin=True)
        st.plotly_chart(fig, use_container_width=True)
else:
    with chart_right:
        st.info("Risk grafiği için veri bulunamadı.")

st.divider()

# ==================================================
# CUSTOMER RISK TABLE
# ==================================================
st.markdown(
    '<div class="section-label">Customer Risk Explorer</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Müşterileri tahmini risk puanına göre incele ve sonuçları dışa aktar.</div>',
    unsafe_allow_html=True,
)

if "churn_riski" in risk_view.columns:
    min_risk = st.slider(
        "Minimum tahmini risk",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
        format="%d%%",
    )

    table = risk_view[
        risk_view["churn_riski"] >= min_risk / 100
    ].copy()

    table = table.sort_values("churn_riski", ascending=False)

    display_table = table.copy()
    display_table["churn_riski"] = display_table["churn_riski"].map(
        lambda v: f"{v:.1%}" if pd.notna(v) else ""
    )

    if "kayip" in display_table.columns:
        display_table["kayip"] = display_table["kayip"].map(
            {0: "Hayır", 1: "Evet"}
        ).fillna("Bilinmiyor")

    st.caption(f"Görüntülenen kayıt sayısı: {len(display_table):,}")
    st.dataframe(
        display_table,
        use_container_width=True,
        hide_index=True,
        height=370,
    )

    st.download_button(
        "⬇️ Filtrelenmiş risk tablosunu indir",
        data=table.to_csv(index=False).encode("utf-8-sig"),
        file_name="filtrelenmis_churn_analizi.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.warning("Risk dosyasında churn_riski sütunu bulunamadı.")

st.divider()

# ==================================================
# CAMPAIGN PRIORITIZATION
# ==================================================
st.markdown(
    '<div class="section-label">Campaign Prioritization</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">Yüksek riskli müşteriler için önerilen kampanya adayları</div>',
    unsafe_allow_html=True,
)

if not campaign_view.empty:
    campaign_display = campaign_view.copy()

    if "churn_riski" in campaign_display.columns:
        campaign_display = campaign_display.sort_values(
            "churn_riski", ascending=False
        )
        campaign_display["churn_riski"] = campaign_display["churn_riski"].map(
            lambda v: f"{v:.1%}" if pd.notna(v) else ""
        )

    st.caption(f"Kampanya adayı sayısı: {len(campaign_display):,}")
    st.dataframe(
        campaign_display,
        use_container_width=True,
        hide_index=True,
        height=330,
    )

    st.download_button(
        "⬇️ Kampanya listesini indir",
        data=campaign_view.to_csv(index=False).encode("utf-8-sig"),
        file_name="churn_kampanya_listesi.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.info(
        "Seçilen filtrelerde kampanya adayı yok. "
        "Sol paneldeki filtreleri değiştirmeyi deneyebilirsin."
    )

# ==================================================
# FOOTER
# ==================================================

# ==================================================
# BUSINESS INSIGHTS — DATA-DRIVEN RECOMMENDATIONS
# ==================================================
st.divider()

st.markdown(
    '<div class="section-label">🧠 Business Insights</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-note">'
    'Verilerden otomatik üretilen yönetici içgörüleri ve aksiyon önerileri'
    '</div>',
    unsafe_allow_html=True,
)

insight_data = risk_view.copy()

if (
    not insight_data.empty
    and {"segment", "churn_riski"}.issubset(insight_data.columns)
):
    segment_insights = (
        insight_data.groupby("segment", as_index=False)
        .agg(
            musteri_sayisi=("churn_riski", "size"),
            ortalama_risk=("churn_riski", "mean"),
        )
    )

    segment_insights["riskli_musteri"] = (
        insight_data.assign(
            yuksek_risk=insight_data["churn_riski"] > 0.60
        )
        .groupby("segment")["yuksek_risk"]
        .sum()
        .reindex(segment_insights["segment"])
        .to_numpy()
    )

    top_risk_segment = segment_insights.sort_values(
        "ortalama_risk", ascending=False
    ).iloc[0]

    largest_segment = segment_insights.sort_values(
        "musteri_sayisi", ascending=False
    ).iloc[0]

    total_insight_customers = len(insight_data)
    high_risk_total = int((insight_data["churn_riski"] > 0.60).sum())

    i1, i2, i3 = st.columns(3, gap="medium")

    with i1:
        kpi_card(
            "EN YÜKSEK ORTALAMA RİSK",
            f"{top_risk_segment['ortalama_risk']:.1%}",
            str(top_risk_segment["segment"]),
            "#FB7185",
        )

    with i2:
        kpi_card(
            "EN BÜYÜK SEGMENT",
            f"{int(largest_segment['musteri_sayisi']):,}",
            str(largest_segment["segment"]),
            "#38BDF8",
        )

    with i3:
        high_risk_share = (
            high_risk_total / total_insight_customers
            if total_insight_customers else 0
        )
        kpi_card(
            "YÜKSEK RİSK PAYI",
            f"{high_risk_share:.1%}",
            f"{high_risk_total:,} müşteri · risk > %60",
            "#FBBF24",
        )

    st.write("")

    st.markdown("#### 🎯 Önerilen iş aksiyonları")

    action_map = {
        "Champions": (
            "VIP koruma",
            "Değerli müşterileri elde tutmaya odaklan; kişiselleştirilmiş "
            "deneyimler ve seçici sadakat avantajları test et.",
        ),
        "Sadik Musteriler": (
            "Sadakat geliştirme",
            "Sadakat programı, tamamlayıcı ürün önerileri ve müşteri "
            "değerini artırmaya yönelik teklifler değerlendir.",
        ),
        "Yeni / Potansiyel": (
            "İkinci alışveriş",
            "İlk alışverişten sonraki dönemde hatırlatma, ürün önerisi "
            "ve ikinci sipariş teşviklerini test et.",
        ),
        "Risk Altinda": (
            "Geri kazanım",
            "Müşterinin son alışverişinden beri geçen süreyi incele; "
            "uygun müşterilere hedefli geri kazanım iletişimi planla.",
        ),
        "Kaybedilmek Uzere": (
            "Öncelikli geri kazanım",
            "Uzun süredir alışveriş yapmayan müşteriler için hedefli "
            "teklifleri kontrollü bir kampanya testiyle değerlendir.",
        ),
        "Diger": (
            "Davranış analizi",
            "Segment içindeki farklı müşteri davranışlarını incele; "
            "risk ve harcama düzeyine göre daha anlamlı alt gruplar oluştur.",
        ),
    }

    sorted_insights = segment_insights.sort_values(
        ["ortalama_risk", "musteri_sayisi"],
        ascending=[False, False],
    )

    for _, row in sorted_insights.iterrows():
        segment_name = str(row["segment"])
        action_title, action_text = action_map.get(
            segment_name,
            (
                "Segmenti incele",
                "Müşteri davranışını ve risk düzeyini değerlendirerek "
                "uygun aksiyonları test et.",
            ),
        )

        with st.container(border=True):
            col_a, col_b = st.columns([1, 3])

            with col_a:
                st.markdown(f"**{segment_name}**")
                st.metric(
                    "Ortalama risk",
                    f"{row['ortalama_risk']:.1%}",
                )

            with col_b:
                st.markdown(f"**Öneri: {action_title}**")
                st.write(action_text)
                st.caption(
                    f"{int(row['musteri_sayisi']):,} müşteri · "
                    f"{int(row['riskli_musteri']):,} yüksek riskli müşteri"
                )

    st.markdown("#### 📌 Yönetici özeti")

    st.info(
        f"Seçili filtrelerde {total_insight_customers:,} müşteri inceleniyor. "
        f"{high_risk_total:,} müşterinin tahmini churn riski %60'ın üzerinde. "
        f"En yüksek ortalama risk '{top_risk_segment['segment']}' "
        f"segmentinde ({top_risk_segment['ortalama_risk']:.1%}). "
        "Kampanya önceliklerini belirlerken risk puanını müşteri değeri, "
        "iletişim maliyeti ve kampanya sonuçlarıyla birlikte değerlendirin."
    )

    st.caption(
        "İçgörüler mevcut veri ve model skorlarından kurallarla üretilir; "
        "bir üretken yapay zekâ çıktısı değildir. Kampanya etkisi ayrıca "
        "ölçülmelidir."
    )

else:
    st.info(
        "İş içgörüleri için segment ve churn_riski sütunlarını içeren "
        "müşteri verisi gerekiyor."
    )

st.markdown(
    """
    <div class="footer">
        RETAIL INTELLIGENCE · CUSTOMER ANALYTICS<br>
        Churn scores are model estimates, not guarantees of future behavior.
        Campaign effectiveness should be measured separately.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================
# MODEL PERFORMANCE CENTER
# ==============================

st.markdown("---")
st.header("🎯 Model Performance Center")

performans_dosyasi = DATA_DIR / "model_performans_042.csv"

if not performans_dosyasi.exists():
    st.warning(
        "model_performans_042.csv dosyası "
        "app2.py ile aynı klasörde bulunamadı."
    )
else:
    performans = pd.read_csv(performans_dosyasi, sep=";")

    if performans.empty:
        st.error("Model performans dosyası boş.")
    else:
        metrik = performans.iloc[0]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("ROC-AUC", f"{metrik['ROC_AUC']:.3f}")
        c2.metric("Precision", f"%{metrik['Precision'] * 100:.1f}")
        c3.metric("Recall", f"%{metrik['Recall'] * 100:.1f}")
        c4.metric("F1 Score", f"{metrik['F1']:.3f}")

        st.caption(
            "Random Forest | Test dönemi: 09.09.2011 | "
            "Karar eşiği: 0.42"
        )

        st.subheader("📊 Kampanya Kapasitesi")

        c5, c6 = st.columns(2)
        c5.metric(
            "Kampanya Adayı",
            f"{int(metrik['Kampanya_adayi']):,}"
        )
        c6.metric(
            "Kampanya Oranı",
            f"%{metrik['Kampanya_orani_yuzde']:.2f}"
        )

        # Confusion Matrix
        st.subheader("🔍 Confusion Matrix")

        tn = int(metrik["Dogru_aktif"])
        fp = int(metrik["Yanlis_alarm"])
        fn = int(metrik["Kacirilan_kayip"])
        tp = int(metrik["Yakalanan_kayip"])

        confusion_df = pd.DataFrame(
            [[tn, fp], [fn, tp]],
            index=["Gerçek: Aktif", "Gerçek: Kayıp"],
            columns=["Tahmin: Aktif", "Tahmin: Kayıp"]
        )

        st.dataframe(
            confusion_df.style.format("{:,}"),
            use_container_width=True
        )

        st.caption(
            "Doğru aktif: Aktif müşteriyi doğru tanıma. "
            "Yanlış alarm: Aktif müşteriye kayıp tahmini. "
            "Kaçırılan kayıp: Kayıp müşteriyi aktif tahmin etme. "
            "Yakalanan kayıp: Kayıp müşteriyi doğru tanıma."
        )

# ==============================
# FEATURE IMPORTANCE
# ==============================

st.markdown("---")
st.header("🧠 Feature Importance")
st.caption(
    "Random Forest modelinin tahminlerinde kullandığı "
    "özelliklerin göreli önem sıralaması."
)

importance_path = DATA_DIR / "feature_importance.csv"

if not importance_path.exists():
    st.warning(
        "feature_importance.csv dosyasını "
        "app2.py ile aynı klasöre koy."
    )
else:
    importance_df = pd.read_csv(importance_path)

    importance_df = importance_df.sort_values(
        "onem", ascending=True
    )

    fig_importance = px.bar(
        importance_df,
        x="onem",
        y="ozellik",
        orientation="h",
        text="onem_yuzde",
        labels={
            "onem": "Göreli önem",
            "ozellik": "Müşteri özelliği",
            "onem_yuzde": "Önem (%)"
        },
        color="onem",
        color_continuous_scale=[
            "#14213A",
            "#1679A8",
            "#38BDF8"
        ]
    )

    fig_importance.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig_importance.update_layout(
        paper_bgcolor="#101B30",
        plot_bgcolor="#101B30",
        font=dict(color="#DCE7F5"),
        xaxis_title="Göreli önem",
        yaxis_title="",
        xaxis_tickformat=".0%",
        coloraxis_showscale=False,
        margin=dict(l=20, r=55, t=25, b=45),
        height=430
    )

    fig_importance.update_xaxes(
        gridcolor="#263750"
    )

    st.plotly_chart(
        fig_importance,
        use_container_width=True
    )

    st.caption(
        "Not: Feature importance değerleri göreli önem ölçüsüdür; "
        "nedensellik veya bir özelliğin riski hangi yönde "
        "etkilediğini tek başına göstermez."
    )

# ==============================
# SHAP EXPLAINABILITY
# ==============================
st.markdown("---")
st.header("🔎 SHAP Explainability")
st.caption(
    "Modelin müşteri kaybı tahminlerinde hangi özelliklerin "
    "etkili olduğunu gösteren açıklanabilirlik analizi."
)

shap_path = DATA_DIR / "shap_summary.png"

if shap_path.exists():
    st.image(
        str(shap_path),
        caption="SHAP Summary Plot — Müşteri kaybı tahminlerine etki eden özellikler",
        use_container_width=True
    )
    st.markdown("""
    **Grafik nasıl okunur?**
    - **Sağ taraf:** Model çıktısını `kayip=1` yönünde artıran SHAP katkıları.
    - **Sol taraf:** Model çıktısını `kayip=1` yönünde azaltan SHAP katkıları.
    - **Pembe:** Özelliğin yüksek değerleri.
    - **Mavi:** Özelliğin düşük değerleri.

    *SHAP değerleri modelin öğrendiği ilişkileri açıklar; nedensellik göstermez.*
    """)
else:
    st.warning(
        "shap_summary.png dosyasını app2.py ile aynı klasöre koy."
    )

# ==============================
# CUSTOMER-LEVEL SHAP EXPLANATION
# ==============================
st.markdown("---")
st.header("🧑‍💼 Customer-Level SHAP Explanation")
st.caption(
    "Müşteri bazında kayıp olasılığı ve tahmini etkileyen özellikler."
)

customer_shap_path = DATA_DIR / "shap_customer_explanations.csv"

if not customer_shap_path.exists():
    st.warning(
        "shap_customer_explanations.csv dosyasını app2.py ile aynı klasöre koy."
    )
else:
    customer_shap = pd.read_csv(customer_shap_path, sep=";")

    if customer_shap.empty:
        st.error("Müşteri SHAP dosyası boş.")
    else:
        customer_shap["musteri_id"] = (
            customer_shap["musteri_id"].astype(str)
        )

        secilen_musteri = st.selectbox(
            "Müşteri seç",
            options=customer_shap["musteri_id"].drop_duplicates().tolist()
        )

        musteri = customer_shap[
            customer_shap["musteri_id"] == secilen_musteri
        ].iloc[0]

        olasilik = float(musteri["kayip_olasiligi"])

        c1, c2 = st.columns(2)
        c1.metric("Müşteri ID", secilen_musteri)
        c2.metric("Tahmini kayıp olasılığı", f"%{olasilik * 100:.1f}")

        st.progress(max(0.0, min(1.0, olasilik)))

        shap_cols = {
            col.replace("shap_", ""): col
            for col in customer_shap.columns
            if col.startswith("shap_")
        }

        etkiler = pd.DataFrame({
            "Özellik": list(shap_cols.keys()),
            "SHAP": [
                float(musteri[col]) for col in shap_cols.values()
            ]
        })

        etkiler = etkiler.sort_values(
            "SHAP", key=lambda s: s.abs(), ascending=False
        )

        st.subheader("📊 Müşterinin Tahminini Etkileyen Özellikler")

        fig_customer = px.bar(
            etkiler.head(9).sort_values("SHAP"),
            x="SHAP",
            y="Özellik",
            orientation="h",
            color="SHAP",
            color_continuous_scale=["#38BDF8", "#14213A", "#F472B6"],
            labels={"SHAP": "SHAP katkısı", "Özellik": ""}
        )

        fig_customer.update_layout(
            paper_bgcolor="#101B30",
            plot_bgcolor="#101B30",
            font=dict(color="#DCE7F5"),
            coloraxis_showscale=False,
            height=400
        )
        fig_customer.update_xaxes(
            zeroline=True,
            zerolinecolor="#DCE7F5",
            gridcolor="#263750"
        )

        st.plotly_chart(fig_customer, use_container_width=True)

        st.subheader("🔍 En Önemli Etkenler")

        artiran = etkiler[etkiler["SHAP"] > 0].sort_values(
            "SHAP", ascending=False
        ).head(3)

        azaltan = etkiler[etkiler["SHAP"] < 0].sort_values(
            "SHAP", ascending=True
        ).head(3)

        sol, sag = st.columns(2)

        with sol:
            st.markdown("**🔴 Kayıp tahminini artıranlar**")
            if artiran.empty:
                st.write("Pozitif katkı bulunamadı.")
            else:
                for _, satir in artiran.iterrows():
                    st.write(f"↑ {satir['Özellik']}")

        with sag:
            st.markdown("**🔵 Kayıp tahminini azaltanlar**")
            if azaltan.empty:
                st.write("Negatif katkı bulunamadı.")
            else:
                for _, satir in azaltan.iterrows():
                    st.write(f"↓ {satir['Özellik']}")

        st.caption(
            "Pozitif SHAP katkısı kayıp sınıfı (kayip=1) yönündedir; "
            "negatif katkı bu sınıftan uzaklaştırır. Katkılar tek başına "
            "nedensellik göstermez."
        )

# ==============================
# GEMINI AI CUSTOMER INSIGHTS
# ==============================
st.markdown("---")
st.header("🤖 AI Customer Insights")

st.caption(
    "Gemini, müşteri kayıp riskini SHAP sonuçlarıyla birlikte yorumlar "
    "ve kampanya önerileri üretir."
)

if "customer_shap" in locals() and not customer_shap.empty:

    musteri_satiri = customer_shap[
        customer_shap["musteri_id"].astype(str) == str(secilen_musteri)
    ]

    if not musteri_satiri.empty:
        musteri_verisi = musteri_satiri.iloc[0]
        risk = float(musteri_verisi["kayip_olasiligi"])

        st.subheader("🎯 Müşteri Kayıp Risk Seviyesi")
        st.metric("Kayıp Olasılığı", f"%{risk * 100:.1f}")

        if risk >= 0.70:
            st.error("🔴 Yüksek Risk")
        elif risk >= 0.40:
            st.warning("🟠 Orta Risk")
        else:
            st.success("🟢 Düşük Risk")

        if st.button(
            "✨ AI ile Müşteriyi Analiz Et",
            key="gemini_customer_analysis"
        ):
            try:
                from google import genai

                api_key = st.secrets["GEMINI_API_KEY"]
                client = genai.Client(api_key=api_key)

                shap_cols = [
                    col for col in customer_shap.columns
                    if col.startswith("shap_")
                ]

                katkilar = sorted(
                    [
                        {
                            "ozellik": col.replace("shap_", ""),
                            "shap_katkisi": round(
                                float(musteri_verisi[col]), 4
                            )
                        }
                        for col in shap_cols
                    ],
                    key=lambda x: abs(x["shap_katkisi"]),
                    reverse=True
                )

                ozellik_listesi = [
                    "recency_gun",
                    "tenure_gun",
                    "fatura_sayisi",
                    "fatura_son180",
                    "toplam_tutar",
                    "tutar_son180",
                    "ort_fatura_tutari",
                    "urun_cesidi",
                    "ingiltere_mi"
                ]

                analiz_verisi = {
                    "musteri_id": str(secilen_musteri),
                    "kayip_olasiligi": round(risk, 4),
                    "ozellikler": {
                        ozellik: float(musteri_verisi[ozellik])
                        for ozellik in ozellik_listesi
                        if ozellik in customer_shap.columns
                    },
                    "shap_katkilari": katkilar
                }

                prompt = f"""
Sen bir perakende müşteri analitiği uzmanısın.
Verilen model çıktısını Türkçe analiz et.

VERİ:
{analiz_verisi}

Raporu aşağıdaki beş başlıkla ve bu sırayla hazırla:

1. Risk Değerlendirmesi
2. Riski Artıran En Önemli Etkenler
3. Riski Azaltan Etkenler
4. Önerilen Müşteri Geri Kazanım Kampanyası
5. İşletme İçin Kısa Aksiyon Planı

Kurallar:
- Yalnızca verilen verileri kullan.
- SHAP katkılarını nedensellik kanıtı olarak sunma.
- Pozitif SHAP katkılarını model çıktısına göre yorumla;
  kullanılan açıklama ölçeği hakkında bilgi yoksa kesinlik iddia etme.
- Negatif katkı yoksa bunu açıkça belirt.
- Bilinmeyen müşteri davranışlarını uydurma.
- Kayıp olasılığını kesin sonuç gibi yorumlama.
- Kampanya hedefi, aksiyonu ve zamanlamasını belirt.
- Ölçülebilir KPI öner; örneğin 30 günlük tekrar alışveriş oranı.
- Maliyet ve getiri verisi yoksa sayı uydurma.
- İndirim dışı kişiselleştirilmiş öneriler de sun.
- Veride bulunmayan ürün kategorisi veya satın alma geçmişi uydurma.
"""

                with st.spinner("Gemini müşteri analizini hazırlıyor..."):
                    response = client.interactions.create(
                        model="gemini-3.8-flash",
                        input=prompt
                    )

                
                rapor = response.output_text

                import re

                # Gemini'nin başlıklarını standartlaştır.
                basliklar = [
                    ("Risk Değerlendirmesi", "🎯"),
                    ("Riski Artıran En Önemli Etkenler", "📈"),
                    ("Riski Azaltan Etkenler", "🛡️"),
                    ("Önerilen Müşteri Geri Kazanım Kampanyası", "💡"),
                    ("İşletme İçin Kısa Aksiyon Planı", "🗂️"),
                ]

                # Başlıkları bulurken numaraları ve Markdown işaretlerini
                # dikkate alma; başlıkların bulunduğu satırları yakala.
                baslik_regexleri = [
                    re.compile(
                        r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?"
                        r"(?:\d+[.)][ \t]*)?"
                        + re.escape(baslik)
                        + r"[ \t]*:?[ \t]*$"
                    )
                    for baslik, _ in basliklar
                ]

                bulunanlar = []

                for (baslik, emoji), regex in zip(
                    basliklar, baslik_regexleri
                ):
                    eslesme = regex.search(rapor)
                    if eslesme:
                        bulunanlar.append(
                            (eslesme.start(), eslesme.end(), baslik, emoji)
                        )

                bulunanlar.sort(key=lambda x: x[0])

                st.success("✅ Müşteri analizi tamamlandı.")
                st.subheader("📋 AI Analiz Raporu")

                with st.expander(
                    "📋 Detaylı AI Analiz Raporu",
                    expanded=True
                ):
                    if bulunanlar:
                        for i, (
                            baslangic, baslik_sonu, baslik, emoji
                        ) in enumerate(bulunanlar):

                            if i + 1 < len(bulunanlar):
                                bitis = bulunanlar[i + 1][0]
                            else:
                                bitis = len(rapor)

                            icerik = rapor[baslik_sonu:bitis].strip()

                            # Sonraki bölümün numarası kalmışsa temizle.
                            icerik = re.sub(
                                r"(?m)^[ \t]*#{1,6}[ \t]*"
                                r"\d+[.)][ \t]*[^\n]*$",
                                "",
                                icerik
                            ).strip()

                            st.markdown(f"### {emoji} {baslik}")

                            if icerik:
                                st.markdown(icerik)
                            else:
                                st.caption(
                                    "Bu bölümde gösterilecek metin bulunamadı."
                                )
                    else:
                        # Başlıklar tanınmazsa rapor kaybolmasın.
                        st.markdown(rapor)


            except Exception as e:
                st.error(
                    f"Gemini analizi sırasında hata oluştu: {e}"
                )

    else:
        st.warning(
            "Seçilen müşteri SHAP dosyasında bulunamadı. "
            "Müşteri seçimini kontrol et."
        )

else:
    st.info(
        "AI analizi için Customer-Level SHAP verilerinin "
        "yüklenmiş olması gerekiyor."
    )
