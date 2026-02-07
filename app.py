from flask import Flask, render_template, request, jsonify
from chatbot import get_response
from utils import validate_response

app = Flask(__name__)

# ─── Routes ─────────────────────────────────────────────────────────────
@app.route('/')
def index():
    """
    Renders the main simulation interface.
    """
    # This looks for 'index.html' inside the 'templates' folder
    return render_template('index.html') 

@app.route('/simulate', methods=['POST'])
def simulate():
    """
    Endpoint for running attack simulations.
    Expects JSON: {"prompt": "...", "mode": "full_chain" or "single"}
    """
    try:
        data = request.get_json()
        
        # Matches the keys sent by your new index.html
        user_input = data.get("prompt", "")
        mode = data.get("mode", "single")
        tactic = data.get("tactic", "recon_gatherer")

        # Get response from chatbot orchestrator
        raw_output = get_response(user_input, mode=mode, tactic=tactic)

        # Sanitize and validate before returning
        if isinstance(raw_output, dict):
            final_output = {k: validate_response(v) for k, v in raw_output.items()}
        else:
            final_output = validate_response(raw_output)

        return jsonify({
            "status": "success",
            "data": final_output 
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)