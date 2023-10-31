import yfinance as yf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import datetime



def get_buy_sell_advice(current_price, predicted_price_next_day):
    percent_difference = (predicted_price_next_day - current_price) / current_price * 100

    if percent_difference >= 5:  # Adjust these thresholds as needed
        return ("Very Good Time",50)
    elif percent_difference >= 2:
        return ("Good Time",25)
    elif percent_difference >= -2:
        return ("Neutral",0)
    elif percent_difference >= -5:
        return ("Bad Time",-25)
    else:
        return ("Very Bad Time",-50)

def get_upcoming_dates(number_of_days):
    today = datetime.date.today()
    dates = [(today + datetime.timedelta(days=i)).strftime('%a | %d') for i in range(1, number_of_days+1)]
    return dates
def get_stock_prediction(symbol,days):
    # ticker_symbol = request.args.get('ticker', default='AAPL', type=str)
    # days_in_future = request.args.get('days', default=1, type=int)

    ticker_symbol = symbol

    days_in_future = days

    # Fetch data
    stock_data = yf.download(ticker_symbol, start="2000-01-01", end="2023-01-01")
    stock_data['Prediction'] = stock_data['Adj Close'].shift(-days_in_future)

    # Prepare the feature dataset (X) and the target dataset (y)
    X = np.array(stock_data.drop(columns=['Prediction']))[:-days_in_future]
    y = np.array(stock_data['Prediction'])[:-days_in_future]

    # Split the data into training and testing datasets
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Create and train the model
    lr = LinearRegression().fit(x_train, y_train)

    # Testing model accuracy
    lr_confidence = lr.score(x_test, y_test)

    lr_confidence_percentage = round(lr_confidence * 100,0)

    # Predict the future prices
    x_forecast = np.array(stock_data.drop(columns=['Prediction']))[-days_in_future:]
    lr_prediction = lr.predict(x_forecast)

    upcoming_dates = get_upcoming_dates(days_in_future)

    prediction_list = [(x,round(y,2)) for x,y in zip(upcoming_dates,lr_prediction.tolist())]
    # Response object

    ticker = yf.Ticker(symbol)
    data_today = round(ticker.history(period="1d")['Close'].tail(1).iloc[0],2)

    recommendation = get_buy_sell_advice(data_today, prediction_list[0][1])
    print(lr_confidence_percentage)
    response = {
        "ticker": ticker_symbol,
        "confidence": lr_confidence_percentage,
        "predictions": prediction_list,
        "recommendation":recommendation
    }

    return response