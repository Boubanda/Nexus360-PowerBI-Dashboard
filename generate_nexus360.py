"""
=============================================================
  NEXUS 360 — Générateur de données synthétiques
  Projet Power BI multi-secteurs
  5 fichiers CSV : fact_operations, dim_date, dim_entity,
                   dim_kpi, dim_geo
=============================================================
"""

import pandas as pd
import numpy as np
from datetime import date, timedelta
import random
import os

# Reproductibilité
np.random.seed(42)
random.seed(42)

OUTPUT_DIR = "nexus360_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 55)
print("  NEXUS 360 — Génération des données synthétiques")
print("=" * 55)


# ─────────────────────────────────────────────
# 1. DIM_DATE
# ─────────────────────────────────────────────
print("\n[1/5] Génération de Dim_Date...")

start_date = date(2021, 1, 1)
end_date   = date(2024, 12, 31)

dates = pd.date_range(start=start_date, end=end_date, freq="D")

FRENCH_MONTHS = {
    1:"Janvier", 2:"Février",  3:"Mars",      4:"Avril",
    5:"Mai",     6:"Juin",     7:"Juillet",   8:"Août",
    9:"Septembre",10:"Octobre",11:"Novembre",12:"Décembre"
}
FRENCH_DAYS = {
    0:"Lundi", 1:"Mardi", 2:"Mercredi", 3:"Jeudi",
    4:"Vendredi", 5:"Samedi", 6:"Dimanche"
}

dim_date = pd.DataFrame({
    "date_id":        dates.strftime("%Y%m%d").astype(int),
    "date":           dates.strftime("%Y-%m-%d"),
    "year":           dates.year,
    "quarter":        dates.quarter,
    "quarter_label":  ["Q" + str(q) for q in dates.quarter],
    "month":          dates.month,
    "month_label":    [FRENCH_MONTHS[m] for m in dates.month],
    "week":           dates.isocalendar().week.astype(int),
    "day":            dates.day,
    "day_of_week":    dates.dayofweek,
    "day_label":      [FRENCH_DAYS[d] for d in dates.dayofweek],
    "is_weekend":     dates.dayofweek >= 5,
    "is_month_start": dates.is_month_start,
    "is_month_end":   dates.is_month_end,
    "fiscal_year":    np.where(dates.month >= 10, dates.year + 1, dates.year),
    "fiscal_period":  np.where(dates.month >= 10,
                               dates.month - 9,
                               dates.month + 3),
})

dim_date.to_csv(f"{OUTPUT_DIR}/dim_date.csv", index=False)
print(f"   ✓ {len(dim_date):,} lignes — dim_date.csv")


# ─────────────────────────────────────────────
# 2. DIM_GEO
# ─────────────────────────────────────────────
print("\n[2/5] Génération de Dim_Geo...")

geo_data = [
    # --- AeroMRO sites ---
    ("GEO001", "France",     "Île-de-France",   "Paris",      48.8566,  2.3522,  "hub"),
    ("GEO002", "France",     "Occitanie",       "Toulouse",   43.6047,  1.4442,  "hub"),
    ("GEO003", "Allemagne",  "Bavière",         "Munich",     48.1351, 11.5820,  "site"),
    ("GEO004", "Espagne",    "Catalogne",       "Barcelone",  41.3851,  2.1734,  "site"),
    ("GEO005", "Royaume-Uni","Angleterre",      "Londres",    51.5074, -0.1278,  "site"),
    # --- FinServ sites ---
    ("GEO006", "France",     "Île-de-France",   "La Défense", 48.8924,  2.2360,  "hub"),
    ("GEO007", "Luxembourg", "Luxembourg",      "Luxembourg", 49.6116,  6.1319,  "hub"),
    ("GEO008", "Suisse",     "Genève",          "Genève",     46.2044,  6.1432,  "site"),
    ("GEO009", "Pays-Bas",   "Hollande-du-Nord","Amsterdam",  52.3676,  4.9041,  "site"),
    ("GEO010", "Belgique",   "Bruxelles",       "Bruxelles",  50.8503,  4.3517,  "site"),
    # --- MedOps sites ---
    ("GEO011", "France",     "Île-de-France",   "Paris",      48.8566,  2.3522,  "hub"),
    ("GEO012", "France",     "Auvergne-Rhône",  "Lyon",       45.7640,  4.8357,  "hub"),
    ("GEO013", "France",     "PACA",            "Marseille",  43.2965,  5.3698,  "site"),
    ("GEO014", "France",     "Bretagne",        "Rennes",     48.1173, -1.6778,  "site"),
    ("GEO015", "France",     "Hauts-de-France", "Lille",      50.6292,  3.0573,  "site"),
]

