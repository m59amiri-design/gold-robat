from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 🔹 این تابع جدید - GET و POST هر دو را پشتیبانی می‌کند
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        # پاسخ برای درخواست‌های GET (مخصوص تست مرورگر)
        return jsonify({
            "status": "success",
            "message": "This is a GET request test. Server is working!",
            "prediction": "TEST_BUY",
            "confidence": 0.85,
            "timestamp": datetime.now().isoformat(),
            "instruction": "Send POST request with JSON data for real predictions"
        })
    
    elif request.method == 'POST':
        # پردازش درخواست‌های POST از ربات MQL5
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    "status": "error",
                    "message": "No data received"
                }), 400
            
            # استخراج داده‌ها
            symbol = data.get('symbol', 'XAUUSD')
            timeframe = data.get('timeframe', 'M5')
            
            price_data = data.get('price_data', {})
            blue_rectangle = data.get('blue_rectangle', {})
            gray_rectangle = data.get('gray_rectangle', {})
            
            close_price = price_data.get('close', 1900)
            blue_high = blue_rectangle.get('high', 1895)
            blue_low = blue_rectangle.get('low', 1885)
            
            # منطق پیش‌بینی
            prediction = "NONE"
            confidence = 0.5
            
            if close_price > blue_high:
                prediction = "BUY"
                confidence = 0.75
            elif close_price < blue_low:
                prediction = "SELL"
                confidence = 0.75
            
            # محاسبه حد ضرر و حد سود
            stop_loss = 0
            take_profit = 0
            
            if prediction == "BUY":
                stop_loss = close_price * 0.995
                take_profit = close_price * 1.015
            elif prediction == "SELL":
                stop_loss = close_price * 1.005
                take_profit = close_price * 0.985
            
            return jsonify({
                "status": "success",
                "prediction": prediction,
                "confidence": confidence,
                "predicted_price": round(close_price, 2),
                "stop_loss": round(stop_loss, 2),
                "take_profit": round(take_profit, 2),
                "message": "Prediction completed",
                "timestamp": datetime.now().isoformat(),
                "symbol": symbol,
                "timeframe": timeframe
            })
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

# دیگر endpointها
@app.route('/')
def home():
    return jsonify({
        "message": "Gold Robot AI Server",
        "endpoints": {
            "/": "این صفحه",
            "/health": "بررسی سلامت سرور",
            "/predict": "دریافت پیش‌بینی (GET برای تست، POST برای ربات)",
            "/test": "تست ساده"
        }
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/test')
def test():
    return jsonify({"message": "Server is working!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
