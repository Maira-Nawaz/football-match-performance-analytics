-- Optional SQL examples after exporting the flattened events dataframe to a table
-- named match_events in SQLite / DuckDB / BigQuery.

-- 1. Shot and xG summary by team
SELECT
    team,
    COUNT(*) AS shots,
    SUM(CASE WHEN shot_outcome = 'Goal' THEN 1 ELSE 0 END) AS goals,
    ROUND(SUM(COALESCE(xg, 0)), 2) AS total_xg
FROM match_events
WHERE type = 'Shot'
GROUP BY team
ORDER BY total_xg DESC;

-- 2. Passing volume and completion by player
SELECT
    team,
    player,
    COUNT(*) AS passes_attempted,
    SUM(CASE WHEN pass_outcome IS NULL THEN 1 ELSE 0 END) AS passes_completed,
    ROUND(
        100.0 * SUM(CASE WHEN pass_outcome IS NULL THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1
    ) AS pass_completion_pct
FROM match_events
WHERE type = 'Pass'
GROUP BY team, player
ORDER BY passes_attempted DESC;
