import sqlite3
import os
import datetime

DB_PATH = "data/learn.db"

# A függvény a Q-learning ügynökkel integrálva működik
def update_learning(pair, action, reward, next_state, agent):
    # 1. Q-learning frissítés
    agent.learn(pair, action, reward, next_state)  # A Q-tábla frissítése

    # 2. Tanulási eredmény mentése adatbázisba
    # A döntéshez tartozó Q-érték (bias)
    bias = agent.q_table.loc[pair, action]  
    risk = calculate_risk(bias)  # Kockázat kiszámítása (például a bias alapján)
    decision = action  # A választott akció (pl. buy, sell, hold)

    # 3. Az adatbázisba való mentés
    save_to_db(pair, bias, risk, decision)

# Kockázat számítása (például abszolút érték alapján)
def calculate_risk(bias):
    return abs(bias)  # Példa: kockázat lehet a bias abszolút értéke

# Az adatbázisba történő mentés
def save_to_db(pair, bias, risk, decision):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Biztosítjuk, hogy a mappa létezzen
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Ha nincs még a tábla, létrehozzuk
    cur.execute("""CREATE TABLE IF NOT EXISTS learning (
        ts TEXT, pair TEXT, bias REAL, decision TEXT, risk_pct REAL, leverage INTEGER)""")
    
    # Új adat beszúrása
    cur.execute("INSERT INTO learning VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.datetime.now().isoformat(), pair, bias, decision, risk, 1))  # Tőkeáttétel alapértelmezett értéke 1

    # Változások mentése és kapcsolat lezárása
    conn.commit()
    conn.close()
