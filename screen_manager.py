viewing_screen = "main menu"

possible_screens = [
    "main menu",
    "game",
    "credits",
]


def get_current_screen() -> str:
    return viewing_screen


def set_current_screen(set_to: str) -> None:
    global viewing_screen
    viewing_screen = set_to
    if set_to not in possible_screens:
        raise NotImplementedError(f"trying to set viewing screen to {set_to}")
