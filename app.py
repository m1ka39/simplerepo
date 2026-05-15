from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)
# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@app.route("/summarize", methods=["POST", "OPTIONS"])
def summarize():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    user_text = data["text"]

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Summarize this clearly and concisely:\n\n{user_text}"
        )

        return jsonify({
            "summary": response.text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
        
@app.route("/", methods=["GET"])
def home():
    return "Backend is alive"
    
if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=5000)

