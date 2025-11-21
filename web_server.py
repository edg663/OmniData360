# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
import json
import os

# 初始化 Flask 应用
app = Flask(__name__, template_folder='templates')

# 指向 data 文件夹下的 market_data.json
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "market_data.json")

def get_data():
    """辅助函数：读取最新的 JSON 数据"""
    if not os.path.exists(DATA_FILE):
        print(f"[WARN] 数据文件不存在: {DATA_FILE}")
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# --- 路由 1: 首页仪表盘 ---
@app.route('/')
def dashboard():
    assets = get_data()
    return render_template('dashboard.html', assets=assets)

# --- 路由 2: 数据 API (JSON) ---
@app.route('/api/data')
def api_data():
    assets = get_data()
    return jsonify(assets)

if __name__ == '__main__':
    print(" [Web] 正在启动服务器...")
    print(" [Web] 请在浏览器访问: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
