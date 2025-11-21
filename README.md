# OmniData 360 - 全栈智能化金融数据分析平台

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 项目简介

OmniData 360 是一个集数据采集、清洗、存储、分析、可视化、Web 展示与自动化运维于一体的全栈 Python 项目。它模拟了一个专业的金融监控系统，能够处理股票与加密货币数据。

## 🚀 核心功能

* **数据采集**: 多线程并发爬虫 (Threading + Queue) 与 API 调用。
* **数据存储**: 支持 JSON 文件持久化与 SQLite/MySQL 数据库归档。
* **量化分析**: 使用 Pandas 进行数据清洗与报表生成，NumPy 进行统计计算。
* **可视化**: 自动生成 Matplotlib 柱状图与分析图表。
* **交互界面**: 
    * 桌面端: PyQt6 现代化 GUI。
    * Web 端: Flask + Jinja2 数据看板。
* **自动化**: Selenium 浏览器自动截图存档，Crontab/Subprocess 任务调度。
* **安全**: Hashlib 数据完整性校验与防篡改机制。

## 🛠️ 技术栈

* **语言**: Python 3
* **GUI**: PyQt6
* **Web**: Flask, HTML/CSS
* **数据科学**: Pandas, NumPy, Matplotlib
* **爬虫**: Requests, Selenium
* **数据库**: SQLite, PyMySQL
* **工具**: Pickle, Logging, PyInstaller

## 📦 快速开始

1.  克隆项目
    ```bash
    git clone [https://github.com/](https://github.com/)<你的用户名>/OmniData360.git
    ```

2.  安装依赖
    ```bash
    pip install -r requirements.txt
    ```

3.  运行程序
    * **桌面版**: `python gui_app.py`
    * **命令行版**: `python main.py`
    * **Web服务器**: `python web_server.py`

## 📄 许可证

本项目采用 MIT 许可证。