from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Pour l'instant, accepter tous les logins
    return jsonify({'success': True})

@app.route('/vente', methods=['POST'])
def vente():
    data = request.get_json()
    print("Données de vente reçues:", data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
