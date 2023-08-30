from PyQt5.QtWidgets import QLayout, QHBoxLayout, QVBoxLayout


class _LayoutManager:
    # def __init__(self, parent=None):
    #     print(f"The layout manager is {self}")
    #     super().__init__(parent)

    def __new__(cls, parent=None) -> QLayout:
        # Ovde bi se mogao npr. konkretan tip layouta izvuci iz konfiguracije i kao takav vratiti.
        return QVBoxLayout(parent)
