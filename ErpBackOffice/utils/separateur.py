import math

def AfficheEntier(n, sep=" "):
    """
        #print(n)
        s = str(n)
        #print(s)
        l = len(s)
        nc = 0
        res = ""
        for i in range(l-1, -1, -1):
            res = s[i] + res
            nc += 1
            if nc == 3:
                res = sep + res
                nc = 0
        if res.startswith(sep):
            res = res[1:]

        if n < 0 and res[1] == sep:
            res = list(res)
            del res[1]
            res = "".join(res)
        return res
    """
    s = 0
    if n % 1 == 0:
            s = str(int(n))
    else:
            s = str(n)

    #print(s)

    l = len(s)
    nc = 0
    res = ""
    for i in range(l-1, -1, -1):
        res = s[i] + res
        nc += 1
        if nc == 3:
            res = sep + res
            nc = 0
    if res.startswith(sep):
        res = res[1:]
    if n < 0 and res[1] == sep:
        res = list(res)
        del res[1]
        res = "".join(res)
    return res



def makeFloat(nombre):
    if isinstance(nombre,str):
        nombre = nombre.replace(" ","")
        nombre = nombre.replace(",",".")
        if nombre == "": nombre = "0.0"
        # print("nombre str {}".format(nombre))
        nombre = float(nombre)
        if math.isnan(nombre): nombre = 0.0
        return nombre
    elif isinstance(nombre, int):
        nombre = str(nombre)
        if nombre == "": nombre = "0.0"
        #print("nombre int {}".format(nombre))
        nombre = float(nombre)
        if math.isnan(nombre): nombre = 0.0
        return nombre
    elif isinstance(nombre, float):
        #print("nombre float {}".format(nombre))
        if math.isnan(nombre): nombre = 0.0
        return nombre
    elif nombre is None:
        #print("nombre float {}".format(nombre))
        nombre = 0.0
        return nombre
    else:
        #print("nombre others {}".format(nombre))
        nombre = float(nombre)
        if math.isnan(nombre): nombre = 0.0
        return nombre


def makeStringFromFloatExcel(nombre):
    if nombre:
        if isinstance(nombre, float):
            return str(int(nombre))
    return nombre

def makeInt(nombre):
    if isinstance(nombre,str):
        if nombre == "": nombre = "0"
        #print("nombre str {}".format(nombre))
        nombre = int(nombre)
        if math.isnan(nombre): nombre = 0
        return nombre
    elif isinstance(nombre, float):
        nombre = str(nombre)
        if nombre == "": nombre = "0"
        #print("nombre float {}".format(nombre))
        nombre = int(nombre)
        if math.isnan(nombre): nombre = 0
        return nombre
    elif isinstance(nombre, int):
        #print("nombre int {}".format(nombre))
        if math.isnan(nombre): nombre = 0
        return nombre
    elif nombre is None:
        #print("nombre int {}".format(nombre))
        nombre = 0
        return nombre
    else:
        #print("nombre others {}".format(nombre))
        nombre = int(nombre)
        if math.isnan(nombre): nombre = 0
        return nombre

def makeIntId(nombre):
    nombre = makeInt(nombre)
    if nombre == 0: nombre = None
    return nombre

