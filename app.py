from flask import Flask
from blockchain import Blockchain
from app.routes import create_routes
import os

app = Flask(__name__)
blockchain = Blockchain(difficulty=4)

# Cria a pasta para armazenar os QR Codes se não existir
os.makedirs('static/qrcodes', exist_ok=True)
os.makedirs('static/uploaded_qrcodes', exist_ok=True)

create_routes(app, blockchain)

if __name__ == '__main__':
    app.run(debug=True)
