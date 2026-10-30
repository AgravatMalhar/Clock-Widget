from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QMenu
)

from PyQt5.QtCore import Qt, QTimer, QDateTime

from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont,
    QPainterPath,
    QRegion
)

import sys


class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.drag_pos = None

        # Decorative line
        self.deco_label = QLabel("✦ ✦ ✦ ✦ ✦ ✦ ✦")

        # Time
        self.time_label = QLabel()

        # Date
        self.date_label = QLabel()

        # Fonts
        self.deco_label.setFont(QFont("Crimson", 12))
        self.time_label.setFont(QFont("Crimson", 42))

        date_font = QFont("Segoe UI", 11)
        self.date_label.setFont(date_font)

        # Colors
        self.deco_label.setStyleSheet(
            "color:#BFEFFF; background:transparent;"
        )

        self.time_label.setStyleSheet(
            "color:white; background:transparent;"
        )

        self.date_label.setStyleSheet(
            "color:#E6F7FF; background:transparent;"
        )

        # Alignment
        for label in (
            self.deco_label,
            self.time_label,
            self.date_label
        ):
            label.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()

        layout.setContentsMargins(
            35,
            20,
            35,
            20
        )

        layout.setSpacing(3)

        layout.addWidget(self.deco_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.date_label)

        self.setLayout(layout)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

        self.resize(340, 170)

    def update_time(self):
        now = QDateTime.currentDateTime()

        self.time_label.setText(
            now.toString("hh:mm:ss")
        )

        self.date_label.setText(
            now.toString("dddd, d MMM yyyy")
        )

    def resizeEvent(self, event):
        path = QPainterPath()

        path.addRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            30,
            30
        )

        self.setMask(
            QRegion(
                path.toFillPolygon().toPolygon()
            )
        )

        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        path = QPainterPath()

        path.addRoundedRect(
            1,
            1,
            self.width() - 2,
            self.height() - 2,
            30,
            30
        )

        # Transparent Blue Background
        painter.fillPath(
            path,
            QColor(0, 140, 255, 110)
        )

        # Border
        painter.setPen(
            QPen(
                QColor(200, 235, 255, 220),
                2
            )
        )

        painter.drawPath(path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = (
                event.globalPos()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if (
            event.buttons() & Qt.LeftButton
            and self.drag_pos is not None
        ):
            self.move(
                event.globalPos()
                - self.drag_pos
            )

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        menu.setStyleSheet("""
            QMenu {
                background:#0F172A;
                color:white;
                border:1px solid #60A5FA;
            }

            QMenu::item:selected {
                background:#2563EB;
            }
        """)

        close_action = menu.addAction("Close")

        chosen = menu.exec_(event.globalPos())

        if chosen == close_action:
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    clock = ClockWidget()

    clock.move(100, 100)

    clock.show()

    sys.exit(app.exec_())