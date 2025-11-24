from estilos_programa import ERROR, NEGRITA

from funciones import (
    agregar_producto,
    mostrar_producto,
    modificar_producto,
    buscar_producto,
    eliminar_producto,
    salir_sistema_gestion,
    inventario_db,
)

inventario_db()

print(NEGRITA + "\nBienvenido")

menu = """
    *****  Menú de opciones  *****
    1. Agregar un producto
    2. Mostrar todos los productos
    3. Buscar un producto
    4. Modificar un producto
    5. Eliminar un producto
    6. Salir
    ******************************\n
"""
while True:

    print(menu)
    opcion = input(NEGRITA + "Seleccione una opcíon para continuar: ")

    match opcion:
        case "1":
            agregar_producto()
        case "2":
            mostrar_producto()
        case "3":
            buscar_producto()
        case "4":
            modificar_producto()
        case "5":
            eliminar_producto()
        case "6":
            if salir_sistema_gestion() == False:
                break
        case _:
            print(ERROR + "\nOpción incorrecta. Intente de nuevo.")
