import os
from flask import Flask, request, jsonify, render_template
from jinja2 import TemplateNotFound
from flask_cors import CORS
import chatbot
from chatbot import get_response

# === Path Configuration ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# === Sanity Checks (optional) ===
print(f"▶️  Base directory: {BASE_DIR}")
print(f"▶️  Templates directory: {TEMPLATES_DIR}")
print(f"▶️  Root listing: {os.listdir(BASE_DIR)}")
if os.path.isdir(TEMPLATES_DIR):
    print(f"▶️  Template folder listing: {os.listdir(TEMPLATES_DIR)}")
else:
    print("❌  ERROR: 'templates' directory not found!")

# === Flask App Initialization ===
app = Flask(__name__, template_folder=TEMPLATES_DIR)
CORS(app)  # Allow cross-origin requests if needed

# === Routes ===
@app.route('/', methods=['GET'])
def index():
    """Serve the main HTML page."""
    try:
        return render_template('index.html')
    except TemplateNotFound:
        return (
            "Template not found! Ensure 'templates/index.html' exists next to app.py.",
            500
        )

@app.route('/api/run', methods=['POST'])
def run_cmd():
    """Handle POST requests from the UI and return chatbot responses."""
    data = request.get_json() or {}
    cmd = data.get('cmd', '').strip()
    if not cmd:
        return jsonify({'error': 'No command provided'}), 400

    try:
        # Pass the UI input to your chatbot
        bot_reply = get_response(cmd)
        return jsonify({
            'stdout': bot_reply,
            'stderr': '',
            'returncode': 0
        })
    except Exception as e:
        return jsonify({
            'stdout': '',
            'stderr': str(e),
            'returncode': 1
        }), 500

# === Entry Point ===
if __name__ == '__main__':
    # debug=True for development; disable in production
    app.run(host='0.0.0.0', port=5000, debug=True)
