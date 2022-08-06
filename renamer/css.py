from PySide2.QtGui import QColor
from PySide2.QtWidgets import QGraphicsDropShadowEffect


def css_button(qt_window, button, color=None, shadow=True):
    ''' apply style to a button widget '''

    # default bg color is gray 80
    if color == 'red':
        bg_color = 'rgb(160, 20, 20)'  # red/white
        tx_color = 'rgb(255, 255, 255)'
    elif color == 'disabled':
        bg_color = 'rgb(80, 80, 80)'  # gray/gray
        tx_color = 'rgb(180, 180, 180)'
    elif color == 'blue':
        bg_color = 'rgb(46, 134, 193)'  # blue arcane/white
        tx_color = 'rgb(230, 230, 230)'
    else:
        bg_color = 'rgb(80, 80, 80)'  # gray
        tx_color = 'rgb(230, 230, 230)'

    css = "border-radius:3px;color:{};background:{};font-size:12px;font-family:Segoe UI;".format(
        tx_color, bg_color)
    button.setStyleSheet(css)

    if shadow:
        shadow = QGraphicsDropShadowEffect(qt_window)
        shadow.setBlurRadius(6)
        shadow.setOffset(4)
        shadow.setColor(QColor(20, 20, 20, 200))
        button.setGraphicsEffect(shadow)


groupbox_css = ("""
    QGroupBox {
        font: bold;
        border: 1px solid silver;
        border-radius: 6px;
        margin-top: 3px;
        background: rgb(60, 60, 60);
    }
    QGroupBox:title {
        subcontrol-origin: margin;
        left: 10px;
        padding: -5px 5px 0px 5px;
    }
        """)

checkbox_css = ("""
    QCheckBox {
        color: rgb(230, 230, 230);
    }

    QCheckBox:indicator:checked {
        background-color: rgb(52, 152, 219);
        border: 1px solid rgb(50, 50, 50);
    }

    QCheckBox:indicator:disabled {
        color: rgb(100,100,100);
        background-color: rgb(100, 100, 100);
        border: 1px solid rgb(100, 100, 100);
        width: 10px;
        height: 10px;
    }

    QCheckBox:indicator {
        background-color: rgb(50,50,50);
        border: 1px solid rgb(120,120,120);
        width: 10px;
        height: 10px;
    }

    QCheckBox:indicator:hover {
        border: 1px solid rgb(200, 200, 200);
    }
    """)

label_css = ("""
    QLabel {
        color: rgb(230, 230, 230);
    }
    """)
