import random
from itertools import product
from pyautocad import Autocad, APoint

acad = Autocad(create_if_not_exists=True)
print(f"Conectado a: {acad.doc.Name}")

muros_dibujados = set()
modulo = 3000
puerta_ancho = 900

def dibujar_linea(p1, p2):
    acad.model.AddLine(APoint(*p1), APoint(*p2))

def dibujar_pared_con_puerta(p1, p2, puerta_pos, orientacion):
    if orientacion == "horizontal":
        x1, y = p1
        px = puerta_pos
        dibujar_linea((x1, y), (px, y))
        dibujar_linea((px + puerta_ancho, y), (p2[0], y))
    else:
        x, y1 = p1
        py = puerta_pos
        dibujar_linea((x, y1), (x, py))
        dibujar_linea((x, py + puerta_ancho), (x, p2[1]))

def key_muro(p1, p2):
    return tuple(sorted([p1, p2]))

def dibujar_muro_unico(p1, p2, orientacion, puerta_pos=None):
    clave = key_muro(p1, p2)
    if clave in muros_dibujados:
        return
    muros_dibujados.add(clave)
    if puerta_pos:
        dibujar_pared_con_puerta(p1, p2, puerta_pos, orientacion)
    else:
        dibujar_linea(p1, p2)

def dibujar_cuarto(x, y, ancho, alto, nombre, muros={}):
    sup_izq = (x, y + alto)
    sup_der = (x + ancho, y + alto)
    inf_izq = (x, y)
    inf_der = (x + ancho, y)
    centro = APoint(x + ancho / 2, y + alto / 2)
    acad.model.AddText(nombre, centro, 300)

    # Inferior
    if muros.get("inferior") != "omit":
        puerta = muros["inferior"] if isinstance(muros.get("inferior"), int) else None
        dibujar_muro_unico(inf_izq, inf_der, "horizontal", puerta)

    # Superior
    if muros.get("superior") != "omit":
        puerta = muros["superior"] if isinstance(muros.get("superior"), int) else None
        dibujar_muro_unico(sup_der, sup_izq, "horizontal", puerta)

    # Izquierda
    if muros.get("izquierda") != "omit":
        puerta = muros["izquierda"] if isinstance(muros.get("izquierda"), int) else None
        dibujar_muro_unico(sup_izq, inf_izq, "vertical", puerta)

    # Derecha
    if muros.get("derecha") != "omit":
        puerta = muros["derecha"] if isinstance(muros.get("derecha"), int) else None
        dibujar_muro_unico(inf_der, sup_der, "vertical", puerta)

# 1. Grilla y selección aleatoria
grilla = list(product(range(3), range(3)))
random.shuffle(grilla)
cuartos_pos = grilla[:random.randint(4, 6)]
nombres_disponibles = ["HAB", "SALA", "COCINA", "BAÑO", "ESTUDIO", "COMEDOR"]

cuartos = []
for i, (gx, gy) in enumerate(cuartos_pos):
    cuartos.append({
        "nombre": nombres_disponibles[i % len(nombres_disponibles)],
        "grid": (gx, gy),
        "x": gx * modulo,
        "y": gy * modulo
    })

# 2. Detectar adyacencias
direcciones = {
    (1, 0): ("derecha", "izquierda"),
    (-1, 0): ("izquierda", "derecha"),
    (0, 1): ("superior", "inferior"),
    (0, -1): ("inferior", "superior")
}

# Inicializar muros de cada cuarto
for c in cuartos:
    c["muros"] = {}

# Crear puertas entre cuartos adyacentes
for i, c1 in enumerate(cuartos):
    for j, c2 in enumerate(cuartos):
        if i >= j:
            continue
        dx = c2["grid"][0] - c1["grid"][0]
        dy = c2["grid"][1] - c1["grid"][1]
        if (dx, dy) in direcciones:
            lado_c1, lado_c2 = direcciones[(dx, dy)]

            if lado_c1 in ["superior", "inferior"]:
                puerta_pos = c1["x"] + modulo // 3
            else:
                puerta_pos = c1["y"] + modulo // 3

            c1["muros"][lado_c1] = puerta_pos
            c2["muros"][lado_c2] = "omit"  # evita línea duplicada

# 3. Dibujar todos los cuartos
for c in cuartos:
    dibujar_cuarto(c["x"], c["y"], modulo, modulo, c["nombre"], c["muros"])

print("✅ Plano aleatorio con cuartos conectados generado exitosamente.")
