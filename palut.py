import math
from pxr import Usd, UsdGeom, Sdf
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


def ColorInterpolate(lamda: float, c1l: tuple, c2l: tuple):
    l1 = lamda
    l2 = 1 - lamda
    c1 = c1l[0]
    c2 = c2l[0]
    r = c1[0] * l1 + c2[0] * l2
    g = c1[1] * l1 + c2[1] * l2
    b = c1[2] * l1 + c2[2] * l2
    return [(r, g, b)]


def SetUsdPrimAttrString(graphPrim, attrName, attrValue: str):
    prim: Usd.Prim = graphPrim.GetPrim()
    attr = prim.CreateAttribute(attrName, Sdf.ValueTypeNames.String)
    attr.Set(attrValue)


def SetUsdPrimAttrFloat(graphPrim, attrName, attrValue: float):
    prim: Usd.Prim = graphPrim.GetPrim()
    attr = prim.CreateAttribute(attrName, Sdf.ValueTypeNames.Float)
    attr.Set(attrValue)


def SetUsdPrimAttrInt(graphPrim, attrName, attrValue: int):
    prim: Usd.Prim = graphPrim.GetPrim()
    attr = prim.CreateAttribute(attrName, Sdf.ValueTypeNames.Int)
    attr.Set(attrValue)


def SetUsdPrimAttrStringArray(graphPrim, attrName, attrValue: list):
    prim: Usd.Prim = graphPrim.GetPrim()
    attr = prim.CreateAttribute(attrName, Sdf.ValueTypeNames.StringArray)
    attr.Set(attrValue)


def DefinePrimFromString(stage, primname: str, formname: str):
    if formname == "xform":
        prim = UsdGeom.Xform.Define(stage, primname)
    elif formname == "cone":
        prim = UsdGeom.Cone.Define(stage, primname)
    elif formname == "cube":
        prim = UsdGeom.Cube.Define(stage, primname)
    elif formname == "sphere":
        prim = UsdGeom.Sphere.Define(stage, primname)
    else:
        if formname != "cyl":
            print(f"Unknown form: {formname}")
        prim = UsdGeom.Cylinder.Define(stage, primname)
    return prim


def AddLinkToPoint(stage, linkname, linkform, linkrad, linkcolor, ptarg, showlink=True):
    (xtarg, ytarg, ztarg) = ptarg
    leng = Magnitude(ptarg)
    lengzx = Magnitude((ztarg, xtarg))
    linkForm = linkform
    lnkrad = linkrad
    if not showlink:
        linkPrim = UsdGeom.Xform.Define(stage, linkname)
    else:
        linkPrim = DefinePrimFromString(stage, linkname, linkForm)

    yang = math.atan2(xtarg, ztarg) * 180 / math.pi
    linkPrim.AddRotateYOp().Set(yang)
    xang = math.atan2(-ytarg, lengzx) * 180 / math.pi
    linkPrim.AddRotateXOp().Set(xang)
    # the cylinder mesh is 2 units long, so scale it to half the length
    linkPrim.AddScaleOp().Set((lnkrad, lnkrad, leng / 2))
    linkPrim.AddTranslateOp().Set((0, 0, 1))

    if showlink:
        linkPrim.GetDisplayColorAttr().Set([linkcolor])

    SetUsdPrimAttrString(linkPrim, "deb:linkForm", linkForm)
    SetUsdPrimAttrFloat(linkPrim, "deb:linkRad", lnkrad)
    SetUsdPrimAttrFloat(linkPrim, "deb:xtarg", xtarg)
    SetUsdPrimAttrFloat(linkPrim, "deb:ytarg", ytarg)
    SetUsdPrimAttrFloat(linkPrim, "deb:ztarg", ztarg)
    SetUsdPrimAttrFloat(linkPrim, "deb:xang", xang)
    SetUsdPrimAttrFloat(linkPrim, "deb:yang", yang)

    return (xang, yang)


def DefineGrid(stage, gridparentname="/world", xmin=-20, xmax=20, zmin=-20, zmax=20, yval=0):
    gridname = f"{gridparentname}/grid"
    orgname = f"{gridname}/origin"
    org = UsdGeom.Sphere.Define(stage, orgname)
    org.AddTranslateOp().Set((0, yval, 0))
    org.AddScaleOp().Set((0.3, 0.3, 0.3))
    org.GetDisplayColorAttr().Set([(1, 1, 0.1)])
    xprim = UsdGeom.Xform.Define(stage, gridname)
    for i in range(xmin, xmax+1):
        for j in range(zmin, zmax+1):
            cname = f"{gridname}/cube_{i+1000}_{j+1000}"
            # print(cname)

            cube = UsdGeom.Cube.Define(stage, cname)
            cube.AddTranslateOp().Set((i, yval, j))
            cube.AddScaleOp().Set((0.1, 0.1, 0.1))
            if i % 10 == 0 and j % 10 == 0:
                cube.GetDisplayColorAttr().Set([(1, 0, 1)])
            elif i % 10 == 0:
                cube.GetDisplayColorAttr().Set([(0.15, 0.15, 1)])
            elif j % 10 == 0:
                cube.GetDisplayColorAttr().Set([(1, 0.15, 0.15)])


def LinComb(s1: float, v1: list, s2: float, v2: list):
    if len(v1) != len(v2):
        return None
    rv = []
    for i in range(len(v1)):
        n = s1 * v1[i] + s2 * v2[i]
        rv.append(n)
    return rv


def Magnitude(v: list):
    sumsq = 0
    for i in range(len(v)):
        sumsq += v[i] * v[i]
    mag = math.sqrt(sumsq)
    return mag
