__author__ = "kai_Ker"
__version__ = "1.3.3"


class MainWindow:
    size = (1200, 650)

    class Labels:
        main_geometry = (100, 30, 1000, 300)

        @staticmethod
        def hint_geometry(idx) -> tuple[int, int, int, int]:
            return 170 * idx + 20, 360, 140, 200

    class AutoPlay:
        slider_geometry = (300, 600, 600, 35)
        play_geometry = (220, 600, 70, 35)
        load_geometry = (910, 600, 70, 35)
        info_geometry = (20, 600, 190, 35)
        file_geometry = (990, 600, 190, 35)

    class CreateVideo:
        button_geometry = (0, 0, 60, 30)


class Style:
    slider = """\
/* 滑块的样式 */
QSlider::groove:horizontal {
    border: .5px solid #00B0AE;
    background: #00B0AE;
    height: 2px;
    border-radius: 1px;
    padding-left:0px;
    padding-right:0px;
}

/* 滑块经过的颜色:前面的颜色 */
QSlider::sub-page:horizontal {
    background: #00B0AE;
    border: 1px solid #00B0AE;
    height: 2px;
    border-radius: 2px;
}

QSlider::add-page:horizontal {
    background: #EAEAEA;
    border: 0px solid #EAEAEA;
    height: 2px;
    border-radius: 2px;
}

QSlider::handle:horizontal 
{
    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, 
    stop: 0.6 #00B0AE, stop:0.98409 rgba(255, 255, 255, 255));

    width: 15px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 5px;
}

QSlider::handle:horizontal:hover {
    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, 
    stop:0.6 #00B0AE,stop:0.98409 rgba(255, 255, 255, 255));

    width: 15px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: 5px;
}"""
