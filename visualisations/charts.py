import matplotlib.pyplot as plt
import seaborn as sns

# --> Appliquer un thème professionnel et épuré globalement
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.size': 10,
    'axes.titleweight': 'bold',
    'axes.titlesize': 13,
    'axes.labelweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False
})

def plot_ventes_par_categorie(df):
    ventes_cat = df.groupby('category_name')['sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    if not ventes_cat.empty:
        sns.barplot(data=ventes_cat, x='category_name', y='sales', ax=ax, palette='Blues_d')
        ax.tick_params(axis='x', rotation=45)
    ax.set_title("Ventes par catégorie", pad=15)
    ax.set_ylabel("Ventes ($)")
    ax.set_xlabel("")
    fig.tight_layout()
    return fig

def plot_ventes_par_mois(df):
    ventes_mois = df.groupby('mois_annee')['sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    if not ventes_mois.empty:
        sns.lineplot(data=ventes_mois, x='mois_annee', y='sales', ax=ax, marker='o', color='#2b5c8f', linewidth=2.5)
        ax.tick_params(axis='x', rotation=45)
        ax.fill_between(ventes_mois['mois_annee'], ventes_mois['sales'], color='#2b5c8f', alpha=0.1) # Effet d'aire sous la courbe
    ax.set_title("Évolution des Ventes par mois", pad=15)
    ax.set_ylabel("Ventes ($)")
    ax.set_xlabel("")
    fig.tight_layout()
    return fig

def plot_profit_par_region(df):
    profit_region = df.groupby('region_name')['profit_ratio'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    if not profit_region.empty:
        sns.barplot(data=profit_region, x='region_name', y='profit_ratio', ax=ax, palette='vlag')
    ax.set_title("Marge moyenne par région", pad=15)
    ax.set_ylabel("Marge Moyenne")
    ax.set_xlabel("")
    fig.tight_layout()
    return fig

def plot_top_produits(df):
    top_prod = df.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    if not top_prod.empty:
        # L'affichage horizontal est souvent plus lisible pour les noms longs
        sns.barplot(data=top_prod, x='sales', y='product_name', ax=ax, palette='crest')
    ax.set_title("Top 10 Produits (Ventes)", pad=15)
    ax.set_xlabel("Ventes ($)")
    ax.set_ylabel("")
    fig.tight_layout()
    return fig

def plot_distribution_profits(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    if not df['profit_ratio'].dropna().empty:
        sns.histplot(df['profit_ratio'].dropna(), bins=30, kde=True, ax=ax, color='#5c5c8f', edgecolor='white')
    ax.set_title("Distribution des Marges", pad=15)
    ax.set_xlabel("Profit Ratio")
    ax.set_ylabel("Fréquence")
    fig.tight_layout()
    return fig

def plot_top_clients(df):
    top_cli = df.groupby('customer_name')['sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    if not top_cli.empty:
        # Affichage horizontal également
        sns.barplot(data=top_cli, x='sales', y='customer_name', ax=ax, palette='mako')
    ax.set_title("Top 10 Clients (Ventes)", pad=15)
    ax.set_xlabel("Ventes ($)")
    ax.set_ylabel("")
    fig.tight_layout()
    return fig
