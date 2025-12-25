#!/usr/bin/env python3
"""Quick Phase 2 completion check"""
import psycopg2
import os

# Database connection
conn = psycopg2.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432'),
    database=os.getenv('DB_NAME', 'stock_scanner'),
    user=os.getenv('DB_USER', 'mlscanner'),
    password=os.getenv('DB_PASSWORD', '')
)

cursor = conn.cursor()

print("=" * 70)
print("PHASE 2 COMPLETION CHECK")
print("=" * 70)

# Check row counts
queries = {
    'Tickers': 'SELECT COUNT(*) FROM raw_data.tickers',
    'OHLCV Rows': 'SELECT COUNT(*) FROM raw_data.ohlcv',
    'OHLCV Tickers': 'SELECT COUNT(DISTINCT ticker) FROM raw_data.ohlcv',
    'Technical Indicators Rows': 'SELECT COUNT(*) FROM raw_data.technical_indicators',
    'Technical Indicators Tickers': 'SELECT COUNT(DISTINCT ticker) FROM raw_data.technical_indicators',
    'Features Rows': 'SELECT COUNT(*) FROM raw_data.features',
    'Features Tickers': 'SELECT COUNT(DISTINCT ticker) FROM raw_data.features',
    'Labels Rows': 'SELECT COUNT(*) FROM raw_data.labels',
    'Labels Tickers': 'SELECT COUNT(DISTINCT ticker) FROM raw_data.labels',
}

print("\n📊 DATA COMPLETENESS:\n")
for name, query in queries.items():
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"  {name:30s}: {count:,}")

# Calculate average rows per ticker
cursor.execute('SELECT COUNT(*) FROM raw_data.ohlcv')
total_ohlcv = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(DISTINCT ticker) FROM raw_data.ohlcv')
ticker_count = cursor.fetchone()[0]
if ticker_count > 0:
    avg = total_ohlcv / ticker_count
    print(f"  {'Avg OHLCV rows/ticker':30s}: {avg:,.0f}")

# Date range
cursor.execute('SELECT MIN(date), MAX(date) FROM raw_data.ohlcv')
min_date, max_date = cursor.fetchone()
print(f"\n📅 DATE RANGE:")
print(f"  First Date: {min_date}")
print(f"  Last Date:  {max_date}")

# Data quality checks
print(f"\n🔍 DATA QUALITY:")
cursor.execute('SELECT COUNT(*) FROM raw_data.ohlcv WHERE close IS NULL OR volume IS NULL')
missing = cursor.fetchone()[0]
print(f"  Missing values: {missing}")

cursor.execute('SELECT COUNT(*) FROM raw_data.ohlcv WHERE volume = 0')
zero_vol = cursor.fetchone()[0]
print(f"  Zero volume:    {zero_vol} ({zero_vol/total_ohlcv*100:.2f}%)")

# Label distribution
print(f"\n📈 LABEL DISTRIBUTION (1-day binary):")
cursor.execute('''
    SELECT label_1d_binary, COUNT(*)
    FROM raw_data.labels
    WHERE label_1d_binary IS NOT NULL
    GROUP BY label_1d_binary
''')
for label, count in cursor.fetchall():
    total_labels = cursor.execute('SELECT COUNT(*) FROM raw_data.labels WHERE label_1d_binary IS NOT NULL')
    cursor.execute('SELECT COUNT(*) FROM raw_data.labels WHERE label_1d_binary IS NOT NULL')
    total = cursor.fetchone()[0]
    pct = count / total * 100 if total > 0 else 0
    label_name = 'Up' if label == 1 else 'Down'
    print(f"  {label_name}: {count:,} ({pct:.1f}%)")

print("\n" + "=" * 70)
print("✓ PHASE 2 VERIFICATION COMPLETE")
print("=" * 70)

cursor.close()
conn.close()