dim_geo = pd.DataFrame(geo_data, columns=[
    "geo_id","country","region","city",
    "latitude","longitude","zone_type"
])

dim_geo.to_csv(f"{OUTPUT_DIR}/dim_geo.csv", index=False)
print(f"   ✓ {len(dim_geo):,} lignes — dim_geo.csv")


# ─────────────────────────────────────────────
# 3. DIM_ENTITY
# ─────────────────────────────────────────────
print("\n[3/5] Génération de Dim_Entity...")

entity_data = [
    # BU: AeroMRO
    ("ENT001","BU001","AeroMRO","MRO Paris CDG",      "Base de maintenance","GEO001"),
    ("ENT002","BU001","AeroMRO","MRO Toulouse",        "Centre d'excellence", "GEO002"),
    ("ENT003","BU001","AeroMRO","MRO Munich",          "Base régionale",      "GEO003"),
    ("ENT004","BU001","AeroMRO","MRO Barcelone",       "Base régionale",      "GEO004"),
    ("ENT005","BU001","AeroMRO","MRO London Heathrow", "Base régionale",      "GEO005"),
    ("ENT006","BU001","AeroMRO","Centre Avionique",    "Spécialiste avionique","GEO002"),
    ("ENT007","BU001","AeroMRO","Atelier Moteurs",     "Révision moteurs",    "GEO001"),

    # BU: FinServ
    ("ENT008","BU002","FinServ Risk","Corporate Banking",    "Banque corporative",  "GEO006"),
    ("ENT009","BU002","FinServ Risk","Retail Banking",       "Banque de détail",    "GEO006"),
    ("ENT010","BU002","FinServ Risk","Asset Management",     "Gestion d'actifs",    "GEO007"),
    ("ENT011","BU002","FinServ Risk","Trade Finance",        "Finance commerciale", "GEO008"),
    ("ENT012","BU002","FinServ Risk","Risk & Compliance",    "Gestion des risques", "GEO009"),
    ("ENT013","BU002","FinServ Risk","Private Equity Desk",  "Capital investissement","GEO010"),

    # BU: MedOps
    ("ENT014","BU003","MedOps","Hôpital Paris Nord",   "Médecine générale",   "GEO011"),
    ("ENT015","BU003","MedOps","Clinique Lyon Sud",    "Chirurgie",           "GEO012"),
    ("ENT016","BU003","MedOps","Centre Oncologie",     "Oncologie",           "GEO011"),
    ("ENT017","BU003","MedOps","Polyclinique Marseille","Multi-spécialités",  "GEO013"),
    ("ENT018","BU003","MedOps","Clinique Rennes",      "Cardiologie",         "GEO014"),
    ("ENT019","BU003","MedOps","Centre Urgences Lille","Urgences 24h",        "GEO015"),
]

dim_entity = pd.DataFrame(entity_data, columns=[
    "entity_id","bu_id","bu_name",
    "entity_name","entity_type","geo_id"
])

dim_entity.to_csv(f"{OUTPUT_DIR}/dim_entity.csv", index=False)
print(f"   ✓ {len(dim_entity):,} lignes — dim_entity.csv")


# ─────────────────────────────────────────────
# 4. DIM_KPI
# ─────────────────────────────────────────────
print("\n[4/5] Génération de Dim_KPI...")

kpi_data = [
    # AeroMRO KPIs
    ("KPI001","BU001","MTBF (Mean Time Between Failures)",
     "Fiabilité","heures",2000,1500,"higher_is_better"),
    ("KPI002","BU001","Disponibilité flotte",
     "Performance","%",98.0,95.0,"higher_is_better"),
    ("KPI003","BU001","Coût par intervention",
     "Finance","€",8000,12000,"lower_is_better"),
    ("KPI004","BU001","Turn Around Time (TAT)",
     "Délai","jours",5,10,"lower_is_better"),
    ("KPI005","BU001","Taux de panne critique",
     "Sécurité","%",0.5,2.0,"lower_is_better"),
    ("KPI006","BU001","Taux de conformité réglementaire",
     "Conformité","%",99.5,98.0,"higher_is_better"),

    # FinServ KPIs
    ("KPI007","BU002","VaR 95% (Value at Risk)",
     "Risque marché","M€",50,80,"lower_is_better"),
    ("KPI008","BU002","NPL Ratio (Non-Performing Loans)",
     "Risque crédit","%",2.5,5.0,"lower_is_better"),
    ("KPI009","BU002","Capital Adequacy Ratio (CAR)",
     "Solvabilité","%",15,12,"higher_is_better"),
    ("KPI010","BU002","Net Interest Margin (NIM)",
     "Rentabilité","%",3.2,2.0,"higher_is_better"),
    ("KPI011","BU002","Taux de défaut",
     "Risque crédit","%",1.5,3.5,"lower_is_better"),
    ("KPI012","BU002","Return on Equity (ROE)",
     "Rentabilité","%",12,8,"higher_is_better"),

    # MedOps KPIs
    ("KPI013","BU003","Taux d'occupation",
     "Capacité","%",85,70,"higher_is_better"),
    ("KPI014","BU003","Durée Moyenne de Séjour (DMS)",
     "Efficacité","jours",4.5,7,"lower_is_better"),
    ("KPI015","BU003","Coût par séjour",
     "Finance","€",3500,5000,"lower_is_better"),
    ("KPI016","BU003","Taux de réadmission à 30j",
     "Qualité","%",8,15,"lower_is_better"),
    ("KPI017","BU003","Délai prise en charge urgences",
     "Qualité","minutes",25,45,"lower_is_better"),
    ("KPI018","BU003","Satisfaction patient (NPS)",
     "Qualité","score",72,50,"higher_is_better"),
]

