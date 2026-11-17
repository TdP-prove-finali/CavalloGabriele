
from math import isfinite

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QCursor, QPainter, QPen, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QToolTip
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSet,
    QStackedBarSeries,
    QBarCategoryAxis,
    QValueAxis,
    QLineSeries,
    QScatterSeries,
)


BG = QColor("#303030")
PLOT_BG = QColor("#383838")
FG = QColor("#F0F0F0")
GRID = QColor("#555555")

COLORS = [
    "#4978C8",
    "#E4A84A",
    "#33A6A0",
    "#9673D3",
    "#68B77B",
    "#D77B9D",
]


def _financial_format(value):
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def _financial_scale(maximum):
    if maximum >= 1_000_000_000:
        return 1_000_000_000, "Mld €"
    if maximum >= 1_000_000:
        return 1_000_000, "Mln €"
    if maximum >= 1_000:
        return 1_000, "Migliaia €"
    return 1, "€"


def _financial_style(chart, title):
    chart.setTitle(title)
    chart.setTitleBrush(FG)
    chart.setBackgroundBrush(BG)
    chart.setBackgroundRoundness(0)
    chart.setPlotAreaBackgroundVisible(True)
    chart.setPlotAreaBackgroundBrush(PLOT_BG)
    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
    chart.legend().setLabelColor(FG)


def _financial_axis_style(axis):
    axis.setLabelsColor(FG)
    axis.setLinePenColor(GRID)
    axis.setGridLineColor(GRID)


class FinancialChartView(QChartView):

    def __init__(
        self,
        chart,
        label_values,
        label_series,
        scale=1,
        suffix="",
        parent=None,
    ):
        super().__init__(chart, parent)

        self.label_values = label_values
        self.label_series = label_series
        self.scale = scale
        self.suffix = suffix

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setStyleSheet(
            "background: #303030; border: none;"
        )

    def drawForeground(self, painter, rect):
        super().drawForeground(painter, rect)

        if not self.label_values:
            return

        chart = self.chart()
        plot = chart.plotArea()

        painter.save()
        painter.setPen(FG)
        painter.setFont(QFont("Arial", 9))

        metrics = painter.fontMetrics()

        for i, value in enumerate(self.label_values):
            if value is None:
                continue

            point = chart.mapToPosition(
                QPointF(i, value / self.scale),
                self.label_series,
            )

            text = (
                f"{_financial_format(value / self.scale)}"
                f"{self.suffix}"
            )

            width = metrics.horizontalAdvance(text)
            height = metrics.height()

            x = point.x() - width / 2
            y = point.y() - height - 7

            x = max(plot.left(), min(x, plot.right() - width))
            y = max(plot.top() + 2, y)

            painter.drawText(
                QPointF(x, y + metrics.ascent()),
                text,
            )

        painter.restore()


