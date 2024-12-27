from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/meme', methods=['GET'])
def get_meme():
    return {"message": "Get a meme!"}

@api.route('/meme', methods=['POST'])
def create_meme():
    return {"message": "Create a new meme!"}

@api.route('/trading', methods=['GET'])
def get_trading_info():
    return {"message": "Get trading information!"}

@api.route('/trading', methods=['POST'])
def execute_trade():
    return {"message": "Execute a trade!"}