from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Пример "базы данных" инцидентов
incidents = [
    {"id": 1, "description": "Incident A", "threat_level": 3},
    {"id": 2, "description": "Incident B", "threat_level": 7},
    {"id": 3, "description": "Incident C", "threat_level": 5},
    {"id": 4, "description": "Incident D", "threat_level": 9},
]

@app.route('/incidents/search', methods=['GET'])
def search_incidents():
    # Получаем параметры из query string
    try:
        threat_min = int(request.args.get('threat_min', 0))
        threat_max = int(request.args.get('threat_max', 10))
    except ValueError:
        return jsonify({"error": "Invalid threat_min or threat_max"}), 400

    # Фильтрация инцидентов по диапазону угрозы
    filtered = [
        inc for inc in incidents
        if threat_min <= inc['threat_level'] <= threat_max
    ]

    return jsonify(filtered)

if __name__ == '__main__':
    app.run(debug=True)
