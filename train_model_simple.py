from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib
import os

print("🤖 Creating simple AI models for testing...")

# ایجاد داده‌های نمونه
X = np.random.rand(100, 5)  # 100 نمونه، 5 ویژگی
y = np.random.randint(0, 2, 100)  # برچسب‌های تصادفی

# ایجاد مدل
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

# ایجاد پوشه models
os.makedirs('models', exist_ok=True)

# ذخیره مدل‌ها
joblib.dump(model, 'models/buy_model.pkl')
joblib.dump(model, 'models/sell_model.pkl')

print("✅ Simple AI models created successfully!")
print("📁 Models saved in: models/")
