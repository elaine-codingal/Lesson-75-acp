import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('basketball.sqlite')

# 1. List all tables
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in the database:")
print(tables)
print("\n" + "-" * 50)

# 2. Preview the Team table
team_df = pd.read_sql("SELECT * FROM Team LIMIT 5;", conn)
print("Team Table Structure:")
print(f"Columns: {list(team_df.columns)}\n")
print("Sample Data:")
print(team_df)
print("\n" + "-" * 50)

# 3. Distinct values in typeOrganizationFrom
org_types = pd.read_sql("""
    SELECT DISTINCT typeOrganizationFrom FROM Draft;
""", conn)
print("Distinct typeOrganizationFrom values in Draft table:")
print(org_types)
print("\n" + "-" * 50)

# 4. Preview Draft table to debug
draft_preview = pd.read_sql("""
    SELECT idPlayer, idTeam, typeOrganizationFrom 
    FROM Draft 
    LIMIT 10;
""", conn)
print("Sample rows from Draft table:")
print(draft_preview)
print("\n" + "-" * 50)

# 5. Debug Join Output to verify fix
debug_join = pd.read_sql("""
    SELECT 
        d.idPlayer, d.idTeam, d.typeOrganizationFrom,
        t.abbreviation
    FROM Draft d
    LEFT JOIN Team t ON CAST(d.idTeam AS INTEGER) = t.id
    WHERE LOWER(d.typeOrganizationFrom) = 'college/university'
    LIMIT 20;
""", conn)
print("Debug Join Output:")
print(debug_join)
print("\n" + "-" * 50)

# 6. Top 10 Teams by University Drafts (final working query)
top_draft_teams = pd.read_sql("""
    SELECT 
        t.abbreviation AS Team,
        COUNT(DISTINCT d.idPlayer) AS Players_Drafted
    FROM Draft d
    JOIN Team t ON CAST(d.idTeam AS INTEGER) = t.id
    WHERE LOWER(d.typeOrganizationFrom) = 'college/university'
    GROUP BY t.abbreviation
    ORDER BY Players_Drafted DESC
    LIMIT 10;
""", conn)
print("Top 10 Teams by University Drafts:")
print(top_draft_teams)

# Close the connection
conn.close()
