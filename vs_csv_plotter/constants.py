"""Constants used by csv_plotter"""
from matplotlib.font_manager import FontProperties

# File settings
DATA_FOLDER = "data/csv"
PLOT_FOLDER = "plot"
CSV_DOWNLOAD_LIST = [
    "https://cloud.vs-hdm.de/ocs/v2.php/apps/forms/api/v1.1/submissions/export/mLZLNgcYGBwR8JJg",
    "https://cloud.vs-hdm.de/ocs/v2.php/apps/forms/api/v1.1/submissions/export/G6fDXyzcQFZX2nSG"
]
PLOT_FILETYPE_LIST=["svg", "png"]

# Data
STUDENTS = 5500

# Default Settings
SAVE_PLOT = True
SHOW_PLOT = False
PLOTHEIGHT = 27
PLOTWIDTH = 17

# Style settings
HEADLINE_FONTSTYLE = FontProperties(
    fname="data/fonts/futura/Futura Bold font.ttf"
)
STANDART_FONTSTYLE = FontProperties(
    fname="data/fonts/futura/Futura Book font.ttf"
)
FOOTNOTE_FONTSTYLE = FontProperties(
    fname="data/fonts/futura/Futura Light Italic font.ttf"
)

CUSTOM_COLORS = [
    "#FEED00",
    "#FFB30D",
    "#B9E3F9",
]
TEXTCOLOR = "white"
BACKGROUNDCOLOR = "black"


HEADLINE_FONT = {
    "fontsize": 50,
    "weight": "bold",
    "fontproperties": HEADLINE_FONTSTYLE
}
DESCRIPTION_FONT = {
    "fontsize": 30,
    "fontproperties": STANDART_FONTSTYLE
}
FOOTNOTE_FONT = {
    "fontsize": 16,
    "color": "gray",
    "fontproperties": FOOTNOTE_FONTSTYLE
}
