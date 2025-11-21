# -*- coding: utf-8 -*-
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit,
    QVBoxLayout, QWidget, QLabel, QMessageBox,
    QLineEdit, QGroupBox, QHBoxLayout, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

# -------- 核心模块 --------
from core.config import APP_NAME, VERSION
from core.storage import load_data, save_data
from core.async_worker import start_concurrent_update
from core.visualizer import generate_report_chart
from core.models import Stock, Crypto
from core.pandas_analyzer import export_financial_report
from core.text_parser import parse_financial_news

# 新增：快照与内存流
from core.checkpoint import save_system_snapshot, load_system_snapshot, generate_memory_log

# 日志系统
from utils.logger import log

# 数据库
from core.db_manager import db_engine


class OmniWindow(QMainWindow):
    """OmniData 360 主窗口"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{APP_NAME} v{VERSION} (桌面版)")
        self.setGeometry(100, 100, 950, 720)

        # 初始化资产列表
        self.assets = load_data() or [Stock("AAPL", 150.0), Crypto("BTC", 40000.0)]

        self.init_ui()

    # ---------------------------
    # UI 布局
    # ---------------------------
    def init_ui(self):
        center = QWidget()
        self.setCentralWidget(center)
        main_layout = QVBoxLayout()

        # --- 标题 ---
        title = QLabel("💎 欢迎使用 OmniData 360")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color:#0055aa; margin:10px;")
        main_layout.addWidget(title)

        # --- 日志区 ---
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("""
            background:#1e1e1e; color:#00ff88; 
            font-family:Consolas; font-size:12pt;
            border-radius:5px;
        """)
        main_layout.addWidget(self.log_box, stretch=2)

        # --- 功能区按钮 ---
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("🚀 启动全网扫描 (并发)")
        self.btn_refresh.clicked.connect(self.run_scan)
        self.btn_refresh.setFixedHeight(50)
        btn_layout.addWidget(self.btn_refresh)

        self.btn_export = QPushButton("📊 导出 Excel 分析报告")
        self.btn_export.clicked.connect(self.export_excel)
        self.btn_export.setFixedHeight(50)
        btn_layout.addWidget(self.btn_export)

        main_layout.addLayout(btn_layout)

        # --- 智能文本分析 ---
        group_news = QGroupBox("📰 智能文本解析")
        group_news.setStyleSheet("QGroupBox { font-weight:bold; }")
        layout_news = QVBoxLayout()
        self.input_news = QLineEdit()
        self.input_news.setPlaceholderText("输入财经新闻标题，例如: AAPL hits $150 after big earnings...")
        layout_news.addWidget(self.input_news)
        self.btn_analyze = QPushButton("🔍 解析文本")
        self.btn_analyze.clicked.connect(self.run_text_analysis)
        layout_news.addWidget(self.btn_analyze)
        group_news.setLayout(layout_news)
        main_layout.addWidget(group_news)

        # --- 系统快照 (Pickle & StringIO) ---
        group_sys = QGroupBox("💾 系统快照与内存报告")
        layout_sys = QHBoxLayout()
        self.btn_save_snap = QPushButton("❄️ 冻结状态 (Save)")
        self.btn_save_snap.clicked.connect(self.do_snapshot_save)
        self.btn_load_snap = QPushButton("🔥 解冻状态 (Load)")
        self.btn_load_snap.clicked.connect(self.do_snapshot_load)
        self.btn_mem_report = QPushButton("📝 内存报告 (StringIO)")
        self.btn_mem_report.clicked.connect(self.show_memory_report)
        for btn in [self.btn_save_snap, self.btn_load_snap, self.btn_mem_report]:
            btn.setFixedHeight(40)
            layout_sys.addWidget(btn)
        group_sys.setLayout(layout_sys)
        main_layout.addWidget(group_sys)

        # --- 图表显示区域 ---
        self.image_label = QLabel("📈 图表将显示在这里")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(320)
        self.image_label.setStyleSheet("border:2px dashed #aaa; padding:15px; font-size:14pt; color:#888;")
        main_layout.addWidget(self.image_label, stretch=3)

        center.setLayout(main_layout)
        self.log("系统就绪。点击扫描开始。")

    # ---------------------------
    # 日志方法
    # ---------------------------
    def log(self, msg):
        self.log_box.append(f">> {msg}")
        cursor = self.log_box.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_box.setTextCursor(cursor)
        QApplication.processEvents()
        log.info(msg)

    # ---------------------------
    # 文本解析功能
    # ---------------------------
    def run_text_analysis(self):
        text = self.input_news.text().strip()
        if not text:
            QMessageBox.warning(self, "提示", "请输入文本！")
            return
        result = parse_financial_news(text)
        assets = ", ".join(result["mentioned_assets"]) or "无"
        prices = ", ".join([str(p) for p in result["mentioned_prices"]]) or "无"
        msg = f"📌 提及资产: {assets}\n💰 提及价格: {prices}\n\n(详细记录已写入 system.log)"
        QMessageBox.information(self, "解析成功", msg)
        self.log(f"[文本解析] 资产: {assets} | 价格: {prices}")

    # ---------------------------
    # 扫描 & 保存 & 数据库
    # ---------------------------
    def run_scan(self):
        self.btn_refresh.setEnabled(False)
        self.log("正在连接交易所...")
        try:
            start_concurrent_update(self.assets)
            self.log("数据更新完毕。")
            save_data(self.assets)
            self.log("JSON 数据已保存。")
            self.log("写入数据库历史记录...")
            for asset in self.assets:
                db_engine.log_price(asset)
            total = db_engine.get_total_records()
            self.log(f"数据库写入完成，总记录数: {total}")

            generate_report_chart(self.assets)
            img_path = os.path.join("reports", "portfolio_analysis.png")
            if os.path.exists(img_path):
                pix = QPixmap(img_path).scaled(
                    self.image_label.width(), self.image_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio
                )
                self.image_label.setPixmap(pix)
            QMessageBox.information(self, "完成", "任务执行成功！")
        except Exception as e:
            self.log(f"发生错误: {e}")
            QMessageBox.critical(self, "错误", str(e))
        finally:
            self.btn_refresh.setEnabled(True)

    # ---------------------------
    # Excel 导出
    # ---------------------------
    def export_excel(self):
        self.log("正在导出 Excel ...")
        path = export_financial_report(self.assets)
        if path:
            self.log(f"Excel 文件保存至: {path}")
            QMessageBox.information(self, "成功", f"Excel 已保存到：\n{path}")
        else:
            self.log("导出失败")
            QMessageBox.warning(self, "失败", "导出失败，请检查日志")

    # ---------------------------
    # 系统快照
    # ---------------------------
    def do_snapshot_save(self):
        save_system_snapshot(self.assets)
        self.log("系统状态已冻结 (Pickle)。")
        QMessageBox.information(self, "成功", "系统对象已保存到 system_state.pkl")

    def do_snapshot_load(self):
        loaded_assets = load_system_snapshot()
        if loaded_assets:
            self.assets = loaded_assets
            self.log(f"系统状态已恢复，共加载 {len(self.assets)} 个对象。")
            self.log(f"首个资产: {self.assets[0]}")
            QMessageBox.information(self, "成功", "系统状态恢复完成！")
        else:
            QMessageBox.warning(self, "失败", "未找到快照文件。")

    # ---------------------------
    # 内存报告
    # ---------------------------
    def show_memory_report(self):
        report = generate_memory_log(self.assets)
        self.log("构建内存诊断报告...")
        dlg = QDialog(self)
        dlg.setWindowTitle("📄 内存报告 (StringIO)")
        dlg.resize(850, 600)
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(report)
        text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(text_edit)
        dlg.setLayout(layout)
        dlg.exec()

    # ---------------------------
    # 缩放时刷新图表
    # ---------------------------
    def resizeEvent(self, event):
        if self.image_label.pixmap():
            pix = self.image_label.pixmap()
            self.image_label.setPixmap(pix.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        super().resizeEvent(event)

    # ---------------------------
    # 关闭窗口时关闭数据库
    # ---------------------------
    def closeEvent(self, event):
        db_engine.close()
        event.accept()


# ===========================
# 程序入口
# ===========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = OmniWindow()
    win.show()
    sys.exit(app.exec())
