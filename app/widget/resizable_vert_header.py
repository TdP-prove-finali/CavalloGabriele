
from PySide6.QtCore import Qt, QSize, QEvent, QTimer
from PySide6.QtWidgets import QHeaderView, QTableView


class ResizableVerticalHeader(QHeaderView):
    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Vertical, parent)

        self.setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.setMinimumSectionSize(35)
        self.setDefaultSectionSize(35)
        self.setMouseTracking(True)
        self.setSectionsClickable(True)

        self._header_width = 200
        self._min_width = 60
        self._resize_margin = 20

        self._resizing_width = False
        self._auto_width = True
        self._updating_width = False

        self._table = None
        self._connected_horizontal_header = None

        if isinstance(parent, QTableView):
            self.attachToTable(parent)

    def attachToTable(self, table: QTableView):
        if self._table is table:
            return

        if self._table is not None:
            self._table.removeEventFilter(self)

        if self._connected_horizontal_header is not None:
            try:
                self._connected_horizontal_header.sectionResized.disconnect(
                    self._on_horizontal_section_resized
                )
            except (TypeError, RuntimeError):
                pass

        self._table = table
        self._table.installEventFilter(self)

        horizontal_header = table.horizontalHeader()

        horizontal_header.sectionResized.connect(
            self._on_horizontal_section_resized
        )

        self._connected_horizontal_header = horizontal_header

        QTimer.singleShot(0, self.updateAutoWidth)

    def sizeHint(self):
        size = super().sizeHint()
        return QSize(self._header_width, size.height())

    def setAutoWidth(self, enabled: bool):
        self._auto_width = enabled

        if enabled:
            self.updateAutoWidth()

    def isAutoWidth(self):
        return self._auto_width

    def setHeaderWidth(self, width: int):
        self._auto_width = False
        self._apply_width(width)

    def _apply_width(self, width: int):
        width = max(self._min_width, int(width))

        if self._header_width == width:
            return

        if self._updating_width:
            return

        self._updating_width = True

        try:
            self._header_width = width
            self.updateGeometry()

            if self._table is not None:
                self._table.updateGeometries()

        finally:
            self._updating_width = False

    def updateAutoWidth(self):
        if not self._auto_width:
            return

        if self._resizing_width:
            return

        if self._table is None:
            return

        table = self._table

        if not table.isVisible():
            return

        available_width = table.contentsRect().width()
        columns_width = 0

        for column in range(table.model().columnCount()) if table.model() else []:
            if not table.isColumnHidden(column):
                columns_width += table.columnWidth(column)
        scrollbar = table.verticalScrollBar()

        scrollbar_width = (
            scrollbar.width() if scrollbar.isVisible() else 0
        )
        remaining_width = (
            available_width
            - columns_width
            - scrollbar_width
        )

        self._apply_width(
            max(self._min_width, remaining_width)
        )

    def _on_horizontal_section_resized(
        self
    ):
        if self._auto_width:
            QTimer.singleShot(0, self.updateAutoWidth)

    def eventFilter(self, watched, event):
        if watched is self._table:
            if event.type() in (
                QEvent.Type.Resize,
                QEvent.Type.Show,
                QEvent.Type.LayoutRequest,
            ):
                if self._auto_width:
                    QTimer.singleShot(0, self.updateAutoWidth)

        return super().eventFilter(watched, event)

    def mousePressEvent(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and event.position().x()
            >= self.width() - self._resize_margin
        ):
            self._resizing_width = True
            self._auto_width = False

            self.setCursor(Qt.CursorShape.SizeHorCursor)

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        x = event.position().x()

        if self._resizing_width:
            new_width = max(self._min_width, int(x))

            self._apply_width(new_width)

            event.accept()
            return

        if x >= self.width() - self._resize_margin:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            event.accept()
            return

        self.unsetCursor()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._resizing_width:
            self._resizing_width = False

            x = event.position().x()

            if x >= self.width() - self._resize_margin:
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            else:
                self.unsetCursor()

            event.accept()
            return

        super().mouseReleaseEvent(event)

    def leaveEvent(self, event):
        if not self._resizing_width:
            self.unsetCursor()

        super().leaveEvent(event)