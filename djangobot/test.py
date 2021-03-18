import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
try:
    cursor.execute('SELECT JSON(\'{"a": "b"}\')')
    print("the JSON capability is there")
except:
    print("the JSON capability is not there")