dim_kpi = pd.DataFrame(kpi_data, columns=[
    "kpi_id","bu_id","kpi_name",
    "kpi_category","unit","target_value",
    "alert_threshold","direction"
])

dim_kpi.to_csv(f"{OUTPUT_DIR}/dim_kpi.csv", index=False)
print(f"   ✓ {len(dim_kpi):,} lignes — dim_kpi.csv")


# ─────────────────────────────────────────────
# 5. FACT_OPERATIONS
# ─────────────────────────────────────────────
print("\n[5/5] Génération de Fact_Operations (~50 000 lignes)...")

# ── Helpers ──────────────────────────────────

def seasonal_factor(month, bu):
    """Facteur saisonnier réaliste par BU et mois."""
    if bu == "BU001":  # AeroMRO — pic été et hiver (forte activité aéronautique)
        return {1:1.05,2:0.95,3:1.0,4:1.05,5:1.1,6:1.2,
                7:1.25,8:1.2,9:1.1,10:1.0,11:0.95,12:1.05}[month]
    elif bu == "BU002":  # FinServ — pic T1 et T4 (clôtures)
        return {1:1.15,2:1.1,3:1.2,4:0.95,5:0.9,6:1.0,
                7:0.85,8:0.8,9:1.0,10:1.05,11:1.1,12:1.25}[month]
    else:              # MedOps — pic hiver (pathologies saisonnières)
        return {1:1.2,2:1.15,3:1.05,4:0.95,5:0.9,6:0.85,
                7:0.8,8:0.75,9:0.95,10:1.0,11:1.1,12:1.2}[month]

def yoy_growth(year, bu):
    """Tendance de croissance annuelle réaliste."""
    trends = {
        "BU001": {2021:1.0, 2022:1.08, 2023:1.15, 2024:1.22},
        "BU002": {2021:1.0, 2022:0.95, 2023:1.05, 2024:1.12},
        "BU003": {2021:1.0, 2022:1.12, 2023:1.18, 2024:1.25},
    }
    return trends[bu][year]

# ── Paramètres par BU ────────────────────────

BU_PARAMS = {
    "BU001": {  # AeroMRO
        "entities":    ["ENT001","ENT002","ENT003","ENT004","ENT005","ENT006","ENT007"],
        "kpis":        ["KPI001","KPI002","KPI003","KPI004","KPI005","KPI006"],
        "rows_per_day": 4,
        "rev_base":    85_000,  "rev_std":  20_000,
        "cost_ratio":  0.68,    "cost_std": 0.06,
        "qty_base":    3,       "qty_std":  2,
        "duration":    (2, 15),
        "status_weights": [0.78, 0.12, 0.06, 0.04],
    },
    "BU002": {  # FinServ
        "entities":    ["ENT008","ENT009","ENT010","ENT011","ENT012","ENT013"],
        "kpis":        ["KPI007","KPI008","KPI009","KPI010","KPI011","KPI012"],
        "rows_per_day": 4,
        "rev_base":    220_000, "rev_std":  80_000,
        "cost_ratio":  0.42,    "cost_std": 0.08,
        "qty_base":    1,       "qty_std":  1,
        "duration":    (1, 30),
        "status_weights": [0.82, 0.08, 0.06, 0.04],
    },
    "BU003": {  # MedOps
        "entities":    ["ENT014","ENT015","ENT016","ENT017","ENT018","ENT019"],
        "kpis":        ["KPI013","KPI014","KPI015","KPI016","KPI017","KPI018"],
        "rows_per_day": 4,
        "rev_base":    45_000,  "rev_std":  15_000,
        "cost_ratio":  0.75,    "cost_std": 0.07,
        "qty_base":    12,      "qty_std":  5,
        "duration":    (1, 20),
        "status_weights": [0.80, 0.10, 0.07, 0.03],
    },
}

