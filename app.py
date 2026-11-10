import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.statsbomb import get_competitions, get_matches, get_events, flatten_events
from src.visuals import draw_pitch, plot_shots, plot_passes

st.set_page_config(page_title="Football Match Performance Analytics", page_icon="⚽", layout="wide")
st.title("⚽ Football Match Performance Analytics")
st.caption("An exploratory match-analysis dashboard powered by StatsBomb Open Data.")

st.sidebar.header("Select a match")
try:
    competitions = get_competitions()
    competitions["label"] = competitions.apply(
        lambda r: f'{r.get("competition_name", "Competition")} — {r.get("season_name", "Season")} '
                  f'({r.get("country_name", "International")})', axis=1)
    selected_label = st.sidebar.selectbox("Competition / season", competitions["label"].tolist())
    comp = competitions.loc[competitions["label"] == selected_label].iloc[0]
    matches = get_matches(int(comp["competition_id"]), int(comp["season_id"]))
    if matches.empty:
        st.warning("No matches were found for this competition and season.")
        st.stop()
    matches["label"] = matches.apply(
        lambda r: f'{r.get("match_date", "")} | {r.get("home_team", {}).get("home_team_name", "Home")} '
                  f'vs {r.get("away_team", {}).get("away_team_name", "Away")}', axis=1)
    match_label = st.sidebar.selectbox("Match", matches["label"].tolist())
    match = matches.loc[matches["label"] == match_label].iloc[0]
    events_raw = get_events(int(match["match_id"]))
    events = flatten_events(events_raw)
except Exception as exc:
    st.error(f"Could not load StatsBomb data: {exc}")
    st.info("Check your internet connection and try again.")
    st.stop()

home = match.get("home_team", {}).get("home_team_name", "Home")
away = match.get("away_team", {}).get("away_team_name", "Away")
home_score = match.get("home_score", 0)
away_score = match.get("away_score", 0)
st.subheader(f"{home}  {home_score} – {away_score}  {away}")
st.caption(f'{match.get("match_date", "Date unavailable")} · {comp.get("competition_name")} · {comp.get("season_name")}')

shots = events[events["type"] == "Shot"].copy()
passes = events[events["type"] == "Pass"].copy()
goals = shots[shots["shot_outcome"] == "Goal"]
total_xg = shots["xg"].fillna(0).sum()
completed_passes = passes[passes["pass_outcome"].isna()]
pass_pct = (len(completed_passes) / len(passes) * 100) if len(passes) else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total shots", f"{len(shots)}")
c2.metric("Goals", f"{len(goals)}")
c3.metric("Total xG", f"{total_xg:.2f}")
c4.metric("Pass completion", f"{pass_pct:.1f}%")

left, right = st.columns(2)
with left:
    st.markdown("### Shot map")
    fig, ax = plt.subplots(figsize=(8, 5))
    draw_pitch(ax)
    plot_shots(ax, shots)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
with right:
    st.markdown("### Passing map")
    st.caption("Shows the locations of completed passes; arrows indicate pass direction.")
    fig, ax = plt.subplots(figsize=(8, 5))
    draw_pitch(ax)
    plot_passes(ax, completed_passes)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.markdown("### Player performance")
if not shots.empty:
    shot_players = shots.groupby(["player"], dropna=False).agg(
        shots=("id", "count"), goals=("shot_outcome", lambda x: (x == "Goal").sum()),
        xG=("xg", "sum")).reset_index()
else:
    shot_players = pd.DataFrame(columns=["player", "shots", "goals", "xG"])

if not events.empty:
    pass_players = passes.groupby("player", dropna=False).agg(
        passes_attempted=("id", "count"),
        passes_completed=("pass_outcome", lambda x: x.isna().sum())).reset_index()
    player_table = pass_players.merge(shot_players, on="player", how="outer").fillna(0)
    player_table["pass_completion_pct"] = (
        player_table["passes_completed"] / player_table["passes_attempted"].replace(0, pd.NA) * 100
    ).fillna(0).round(1)
    st.dataframe(player_table.sort_values(["xG", "passes_attempted"], ascending=False),
                 use_container_width=True, hide_index=True)
else:
    st.info("No player event data available for this match.")

st.markdown("### Match event data")
with st.expander("Explore cleaned event records"):
    display_cols = [c for c in ["minute", "team", "player", "type", "x", "y", "end_x", "end_y",
                                "shot_outcome", "xg", "pass_outcome"] if c in events.columns]
    st.dataframe(events[display_cols], use_container_width=True, hide_index=True)

st.divider()
st.caption("Data: StatsBomb Open Data. Credit StatsBomb when sharing or publishing analysis. "
           "This is an independent portfolio project, not an official StatsBomb product.")
