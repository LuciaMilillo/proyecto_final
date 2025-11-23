from colorama import Fore, Style, init

init(autoreset=True)
import funciones

funciones.inventario_db()

print("\nBienvenido")

menu = """
    ***** Menú de opciones *****
    1. Agregar un producto
    2. Mostrar todos los productos
    3. Buscar un producto
    4. Modificar un producto
    5. Eliminar un producto
    6. Salir
    ****************************
"""
while True:

    print(menu)
    opcion = input("Seleccione una opcíon para continuar: ")

    match opcion:
        case "1":
            funciones.agregar_producto()
        case "2":
            funciones.mostrar_producto()
        case "3":
            funciones.buscar_producto()
        case "4":
            funciones.modificar_producto()
        case "5":
            funciones.eliminar_producto()
        case "6":
            if funciones.salir_sistema_gestion() == False:
                break
        case _:
            print("\nOpción incorrecta. Intente de nuevo.")
