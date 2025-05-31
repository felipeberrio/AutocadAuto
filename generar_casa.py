from pyautocad import Autocad, APoint

acad = Autocad(create_if_not_exists=True)
print(f"Conectado a: {acad.doc.Name}")

muros_dibujados = set()

def dibujar_linea(p1, p2):
    acad.model.AddLine(APoint(*p1), APoint(*p2))

def dibujar_pared_con_puerta(p1, p2, puerta_pos, puerta_ancho, orientacion):
    if orientacion == "horizontal":
        x1, y = p1
        x2, _ = p2
        px = puerta_pos
        dibujar_linea((x1, y), (px, y))
        dibujar_linea((px + puerta_ancho, y), (x2, y))
    elif orientacion == "vertical":
        x, y1 = p1
        _, y2 = p2
        py = puerta_pos
        dibujar_linea((x, y1), (x, py))
        dibujar_linea((x, py + puerta_ancho), (x, y2))

def key_muro(p1, p2):
    return tuple(sorted([p1, p2]))

def dibujar_muro_unico(p1, p2, orientacion, puerta=None):
    clave = key_muro(p1, p2)
    if clave in muros_dibujados:
        return
    muros_dibujados.add(clave)
    if puerta:
        dibujar_pared_con_puerta(p1, p2, puerta, 900, orientacion)
    else:
        dibujar_linea(p1, p2)

def dibujar_cuarto(x, y, ancho, alto, nombre, muros={}):
    centro = APoint(x + ancho / 2, y + alto / 2)
    acad.model.AddText(nombre, centro, 300)

    sup_izq = (x, y + alto)
    sup_der = (x + ancho, y + alto)
    inf_izq = (x, y)
    inf_der = (x + ancho, y)

    if muros.get("inferior") != "omit":
        puerta = muros["inferior"] if isinstance(muros.get("inferior"), int) else None
        dibujar_muro_unico(inf_izq, inf_der, "horizontal", puerta)

    if muros.get("superior") != "omit":
        puerta = muros["superior"] if isinstance(muros.get("superior"), int) else None
        dibujar_muro_unico(sup_der, sup_izq, "horizontal", puerta)

    if muros.get("izquierda") != "omit":
        puerta = muros["izquierda"] if isinstance(muros.get("izquierda"), int) else None
        dibujar_muro_unico(sup_izq, inf_izq, "vertical", puerta)

    if muros.get("derecha") != "omit":
        puerta = muros["derecha"] if isinstance(muros.get("derecha"), int) else None
        dibujar_muro_unico(inf_der, sup_der, "vertical", puerta)

# Medida por módulo
mod = 3000

# Habitaciones
dibujar_cuarto(0, 6000, mod, mod, "HAB 1", {
    "derecha": 6600
})
dibujar_cuarto(3000, 6000, mod, mod, "SALA", {
    "superior": 3900,
    "inferior": 3900
})
dibujar_cuarto(6000, 6000, mod, mod, "HAB 2", {
    "izquierda": 6900
})
dibujar_cuarto(0, 0, mod, 6000, "COCINA", {
    "superior": 3900
})
dibujar_cuarto(3000, 0, mod, 6000, "SALA", {
    "inferior": 3900,
    "superior": "omit",
    "derecha": "omit"  # ← Agregado
})

dibujar_cuarto(6000, 0, mod, 6000, "BAÑO", {
    "superior": 6900,
    "izquierda": 3000  # Hueco para puerta en la mitad del muro
})

print("✅ ¡Plano corregido!")