STATUSES = ["Terminé", "En cours", "Annulé", "En retard"]

# ── Génération ligne par ligne ────────────────

rows = []
op_id = 1

all_dates = pd.date_range("2021-01-01", "2024-12-31", freq="D")

for d in all_dates:
    month = d.month
    year  = d.year
    date_id = int(d.strftime("%Y%m%d"))

    for bu_id, params in BU_PARAMS.items():
        n_rows = params["rows_per_day"]
        # Légère variation quotidienne
        n_rows = max(1, int(np.random.poisson(n_rows)))

        sf = seasonal_factor(month, bu_id)
        gf = yoy_growth(year, bu_id)

        for _ in range(n_rows):
            entity_id = random.choice(params["entities"])
            kpi_id    = random.choice(params["kpis"])

            # Géo via entity → geo mapping
            entity_row = dim_entity[dim_entity["entity_id"] == entity_id].iloc[0]
            geo_id = entity_row["geo_id"]
            bu_name = entity_row["bu_name"]

            # Revenue avec saisonnalité, tendance et bruit
            rev = max(0, np.random.normal(
                params["rev_base"] * sf * gf,
                params["rev_std"]
            ))

            # Coût corrélé au revenue
            cost_ratio = np.random.normal(params["cost_ratio"], params["cost_std"])
            cost_ratio = np.clip(cost_ratio, 0.2, 0.99)
            cost = rev * cost_ratio

            # Quantité
            qty = max(1, int(np.random.normal(params["qty_base"], params["qty_std"])))

            # Durée (jours)
            dur_min, dur_max = params["duration"]
            duration = random.randint(dur_min, dur_max)

            # Statut
            status = random.choices(STATUSES, weights=params["status_weights"])[0]

            # Score de performance (0-100, corrélé à la marge)
            margin = (rev - cost) / rev if rev > 0 else 0
            perf_score = round(np.clip(margin * 120 + np.random.normal(10, 8), 0, 100), 1)

            rows.append({
                "operation_id":  f"OP{op_id:07d}",
                "date_id":       date_id,
                "entity_id":     entity_id,
                "bu_id":         bu_id,
                "bu_name":       bu_name,
                "kpi_id":        kpi_id,
                "geo_id":        geo_id,
                "revenue":       round(rev, 2),
                "cost":          round(cost, 2),
                "quantity":      qty,
                "duration_days": duration,
                "status":        status,
                "perf_score":    perf_score,
            })
            op_id += 1

fact_operations = pd.DataFrame(rows)

# ── Tri et export ─────────────────────────────
fact_operations.sort_values("operation_id", inplace=True)
fact_operations.to_csv(f"{OUTPUT_DIR}/fact_operations.csv", index=False)
print(f"   ✓ {len(fact_operations):,} lignes — fact_operations.csv")


# ─────────────────────────────────────────────
# RÉSUMÉ FINAL
# ─────────────────────────────────────────────
print("\n" + "=" * 55)
print("  GÉNÉRATION TERMINÉE")
print("=" * 55)
print(f"\n  Dossier de sortie : ./{OUTPUT_DIR}/\n")

files = [
    ("dim_date.csv",         len(dim_date),         "Table de temps complète 2021-2024"),
    ("dim_geo.csv",          len(dim_geo),           "15 sites géographiques"),
    ("dim_entity.csv",       len(dim_entity),        "19 entités sur 3 BUs"),
    ("dim_kpi.csv",          len(dim_kpi),           "18 KPIs métier définis"),
    ("fact_operations.csv",  len(fact_operations),   "Table de faits principale"),
]

total_mb = 0
for fname, nrows, desc in files:
    path = f"{OUTPUT_DIR}/{fname}"
    size_kb = os.path.getsize(path) / 1024
    total_mb += size_kb / 1024
    print(f"  {fname:<28} {nrows:>7,} lignes   {size_kb:>7.1f} KB   {desc}")

print(f"\n  Total : {total_mb:.1f} MB")

print("\n  VÉRIFICATION RAPIDE — Fact_Operations :")
print(f"  • Revenue moyen   : {fact_operations['revenue'].mean():>12,.0f} €")
print(f"  • Revenue total   : {fact_operations['revenue'].sum():>12,.0f} €")
print(f"  • Marge moyenne   : {((fact_operations['revenue']-fact_operations['cost'])/fact_operations['revenue']).mean()*100:>11.1f} %")
print(f"  • Répartition BU  :")
for bu, grp in fact_operations.groupby("bu_name"):
    pct = len(grp) / len(fact_operations) * 100
    print(f"      {bu:<20} {len(grp):>6,} ops   ({pct:.0f}%)")

print("\n  Prochaine étape → Importer les CSV dans Power BI Desktop")
print("=" * 55)
