import pandas as pd

def preparation(engine):
    try:
        print("\n ------> preparation des donnees ")

        query = """
            SELECT 
                v.sales, v.marge_relative, v.quantity,
                r.region_name, c.category_name, d.order_date,
                p.product_name, cl.customer_name
            FROM ventes v
            FULL OUTER JOIN commande co ON v.order_id = co.order_id
            FULL OUTER JOIN date_temps d ON co.date_id = d.date_id
            FULL OUTER JOIN produit p ON v.product_id = p.product_id
            FULL OUTER JOIN sous_categorie sc ON p.sub_category_id = sc.sub_category_id
            FULL OUTER JOIN categorie c ON sc.category_id = c.category_id
            FULL OUTER JOIN client cl ON co.customer_id = cl.customer_id
            FULL OUTER JOIN localisation l ON co.postal_code = l.postal_code
            FULL OUTER JOIN etat e ON l.state_id = e.state_id
            FULL OUTER JOIN region r ON e.region_id = r.region_id
        """

        # --> charger data
        df = pd.read_sql(query, engine)

        # --> Nettoyage des colonnes
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

        # --> Conversion des dates
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

        # --> Vérifier valeurs manquantes
        print("\nValeurs manquantes :")
        print(df.isnull().sum())

        # --> Feature Engineering
        # mois / année
        df['annee'] = df['order_date'].dt.year
        df['mois'] = df['order_date'].dt.month
        df['mois_annee'] = df['order_date'].dt.to_period('M').astype(str)
        # profit ratio
        df['profit_ratio'] = df['marge_relative']

        # --> Agrégations
        # ventes par mois
        ventes_par_mois = df.groupby('mois_annee')['sales'].sum().reset_index()
        # top produits
        top_products = (
            df.groupby('product_name')['sales']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        # top clients
        top_clients = (
            df.groupby('customer_name')['sales']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        print("\n[OK] preparation terminee")

        return df, ventes_par_mois, top_products, top_clients

    except Exception as e:
        print("erreur :", e)
