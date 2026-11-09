
from PySide6.QtCore import Qt, QPointF, QTimer, QSize
from PySide6.QtGui import (
    QColor, QBrush, QPainter, QFont, QPen, QPolygonF
)
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QGraphicsSimpleTextItem, QLabel, QSizePolicy,
)
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QStackedBarSeries,
    QBarSet,
    QBarCategoryAxis,
    QValueAxis,
)


from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QColor, QBrush, QPainter, QFont, QPen
)
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QGraphicsSimpleTextItem,
)
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QStackedBarSeries,
    QBarSet,
    QBarCategoryAxis,
    QValueAxis,
)

def create_balance_chart(
    tab: QWidget,
    immobilizzazioni: float = 600,
    attivo_circolante: float = 400,
    ratei_risconti_attivi: float = 50,
    patrimonio_netto: float = 300,
    fondi_rischi: float = 80,
    fondo_tfr: float = 70,
    debiti: float = 350,
    ratei_risconti_passivi: float = 50,
) -> QChartView:
    """
    Struttura dello stato patrimoniale
    """

    values = [
        immobilizzazioni,
        attivo_circolante,
        ratei_risconti_attivi,
        patrimonio_netto,
        fondi_rischi,
        fondo_tfr,
        debiti,
        ratei_risconti_passivi,
    ]

    if any(value < 0 for value in values):
        raise ValueError(
            "I valori dello Stato Patrimoniale "
            "devono essere non negativi."
        )

    totale_attivo = (
        immobilizzazioni
        + attivo_circolante
        + ratei_risconti_attivi
    )

    totale_passivo = (
        patrimonio_netto
        + fondi_rischi
        + fondo_tfr
        + debiti
        + ratei_risconti_passivi
    )

    def percentage(value, total):
        return value / total * 100 if total else 0.0

    def format_amount(value):
        return (
            f"{value:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    def format_percentage(value):
        return f"{value:.1f}".replace(".", ",") + "%"

    components = [
        (
            "Immobilizzazioni",
            immobilizzazioni,
            totale_attivo,
            0,
            "#2563EB",
        ),
        (
            "Attivo circolante",
            attivo_circolante,
            totale_attivo,
            0,
            "#06B6D4",
        ),
        (
            "Ratei e risconti attivi",
            ratei_risconti_attivi,
            totale_attivo,
            0,
            "#14B8A6",
        ),
        (
            "Patrimonio netto",
            patrimonio_netto,
            totale_passivo,
            1,
            "#16A34A",
        ),
        (
            "Fondi rischi e oneri",
            fondi_rischi,
            totale_passivo,
            1,
            "#EAB308",
        ),
        (
            "Fondo TFR",
            fondo_tfr,
            totale_passivo,
            1,
            "#F97316",
        ),
        (
            "Debiti",
            debiti,
            totale_passivo,
            1,
            "#F59E0B",
        ),
        (
            "Ratei e risconti passivi",
            ratei_risconti_passivi,
            totale_passivo,
            1,
            "#EF4444",
        ),
    ]

    white = QColor(Qt.GlobalColor.white)
    white_brush = QBrush(white)
    white_pen = QPen(white)
    series = QStackedBarSeries()
    series.setBarWidth(0.55)
    series.setLabelsVisible(False)

    label_data = []
    cumulative = [0.0, 0.0]

    for name, value, total, category, color in components:
        pct = percentage(value, total)

        bar_set = QBarSet(name)

        if category == 0:
            bar_set.append([pct, 0])
        else:
            bar_set.append([0, pct])

        bar_set.setColor(QColor(color))
        bar_set.setBorderColor(QColor(color))
        series.append(bar_set)

        if pct > 0:
            center_y = cumulative[category] + pct / 2
            label_data.append(
                (category, center_y, pct)
            )

        cumulative[category] += pct
    chart = QChart()
    chart.setTitle("Composizione dello Stato Patrimoniale")
    chart.setTitleBrush(white_brush)
    chart.addSeries(series)
    chart.setBackgroundVisible(False)
    chart.setPlotAreaBackgroundVisible(False)
    chart.setAnimationOptions(
        QChart.AnimationOption.NoAnimation
    )
    axis_x = QBarCategoryAxis()
    axis_x.append(["Attivo", "Passivo"])
    axis_x.setLabelsColor(white)
    axis_x.setLinePen(white_pen)
    axis_x.setGridLineVisible(False)
    chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
    series.attachAxis(axis_x)
    axis_y = QValueAxis()
    axis_y.setTitleText("Incidenza percentuale")
    axis_y.setRange(0, 100)
    axis_y.setTickCount(6)
    axis_y.setLabelFormat("%.0f%%")
    axis_y.setLabelsColor(white)
    axis_y.setTitleBrush(white_brush)
    axis_y.setLinePen(white_pen)
    axis_y.setGridLineColor(
        QColor(255, 255, 255, 40)
    )
    chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
    series.attachAxis(axis_y)
    legend = chart.legend()
    legend.setVisible(True)
    legend.setAlignment(Qt.AlignmentFlag.AlignBottom)
    legend.setLabelColor(white)

    legend_font = QFont()
    legend_font.setPointSize(9)
    legend.setFont(legend_font)

    class BalanceChartView(QChartView):

        def __init__(self, chart, label_data, parent=None):
            super().__init__(chart, parent)

            self._labels = []

            self.setRenderHint(
                QPainter.RenderHint.Antialiasing
            )

            font = QFont()
            font.setPointSize(10)
            font.setBold(True)

            for category, center_y, pct in label_data:
                label = QGraphicsSimpleTextItem(
                    format_percentage(pct),
                    chart
                )

                label.setBrush(white_brush)
                label.setFont(font)
                label.setZValue(100)

                self._labels.append(
                    (label, category, center_y, pct)
                )

            chart.plotAreaChanged.connect(
                self.update_labels
            )

            QTimer.singleShot(0, self.update_labels)

        def update_labels(self, *_):
            plot = self.chart().plotArea()

            if plot.width() <= 0 or plot.height() <= 0:
                return

            category_width = plot.width() / 2

            for label, category, center_y, pct in self._labels:
                x = (
                    plot.left()
                    + category_width * (category + 0.5)
                )

                y = (
                    plot.bottom()
                    - center_y / 100 * plot.height()
                )

                rect = label.boundingRect()

                segment_height = (
                    pct / 100 * plot.height()
                )

                if segment_height < rect.height() + 4:
                    label.setVisible(False)
                    continue

                label.setVisible(True)
                label.setPos(
                    x - rect.width() / 2,
                    y - rect.height() / 2
                )

        def resizeEvent(self, event):
            super().resizeEvent(event)
            self.update_labels()
    table = QTableWidget()
    table.setObjectName("balance_amounts_table")
    table.setColumnCount(3)

    table.setHorizontalHeaderLabels([
        "Componente",
        "Importo",
        "Incidenza",
    ])
    rows = [
        (
            name,
            value,
            percentage(value, total),
            color,
        )
        for name, value, total, _, color in components
    ]

    table.setRowCount(len(rows))

    for row_index, (name, amount, pct, color) in enumerate(rows):
        name_item = QTableWidgetItem(name)
        amount_item = QTableWidgetItem(
            format_amount(amount)
        )
        pct_item = QTableWidgetItem(
            format_percentage(pct)
        )

        amount_item.setTextAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        pct_item.setTextAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        for item in (
            name_item,
            amount_item,
            pct_item,
        ):
            item.setForeground(white_brush)
            item.setFlags(
                item.flags()
                & ~Qt.ItemFlag.ItemIsEditable
            )

        name_item.setBackground(
            QBrush(QColor(color))
        )

        table.setItem(row_index, 0, name_item)
        table.setItem(row_index, 1, amount_item)
        table.setItem(row_index, 2, pct_item)
    table.horizontalHeader().setSectionResizeMode(
        0,
        QHeaderView.ResizeMode.Stretch
    )

    table.horizontalHeader().setSectionResizeMode(
        1,
        QHeaderView.ResizeMode.ResizeToContents
    )

    table.horizontalHeader().setSectionResizeMode(
        2,
        QHeaderView.ResizeMode.ResizeToContents
    )

    table.verticalHeader().setVisible(False)

    table.setSelectionMode(
        QAbstractItemView.SelectionMode.NoSelection
    )

    table.setFocusPolicy(
        Qt.FocusPolicy.NoFocus
    )

    palette = table.palette()

    palette.setColor(
        palette.ColorRole.Base,
        QColor("#20252D")
    )

    palette.setColor(
        palette.ColorRole.AlternateBase,
        QColor("#2B313B")
    )

    palette.setColor(
        palette.ColorRole.Text,
        white
    )

    palette.setColor(
        palette.ColorRole.WindowText,
        white
    )

    palette.setColor(
        palette.ColorRole.ButtonText,
        white
    )

    table.setPalette(palette)
    table.setAlternatingRowColors(True)
    table.resizeRowsToContents()

    table_height = (
        table.horizontalHeader().height()
        + sum(
            table.rowHeight(i)
            for i in range(table.rowCount())
        )
        + 4
    )
    table.setFixedHeight(table_height)
    layout = tab.layout()

    if layout is None:
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)

    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)
        widget = item.widget()

        if widget is not None and widget.objectName() in (
            "balance_chart_view",
            "balance_amounts_table",
            "balance_error_widget",
        ):
            layout.removeWidget(widget)
            widget.hide()
            widget.deleteLater()

    chart_view = BalanceChartView(
        chart,
        label_data
    )

    chart_view.setObjectName("balance_chart_view")

    layout.addWidget(chart_view, stretch=3)
    layout.addWidget(table, stretch=0)

    return chart_view

