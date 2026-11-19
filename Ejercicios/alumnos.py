alumnos = [
    ('Carlos Gómez', 41008418, 5),
    ('Gabriela Torres', 45790918, 8),
    ('Juan Pérez', 48327044, 9),
    ('Éric Guay', 35360531, 7),
    ('Juana Monte', 31583398, 10),
    ('Carla Díaz', 43772387, 6)]

diccio_notas={}

for nombre, dni, nota in alumnos:
    diccio_notas[nombre] = nota

for nombre, nota in diccio_notas.items():
    print(Alumno: {nombre} - Nota: {nota})