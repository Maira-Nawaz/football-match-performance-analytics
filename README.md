# Football Match Performance Analytics

An interactive football match-analysis portfolio project built with Python, Streamlit, pandas and Matplotlib using StatsBomb Open Data.

## Features
- Browse the competitions and seasons available in StatsBomb's public dataset.
- Select a match and inspect the event data.
- Match KPIs: shots, goals, total expected goals (xG), and pass completion.
- Shot map and completed-pass map on a football pitch.
- Player-level shot, goal, xG, and passing summary.
- Cached data downloads to avoid repeatedly fetching the same JSON files.

## Data source and attribution
This project uses **StatsBomb Open Data**:
https://github.com/statsbomb/open-data

StatsBomb provides selected football competitions and seasons as JSON files. Availability varies by competition and season. Please read the repository's current README and license/terms before publishing or reusing data. Credit StatsBomb when sharing or publishing analysis. This project is independent and is not affiliated with StatsBomb.

## Run locally (Windows)
1. Install Python 3.10 or newer.
2. Extract this project folder.
3. Open Command Prompt or the VS Code terminal in this folder.
4. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Launch the dashboard:

   ```bash
   streamlit run app.py
   ```

The app needs an internet connection to retrieve the public JSON data from GitHub.

## Metric definitions and caveats
- **Shots:** count of StatsBomb events with event type `Shot`.
- **Goals:** shots whose shot outcome is `Goal`.
- **Total xG:** sum of the `statsbomb_xg` value supplied for shot events. This is the provider's model value, not a model trained in this project.
- **Pass completion:** completed passes divided by all pass events. In StatsBomb event data, a missing pass outcome generally indicates a completed pass; review provider documentation for edge cases.
- **Player summary:** event-level totals for shots, goals, xG, attempted passes and completed passes.

The pass map is a sample of up to 180 completed passes for readability. Coordinates are displayed in StatsBomb's 120 x 80 pitch coordinate system.

## Suggested portfolio write-up
**Problem:** Match event data is detailed but difficult for non-technical stakeholders to scan quickly.

**Approach:** Retrieve public event data, normalize nested JSON fields into an analysis-ready table, calculate match and player KPIs, and visualize shots and passing actions.

**Deliverable:** An interactive dashboard that lets a user select a competition, season and match, then explore performance indicators and event-level records.

**Next improvements:** add team filters, possession sequences, pass networks, defensive actions, xG by player, and a multi-match player scouting comparison.

## Project structure
```text
football_match_performance_analytics/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── statsbomb.py
│   └── visuals.py
└── sql/
    └── analysis_queries.sql
```
