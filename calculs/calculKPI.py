

def calculKPI(df):
    try:
        # --> Calculer des métriques clés
        totalSales = df["sales"].sum()
        totalProfit = df["marge_relative"].sum()
        averageProfit = df["marge_relative"].mean()
        totalQuantite = df["quantity"].sum()
        NBcommande = len(df)

        kpis = {
            "total_sales": totalSales,
            "total_profit": totalProfit,
            "average_profit": averageProfit,
            "total_quantity": totalQuantite,
            "nb_commande": NBcommande
        }

        # --> Calculer statistiques de base
        MoyenneV = df["sales"].mean()
        médianeV = df["sales"].median()
        minimumV = df["sales"].min()
        maximumV = df["sales"].max()
        écart_typeV = df["sales"].std()

        stats = {
            "moyenne_ventes": MoyenneV,
            "mediane_ventes": médianeV,
            "min_ventes": minimumV,
            "max_ventes": maximumV,
            "ecart_type_ventes": écart_typeV
        }
    
        return kpis, stats

    except Exception as e :
        print("erreur : ",e )
        return None, None