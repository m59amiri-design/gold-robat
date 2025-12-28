from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS  # اضافه کردن این خط

app = Flask(__name__)
CORS(app)  # اضافه کردن این خط برای اجازه دادن به تمام درخواست‌ها

# ========== اضافه کردن این تابع جدید ==========
@app.route('/predict', methods=['GET'])
def predict_get():
    """پاسخ دادن به درخواست‌های GET برای تست"""
    return jsonify({
        "status": "success",
        "prediction": "TEST_BUY",
        "confidence": 0.85,
        "predicted_price": 1905.50,
        "stop_loss": 1898.00,
        "take_profit": 1920.00,
        "message": "Server is working! Use POST method for real predictions.",
        "timestamp": datetime.now().isoformat(),
        "instructions": "Send POST request with JSON data for real predictions"
    })

@app.route('/predict', methods=['POST'])
def predict_post():
    """پردازش درخواست‌های POST از ربات MQL5"""
    try:
        # کدهای قبلی شما...
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data received"
            }), 400
        
        # استخراج داده‌ها
        symbol = data.get('symbol', 'XAUUSD')
        timeframe = data.get('timeframe', 'M5')
        
        price_data = data.get('price_data', {})
        blue_rectangle = data.get('blue_rectangle', {})
        gray_rectangle = data.get('gray_rectangle', {})
        
        # لاگ اطلاعات دریافتی (برای دیباگ)
        print("=" * 50)
        print(f"📨 Received prediction request at {datetime.now()}")
        print(f"Symbol: {symbol}")
        print(f"Timeframe: {timeframe}")
        print(f"Close Price: {price_data.get('close', 'N/A')}")
        print(f"Blue Rectangle High: {blue_rectangle.get('high', 'N/A')}")
        print("=" * 50)
        
        # منطق پیش‌بینی ساده (می‌توانید پیچیده‌تر کنید)
        close_price = price_data.get('close', 1900)
        blue_high = blue_rectangle.get('high', 1895)
        blue_low = blue_rectangle.get('low', 1885)
        
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
            stop_loss = close_price * 0.995  # 0.5% پایین‌تر
            take_profit = close_price * 1.015  # 1.5% بالاتر
        elif prediction == "SELL":
            stop_loss = close_price * 1.005  # 0.5% بالاتر
            take_profit = close_price * 0.985  # 1.5% پایین‌تر
        
        # پاسخ
        response = {
            "status": "success",
            "prediction": prediction,
            "confidence": confidence,
            "predicted_price": round(close_price, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "message": "AI analysis completed successfully",
            "timestamp": datetime.now().isoformat(),
            "symbol": symbol,
            "timeframe": timeframe,
            "server_version": "2.0.0"
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

# ========== اضافه کردن endpoint های تست ==========
@app.route('/')
def home():
    return '''
    <html>
    <head><title>Gold Robot AI Server</title></head>
    <body>
        <h1>🚀 Gold Robot AI Server</h1>
        <p>Server is running successfully!</p>
        <h3>Available Endpoints:</h3>
        <ul>
            <li><a href="/health">/health</a> - سلامت سرور</li>
            <li><a href="/predict">/predict</a> - تست GET</li>
            <li><a href="/test">/test</a> - تست عمومی</li>
            <li><b>POST /predict</b> - دریافت پیش‌بینی از ربات</li>
        </ul>
        <h3>Test POST Request:</h3>
        <form action="/predict" method="post">
            <button type="submit">Test POST to /predict</button>
        </form>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Gold Robot AI",
        "version": "2.0.0"
    })

@app.route('/test')
def test():
    return jsonify({
        "message": "✅ Server is working perfectly!",
        "timestamp": datetime.now().isoformat(),
        "next_step": "Configure your MQL5 robot to send POST requests to /predict"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
