from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "service": "Gold Robot AI",
        "version": "1.0.0",
        "endpoints": ["/health", "/predict", "/test"],
        "description": "AI prediction server for Gold Trading Robot"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract data
        symbol = data.get('symbol', 'XAUUSD')
        timeframe = data.get('timeframe', 'M5')
        
        price_data = data.get('price_data', {})
        blue_rectangle = data.get('blue_rectangle', {})
        gray_rectangle = data.get('gray_rectangle', {})
        
        close_price = price_data.get('close', 1900)
        blue_high = blue_rectangle.get('high', 1895)
        blue_low = blue_rectangle.get('low', 1885)
        
        # Simple AI logic
        prediction = "NONE"
        confidence = 0.5
        
        if close_price > blue_high:
            prediction = "BUY"
            confidence = 0.75
        elif close_price < blue_low:
            prediction = "SELL"
            confidence = 0.75
        
        # Calculate stop loss and take profit
        stop_loss = 0
        take_profit = 0
        
        if prediction == "BUY":
            stop_loss = close_price * 0.995
            take_profit = close_price * 1.015
        elif prediction == "SELL":
            stop_loss = close_price * 1.005
            take_profit = close_price * 0.985
        
        response = {
            "status": "success",
            "prediction": prediction,
            "confidence": confidence,
            "predicted_price": round(close_price, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "message": "AI analysis completed",
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "message": "Server is working!",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
