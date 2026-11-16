
from PySide6.QtCore import Qt, QLocale, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGraphicsSimpleTextItem,
)
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QCategoryAxis,
    QValueAxis,
)


def format_italian_number(value: float, decimals: int = 0) -> str:
    """Formatta i numeri con il punto come separatore delle migliaia."""
    locale = QLocale(QLocale.Language.Italian, QLocale.Country.Italy)
    return locale.toString(float(value), "f", decimals)


class FinancialChartView(QChartView):
    """Grafico con etichette dei punti disegnate manualmente."""

    def __init__(self, chart: QChart, parent=None):
        super().__init__(chart, parent)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMinimumSize(400, 300)

        self._point_labels = []

        chart.plotAreaChanged.connect(self.update_point_labels)

    def add_point_labels(self, series: QLineSeries, color: QColor):
        """Crea le etichette grafiche associate ai punti."""

        for point in series.points():
            label = QGraphicsSimpleTextItem(self.chart())

            label.setText(format_italian_number(point.y()))
            label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            label.setBrush(QBrush(color))
            label.setZValue(100)

            self._point_labels.append((series, point, label))

        self.update_point_labels()

    def update_point_labels(self, *_):
        """Aggiorna la posizione delle etichette."""

        chart = self.chart()

        for series, point, label in self._point_labels:
            position = chart.mapToPosition(point, series)
            rect = label.boundingRect()

            x = position.x() - rect.width() / 2
            y = position.y() - rect.height() - 12

            label.setPos(x, y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        QTimer.singleShot(0, self.update_point_labels)


def create_financial_chart(
    periods: list[str],
    revenues: list[float],
    costs: list[float],
    extra_costs: list[float] | None = None,
    extra_costs_name: str = "Altri costi",
    title: str = "Andamento ricavi e costi",
) -> FinancialChartView:

    n = len(periods)

    if n == 0:
        raise ValueError("La lista dei periodi non può essere vuota.")

    if len(revenues) != n or len(costs) != n:
        raise ValueError("Le serie devono avere la stessa lunghezza.")

    if extra_costs is not None and len(extra_costs) != n:
        raise ValueError("La terza serie ha una lunghezza non valida.")

    chart = QChart()
    chart.setTitle(title)
    chart.setAnimationOptions(QChart.AnimationOption.NoAnimation)

    # Palette scura
    background_color = QColor("#303030")
    plot_color = QColor("#383838")
    text_color = QColor("#F0F0F0")
    grid_color = QColor("#555555")

    chart.setBackgroundBrush(QBrush(background_color))
    chart.setPlotAreaBackgroundBrush(QBrush(plot_color))
    chart.setPlotAreaBackgroundVisible(True)
    chart.setBackgroundRoundness(8)

    chart.setTitleBrush(QBrush(text_color))
    chart.setTitleFont(QFont("Arial", 13, QFont.Weight.Bold))

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
    chart.legend().setLabelColor(text_color)

    all_values = []
    series_info = []

    def add_series(name, values, color_hex):
        color = QColor(color_hex)

        series = QLineSeries()
        series.setName(name)
        series.setPen(QPen(color, 2.5))
        series.setPointsVisible(True)
        series.setMarkerSize(9)

        for i, value in enumerate(values):
            value = float(value)
            series.append(float(i), value)
            all_values.append(value)

        # Etichette QtCharts disabilitate
        series.setPointLabelsVisible(False)

        chart.addSeries(series)
        series_info.append((series, color))

    add_series("Ricavi", revenues, "#64B5F6")
    add_series("Costi materie prime e consumo", costs, "#EF5350")

    if extra_costs is not None:
        add_series(extra_costs_name, extra_costs, "#FFB74D")

    # Asse X
    axis_x = QCategoryAxis()
    axis_x.setTitleText("Periodo")
    axis_x.setLabelsPosition(
        QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue
    )

    for i, period in enumerate(periods):
        axis_x.append(str(period), float(i))

    axis_x.setRange(-0.3, max(0.3, n - 1 + 0.3))
    axis_x.setLabelsColor(text_color)
    axis_x.setTitleBrush(QBrush(text_color))
    axis_x.setGridLineColor(grid_color)
    axis_x.setLinePenColor(text_color)

    # Asse Y: sempre da zero
    axis_y = QValueAxis()
    axis_y.setTitleText("Valore assoluto (€)")
    axis_y.setTickCount(6)
    axis_y.setLabelFormat("%.0f")

    axis_y.setLabelsColor(text_color)
    axis_y.setTitleBrush(QBrush(text_color))
    axis_y.setGridLineColor(grid_color)
    axis_y.setLinePenColor(text_color)

    maximum = max(all_values)
    y_max = maximum * 1.15 if maximum > 0 else 1.0

    axis_y.setRange(0.0, y_max)

    chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
    chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

    for series, _ in series_info:
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    # Formattazione italiana delle etichette degli assi
    chart.setLocalizeNumbers(True)
    chart.setLocale(
        QLocale(QLocale.Language.Italian, QLocale.Country.Italy)
    )

    view = FinancialChartView(chart)

    # Etichette manuali sopra i punti
    for series, color in series_info:
        view.add_point_labels(series, color)

    return view


def add_financial_chart_to_tab(
    tab: QWidget,
    periods: list[str],
    revenues: list[float],
    costs: list[float],
    extra_costs: list[float] | None = None,
    extra_costs_name: str = "Altri costi",
    title: str = "Andamento ricavi e costi",
    replace_existing: bool = True,
) -> FinancialChartView:
    """Inserisce il grafico in un tab di QTabWidget."""

    if not isinstance(tab, QWidget):
        raise TypeError("tab deve essere un QWidget.")

    layout = tab.layout()

    if layout is None:
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)

    if replace_existing:
        for old_chart in tab.findChildren(FinancialChartView):
            old_chart.hide()
            old_chart.deleteLater()

    chart_view = create_financial_chart(
        periods=periods,
        revenues=revenues,
        costs=costs,
        extra_costs=extra_costs,
        extra_costs_name=extra_costs_name,
        title=title,
    )

    layout.addWidget(chart_view)

    return chart_view