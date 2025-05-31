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
    if puerta is not None:
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

# Medidas base
mod_sala = 3000
mod_hab = 1500
mod_bano = 1000
mod_cocina_ancho = 3000
mod_cocina_alto = 1500

# Coordenadas base
x_sala = 3000
y_sala = 3000

# SALA
dibujar_cuarto(x_sala, y_sala, mod_sala, mod_sala, "SALA", {
    "inferior": x_sala + mod_sala // 2 - 450  # Entrada principal
})

# MASTER BEDROOM
x_master = x_sala
y_master = y_sala + mod_sala
dibujar_cuarto(x_master, y_master, mod_sala, mod_hab, "MASTER", {
    "superior": x_master + mod_sala // 2 - 450,  # hacia baño privado
    "inferior": x_master + mod_sala // 2 - 450   # hacia sala
})

# BAÑO PRIVADO
x_priv = x_master
y_priv = y_master + mod_hab
dibujar_cuarto(x_priv, y_priv, mod_sala, mod_bano, "BAÑO PRIV", {
    "inferior": x_priv + mod_sala // 2 - 450
})

# BAÑO AUXILIAR (a la derecha de la sala)
x_aux = x_sala + mod_sala
y_aux = y_sala + mod_sala // 2
dibujar_cuarto(x_aux, y_aux, mod_hab, mod_bano, "BAÑO AUX", {
    "izquierda": y_aux + mod_bano // 2 - 450
})

# HABITACIÓN 2 (abajo a la derecha)
x_hab2 = x_sala + mod_sala // 2 + mod_hab // 2
y_hab2 = y_sala - mod_hab * 2
dibujar_cuarto(x_hab2, y_hab2, mod_hab, mod_sala, "HAB 2", {
    "superior": x_hab2 + mod_hab // 2 - 450  # hacia sala
})

# COCINA (abajo a la izquierda)
x_cocina = x_sala - mod_cocina_ancho
y_cocina = y_sala - mod_cocina_alto
dibujar_cuarto(x_cocina, y_cocina, mod_cocina_ancho, mod_cocina_alto, "COCINA", {
    "superior": x_cocina + mod_cocina_ancho // 2 - 450,  # hacia sala
    "inferior": x_cocina + mod_cocina_ancho // 2 - 450   # salida secundaria
})

print("✅ Plano generado en AutoCAD con distribución completa.")
