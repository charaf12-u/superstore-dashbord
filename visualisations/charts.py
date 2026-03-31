import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# --> Thème global dark
DARK_BG = '#1a1a1a'
CARD_BG = '#242424'
GOLD    = '#CBA135'
BLUE    = '#4A9EE0'
TEAL    = '#2EC4A5'
TEXT    = '#FFFFFF'
SUBTEXT = '#AAAAAA'

def _apply_dark_style(fig, ax):
    """Applique le style dark sur fig + ax"""
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=SUBTEXT, labelsize=9)
    ax.xaxis.label.set_color(SUBTEXT)
    ax.yaxis.label.set_color(SUBTEXT)
    ax.title.set_color(TEXT)
    ax.title.set_fontfamily('DejaVu Sans')
    ax.title.set_fontweight('bold')
    ax.title.set_fontsize(13)
    ax.title.set_text(ax.get_title().upper())
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')
    ax.yaxis.grid(True, color='#2e2e2e', linewidth=0.8, linestyle='--')
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)


def plot_ventes_par_mois(df):
    ventes_mois = df.groupby('mois_annee')['sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    if not ventes_mois.empty:
        ax.plot(ventes_mois['mois_annee'], ventes_mois['sales'],
                color=BLUE, linewidth=2.5, marker='o', markersize=4, zorder=3)
        ax.fill_between(ventes_mois['mois_annee'], ventes_mois['sales'],
                        color=BLUE, alpha=0.15)
        ax.tick_params(axis='x', rotation=90)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.set_title("Évolution des Ventes par mois", pad=15)
    ax.set_ylabel("Ventes ($)")
    ax.set_xlabel("")
    _apply_dark_style(fig, ax)
    fig.tight_layout()
    return fig


def plot_ventes_par_categorie(df):
    ventes_cat = df.groupby('category_name')['sales'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    if not ventes_cat.empty:
        colors = [BLUE, GOLD, TEAL][:len(ventes_cat)]
        bars = ax.bar(ventes_cat['category_name'], ventes_cat['sales'],
                      color=colors, width=0.5, zorder=3)
        # Valeurs sur les barres
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h * 1.01,
                    f'${h/1000:.0f}k', ha='center', va='bottom',
                    color=TEXT, fontsize=9, fontweight='bold')
        ax.tick_params(axis='x', rotation=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
    ax.set_title("Ventes par catégorie", pad=15)
    ax.set_ylabel("Ventes ($)")
    ax.set_xlabel("")
    _apply_dark_style(fig, ax)
    fig.tight_layout()
    return fig


def plot_profit_par_region(df):
    profit_region = df.groupby('region_name')['profit_ratio'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    if not profit_region.empty:
        colors = [BLUE, GOLD, TEAL, '#E05A5A'][:len(profit_region)]
        bars = ax.bar(profit_region['region_name'], profit_region['profit_ratio'],
                      color=colors, width=0.5, zorder=3)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h * 1.01,
                    f'{h:.1%}', ha='center', va='bottom',
                    color=TEXT, fontsize=9, fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0%}'))
    ax.set_title("Marge moyenne par région", pad=15)
    ax.set_ylabel("Marge Moyenne")
    ax.set_xlabel("")
    _apply_dark_style(fig, ax)
    fig.tight_layout()
    return fig


def plot_distribution_profits(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    data = df['profit_ratio'].dropna()
    if not data.empty:
        ax.hist(data, bins=30, color=BLUE, alpha=0.7,
                edgecolor='#333333', zorder=3)
        # KDE line
        from scipy.stats import gaussian_kde
        import numpy as np
        kde = gaussian_kde(data)
        x_range = np.linspace(data.min(), data.max(), 200)
        ax2 = ax.twinx()
        ax2.plot(x_range, kde(x_range), color=GOLD, linewidth=2.5)
        ax2.set_yticks([])
        ax2.set_facecolor(CARD_BG)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0%}'))
    ax.set_title("Distribution des Marges", pad=15)
    ax.set_xlabel("Profit Ratio")
    ax.set_ylabel("Fréquence")
    _apply_dark_style(fig, ax)
    fig.tight_layout()
    return fig


def plot_top_produits(df):
    top_prod = (df.groupby('product_name')['sales']
                  .sum().sort_values(ascending=True)
                  .tail(10).reset_index())
    fig, ax = plt.subplots(figsize=(10, 6))
    if not top_prod.empty:
        colors = [BLUE if i % 2 == 0 else TEAL for i in range(len(top_prod))]
        bars = ax.barh(top_prod['product_name'], top_prod['sales'],
                       color=colors, height=0.6, zorder=3)
        for bar in bars:
            w = bar.get_width()
            ax.text(w * 1.01, bar.get_y() + bar.get_height()/2,
                    f'${w/1000:.0f}k', va='center',
                    color=TEXT, fontsize=8, fontweight='bold')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
    ax.set_title("Top 10 Produits (Ventes)", pad=15)
    ax.set_xlabel("Ventes ($)")
    ax.set_ylabel("")
    _apply_dark_style(fig, ax)
    fig.tight_layout()
    return fig


def plot_top_clients(df):
    top_cli = (df.groupby('customer_name')['sales']
                 .sum().sort_values(ascending=True)
                 .tail(10).reset_index())
    fig, ax = plt.subplots(figsize=(10, 6))
    if not top_cli.empty:
        colors = [GOLD if i % 2 == 0 else '#E08A4A' for i in range(len(top_cli))]
        bars = ax.barh(top_cli['customer_name'], top_cli['sales'],
                       color=colors, height=0.6, zorder=3)
        for bar in bars:
            w = bar.get_width()
            ax.text(w * 1.01, bar.get_y() + bar.get_height()/2,
                    f'${w/1000:.0f}k', va='center',
                    color=TEXT, fontsize=8, fontweight='bold')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1000:.0f}k'))
    ax.set_title("Top 10 Clients (Ventes)", pad=15)
    ax.set_xlabel("Ventes ($)")
    ax.set_ylabel("")
    _apply_dark_style(fig, ax)
    fig.tight_layout()
    return fig
