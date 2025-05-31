from pyautocad import Autocad, APoint

# Conecta con AutoCAD
acad = Autocad(create_if_not_exists=True)

# Imprime nombre del documento actual
print(f"Conectado a: {acad.doc.Name}")

# Dibuja un rectángulo en coordenadas 0,0 con tamaño 5000x3000
p1 = APoint(0, 0)
p2 = APoint(5000, 0)
p3 = APoint(5000, 3000)
p4 = APoint(0, 3000)

# Añade líneas al modelo
acad.model.AddLine(p1, p2)
acad.model.AddLine(p2, p3)
acad.model.AddLine(p3, p4)
acad.model.AddLine(p4, p1)

print("Rectángulo dibujado")
