from flask import Blueprint, jsonify, request, current_app
from .stock_utils import get_stock_data, get_stock_news, fetch_historical_data
from .ml_model import get_stock_prediction, get_buy_sell_advice

stock_bp = Blueprint('stock_bp', __name__)



@stock_bp.route('/stock/<symbol>', methods=['GET'])
def stock(symbol):
    # stock_prediction = get_stock_prediction(symbol)
    # print(stock_prediction)
    # return jsonify(stock_prediction)

    api_key = current_app.config['NEWS_API_KEY']

    stock_data = get_stock_data(symbol)
    stock_news = get_stock_news(symbol,api_key)

    historical_data = fetch_historical_data(symbol)
    stock_prediction = get_stock_prediction(symbol,10)
    #stock_advice = get_buy_sell_advice(stock_data, stock_prediction)

    return jsonify({
        'data': stock_data,
        'news': stock_news,
        'prediction': stock_prediction,
        'advice': 'stock_advice',
        'history' : historical_data,
    })
