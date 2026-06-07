import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from pathlib import Path

# ─────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────

st.set_page_config(
    page_title="E-commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CSS personnalisé
# ─────────────────────────────────────────

st.markdown("""
<style>
    /* Police globale */
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

    /* Sidebar dégradé sombre */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    [data-testid="stSidebar"] * { color: #e8f4f8 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
        font-size: 1.1rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: #90caf9 !important;
    }
    [data-testid="stSidebar"] .stRadio > div { gap: 6px; }
    [data-testid="stSidebar"] .stRadio label {
        font-size: 0.95rem;
        padding: 6px 10px;
        border-radius: 8px;
        transition: background 0.2s;
    }
    [data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.08); }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #f0f4ff;
        border-radius: 14px;
        padding: 18px 22px;
        border-left: 5px solid #4361ee;
        box-shadow: 0 2px 12px rgba(67,97,238,0.10);
    }
    [data-testid="stMetricLabel"] { font-weight: 700; color: #5c677d; font-size: 0.85rem; }
    [data-testid="stMetricValue"] { font-size: 1.9rem; font-weight: 800; color: #1a1a2e; }

    /* Titres */
    h1 {
        color: #1a1a2e;
        padding-bottom: 6px;
        border-bottom: 3px solid #4361ee;
        margin-bottom: 24px;
    }
    h2 { color: #203a43; margin-top: 28px; }
    h3 { color: #4361ee; }

    /* Séparateur coloré */
    hr { border: none; border-top: 2px solid #e0e7ff; margin: 28px 0; }

    /* Badge de page */
    .page-badge {
        display: inline-block;
        background: #4361ee;
        color: white !important;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Palette & thème graphiques
# ─────────────────────────────────────────

PALETTE = ["#4361ee", "#7209b7", "#f72585", "#4cc9f0", "#4895ef", "#3a0ca3"]
sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.titleweight":   "bold",
    "axes.titlesize":     14,
    "axes.labelsize":     11,
    "figure.facecolor":   "white",
    "axes.facecolor":     "#fafbff",
})

# ─────────────────────────────────────────
# Chargement des données
# ─────────────────────────────────────────

@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parents[2]
    data_dir = project_root / "shared_data"

    customers = pd.read_csv(
        data_dir / "Customers.csv",
        sep="\t"
    )
    orders = pd.read_csv(
        data_dir / "data_Orders.csv",
        encoding="latin1"
    )
    return customers, orders

customers, data_Orders = load_data()

# ─────────────────────────────────────────
# Feature Engineering
# ─────────────────────────────────────────

data_Orders["Revenue"] = data_Orders["Quantity"] * data_Orders["UnitPrice"]

customers["Age"] = 2026 - customers["Year_Birth"]

customers["Total_Spending"] = (
    customers["MntWines"] +
    customers["MntFruits"] +
    customers["MntMeatProducts"] +
    customers["MntFishProducts"] +
    customers["MntSweetProducts"] +
    customers["MntGoldProds"]
)

# ─────────────────────────────────────────
# Sidebar — Navigation
# ─────────────────────────────────────────

st.sidebar.markdown("## 📊 Analytics Hub")
st.sidebar.markdown("---")

PAGES = {
    "🏠  Accueil":          "Accueil",
    "📈  Direction":        "Direction",
    "🎯  Marketing":        "Marketing",
    "⚙️  Opérations":       "Opérations",
    "🤖  Machine Learning": "Machine Learning",
}

page_label = st.sidebar.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
page = PAGES[page_label]

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small style='opacity:.5'>DDDM Projet — S4 2026</small>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────
# ACCUEIL
# ─────────────────────────────────────────

if page == "Accueil":

    st.markdown('<div class="page-badge">Tableau de bord</div>', unsafe_allow_html=True)
    st.title("📊 Dashboard E-commerce Analytics")
    st.caption("Vue consolidée des indicateurs clés de performance")

    st.markdown("---")

    # KPIs
    total_revenue   = data_Orders["Revenue"].sum()
    nb_clients      = customers.shape[0]
    avg_spending    = customers["Total_Spending"].mean()
    nb_orders       = data_Orders["InvoiceNo"].nunique() if "InvoiceNo" in data_Orders.columns else len(data_Orders)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue",     f"{total_revenue:,.0f} €")
    col2.metric("👥 Clients",           f"{nb_clients:,}")
    col3.metric("🛒 Commandes",         f"{nb_orders:,}")
    col4.metric("📦 Dépense moyenne",   f"{avg_spending:,.1f} €")

    st.markdown("---")

    # Aperçu rapide — deux mini-graphiques côte à côte
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top 5 pays par revenu")
        top5 = (
            data_Orders.groupby("Country")["Revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        fig, ax = plt.subplots(figsize=(6, 3.5))
        bars = ax.barh(top5.index[::-1], top5.values[::-1], color=PALETTE[:5])
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x/1000:.0f}k €"))
        ax.set_xlabel("Revenu total")
        ax.bar_label(bars, fmt=lambda x: f"{x/1000:.1f}k €", padding=4, fontsize=9)
        fig.tight_layout()
        st.pyplot(fig)

    with col_right:
        st.subheader("Distribution des dépenses clients")
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.hist(customers["Total_Spending"], bins=30, color=PALETTE[2], edgecolor="white", linewidth=0.5)
        ax.set_xlabel("Dépense totale (€)")
        ax.set_ylabel("Nombre de clients")
        fig.tight_layout()
        st.pyplot(fig)

# ─────────────────────────────────────────
# DIRECTION
# ─────────────────────────────────────────

elif page == "Direction":

    st.markdown('<div class="page-badge">Direction</div>', unsafe_allow_html=True)
    st.title("📈 Vue Direction")
    st.caption("Performance financière et géographique")

    st.markdown("---")

    # Revenu par pays
    revenue_country = (
        data_Orders.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Top 10 pays par revenu")
        fig, ax = plt.subplots(figsize=(9, 4.5))
        colors = [PALETTE[0] if i == 0 else "#c5cae9" for i in range(len(revenue_country))]
        bars = ax.bar(revenue_country.index, revenue_country.values, color=colors, edgecolor="white")
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
        ax.set_ylabel("Revenu (k€)")
        ax.bar_label(bars, fmt=lambda x: f"{x/1000:.0f}k", padding=3, fontsize=8)
        plt.xticks(rotation=35, ha="right")
        fig.tight_layout()
        st.pyplot(fig)

    with col_right:
        st.subheader("Détail par pays")
        df_display = revenue_country.reset_index()
        df_display.columns = ["Pays", "Revenu (€)"]
        df_display["Revenu (€)"] = df_display["Revenu (€)"].map("{:,.0f}".format)
        st.dataframe(df_display, hide_index=True, use_container_width=True)

    st.markdown("---")

    # Volume de commandes par pays
    st.subheader("Volume de commandes — Top 10 pays")
    orders_country = (
        data_Orders.groupby("Country")["InvoiceNo"].nunique()
        .sort_values(ascending=False)
        .head(10)
        if "InvoiceNo" in data_Orders.columns
        else data_Orders.groupby("Country").size().sort_values(ascending=False).head(10)
    )
    fig, ax = plt.subplots(figsize=(11, 4))
    sns.barplot(x=orders_country.index, y=orders_country.values, palette=PALETTE, ax=ax)
    ax.set_ylabel("Nombre de commandes")
    plt.xticks(rotation=35, ha="right")
    fig.tight_layout()
    st.pyplot(fig)

# ─────────────────────────────────────────
# MARKETING
# ─────────────────────────────────────────

elif page == "Marketing":

    st.markdown('<div class="page-badge">Marketing</div>', unsafe_allow_html=True)
    st.title("🎯 Vue Marketing")
    st.caption("Analyse des campagnes et profils clients")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Réponse aux campagnes")
        response_counts = customers["Response"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 5))
        wedges, texts, autotexts = ax.pie(
            response_counts,
            labels=["Non répondants", "Répondants"],
            autopct="%1.1f%%",
            colors=[PALETTE[4], PALETTE[0]],
            startangle=90,
            wedgeprops={"edgecolor": "white", "linewidth": 2},
        )
        for at in autotexts:
            at.set_fontsize(12)
            at.set_fontweight("bold")
        ax.set_title("Taux de réponse", fontsize=14, fontweight="bold")
        fig.tight_layout()
        st.pyplot(fig)

    with col_right:
        st.subheader("Dépenses par catégorie")
        spending_cols = {
            "Vins":     "MntWines",
            "Fruits":   "MntFruits",
            "Viandes":  "MntMeatProducts",
            "Poissons": "MntFishProducts",
            "Sucreries":"MntSweetProducts",
            "Or":       "MntGoldProds",
        }
        avg_spending = {k: customers[v].mean() for k, v in spending_cols.items()}
        fig, ax = plt.subplots(figsize=(6, 4.5))
        bars = ax.barh(list(avg_spending.keys()), list(avg_spending.values()), color=PALETTE)
        ax.bar_label(bars, fmt="%.1f €", padding=4, fontsize=9)
        ax.set_xlabel("Dépense moyenne (€)")
        fig.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("Distribution de l'âge des clients")
    fig, ax = plt.subplots(figsize=(11, 3.5))
    ax.hist(customers["Age"].dropna(), bins=25, color=PALETTE[3], edgecolor="white", linewidth=0.6)
    ax.set_xlabel("Âge")
    ax.set_ylabel("Nombre de clients")
    fig.tight_layout()
    st.pyplot(fig)

# ─────────────────────────────────────────
# OPÉRATIONS
# ─────────────────────────────────────────

elif page == "Opérations":

    st.markdown('<div class="page-badge">Opérations</div>', unsafe_allow_html=True)
    st.title("⚙️ Vue Opérations")
    st.caption("Performance produits et activité transactionnelle")

    st.markdown("---")

    # Top produits
    top_products = (
        data_Orders.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("Top 10 produits par revenu")
    fig, ax = plt.subplots(figsize=(12, 4.5))
    colors = [PALETTE[0] if i < 3 else "#c5cae9" for i in range(len(top_products))]
    bars = ax.bar(range(len(top_products)), top_products.values, color=colors, edgecolor="white")
    ax.set_xticks(range(len(top_products)))
    ax.set_xticklabels(
        [t[:30] + ("…" if len(t) > 30 else "") for t in top_products.index],
        rotation=35,
        ha="right",
        fontsize=9,
    )
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x/1000:.1f}k €"))
    ax.bar_label(bars, fmt=lambda x: f"{x/1000:.1f}k", padding=3, fontsize=8)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top 10 produits — Quantité vendue")
        top_qty = (
            data_Orders.groupby("Description")["Quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        fig, ax = plt.subplots(figsize=(6, 4.5))
        ax.barh(
            [t[:28] + ("…" if len(t) > 28 else "") for t in top_qty.index[::-1]],
            top_qty.values[::-1],
            color=PALETTE[1],
        )
        ax.set_xlabel("Quantité")
        fig.tight_layout()
        st.pyplot(fig)

    with col_right:
        st.subheader("Tableau — Top 10 produits")
        df_top = top_products.reset_index()
        df_top.columns = ["Produit", "Revenu (€)"]
        df_top["Produit"] = df_top["Produit"].str[:40]
        df_top["Revenu (€)"] = df_top["Revenu (€)"].map("{:,.0f}".format)
        st.dataframe(df_top, hide_index=True, use_container_width=True, height=370)

# ─────────────────────────────────────────
# MACHINE LEARNING
# ─────────────────────────────────────────

elif page == "Machine Learning":

    st.markdown('<div class="page-badge">Machine Learning</div>', unsafe_allow_html=True)
    st.title("🤖 Vue Machine Learning")
    st.caption("Comparaison des modèles de prédiction — réponse campagne")

    st.markdown("---")

    models = pd.DataFrame({
        "Modèle":    ["Logistic Regression", "Random Forest", "Decision Tree"],
        "Accuracy":  [0.857, 0.844, 0.768],
        "Precision": [0.831, 0.819, 0.741],
        "Recall":    [0.812, 0.803, 0.724],
        "F1-Score":  [0.821, 0.811, 0.732],
    })

    # Métriques en colonnes
    col1, col2, col3 = st.columns(3)
    for col, (_, row) in zip([col1, col2, col3], models.iterrows()):
        col.metric(
            row["Modèle"],
            f"{row['Accuracy']*100:.1f}% Acc",
            f"F1 = {row['F1-Score']:.3f}"
        )

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("Accuracy par modèle")
        fig, ax = plt.subplots(figsize=(8, 4.5))
        bar_colors = [PALETTE[0], PALETTE[2], PALETTE[3]]
        bars = ax.bar(models["Modèle"], models["Accuracy"], color=bar_colors, edgecolor="white", width=0.5)
        ax.set_ylim(0.7, 0.9)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax.bar_label(bars, fmt=lambda x: f"{x*100:.1f}%", padding=4, fontsize=11, fontweight="bold")
        ax.axhline(0.80, color="gray", linestyle="--", linewidth=1, alpha=0.6, label="Baseline 80%")
        ax.legend(fontsize=9)
        fig.tight_layout()
        st.pyplot(fig)

    with col_right:
        st.subheader("Comparaison multi-métriques")
        metrics = ["Accuracy", "Precision", "Recall", "F1-Score"]
        fig, ax = plt.subplots(figsize=(6, 4.5))
        x = range(len(metrics))
        width = 0.25
        for i, (_, row) in enumerate(models.iterrows()):
            offset = (i - 1) * width
            ax.bar([xi + offset for xi in x], [row[m] for m in metrics],
                   width=width, label=row["Modèle"], color=bar_colors[i], edgecolor="white")
        ax.set_xticks(list(x))
        ax.set_xticklabels(metrics, fontsize=10)
        ax.set_ylim(0.65, 0.92)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax.legend(fontsize=8)
        fig.tight_layout()
        st.pyplot(fig)

    st.markdown("---")

    st.subheader("Tableau de synthèse")
    styled = models.copy()
    for col in ["Accuracy", "Precision", "Recall", "F1-Score"]:
        styled[col] = styled[col].map("{:.1%}".format)
    st.dataframe(styled, hide_index=True, use_container_width=True)
