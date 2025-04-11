from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://payment.cokipul.my.id/generate_webhook.php"
SECRET_HEADER = "gundulxxx423"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    token = request.form['token']
    saweria = request.form['saweria']

    # Validasi Bot Token
    check = requests.get(f"https://api.telegram.org/bot{token}/getMe")
    if check.status_code != 200:
        return jsonify({'status': 'error', 'message': 'Token Salah'})

    bot_id = check.json()['result']['id']

    data = {
        "owner_id": bot_id,
        "token": token,
        "saweria": saweria
    }

    headers = {
        "X-Secret": SECRET_HEADER
    }

    res = requests.post(WEBHOOK_URL, data=data, headers=headers)

    if res.status_code == 200:
        url = f"https://payment.cokipul.my.id/webhook/{res.text.strip()}"
        return jsonify({'status': 'success', 'url': url})

    return jsonify({'status': 'error', 'message': 'Gagal Generate Webhook'})

if __name__ == "__main__":
    app.run(debug=True)
