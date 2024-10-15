from flask import Flask, jsonify, request
import subprocess
import os
from preprocess_functions import *
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

def check_authorizerd():
    # Récupérer l'en-tête Authorization
    auth_header = request.headers.get('Authorization')

    if auth_header:
        # Vérifier si l'en-tête contient le type Bearer
        token_type, token = auth_header.split(' ', 1) if ' ' in auth_header else (None, None)

        if token_type.lower() == 'bearer':
            # Vérifier si le token reçu correspond au token attendu
            if token != os.getenv("API_TOKEN"):
                return jsonify({"error": "Token non valide"}), 401
        else:
            return jsonify({"error": "Type d'authentification non supporté"}), 401
    else:
        return jsonify({"error": "Token manquant"}), 401
    
configure_azure_monitor()

FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)

# Simple Hello world pour vérifier si le déploiement automatiquement a bien mis à jour la nouvelle version
@app.route('/')
def hello_world():
    return 'Hello from Flask! Reload v2!'

# Api de prédiction
@app.route("/predict", methods=["GET"])
def predict():
        texte = request.args.get("texte")
        predictions = process_transform_text([texte])

        return jsonify({"predict": predictions})

# Api de déploiement de la nouvelle version
@app.route("/deploy", methods=["POST"])
def deploy():
    check_authorizerd()
    try:
        subprocess.run(["bash", "deploy.sh"], check=True, capture_output=True, text=True)
        return jsonify({"message": "deploiement succes"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"message": "" ,"error": e.stderr}), 200

# Api de demande de rédémarrage du serveur API
@app.route("/restart", methods=["POST"])
def restart_gunicorn():
    check_authorizerd()
    try:
        # Rediriger stdout et stderr vers un fichier de log
        log_file = open("gunicorn_restart.log", "a")
        
        # Exécuter le script en arrière-plan en redirigeant la sortie
        subprocess.Popen(["bash", "start_app.sh"], stdout=log_file, stderr=log_file)
        
        return jsonify({"message": "Le redémarrage de Gunicorn a été lancé."}), 200
    except Exception as e:
        return jsonify({"message": "Erreur lors du démarrage de Gunicorn", "error": str(e)}), 500

# vérifier l'état de l'api, si ok c'est que l'api fonctionne
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

# Envoyer des feedback pour les prédictions correctes ou erronnées
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    if data["feedback"] == 0:
        with trace.get_tracer(__name__).start_as_current_span("wrong_predict") as span:
           span.set_attribute("error", "Mauvaise prédiction")
           span.set_attribute("text", data["text"])
           span.set_attribute("predicted", data["predicted"])


    return jsonify({"statut": "feedback enregistré"}), 200
    
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000, debug=False)