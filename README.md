# 🏀 NBA Player Stats Analyzer

This project explores and analyzes NBA player statistics over the past 5 seasons (2021–2025) using Python, Pandas, and Matplotlib. 
It includes a player lookup tool, general statistical analysis, and a custom-built Most Improved Player (MIP) detector.

---

## 📁 Project Structure

- `01_cleaned_data.ipynb` – Loads and cleans the raw NBA data
- `Player_Stat_Lookup.ipynb` – Look up a player's stats by season or across all 5 years
- `analysis.ipynb` – Explore league-wide trends like top scorers, correlations, and team averages
- `MIP_Detector.ipynb` – Identifies the top 3 Most Improved Player (MIP) candidates per season using a custom stat formula

---

## 🔍 Features

- View top scorers, rebounders, and assist leaders by season
- Analyze correlation between minutes played and point production
- Calculate team-wise average stats
- Search for a player and view detailed performance stats
- Identify MIP candidates using a custom-built **Impact Score**

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

📊 Dataset
The dataset consists of NBA player season stats for the 2021 to 2025 seasons, gathered from Basketball Reference and cleaned manually. It includes over 30 columns covering scoring, defense, efficiency, and team data.


