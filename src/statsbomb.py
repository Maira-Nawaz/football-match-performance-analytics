import requests
import pandas as pd
import streamlit as st

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

@st.cache_data(ttl=3600, show_spinner=False)
def _get_json(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=3600, show_spinner=False)
def get_competitions():
    data = _get_json(f"{BASE}/competitions.json")
    df = pd.DataFrame(data)
    return df.sort_values(["competition_name", "season_name"]).reset_index(drop=True)

@st.cache_data(ttl=3600, show_spinner=False)
def get_matches(competition_id, season_id):
    data = _get_json(f"{BASE}/matches/{competition_id}/{season_id}.json")
    return pd.DataFrame(data)

@st.cache_data(ttl=3600, show_spinner=False)
def get_events(match_id):
    return _get_json(f"{BASE}/events/{match_id}.json")

def _nested(obj, *keys, default=None):
    for key in keys:
        if not isinstance(obj, dict):
            return default
        obj = obj.get(key)
    return obj if obj is not None else default

def flatten_events(raw_events):
    rows = []
    for e in raw_events:
        loc = e.get("location") or [None, None]
        pass_data = e.get("pass") or {}
        shot_data = e.get("shot") or {}
        end_loc = pass_data.get("end_location") or [None, None]
        rows.append({
            "id": e.get("id"),
            "minute": e.get("minute"),
            "second": e.get("second"),
            "team": _nested(e, "team", "name"),
            "player": _nested(e, "player", "name"),
            "type": _nested(e, "type", "name"),
            "x": loc[0] if len(loc) > 0 else None,
            "y": loc[1] if len(loc) > 1 else None,
            "end_x": end_loc[0] if len(end_loc) > 0 else None,
            "end_y": end_loc[1] if len(end_loc) > 1 else None,
            "pass_outcome": _nested(pass_data, "outcome", "name"),
            "shot_outcome": _nested(shot_data, "outcome", "name"),
            "xg": shot_data.get("statsbomb_xg"),
        })
    return pd.DataFrame(rows)
