from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        database=os.getenv("POSTGRES_DB", "myapp"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password")
    )

# Retry DB connection (important in K8s)
def wait_for_db():
    while True:
        try:
            conn = get_db_connection()
            conn.close()
            print("Connected to DB ✅")
            break
        except Exception as e:
            print("Waiting for DB ⏳...")
            time.sleep(2)

wait_for_db()

# Health check
@app.route("/health")
def health():
    return "OK", 200

# API endpoint
@app.route("/api")
def api():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY);")
        cur.execute("INSERT INTO visits DEFAULT VALUES;")
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM visits;")
        count = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({
            "message": "Backend Service 🔥",
            "visits": count
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)