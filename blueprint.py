from pyautocad import Autocad, APoint
import random

acad = Autocad(create_if_not_exists=True)
print(f"✅ Connected to AutoCAD: {acad.doc.Name}")

habitaciones = []

def draw_line(p1, p2):
    acad.model.AddLine(APoint(*p1), APoint(*p2))

def draw_wall_with_door(p1, p2, door_pos, door_width, orientation):
    if orientation == "horizontal":
        x1, y = p1
        draw_line((x1, y), (door_pos, y))
        draw_line((door_pos + door_width, y), (p2[0], y))
    elif orientation == "vertical":
        x, y1 = p1
        draw_line((x, y1), (x, door_pos))
        draw_line((x, door_pos + door_width), (x, p2[1]))

def draw_wall(p1, p2, orientation, door=None):
    if door is not None:
        draw_wall_with_door(p1, p2, door, 900, orientation)
    else:
        draw_line(p1, p2)

def draw_room(x, y, width, height, name, walls={}):
    habitaciones.append((x, y, width, height))
    center = APoint(x + width / 2, y + height / 2)
    acad.model.AddText(name, center, 150)

    top_left = (x, y + height)
    top_right = (x + width, y + height)
    bottom_left = (x, y)
    bottom_right = (x + width, y)

    if "top" in walls:
        draw_wall(top_right, top_left, "horizontal", walls["top"])
    else:
        draw_wall(top_right, top_left, "horizontal")

    if "bottom" in walls:
        draw_wall(bottom_left, bottom_right, "horizontal", walls["bottom"])
    else:
        draw_wall(bottom_left, bottom_right, "horizontal")

    if "left" in walls:
        draw_wall(top_left, bottom_left, "vertical", walls["left"])
    else:
        draw_wall(top_left, bottom_left, "vertical")

    if "right" in walls:
        draw_wall(bottom_right, top_right, "vertical", walls["right"])
    else:
        draw_wall(bottom_right, top_right, "vertical")

# Dimensiones
sala = 3000
hab = sala // 2
bano = hab // 3
cocina_w = sala
cocina_h = hab

# Posiciones alineadas correctamente
layout = {
    "Living Room": (3000, 3000),
    "Master Bedroom": (3000, 6000),
    "Private Bathroom": (3000, 7500),
    "Guest Bathroom": (6000, 3000),
    "Bedroom 2": (6000, 0),
    "Kitchen": (3000, 0),
}

# Funciones para calcular puertas centradas
def puerta_h(x_ini, x_fin):
    return x_ini + (x_fin - x_ini) // 2 - 450

def puerta_v(y_ini, y_fin):
    return y_ini + (y_fin - y_ini) // 2 - 450

# Dibujo de cada habitación con puertas interiores correctas
draw_room(*layout["Living Room"], sala, sala, "Living Room", {
    "bottom": puerta_h(layout["Living Room"][0], layout["Living Room"][0] + sala),
    "right": puerta_v(layout["Living Room"][1], layout["Living Room"][1] + sala)
})
draw_room(*layout["Master Bedroom"], sala, hab, "Master Bedroom", {
    "top": puerta_h(layout["Master Bedroom"][0], layout["Master Bedroom"][0] + sala),
    "bottom": puerta_h(layout["Master Bedroom"][0], layout["Master Bedroom"][0] + sala)
})
draw_room(*layout["Private Bathroom"], sala, bano, "Private Bathroom", {
    "bottom": puerta_h(layout["Private Bathroom"][0], layout["Private Bathroom"][0] + sala)
})
draw_room(*layout["Guest Bathroom"], hab, bano, "Guest Bathroom", {
    "left": puerta_v(layout["Guest Bathroom"][1], layout["Guest Bathroom"][1] + bano)
})
draw_room(*layout["Bedroom 2"], hab, sala, "Bedroom 2", {
    "top": puerta_h(layout["Bedroom 2"][0], layout["Bedroom 2"][0] + hab)
})
draw_room(*layout["Kitchen"], cocina_w, cocina_h, "Kitchen", {
    "top": puerta_h(layout["Kitchen"][0], layout["Kitchen"][0] + cocina_w)
})

# Contorno más amplio (jardín)
min_x = min(x for x, y, w, h in habitaciones) - 1500
max_x = max(x + w for x, y, w, h in habitaciones) + 1500
min_y = min(y for x, y, w, h in habitaciones) - 1500
max_y = max(y + h for x, y, w, h in habitaciones) + 1500

draw_line((min_x, min_y), (max_x, min_y))
draw_line((max_x, min_y), (max_x, max_y))
draw_line((max_x, max_y), (min_x, max_y))
draw_line((min_x, max_y), (min_x, min_y))

print("✅ Plano generado con puertas internas visibles y cocina conectada a sala.")
