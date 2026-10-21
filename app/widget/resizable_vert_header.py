from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtWidgets import QHeaderView, QTableView


class ResizableVerticalHeader(QHeaderView):
    """Vertical Header per le tabelle che è ridimensionabile in tutte le dimensioni.
    La riga corrispondente ad una sezione può essere evidenziata cliccando
    sulla rispettiva sezione. """

    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Vertical, parent)
        self.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.setMinimumSectionSize(25)
        self._header_width = 200
        self._resizing_width = False
        self._resize_margin = 20        # Indica il margine interno in cui si può ridimensionare
        self._min_width = 60
        self.setDefaultSectionSize(35)
        self.setMouseTracking(True)
        self.setSectionsClickable(True)

    def sizeHint(self):
        size = super().sizeHint()
        return QSize(self._header_width, size.height())

    def mousePressEvent(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and event.position().x() >= self.width() - self._resize_margin
        ):
            self._resizing_width = True
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        x = event.position().x()

        if self._resizing_width:
            new_width = max(self._min_width, int(x))
            self._header_width = new_width
            self.updateGeometry()

            if self.parentWidget():
                self.parentWidget().updateGeometries()

            event.accept()
            return

        if x >= self.width() - self._resize_margin:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            event.accept()
            return

        self.unsetCursor()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        if not self._resizing_width:
            self.unsetCursor()
        super().leaveEvent(event)

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