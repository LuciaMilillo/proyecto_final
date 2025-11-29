from estilos_programa import ERROR, OK, AVISO, INFO, NEGRITA


def validar_nombre(producto):
    while True:
        if producto.strip():
            return producto.title()
        else:
            # evita vacío en producto ingresado
            print(
                ERROR
                + "\nEl nombre del producto no puede estar vacío. Pruebe reingresar"
            )
            producto = input("\nIngrese nuevamente el nombre del producto: ")


def validar_categoria(categoria):
    while True:

        if categoria.strip():  # evita vacío en categoría
            return categoria.title()
        else:
            print(
                ERROR
                + "\nLa categoría del producto no puede estar vacía. Pruebe reingresar"
            )
            categoria = input("\nIngrese nuevamente la categoría: ")


def validar_valor(precio):
    while True:
        precio = precio.strip()
        if precio.isdigit() and int(precio) > 0:
            return int(precio)
        else:
            print(
                ERROR
                + "\nEl valor precio debe ser un número entero positivo y no puede estar vacío. Intente nuevamente"
            )
            precio = input("\nIngrese el precio del producto nuevamente: ")


def validar_cantidad(unidades):
    while True:
        unidades = unidades.strip()
        if (
            unidades.isdigit() and int(unidades) > 0
        ):  # se va a asegurar que sea numérico y que sea mayor a cero.
            return int(unidades)
        else:
            print(
                ERROR
                + "\nLa cantidad de unidades debe ser un número entero positivo y no puede quedar vacía. Intente nuevamente"
            )
            unidades = input("\nIngrese la cantidad de unidades nuevamente: ")


def validar_informacion(descripcion):
    while True:

        if descripcion.strip():
            return descripcion.title()
        else:
            print(ERROR + "\nLa descripción no puede estar vacía.Pruebe reingresar.")
            descripcion = input("\nIngrese la descripción del producto nuevamente.")
