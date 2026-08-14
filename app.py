import sqlite3
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


# Initialize SQLite Database for eBuilds
def init_db():
  conn = sqlite3.connect("ebuilds_laios.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_id TEXT,
            client TEXT,
            material TEXT,
            tons REAL,
            status TEXT,
            date TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()


@app.route("/", methods=["GET"])
def home():
  return "eBuilds LAIOS Server Online", 200


# Receive Incoming WhatsApp Messages from Twilio
@app.route("/whatsapp", methods=["POST"])
def receive_whatsapp():
  # Twilio sends incoming data as form values, not JSON
  incoming_msg = request.values.get("Body", "").strip().lower()
  sender = request.values.get("From", "")

  # Simple parser for building materials & tonnage
  material = "Aggregate G1"  # Default
  if "crusher dust" in incoming_msg:
    material = "Crusher Dust"
  elif "sand" in incoming_msg:
    material = "Building Sand"
  elif "19mm" in incoming_msg or "stone" in incoming_msg:
    material = "19mm Stone"
  elif "g2" in incoming_msg:
    material = "Aggregate G2"

  # Log into SQLite database
  conn = sqlite3.connect("ebuilds_laios.db")
  cursor = conn.cursor()
  cursor.execute("SELECT COUNT(*) FROM quotes")
  count = cursor.fetchone()[0]
  quote_id = f"Q-20{count + 1}"

  # Insert quote record (defaulting to 1 ton for test messages)
  cursor.execute(
      "INSERT INTO quotes (quote_id, client, material, tons, status, date) VALUES"
      " (?, ?, ?, ?, ?, datetime('now'))",
      (quote_id, sender, material, 1.0, "Pending"),
  )
  conn.commit()
  conn.close()

  # Create automated reply back via Twilio
  resp = MessagingResponse()
  msg = resp.message()
  msg.body(
      f"Thanks from eBuilds! Your quote ({quote_id}) for {material} has been"
      " logged successfully."
  )

  return str(resp)


if __name__ == "__main__":
  app.run(port=5000)
