from pygame import Color

# noinspection PyBroadException
try:
    # noinspection PyPackageRequirements
    from win32api import EnumDisplayDevices, EnumDisplaySettings
    FRAMERATE = EnumDisplaySettings(EnumDisplayDevices().DeviceName, -1).DisplayFrequency
except Exception:  # for whatever reason, if cannot find it or error with the module
    FRAMERATE = 60

BG_COLOR = Color(31, 35, 45)
DARKER_BLACK = Color(20, 20, 20)
DARK_WHITE = Color(245, 240, 246)
ACCENT_COLOR = Color(204, 255, 102)

WIDTH, HEIGHT = 1200, 800
