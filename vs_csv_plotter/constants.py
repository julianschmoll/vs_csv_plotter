from matplotlib.font_manager import FontProperties


# File settings
DATA_FOLDER = "data/csv"
PLOT_FOLDER = "plot"

# Data
STUDENTS=5500

# Default Settings
SAVE_PLOT = True
SHOW_PLOT = False

# Style settings
HEADLINE_FONTSTYLE = FontProperties(fname="data/fonts/open-sans-v34-latin-800.ttf")
STANDART_FONTSTYLE = FontProperties(fname="data/fonts/open-sans-v34-latin-500.ttf")
FOOTNOTE_FONTSTYLE = FontProperties(fname="data/fonts/open-sans-v34-latin-300italic.ttf")

CUSTOM_COLORS = [
    "#086b66", 
    "#f7931e", 
    "#ffcb05", 
]
HEADLINE_FONT = {
    "fontsize": 16, 
    "weight": "bold", 
    "fontproperties": HEADLINE_FONTSTYLE
}
DESCRIPTION_FONT = {
    "fontsize": 10,
    "fontproperties": STANDART_FONTSTYLE
}
FOOTNOTE_FONT = {
    "fontsize": 5, 
    "color": "gray",
    "fontproperties": FOOTNOTE_FONTSTYLE
}