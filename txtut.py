from colored import fg, bg, Style

r1 = bg('navy_blue') + fg('red')
c1 = bg('navy_blue') + fg('white')
c2 = bg('navy_blue') + fg('light_yellow')
c3 = bg('navy_blue') + fg('green')
c4 = bg('navy_blue') + fg('light_magenta')
c5 = bg('navy_blue') + fg('light_cyan')
rst = Style.reset


def StrToColor(colorstr: str):
    nclr = colorstr
    if colorstr[0] == "#":
        nclr = colorstr[1:]
    if len(nclr) != 6:
        return (False, [(0.5, 0, 0)])
    r = int(nclr[0:2], 16) / 255.0
    g = int(nclr[2:4], 16) / 255.0
    b = int(nclr[4:6], 16) / 255.0
    color = [(r, g, b)]
    return (True, color)
