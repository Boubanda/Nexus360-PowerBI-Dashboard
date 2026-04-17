# 📊 Nexus 360 — Multi-Sector Business Intelligence Dashboard

<div align="center">

![Banner](https://img.shields.io/badge/NEXUS%20360-Business%20Intelligence-1A56DB?style=for-the-badge&labelColor=1E2A3B)

[![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Python%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)

**Dashboard décisionnel multi-secteurs couvrant 3 Business Units, 17 669 opérations et 2,27 milliards € de revenue analysés sur 4 ans (2021–2024)**

[📥 Télécharger le rapport](#installation) · [📊 Voir les pages](#pages-du-rapport) · [🗄️ Analyses SQL](#analyses-sql)

</div>

---

## 📌 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture des données](#architecture-des-données)
- [Stack technique](#stack-technique)
- [Pages du rapport](#pages-du-rapport)
- [Mesures DAX](#mesures-dax)
- [Analyses SQL](#analyses-sql)
- [Insights clés](#insights-clés)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [Auteur](#auteur)

---

## 🎯 Vue d'ensemble

**Nexus 360** est un projet complet de Business Intelligence simulant le système de pilotage décisionnel d'un groupe multi-activités. Il couvre 3 Business Units aux logiques métier distinctes :

| Business Unit | Secteur | Couleur | Entités |
|---------------|---------|---------|---------|
| ✈️ **AeroMRO** | Maintenance aéronautique (MRO) | Vert `#064E3B` | 7 bases MRO en Europe |
| 💰 **FinServ Risk** | Finance & gestion des risques | Bordeaux `#831843` | 6 desks financiers |
| 🏥 **MedOps** | Performance hospitalière | Orange `#7C2D12` | 6 établissements de santé |

### Chiffres clés du projet

```
┌─────────────────────┬──────────────────────┬───────────────────────┐
│  Revenue Total       │  Marge Moyenne        │  Nb Opérations        │
│  2,27 Milliards €    │  38,3 %               │  17 669               │
├─────────────────────┼──────────────────────┼───────────────────────┤
│  Période analysée    │  Sites géographiques  │  KPIs métier définis  │
│  2021 → 2024         │  15 villes (9 pays)   │  18 KPIs              │
└─────────────────────┴──────────────────────┴───────────────────────┘
```

---

## 🗄️ Architecture des données

### Modèle en étoile (Star Schema)

```
                    ┌─────────────┐
                    │  Dim_Entity │
                    │  19 entités │
                    └──────┬──────┘
                           │
┌──────────────┐    ┌──────┴────────────┐    ┌─────────────┐
│   Dim_Date   │    │  Fact_Operations  │    │   Dim_Geo   │
│  1 461 jours │────│   17 669 lignes   │────│  15 sites   │
└──────────────┘    └──────┬────────────┘    └─────────────┘
                           │
                    ┌──────┴──────┐
                    │   Dim_KPI   │
                    │  18 KPIs    │
                    └─────────────┘
```

### Description des tables

| Table | Lignes | Taille | Description |
|-------|-------:|-------:|-------------|
| `fact_operations` | 17 669 | 1 614 KB | Table de faits centrale — opérations avec revenue, cost, perf_score |
| `dim_date` | 1 461 | 115 KB | Calendrier complet 2021–2024 avec labels FR, trimestres fiscaux |
| `dim_entity` | 19 | 1.3 KB | Entités des 3 BUs avec types et géolocalisation |
| `dim_kpi` | 18 | 1.5 KB | KPIs métier avec valeurs cibles et seuils d'alerte |
| `dim_geo` | 15 | 0.9 KB | Sites géographiques avec coordonnées GPS réelles |

### Génération des données synthétiques

Les données sont générées avec une **saisonnalité réaliste par BU** :

```python
# Logique de saisonnalité implémentée
AeroMRO     → Pic en été (juillet/août)     — activité MRO estivale
FinServ Risk → Pic en T1 et T4              — clôtures comptables
MedOps       → Pic en hiver (jan/fév/déc)  — pathologies saisonnières
```

Et une **tendance de croissance annuelle différenciée** :

| BU | 2021 | 2022 | 2023 | 2024 |
|----|:----:|:----:|:----:|:----:|
| AeroMRO | base | +8% | +15% | +22% |
| FinServ Risk | base | -5% | +5% | +12% |
| MedOps | base | +12% | +18% | +25% |

---

## 🛠️ Stack technique

### Langages & outils

| Outil | Usage | Version |
|-------|-------|---------|
| **Python** | Génération données synthétiques, ETL, SQL | 3.11 |
| **Power BI Desktop** | Modélisation, DAX, visualisation | Latest |
| **SQLite** | Base de données relationnelle, requêtes analytiques | 3.x |
| **Pandas** | Manipulation et export des données | 2.x |
| **NumPy** | Distributions statistiques réalistes | 1.x |
| **Azure Maps** | Cartographie géospatiale dans Power BI | — |

### Visuels Power BI utilisés

```
Visuels natifs                    Visuels custom installés
─────────────────────────         ────────────────────────────
✓ Histogramme groupé              ✓ Animated Bar Chart Race
✓ Graphique en courbes            ✓ Radar Chart
✓ Graphique en aires              ✓ Violin Plot
✓ Graphique en anneau             ✓ ClusterdChart
✓ Carte Azure Maps                ✓ Tachometer (Jauge)
✓ Segment (filtre interactif)     ✓ Narratif intelligent
✓ Carte KPI                       ✓ Stacked Vertical Funnel
```

---

## 📊 Pages du rapport

### Page 1 — Executive Summary
> Vue globale multi-BU avec indicateurs de performance et tendances

- 4 cartes KPI : Total Revenue · Marge % · Nb Opérations · Marge Brute
- Histogramme Revenue par BU (vert/rose/orange par secteur)
- Courbe de tendance 2021→2024
- Filtre interactif par année (boutons)
- Jauge Tachometer Total Revenue

### Page 2 — AeroMRO Analytics
> Analyse détaillée de la Business Unit aéronautique

- Animated Bar Chart Race — classement animé des bases MRO par année
- Courbe en aires Revenue mensuel
- Tachometer Marge % vs Objectif

### Page 3 — FinServ Risk Monitor
> Monitoring de la performance financière et des risques

- Radar Chart — profil de performance par entité financière
- Barres horizontales Revenue par desk
- Donut Nb Opérations par BU

### Page 4 — MedOps Performance
> Tableau de bord hospitalier avec géolocalisation

- Carte Azure Maps — 6 établissements géolocalisés en France
- ClusterdChart — comparaison Cost / Revenue / Nb Opérations
- Anneau répartition Revenue par établissement

### Page 5 — Cross-BU Benchmarking
> Comparaison transversale des 3 Business Units

- Violin Plot — distribution du Revenue par année et par BU
- Barres groupées Revenue vs Total Cost par BU
- Tableau comparatif avec totaux
- Carte KPI YoY Growth %

### Page 6 — Predictive Insights
> Analyse prédictive : Réel vs Objectif, tendances et géographie

- Courbe 2 lignes : Revenue réel vs Objectif (+10%)
- Narratif intelligent auto-généré en français
- Barres horizontales classement BU
- ClusterdChart comparaison complète
- Carte Azure Maps — flux de revenue par localisation

---

## 📐 Mesures DAX

```dax
-- KPIs fondamentaux
Total Revenue     = SUM(Fact_Operations[revenue])
Total Cost        = SUM(Fact_Operations[cost])
Marge Brute       = [Total Revenue] - [Total Cost]
Marge %           = DIVIDE([Marge Brute], [Total Revenue], 0)
Nb Operations     = COUNTROWS(Fact_Operations)

-- KPIs par BU (pattern CALCULATE)
Revenue AeroMRO   = CALCULATE([Total Revenue], Dim_Entity[bu_name] = "AeroMRO")
Revenue FinServ   = CALCULATE([Total Revenue], Dim_Entity[bu_name] = "FinServ Risk")
Revenue MedOps    = CALCULATE([Total Revenue], Dim_Entity[bu_name] = "MedOps")

-- Analyse temporelle
Revenue Total YoY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[date]))
YoY Growth %      = DIVIDE([Total Revenue] - [Revenue Total YoY], [Revenue Total YoY], 0)

-- Scénarios prédictifs
Objectif Revenue  = [Total Revenue] * 1.10
Ecart Objectif    = [Total Revenue] - [Objectif Revenue]
Scenario Revenue  = [Total Revenue] * (1 + [Objectif Marge])
```

---

## 🗄️ Analyses SQL

8 requêtes analytiques exécutées sur la base SQLite `nexus360.db` :

```sql
1. Revenue par BU et par année          → Évolution YoY des 3 BUs
2. Top 5 entités les plus rentables     → Classement par marge %
3. Évolution marge par trimestre        → Saisonnalité T1→T4
4. Détection anomalies                  → Opérations avec perf_score < 20
5. Analyse saisonnalité par mois        → Revenue moyen par mois/BU
6. KPIs les plus critiques              → Alertes métier par seuil
7. Vue Executive Summary globale        → Agrégats toutes BUs
8. Classement géographique              → Revenue par ville/pays
```

### Résultats clés SQL

```
Top site géographique  : La Défense (France) → 450 066 228 € 
Entité la + rentable   : Risk & Compliance   → 58,2% de marge
Anomalies détectées    : 10 opérations avec revenue = 0 €
Marge globale          : 38,3% sur 2,27 Milliards €
```

---

## 💡 Insights clés

### Performance par BU

```
FinServ Risk ████████████████████  58% marge  — Leader en rentabilité
AeroMRO      ████████████          32% marge  — Fort volume d'opérations  
MedOps       ████████              25% marge  — Croissance la plus rapide (+29%)
```

### Saisonnalité observée

- **AeroMRO** : Revenue moyen en juillet = **119 153 €** vs 89 210 € en novembre (+34%)
- **FinServ Risk** : Revenue moyen en décembre = **286 401 €** vs 182 974 € en août (+57%)
- **MedOps** : Revenue moyen en janvier = **62 011 €** vs 37 688 € en août (+65%)

### Top 3 sites géographiques

| Rang | Ville | BU | Revenue |
|:----:|-------|-----|--------:|
| 🥇 | La Défense, France | FinServ Risk | 450 066 228 € |
| 🥈 | Genève, Suisse | FinServ Risk | 247 399 456 € |
| 🥉 | Paris, France | AeroMRO | 182 924 412 € |

---

## ⚙️ Installation

### Prérequis

- Python 3.11+
- Power BI Desktop (gratuit)
- Bibliothèques : `pandas`, `numpy`

```bash
pip install pandas numpy
```

### Lancer le projet

```bash
# 1. Cloner le dépôt
git clone https://github.com/Boubanda/Nexus360-PowerBI-Dashboard.git
cd Nexus360-PowerBI-Dashboard

# 2. Générer les données synthétiques (5 CSV → nexus360_data/)
py generate_nexus360.py

# 3. Créer la base SQLite et exécuter les analyses
py nexus360_sqlite.py

# 4. Ouvrir le rapport Power BI
# → Double-cliquer sur Nexus360.pbix
# → Accueil → Actualiser pour recharger les données
```

---

## 📁 Structure du projet

```
Nexus360-PowerBI-Dashboard/
│
├── 📄 generate_nexus360.py       # Générateur de données synthétiques
│                                  # Saisonnalité + tendances YoY réalistes
│
├── 📄 nexus360_sqlite.py         # ETL + 8 requêtes analytiques SQL
│                                  # Export CSV des résultats
│
├── 📊 Nexus360.pbix              # Rapport Power BI complet
│                                  # 6 pages · 12 mesures DAX · modèle étoile
│
├── 📁 nexus360_data/             # [généré] 5 fichiers CSV
│   ├── fact_operations.csv       # 17 669 lignes — table de faits
│   ├── dim_date.csv              # 1 461 jours — calendrier 2021-2024
│   ├── dim_entity.csv            # 19 entités — 3 BUs
│   ├── dim_kpi.csv               # 18 KPIs métier
│   └── dim_geo.csv               # 15 sites avec coordonnées GPS
│
├── 📁 nexus360_sql_results/      # [généré] 8 fichiers résultats SQL
│   ├── revenue_by_bu_year.csv
│   ├── top5_entities.csv
│   ├── marge_by_quarter.csv
│   ├── anomalies.csv
│   ├── saisonnalite.csv
│   ├── kpis_critiques.csv
│   ├── executive_summary.csv
│   └── classement_geo.csv
│
└── 📄 README.md
```

---

## 👤 Auteur

<div align="center">

**Levi Junior Boubanda**

Étudiant Bac+5 — Data Science & Intelligence Artificielle
Aivancity School for Technology, Business & Society — Paris

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Levi%20Junior%20Boubanda-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/ton-profil)
[![GitHub](https://img.shields.io/badge/GitHub-Boubanda-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Boubanda)

*En recherche d'alternance Data Science / Data Analyst — Septembre 2026*
*Secteurs ciblés : Aérospatial · Finance · Santé*

</div>

---

<div align="center">

⭐ Si ce projet vous a été utile, n'hésitez pas à laisser une étoile !

</div>
