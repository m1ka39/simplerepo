from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os


from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(
    app,
    origins=["*"],
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)
# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



@app.route("/summarize", methods=["POST", "OPTIONS"])
def summarize():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    user_text = data["text"]

    try:
        response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "user", "content": "Summarize: " + user_text}
    ]
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

