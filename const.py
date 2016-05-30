

IMAGE_SIZE_MIN = 50
IMAGE_SIZE_MAX = 5000
IMAGE_SIZE_DEF = 500


BACK_COLORS = [
    (247, 202, 201), # Rose Quartz
    (247, 120, 107), # Peach Echo
    (145, 168, 208), # Serenity
    (  3,  79, 132), # Snorkel Blue
    (249, 231,  42), # Buttercup
    (152, 221, 222), # Limpet Shell
    (152, 150, 164), # Lilac Gray
    (220,  68,  58), # Fiesta
    (177, 143, 106), # Iced Coffee
    (121, 199,  83), # Green Flash
]


BODY_COLORS = [
    'aqua', 'azure', 'black', 'brown', 'red', 'blue', 'green', 'cyan',
]


HELP_STRING = (
    'Content-Type: text/plain\n\n'
    '  ** Help **\n\n'
    '  size=integer\n'
    '    sets size of image (square) sides\n'
    '    lies within the range [{}, {}]px, defaulting to {}px\n\n'
    '  help=[true|yes|y|1]\n'
    '    give this help page\n\n'
    '  debug=[true|yes|y|1]\n'
    '    prints values of variables and GET arguments\n'
    '    setting debug to True makes help False\n\n'
).format(IMAGE_SIZE_MIN, IMAGE_SIZE_MAX, IMAGE_SIZE_DEF).encode('utf-8')

