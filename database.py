
import sqlite3
from datetime import datetime


# Create database table
def create_table():

    conn = sqlite3.connect("phishguard.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            scan_time TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save scan details
def save_scan(url, score, risk):

    conn = sqlite3.connect("phishguard.db")
    cursor = conn.cursor()

    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO scan_history
        (url, risk_score, risk_level, scan_time)
        VALUES (?, ?, ?, ?)
    """, (url, score, risk, scan_time))

    conn.commit()
    conn.close()


# Retrieve previous scans
def get_scan_history():

    conn = sqlite3.connect("phishguard.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, url, risk_score, risk_level, scan_time
        FROM scan_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    conn.close()

    return records


# Get dashboard statistics
def get_dashboard_stats():

    conn = sqlite3.connect("phishguard.db")
    cursor = conn.cursor()

    # Count total scans
    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total_scans = cursor.fetchone()[0]

    # Count scans by risk level
    cursor.execute("""
        SELECT risk_level, COUNT(*)
        FROM scan_history
        GROUP BY risk_level
    """)

    risk_counts = cursor.fetchall()

    conn.close()

    stats = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0
    }

    for risk, count in risk_counts:
        stats[risk] = count

    return total_scans, stats
