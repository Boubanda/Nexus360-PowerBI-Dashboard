
import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "generated"
RESULTS_DIR = PROJECT_ROOT / "data" / "analytics"
DB_PATH = PROJECT_ROOT / "data" / "database" / "nexus360.db"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

print("=" * 55)
print("  NEXUS 360 — Chargement dans SQLite")
print("=" * 55)

# ─────────────────────────────────────────────
# 1. CONNEXION ET CHARGEMENT DES CSV
# ─────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)

tables = {
    "dim_date":       "dim_date.csv",
    "dim_geo":        "dim_geo.csv",
    "dim_entity":     "dim_entity.csv",
    "dim_kpi":        "dim_kpi.csv",
    "fact_operations":"fact_operations.csv",
}

for table_name, csv_file in tables.items():
    path = os.path.join(DATA_DIR, csv_file)
    df = pd.read_csv(path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"   ✓ {table_name:<20} {len(df):>6,} lignes chargées")

print(f"\n  Base SQLite créée : {DB_PATH}")

# ─────────────────────────────────────────────
# 2. REQUÊTES ANALYTIQUES
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  ANALYSES SQL")
print("=" * 55)

queries = {

    "1. Revenue par BU et par année": """
        SELECT 
            e.bu_name,
            d.year,
            ROUND(SUM(f.revenue), 2)        AS total_revenue,
            ROUND(SUM(f.cost), 2)           AS total_cost,
            ROUND(SUM(f.revenue - f.cost), 2) AS marge_brute,
            ROUND(AVG((f.revenue - f.cost) / f.revenue) * 100, 1) AS marge_pct
        FROM fact_operations f
        JOIN dim_entity e ON f.entity_id = e.entity_id
        JOIN dim_date   d ON f.date_id   = d.date_id
        GROUP BY e.bu_name, d.year
        ORDER BY e.bu_name, d.year
    """,

    "2. Top 5 entités les plus rentables": """
        SELECT 
            e.entity_name,
            e.bu_name,
            ROUND(SUM(f.revenue), 2)        AS total_revenue,
            ROUND(AVG((f.revenue - f.cost) / f.revenue) * 100, 1) AS marge_pct,
            COUNT(*)                         AS nb_operations
        FROM fact_operations f
        JOIN dim_entity e ON f.entity_id = e.entity_id
        GROUP BY e.entity_name, e.bu_name
        ORDER BY marge_pct DESC
        LIMIT 5
    """,

    "3. Évolution marge par trimestre": """
        SELECT 
            d.year,
            d.quarter_label,
            e.bu_name,
            ROUND(SUM(f.revenue), 2)        AS revenue,
            ROUND(AVG((f.revenue - f.cost) / f.revenue) * 100, 1) AS marge_pct
        FROM fact_operations f
        JOIN dim_entity e ON f.entity_id = e.entity_id
        JOIN dim_date   d ON f.date_id   = d.date_id
        GROUP BY d.year, d.quarter_label, e.bu_name
        ORDER BY d.year, d.quarter, e.bu_name
    """,

    "4. Détection anomalies (perf_score < 20)": """
        SELECT 
            f.operation_id,
            e.entity_name,
            e.bu_name,
            d.date,
            ROUND(f.revenue, 2) AS revenue,
            ROUND(f.cost, 2)    AS cost,
            f.perf_score,
            f.status
        FROM fact_operations f
        JOIN dim_entity e ON f.entity_id = e.entity_id
        JOIN dim_date   d ON f.date_id   = d.date_id
        WHERE f.perf_score < 20
        ORDER BY f.perf_score ASC
        LIMIT 10
    """,

    "5. Analyse saisonnalité par mois": """
        SELECT 
            d.month,
            d.month_label,
            e.bu_name,
            ROUND(AVG(f.revenue), 2) AS revenue_moyen,
            COUNT(*)                  AS nb_operations
        FROM fact_operations f
        JOIN dim_entity e ON f.entity_id = e.entity_id
        JOIN dim_date   d ON f.date_id   = d.date_id
        GROUP BY d.month, d.month_label, e.bu_name
        ORDER BY d.month, e.bu_name
    """,

    "6. KPIs les plus critiques (alerte dépassée)": """
        SELECT 
            k.kpi_name,
            k.bu_id,
            k.kpi_category,
            k.target_value,
            k.alert_threshold,
            k.unit,
            k.direction,
            ROUND(AVG(f.perf_score), 1) AS perf_score_moyen
        FROM fact_operations f
        JOIN dim_kpi k ON f.kpi_id = k.kpi_id
        GROUP BY k.kpi_name, k.bu_id
        ORDER BY perf_score_moyen ASC
        LIMIT 10
    """,

    "7. Vue Executive Summary globale": """
        SELECT
            ROUND(SUM(f.revenue), 2)                              AS total_revenue,
            ROUND(SUM(f.cost), 2)                                 AS total_cost,
            ROUND(SUM(f.revenue - f.cost), 2)                     AS marge_brute,
            ROUND(AVG((f.revenue-f.cost)/f.revenue)*100, 1)       AS marge_pct,
            COUNT(*)                                               AS nb_operations,
            ROUND(AVG(f.perf_score), 1)                           AS perf_score_moyen,
            MIN(d.year)                                            AS annee_debut,
            MAX(d.year)                                            AS annee_fin
        FROM fact_operations f
        JOIN dim_date d ON f.date_id = d.date_id
    """,

    "8. Classement géographique par revenue": """
        SELECT
            g.city,
            g.country,
            e.bu_name,
            ROUND(SUM(f.revenue), 2) AS total_revenue,
            COUNT(*)                  AS nb_operations
        FROM fact_operations f
        JOIN dim_entity e ON f.entity_id = e.entity_id
        JOIN dim_geo    g ON e.geo_id    = g.geo_id
        GROUP BY g.city, g.country, e.bu_name
        ORDER BY total_revenue DESC
    """,
}

# ─────────────────────────────────────────────
# 3. EXÉCUTION ET AFFICHAGE
# ─────────────────────────────────────────────
for title, query in queries.items():
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")
    df = pd.read_sql_query(query, conn)
    print(df.to_string(index=False))

# ─────────────────────────────────────────────
# 4. EXPORT DES RÉSULTATS EN CSV
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  EXPORT DES RÉSULTATS")
print("=" * 55)

export = {
    "revenue_by_bu_year":     list(queries.values())[0],
    "top5_entities":          list(queries.values())[1],
    "marge_by_quarter":       list(queries.values())[2],
    "anomalies":              list(queries.values())[3],
    "saisonnalite":           list(queries.values())[4],
    "kpis_critiques":         list(queries.values())[5],
    "executive_summary":      list(queries.values())[6],
    "classement_geo":         list(queries.values())[7],
}

for name, query in export.items():
    df = pd.read_sql_query(query, conn)
    df.to_csv(RESULTS_DIR / f"{name}.csv", index=False)
    print(f"   ✓ {name}.csv exporté")

conn.close()
print(f"\n  Base SQLite : {DB_PATH}")
print(f"  Résultats   : {RESULTS_DIR}")
print("=" * 55)
