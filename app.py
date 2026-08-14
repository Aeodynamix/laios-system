import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# Initialize SQLite Database for eBuilds
def init_db():
    conn = sqlite3.connect("ebuilds_laios.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_id TEXT,
            client TEXT,
            material TEXT,
            tons REAL,
            status TEXT,
            date TEXT
        )
    """
    )
    conn.commit()
    conn.close()


init_db()


# Webhook verification for Meta WhatsApp API
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    verify_token = "ebuilds_secure_token"  # Set this in your Meta dashboard
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Verification failed", 403
    return "eBuilds LAIOS Webhook Server Online", 200


# Receive Incoming WhatsApp Messages
@app.route("/webhook", methods=["POST"])
def receive_whatsapp():
    data = request.json
    try:
        # Extract message details from Meta WhatsApp Cloud API payload
        message_entry = data["entry"][0]["changes"][0]["value"]
        if "messages" in message_entry:
            sender_phone = message_entry["messages"][0]["from"]
            message_body = message_entry["messages"][0]["text"][
                "body"
            ].lower()

            # Simple parser for building materials & tonnage (e.g., "15 tons of crusher dust")
            material = "Aggregate G1"  # Default
            if "crusher dust" in message_body:
                material = "Crusher Dust"
            elif "sand" in message_body:
                material = "Building Sand"
            elif "19mm" in message_body or "stone" in message_body:
                material = "19mm Stone"
            elif "g2" in message_body:
                material = "Aggregate G2"

            # Log into SQLite database
            conn = sqlite3.connect("ebuilds_laios.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM quotes")
            count = cursor.fetchone()[0]
            quote_id = f"Q-20{count + 1}"

            cursor.execute(
                """
                INSERT INTO quotes (quote_id, client, material, tons, status, date)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
                (quote_id, f"WhatsApp: {sender_phone}", material, 10.0, "Pending"),
            )

            conn.commit()
            conn.close()

            return jsonify({"status": "success", "quote_id": quote_id}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    return jsonify({"status": "ignored"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
