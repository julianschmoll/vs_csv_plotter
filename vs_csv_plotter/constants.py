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
HEADLINE_FONTSTYLE = FontProperties(fname="data/fonts/futura/Futura Bold font.ttf")
STANDART_FONTSTYLE = FontProperties(fname="data/fonts/futura/Futura Book font.ttf")
FOOTNOTE_FONTSTYLE = FontProperties(fname="data/fonts/futura/Futura Light Italic font.ttf")

CUSTOM_COLORS = [
    "#FEED00", 
    "#FFB30D", 
    "#B9E3F9", 
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