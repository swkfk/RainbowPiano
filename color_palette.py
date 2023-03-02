class RainbowColor:
    eng_name = [
        "red",
        "orange",
        "yellow",
        "green",
        "cyan",
        "blue",
        "purple",
    ]

    color_lst = [
        ("赤", (255, 0, 0)),
        ("橙", (255, 165, 0)),
        ("黄", (255, 255, 0)),
        ("绿", (0, 255, 0)),
        ("青", (0, 127, 255)),
        ("蓝", (0, 0, 255)),
        ("紫", (139, 0, 255)),
    ]

    board_lst = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
    ]

    tone_lst = [
        ("do", "060.wav"),
        ("re", "062.wav"),
        ("mi", "064.wav"),
        ("fa", "065.wav"),
        ("sol", "067.wav"),
        ("la", "069.wav"),
        ("si", "071.wav"),
    ]

    @staticmethod
    def get_color_by_board(brd) -> tuple[str, tuple[int, int, int]]:
        return RainbowColor.color_lst[RainbowColor.board_lst[brd]]

    @staticmethod
    def get_tone_by_board(brd) -> tuple[str, str]:
        return RainbowColor.tone_lst[brd]
