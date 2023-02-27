__author__ = "kai_Ker"
__version__ = "1.0.2"


class MainWindow:
    size = (1200, 630)

    class Labels:
        main_geometry = (100, 30, 1000, 300)

        @staticmethod
        def hint_geometry(idx) -> tuple[int, int, int, int]:
            return 170 * idx + 20, 360, 140, 200