def create_financial_evolution_chart(
    years,
    series_data,
    title,
):
    years = [str(y) for y in years]
    n = len(years)

    if not n:
        raise ValueError("Nessun anno disponibile.")

    if not series_data:
        raise ValueError("Nessuna serie disponibile.")

    data = {}

    for name, values in series_data.items():
        if values is None:
            values = [0] * n

        if len(values) != n:
            raise ValueError(
                f"{name}: attesi {n} valori, "
                f"ricevuti {len(values)}"
            )

        values = [
            abs(float(v)) if v is not None else 0.0
            for v in values
        ]

        if not all(isfinite(v) for v in values):
            raise ValueError(f"Valori non validi: {name}")

        data[name] = values

    totals = [
        sum(values[i] for values in data.values())
        for i in range(n)
    ]

    maximum = max(max(totals), 1.0)
    scale, unit = _financial_scale(maximum)

    changes = [None]
    percentages = [None]

    for i in range(1, n):
        delta = totals[i] - totals[i - 1]
        changes.append(delta)
        percentages.append(
            delta / totals[i - 1] * 100
            if totals[i - 1] else None
        )

    container = QWidget()
    container.setStyleSheet("background: #303030;")

    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)

    chart_values = QChart()
    _financial_style(
        chart_values,
        f"{title} — Valori assoluti",
    )

    bars = QStackedBarSeries()
    bars.setBarWidth(0.65)
    bars.setLabelsVisible(False)

    barsets = []

    for index, (name, values) in enumerate(data.items()):
        barset = QBarSet(name)
        barset.setColor(
            QColor(COLORS[index % len(COLORS)])
        )
        barset.append([v / scale for v in values])
        bars.append(barset)
        barsets.append(barset)

    chart_values.addSeries(bars)
    chart_values.createDefaultAxes()

    for axis in chart_values.axes(Qt.Orientation.Horizontal):
        if isinstance(axis, QBarCategoryAxis):
            axis.clear()
            axis.append(years)
            _financial_axis_style(axis)

    for axis in chart_values.axes(Qt.Orientation.Vertical):
        if isinstance(axis, QValueAxis):
            axis.setRange(0, maximum / scale * 1.25)
            axis.setTickCount(6)
            axis.setLabelFormat("%.1f")
            axis.setTitleText(unit)
            axis.setTitleBrush(FG)
            _financial_axis_style(axis)

    def bar_hovered(state, index, barset):
        if not state:
            QToolTip.hideText()
            return

        details = "\n".join(
            f"{name}: {_financial_format(values[index])} €"
            for name, values in data.items()
        )

        text = (
            f"{years[index]}\n"
            f"{details}\n"
            f"Totale: {_financial_format(totals[index])} €"
        )

        if changes[index] is not None:
            text += (
                f"\nVariazione assoluta: "
                f"{changes[index]:+,.2f} €"
            )

            if percentages[index] is not None:
                text += (
                    f"\nVariazione percentuale: "
                    f"{percentages[index]:+.2f}%"
                )

        QToolTip.showText(QCursor.pos(), text)

    bars.hovered.connect(bar_hovered)

    values_view = FinancialChartView(
        chart_values,
        label_values=totals,
        label_series=bars,
        scale=scale,
    )
    values_view.setMinimumHeight(350)

    chart_changes = QChart()
    _financial_style(
        chart_changes,
        f"{title} — Variazione annua (%)",
    )

    line = QLineSeries()
    line.setName("Variazione annua")
    line.setPen(QPen(QColor("#68B77B"), 2.5))

    points = QScatterSeries()
    points.setName("Variazione %")
    points.setColor(QColor("#68B77B"))
    points.setBorderColor(FG)
    points.setMarkerSize(10)
    points.setPointLabelsVisible(False)

    valid = [
        v for v in percentages if v is not None
    ]

    for i, value in enumerate(percentages):
        if value is not None:
            points.append(i, value)

    for i in range(1, n):
        if (
            percentages[i - 1] is not None
            and percentages[i] is not None
        ):
            line.append(i - 1, percentages[i - 1])
            line.append(i, percentages[i])

    chart_changes.addSeries(line)
    chart_changes.addSeries(points)
    chart_changes.createDefaultAxes()

    for axis in chart_changes.axes(Qt.Orientation.Horizontal):
        if isinstance(axis, QValueAxis):
            axis.setRange(-0.5, n - 0.5)
            axis.setTickCount(max(n + 1, 2))
            axis.setLabelFormat("%.0f")
            _financial_axis_style(axis)

    minimum = min(valid + [0])
    maximum_pct = max(valid + [0])
    margin = max((maximum_pct - minimum) * 0.2, 5)

    for axis in chart_changes.axes(Qt.Orientation.Vertical):
        if isinstance(axis, QValueAxis):
            axis.setRange(
                minimum - margin,
                maximum_pct + margin,
            )
            axis.setTickCount(6)
            axis.setLabelFormat("%.1f%%")
            _financial_axis_style(axis)

    def point_hovered(point, state):
        if not state:
            QToolTip.hideText()
            return

        i = round(point.x())

        QToolTip.showText(
            QCursor.pos(),
            f"{years[i]}\n"
            f"Totale: {_financial_format(totals[i])} €\n"
            f"Variazione: {changes[i]:+,.2f} €\n"
            f"Variazione %: {percentages[i]:+.2f}%",
        )

    points.hovered.connect(point_hovered)

    changes_view = FinancialChartView(
        chart_changes,
        label_values=percentages,
        label_series=points,
        scale=1,
        suffix="%",
    )
    changes_view.setMinimumHeight(250)

    layout.addWidget(values_view, 3)
    layout.addWidget(changes_view, 2)

    container._references = (
        bars,
        barsets,
        line,
        points,
    )

    return container


def add_financial_evolution_chart_to_tab(
    tab,
    years,
    series_data,
    title,
):
    widget = create_financial_evolution_chart(
        years=years,
        series_data=series_data,
        title=title,
    )

    layout = tab.layout()

    if layout is None:
        layout = QVBoxLayout(tab)

    layout.addWidget(widget)

    return widget