import streamlit as st
import pandas as pd
from connectionBD.db_connection import get_engine
from extractionDonnees.preparationDonnes import preparation
from calculs.calculKPI import calculKPI
from visualisations.charts import *



# --> Config Page & Custom Styling
st.set_page_config(page_title="Dashboard Superstore", layout="wide", page_icon="📈")

# --> CSS personnalisé pour un rendu plus pro (Premium UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');
    
    /* Masquer le menu hamburger Streamlit en haut à droite pour une UI purifiée */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Titre Graffiti principal façon Logo */
    .graffiti-container {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .main-header {
        font-family: 'Permanent Marker', cursive;
        color: #FFFFFF;
        font-size: 4rem;
        line-height: 1.1;
        letter-spacing: 3px;
        text-shadow: 
            -2px -2px 0 #000,  
             2px -2px 0 #000,
            -2px  2px 0 #000,
             2px  2px 0 #000,
             4px  4px 0 #000,
             6px  6px 0 #000,
             8px  8px 0 #000;
        transform: rotate(-3deg);
        display: inline-block;
    }
    .gold-accent {
        color: #CBA135 !important;
    }
    
    /* Une police urbaine mais LISIBLE (Oswald) pour les sous-titres et autres headings */
    .sub-header {
        font-family: 'Oswald', sans-serif !important;
        color: var(--text-color);
        font-size: 1.3rem;
        text-align: center;
        margin-top: 15px;
        letter-spacing: 1px;
    }
    
    h1, h2, h3 {
        font-family: 'Oswald', sans-serif !important;
        color: var(--text-color) !important;
        letter-spacing: 1px;
    }

    /* Cartes metrics stylisées et adaptées */
    div[data-testid="metric-container"] {
        background-color: var(--secondary-background-color) !important;
        border-left: 5px solid #CBA135 !important;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4) !important;
        transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
    }
    
    /* Valeurs des KPIs façon graffiti or (plus lisible) */
    [data-testid="stMetricValue"] {
        font-family: 'Permanent Marker', cursive !important;
        color: #CBA135 !important;
        text-shadow: 
            -1px -1px 0 #000,  
             1px -1px 0 #000,
            -1px  1px 0 #000,
             1px  1px 0 #000,
             2px  2px 0 #000 !important;
    }
    
    /* Libellés des KPIs avec Oswald */
    [data-testid="stMetricLabel"] {
        font-family: 'Oswald', sans-serif !important;
        color: var(--text-color) !important;
        font-size: 1.1rem !important;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('''
<div class="graffiti-container">
    <div class="main-header">
        DASHBOARD <br><span class="gold-accent">SUPERSTORE</span>
    </div>
    <div class="sub-header">📊 Analyse interactive des ventes, profits et tendances</div>
</div>
''', unsafe_allow_html=True)



# --> Charger les Données
@st.cache_resource
def load_db_engine():
    return get_engine()

@st.cache_data
def load_data():
    engine = load_db_engine()
    if engine is None:
        st.error("Erreur de connexion à la base de données. Vérifiez votre fichier .env")
        st.stop()
    df, _, _, _ = preparation(engine)
    return df

with st.spinner("Synchronisation des données PostgreSQL..."):
    df = load_data()

if df.empty:
    st.warning("Alerte: Aucune donnée locale trouvée dans la base.")
    st.stop()


# --> Sidebar Filters
with st.sidebar:
    st.image("images/logo.png", width=120)
    st.title("Filtres")
    st.markdown("Affinez votre analyse :")

    regions = st.multiselect(
        "📍 Région",
        options=sorted(df['region_name'].dropna().unique()),
        default=sorted(df['region_name'].dropna().unique())
    )

    categories = st.multiselect(
        "🏷️ Catégorie",
        options=sorted(df['category_name'].dropna().unique()),
        default=sorted(df['category_name'].dropna().unique())
    )

    annees_options = sorted(df['annee'].dropna().unique()) if 'annee' in df.columns else []
    if annees_options:
        annees = st.multiselect(
            "📅 Année",
            options=annees_options,
            default=annees_options
        )
    else:
        annees = []

mask = (df['region_name'].isin(regions)) & (df['category_name'].isin(categories))
if annees:
    mask = mask & (df['annee'].isin(annees))

df_filtered = df[mask]

if df_filtered.empty:
    st.info("Aucune donnée pour les filtres actuels. Veuillez élargir votre sélection.")
    st.stop()


# --> KPIs et Statistiques
kpis, stats = calculKPI(df_filtered)

if kpis and stats:
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💰 Total Ventes", f"${kpis['total_sales']:,.0f}")
    col2.metric("📈 Profit Total", f"${kpis['total_profit']:,.0f}")
    col3.metric("📊 Marge Moyenne", f"{kpis['average_profit']:.1%}")
    col4.metric("📦 Qtés Vendues", f"{kpis['total_quantity']:,}")
    col5.metric("🛒 Commandes", f"{kpis['nb_commande']:,}")
    
    st.write("") # Espace


# --> Graphiques - Structure en Onglets
tab1, tab2, tab3 = st.tabs(["📈 Tendances & Ventes", "🌍 Marges & Distributions", "🏆 Top Performances"])

with tab1:
    st.markdown("### Aperçu des Ventes")
    row1_c1, row1_c2 = st.columns([6, 4])
    with row1_c1:
        st.pyplot(plot_ventes_par_mois(df_filtered), use_container_width=True)
    with row1_c2:
        st.pyplot(plot_ventes_par_categorie(df_filtered), use_container_width=True)

with tab2:
    st.markdown("### Analyse de Rentabilité")
    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.pyplot(plot_profit_par_region(df_filtered), use_container_width=True)
    with row2_c2:
        st.pyplot(plot_distribution_profits(df_filtered), use_container_width=True)

with tab3:
    st.markdown("### Leaderboard")
    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        st.pyplot(plot_top_produits(df_filtered), use_container_width=True)
    with row3_c2:
        st.pyplot(plot_top_clients(df_filtered), use_container_width=True)

# Section d'exploration de données brute (en bas dans un expander discret)
st.markdown("---")
with st.expander("🔍 Voir les données brutes & statistiques"):
    col_stat1, col_stat2 = st.columns([1, 2])
    with col_stat1:
        st.markdown("**Statistiques descriptives (Ventes) :**")
        df_stats = pd.DataFrame.from_dict(stats, orient='index', columns=['Valeur'])
        df_stats['Valeur'] = df_stats['Valeur'].apply(lambda x: f"{x:,.2f}")
        st.dataframe(df_stats, use_container_width=True)
    with col_stat2:
        st.markdown("**Aperçu du dataset filtré :**")
        st.dataframe(df_filtered.head(100), use_container_width=True, height=200)