from flask import request, jsonify, render_template, redirect, url_for
from blockchain import Blockchain, Block
from models import Product
import time
import qrcode
import os

def create_routes(app, blockchain):
    @app.route('/')
    def index():
        return render_template('form.html')

    @app.route('/add_product', methods=['POST'])
    def add_product():
        data = request.form.to_dict()
        product = Product(**data)
        product_data = product.to_json()
        
        latest_block = blockchain.get_latest_block()
        new_block = Block(index=latest_block.index + 1,
                          timestamp=time.time(),
                          previous_hash=latest_block.hash,
                          data=product_data,
                          qr_code_path=f"static/qrcodes/{product.serial_number}.png")
        
        blockchain.add_block(new_block)

        # Gerar QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(product_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        qr_code_path = os.path.join('static', 'qrcodes', f"{product.serial_number}.png")
        img.save(qr_code_path)
        
        return redirect(url_for('product_added', qr_code_path=f'qrcodes/{product.serial_number}.png', product_data=product_data))

    @app.route('/product_added')
    def product_added():
        qr_code_path = request.args.get('qr_code_path')
        product_data = request.args.get('product_data')
        product = Product.from_json(product_data)
        return render_template('product_added.html', qr_code_path=qr_code_path, product=product)

    @app.route('/chain', methods=['GET'])
    def get_chain():
        chain_data = [block.__dict__ for block in blockchain.chain]
        return jsonify(chain_data), 200

    @app.route('/validate_chain', methods=['GET'])
    def validate_chain():
        is_valid = blockchain.is_chain_valid()
        return jsonify({'is_valid': is_valid}), 200
