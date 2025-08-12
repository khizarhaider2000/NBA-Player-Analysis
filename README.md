# 🏀 NBA Player Stats Analyzer

This project explores and analyzes NBA player statistics over the past 5 seasons (2021–2025) using Python, Pandas, and Matplotlib. 
It includes:
- A **Fantasy Value Calculator** to find the best/worst contracts relative to player performance
- A **Most Improved Player (MIP) Detector**
- A **Player Stat Lookup Tool**
- League-wide analysis tools for trends, correlations, and averages

---

## 📁 Project Structure (Impact-First Order)

- `Salary_Value_Calculator.ipynb` – Ranks players by value (performance vs. salary) using two complementary methods  
- `MIP_Detector.ipynb` – Identifies the Top 3 Most Improved Players per season using a custom stat formula  
- `Player_Stat_Lookup.ipynb` – Search for any player's stats by season or across all 5 years  
- `analysis.ipynb` – Explore league-wide trends like top scorers, correlations, and team averages  
- `01_cleaned_data.ipynb` – Loads and cleans the raw NBA data
---

## 🔍 Features

- Rank best and worst NBA contracts using the **Fantasy Value Calculator** (performance vs. salary)
- Identify MIP candidates using a custom-built **Impact Score**
- View top scorers, rebounders, and assist leaders by season
- Analyze correlation between minutes played and point production
- Calculate team-wise average stats
- Search for a player and view detailed performance stats

---
🧮 Fantasy Value Calculator
This module ranks NBA players by how much on-court impact you get per dollar of salary.
It produces season-by-season leaderboards for:

📈 Best value contracts – Players outperforming their pay grade

📉 Worst value contracts – Players underperforming relative to salary

📐 Fantasy Value Score Formula:
```python
FantasyScore = f(PTS, AST, TRB, STL, BLK, TOV)  # per-game normalized
```
- Uses per-game rates from core box stats
- Penalizes turnovers
- Filters out players with G ≤ 55 or very low availability
📊 Ranking Logic:
1) Bracketed Z-Score View (Best Value)
   - Groups players into salary tiers (e.g., <$2M, $2–5M, $5–10M, $10–15M, $15–30M, >$30M)
   - Within each tier, computes Z-scores for FantasyScore
   - Ranks Top 5 per season in each tier

2) Impact-per-Dollar View (Worst Value)
   - Normalizes FantasyScore by salary (millions) → AdjustedValue
   - Ranks Bottom 5 per season by efficiency

🧠 Design Choices:
- Fair comparisons – Salary tiers prevent penalizing high earners simply for being expensive
- Bang-for-buck – AdjustedValue view highlights breakout cheap players & overpriced veterans
- Availability guardrails – Removes small-sample flukes from low-game seasons
- Per-game normalization – Removes bias from differences in minutes or pace
- Season reset – Rankings are recalculated fresh each season

📤 Example Output:
Best Value (Z-Score view)
```python
📈 The 5 best value contracts for 2023–24 (Avg Z-Score: 0.85)
• Player Name (SG) – Fantasy Score: 2.97, Salary: $5–10M → Z: 1.92
```
Worst Value (Impact-per-Dollar)
```python
📉 The 5 worst value contracts for 2023–24 (Avg Adjusted Score: 0.41)
• Player Name (PF) – Fantasy Score: 2.1, Salary: $28.0M → Adjusted Value: 0.07
```

---
## 🏆 Most Improved Player (MIP) Detector

This module ranks the **Top 3 most improved players** for each season by comparing their performance to the previous year.

### 📐 Custom Impact Score Formula:
```python
Impact = PTS + TRB + AST + STL + BLK - TOV + 2 × (3P% + FT% + FG%)
```
This score rewards overall performance while penalizing turnovers. Shooting efficiency stats are double-weighted to emphasize quality scoring.

📊 MIP Selection Logic:
Calculate the Impact Score for every player each season

Compute the year-over-year difference in Impact using groupby().diff()

Filter for players with at least 55 games played in both the current and previous season

Rank players by Impact improvement and display the top 3 for each season
---

🔎 Player Stat Lookup Tool
This script allows users to search for any NBA player and view their performance stats by season or across all five years (2021–2025).

🧰 How It Works:
Prompts the user to enter a player's name (case-insensitive)

Then prompts for a specific season (e.g., 2023) or "All" for a 5-year view

Displays key stats such as:

Games Played (G), Points (PTS), Rebounds (TRB) ,Assists (AST), Steals (STL), Blocks (BLK), Turnovers (TOV), 3P%, FT%, FG%

This is a simple, beginner-friendly way to interact with the dataset and explore individual player performances directly from the terminal.

---

## 🧪 Example Usage

```bash
> python Player_Stat_Lookup.py
Welcome to NBA Stat Lookup
Enter the player's name: lebron james
Which season would you like to view the stats for? ['2021', '2022', '2023', '2024', '2025']
If you would like to see average of 5 years, type 'All': all

Stats for Lebron James across all seasons:

     Season Team   G   PTS  TRB  AST  STL  BLK  TOV  3P%  FT%  FG%
11    20_21  LAL  45  25.0  7.7  7.8  1.1  0.6  3.7  0.4  0.7  0.5
259   21_22  LAL  56  30.3  8.2  6.2  1.3  1.1  3.5  0.4  0.8  0.5
524   22_23  LAL  55  28.9  8.3  6.8  0.9  0.6  3.2  0.3  0.8  0.5
807   23_24  LAL  71  25.7  7.3  8.3  1.3  0.5  3.5  0.4  0.8  0.5
1103  24_25  LAL  70  24.4  7.8  8.2  1.0  0.6  3.7  0.4  0.8  0.5
```


📊 Dataset
The dataset consists of NBA player season stats for the 2021 to 2025 seasons, gathered from Basketball Reference and cleaned manually. It includes over 30 columns covering scoring, defense, efficiency, and team data.