def create_chart_error(
    tab: QWidget,
    title: str = "Dati non disponibili",
    message: str = (
        "Non sono disponibili i dati necessari "
        "alla realizzazione del grafico."
    ),
    description: str = (
        "Verifica che i dati dello Stato Patrimoniale "
        "siano stati caricati correttamente e riprova."
    ),
) -> QWidget:
    """
    Messaggio di errore se mancano i dati per fare il grafico
    """

    RED = QColor("#FF5C65")
    WHITE = QColor("#FFFFFF")
    SECONDARY = QColor("#C7CDD5")

    class WarningIcon(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedSize(QSize(76, 76))

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(
                QPainter.RenderHint.Antialiasing
            )

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#49292E"))
            painter.drawEllipse(4, 4, 68, 68)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(
                QPen(RED, 3, Qt.PenStyle.SolidLine,
                     Qt.PenCapStyle.RoundCap,
                     Qt.PenJoinStyle.RoundJoin)
            )

            triangle = QPolygonF([
                QPointF(38, 19),
                QPointF(59, 56),
                QPointF(17, 56),
            ])
            painter.drawPolygon(triangle)
            painter.setPen(
                QPen(RED, 4, Qt.PenStyle.SolidLine,
                     Qt.PenCapStyle.RoundCap)
            )
            painter.drawLine(38, 32, 38, 43)
            painter.drawPoint(38, 50)

            painter.end()
    error_widget = QWidget(tab)
    error_widget.setObjectName("balance_error_widget")

    error_layout = QVBoxLayout(error_widget)
    error_layout.setContentsMargins(30, 30, 30, 30)
    error_layout.setSpacing(14)
    error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    icon = WarningIcon(error_widget)
    error_layout.addWidget(
        icon,
        alignment=Qt.AlignmentFlag.AlignHCenter
    )
    title_label = QLabel(title, error_widget)
    title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_label.setWordWrap(True)

    title_font = QFont()
    title_font.setPointSize(22)
    title_font.setBold(True)
    title_label.setFont(title_font)
    title_palette = title_label.palette()
    title_palette.setColor(
        title_label.foregroundRole(),
        RED
    )
    title_label.setPalette(title_palette)
    error_layout.addWidget(title_label)
    message_label = QLabel(message, error_widget)
    message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    message_label.setWordWrap(True)

    message_font = QFont()
    message_font.setPointSize(13)
    message_font.setWeight(QFont.Weight.Medium)
    message_label.setFont(message_font)
    message_palette = message_label.palette()
    message_palette.setColor(
        message_label.foregroundRole(),
        WHITE
    )
    message_label.setPalette(message_palette)
    error_layout.addWidget(message_label)
    description_label = QLabel(description, error_widget)
    description_label.setAlignment(
        Qt.AlignmentFlag.AlignCenter
    )
    description_label.setWordWrap(True)

    description_font = QFont()
    description_font.setPointSize(11)
    description_label.setFont(description_font)

    description_palette = description_label.palette()
    description_palette.setColor(
        description_label.foregroundRole(),
        SECONDARY
    )
    description_label.setPalette(description_palette)

    error_layout.addWidget(description_label)

    error_widget.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Expanding
    )
    layout = tab.layout()

    if layout is None:
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)
        widget = item.widget()

        if widget is not None and widget.objectName() in (
            "balance_chart_view",
            "balance_amounts_table",
            "balance_error_widget",
        ):
            layout.removeWidget(widget)
            widget.hide()
            widget.deleteLater()

    layout.addWidget(error_widget)

    return error_widget
