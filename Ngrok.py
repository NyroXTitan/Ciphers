from flask import Flask, request, render_template,jsonify
from pyngrok import ngrok
# Open a public URL for the Flask app
NGROK_AUTH_TOKEN = "NGROK_KEY"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
# Flask setup
app = Flask(__name__, template_folder='templates')
#run_with_ngrok(app)

history = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    text = data.get("text", "")
    mode = data.get("mode", "")
    technique = data.get("technique", "")
    key = data.get("key", "")

    try:
        if technique == "caesar":
            key_int = int(key)
            result = caesar_cipher(text, key_int, mode)
        elif technique == "vigenere":
            result = vigenere_cipher(text, key, mode)
        elif technique == "railfence":
            key_int = int(key)
            result = rail_fence(text, key_int, mode)
        elif technique == "playfair":
            result = playfair_cipher(text, key, mode)
        else:
            result = "Invalid technique"
    except Exception as e:
        result = f"Error: {e}"

    # Append operation to history
    history.append({
        "input": text,
        "output": result,
        "mode": mode,
        "technique": technique,
        "key": key
    })

    return jsonify({"result": result})
@app.route("/history")
def get_history():
    return jsonify(history)




# Open a tunnel on port 5000 for the Flask app

public_url = ngrok.connect(5000)
print(" * ngrok tunnel URL:", public_url)
app.run(port=5000)
