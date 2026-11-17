
from collections.abc import Mapping, Sequence
from math import isfinite

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtCharts import (
    QAreaSeries,
    QChart,
    QChartView,
    QLineSeries,
    QScatterSeries,
    QValueAxis,
)


COLORS = [
    "#4978C8",
    "#E4A84A",
    "#33A6A0",
    "#9673D3",
    "#68B77B",
]

BG = QColor("#303030")
PLOT_BG = QColor("#383838")
FG = QColor("#F0F0F0")
RED = QColor("#FF5252")


def _stacked_chart(
    years: Sequence,
    data: Mapping[str, Sequence[float]],
    title: str,
    liquidity_key: str | None = None,
) -> QChartView:

    years = list(years)
    n = len(years)

    if not n:
        raise ValueError("Nessun anno disponibile.")

    prepared = {}
    crises = {}

    for name, values in data.items():
        if len(values) != n:
            raise ValueError(f"Lunghezza non valida: {name}")

        values = [float(v) for v in values]

        if not all(isfinite(v) for v in values):
            raise ValueError(f"Valori non validi: {name}")

        if name == liquidity_key:
            crises = {
                i: v for i, v in enumerate(values) if v < 0
            }
            values = [max(v, 0.0) for v in values]
        elif any(v < 0 for v in values):
            raise ValueError(f"Valori negativi: {name}")

        prepared[name] = values

    totals = [
        sum(values[i] for values in prepared.values())
        for i in range(n)
    ]

    maximum = max(max(totals), 1.0)

    scale, unit = (
        (1_000_000_000, "Miliardi €")
        if maximum >= 1_000_000_000
        else (1_000_000, "Milioni €")
        if maximum >= 1_000_000
        else (1_000, "Migliaia €")
        if maximum >= 1_000
        else (1, "€")
    )

    chart = QChart()
    chart.setTitle(title)
    chart.setTitleBrush(FG)
    chart.setBackgroundBrush(BG)
    chart.setBackgroundRoundness(0)
    chart.setPlotAreaBackgroundVisible(True)
    chart.setPlotAreaBackgroundBrush(PLOT_BG)

    chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
    chart.legend().setLabelColor(FG)

    cumulative = [0.0] * n
    references = []

    for index, (name, values) in enumerate(prepared.items()):
        lower = QLineSeries()
        upper = QLineSeries()

        for i, value in enumerate(values):
            lower.append(i, cumulative[i] / scale)
            cumulative[i] += value
            upper.append(i, cumulative[i] / scale)

        area = QAreaSeries(upper, lower)
        area.setName(name)

        color = QColor(COLORS[index % len(COLORS)])
        area.setBrush(color)
        area.setPen(QPen(color, 1.5))

        chart.addSeries(area)
        references.append((lower, upper, area))

    if crises:
        markers = QScatterSeries()
        markers.setName("Crisi di liquidità")
        markers.setColor(RED)
        markers.setBorderColor(FG)
        markers.setMarkerSize(13)

        for i in crises:
            markers.append(i, totals[i] / scale)

        chart.addSeries(markers)
        references.append(markers)

        def show_crisis(point, state):
            if state:
                i = round(point.x())
                if i in crises:
                    from PySide6.QtGui import QCursor
                    from PySide6.QtWidgets import QToolTip

                    QToolTip.showText(
                        QCursor.pos(),
                        f"{years[i]}\n"
                        f"Liquidità effettiva: {crises[i]:,.0f} €\n"
                        "Liquidità visualizzata: 0 €",
                    )
            else:
                from PySide6.QtWidgets import QToolTip
                QToolTip.hideText()

        markers.hovered.connect(show_crisis)

    chart.createDefaultAxes()

    for axis in chart.axes(Qt.Orientation.Horizontal):
        if isinstance(axis, QValueAxis):
            axis.setRange(0, max(n - 1, 1))
            axis.setTickCount(max(n, 2))
            axis.setLabelFormat("%.0f")
            axis.setLabelsColor(FG)
            axis.setGridLineColor(QColor("#555555"))

    for axis in chart.axes(Qt.Orientation.Vertical):
        if isinstance(axis, QValueAxis):
            axis.setRange(0, maximum / scale * 1.1)
            axis.setTickCount(6)
            axis.setLabelFormat("%.1f")
            axis.setTitleText(unit)
            axis.setTitleBrush(FG)
            axis.setLabelsColor(FG)
            axis.setGridLineColor(QColor("#555555"))

    view = QChartView(chart)
    view.setRenderHint(QPainter.RenderHint.Antialiasing)
    view.setMinimumHeight(300)
    view.setStyleSheet(
        "background-color: #303030; border: none;"
    )

    view._references = references
    view._crises = crises

    return view


def create_attivo_area_chart(
    years,
    immobilizzazioni,
    rimanenze,
    crediti,
    attivita_finanziarie,
    disponibilita_liquide,
):
    return _stacked_chart(
        years,
        {
            "Immobilizzazioni nette": immobilizzazioni,
            "Rimanenze": rimanenze,
            "Crediti": crediti,
            "Attività finanziarie": attivita_finanziarie,
            "Disponibilità liquide": disponibilita_liquide,
        },
        "Evoluzione della struttura dell'attivo",
        liquidity_key="Disponibilità liquide",
    )


def create_passivo_area_chart(
    years,
    patrimonio_netto,
    debiti_lungo_termine,
    debiti_breve_termine,
    fondi_rischi_tfr,
    altre_passivita,
):
    return _stacked_chart(
        years,
        {
            "Patrimonio netto": patrimonio_netto,
            "Debiti a lungo termine": debiti_lungo_termine,
            "Debiti a breve termine": debiti_breve_termine,
            "Fondi rischi e TFR": fondi_rischi_tfr,
            "Altre passività": altre_passivita,
        },
        "Evoluzione del passivo e patrimonio netto",
    )


def add_patrimonial_charts_to_tab(
    tab: QWidget,
    years,
    attivo,
    passivo,
):
    attivo_chart = create_attivo_area_chart(
        years,
        attivo["immobilizzazioni"],
        attivo["rimanenze"],
        attivo["crediti"],
        attivo["attivita_finanziarie"],
        attivo["disponibilita_liquide"],
    )

    passivo_chart = create_passivo_area_chart(
        years,
        passivo["patrimonio_netto"],
        passivo["debiti_lungo_termine"],
        passivo["debiti_breve_termine"],
        passivo["fondi_rischi_tfr"],
        passivo["altre_passivita"],
    )

    layout = tab.layout()

    if layout is None:
        layout = QVBoxLayout(tab)

    if attivo_chart._crises:
        details = " | ".join(
            f"{years[i]}: {value:,.0f} €"
            for i, value in attivo_chart._crises.items()
        )

        warning = QLabel(
            f"CRISI DI LIQUIDITÀ — {details}"
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            "color: #FF5252;"
            "background-color: #303030;"
            "font-weight: bold;"
            "padding: 8px;"
        )

        layout.addWidget(warning)

    layout.addWidget(attivo_chart, 1)
    layout.addWidget(passivo_chart, 1)

    return attivo_chart, passivo_chart