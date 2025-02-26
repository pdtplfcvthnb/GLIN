from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # URL API Ollama.  Убедитесь, что Ollama запущен.
MODEL_NAME = "GLIN" # Или любая другая модель, которую вы установили.

@app.route("/")
def index():
    """Отображает главную страницу с интерфейсом чата."""
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Обрабатывает сообщения от пользователя и отправляет их в Ollama."""
    data = request.get_json()
    user_message = data["message"]

    payload = {
        "prompt": user_message,
        "model": MODEL_NAME,
        "stream": False  #  Важно: Стримминг здесь отключен для простоты.  Стримминг требует другой обработки на клиенте.
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, stream=False)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        json_data = response.json()
        ollama_response = json_data.get("response", "No response from Ollama.")

        return jsonify({"response": ollama_response})

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return jsonify({"response": f"Error: Could not connect to Ollama. {e}"}), 500  #  Возвращает код ошибки HTTP

if __name__ == "__main__":
    app.run(debug=True) # debug=True только для разработки!