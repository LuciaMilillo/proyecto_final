from colorama import Fore, Style, init

init(autoreset=True)

import validaciones
import sqlite3


def inventario_db():

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print("Conexion abierta a la base de datos")
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS inventario_productos(
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_producto TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio INTEGER NOT NULL,
                unidades INTEGER NOT NULL,
                descripcion TEXT NOT NULL
            )
            """
    )

    conexion.commit()
    conexion.close()
    print("Inventario de productos creado exitosamente")


# def inventario_db():

#     with sqlite3.connect("inventario.db") as conexion:
#         print("Conexion abierta a la base de datos")

#         cursor = conexion.cursor()

#         query_sql = """
#             CREATE TABLE IF NOT EXISTS inventario_productos(
#                 id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
#                 nombre_producto TEXT NOT NULL,
#                 categoria TEXT NOT NULL,
#                 precio INTEGER NOT NULL,
#                 unidades INTEGER NOT NULL,
#                 descripcion TEXT NOT NULL
#             )
#             """

#         cursor.execute(query_sql)

#         conexion.commit()
#         print("Inventario de productos creado exitosamente")


# producto_1 = ["Harina", "Almacen", 1000, 40, "Leudante"]
# producto_2 = ["Arroz", "Almacen", 1200, 45, "Parboli"]
# producto_3 = ["Leche", "Lacteos", 1350, 30, "Descremada"]
# producto_4 = ["Detergente", "Limpieza", 900, 80, "Rinde x5"]
# producto_5 = ["Atún ", "Conserva", 3500, 50, "Desmenuzado en Aceite"]


# listado_productos = [producto_1, producto_2, producto_3, producto_4, producto_5]


def gestion_db(operacion, datos):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    if operacion == "agregar":
        cursor.execute(
            """INSERT INTO inventario_productos(nombre_producto, categoria, precio, unidades, descripcion)
            VALUES (?, ?, ?, ?, ?) """,
            datos,
        )
    elif operacion == "mostrar":
        cursor.execute("""SELECT * FROM inventario_productos""")
        resultados = cursor.fetchall()
        return resultados

    elif operacion == "buscar_id":
        cursor.execute(
            """SELECT * FROM inventario_productos WHERE id_producto = ?""",
            (datos,),
        )
        return cursor.fetchall()

    elif operacion == "buscar_nombre":
        texto = normalizar(datos)
        cursor.execute(
            """
        SELECT * FROM inventario_productos
        WHERE
            REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                LOWER(nombre_producto),
                'á','a'),
                'é','e'),
                'í','i'),
                'ó','o'),
                'ú','u'),
                'ü','u'
            ) LIKE ?
    """,
            (f"%{texto}%",),
        )
        return cursor.fetchall()

    elif operacion == "buscar_categoria":
        texto = normalizar(datos)
        cursor.execute(
            """SELECT * FROM inventario_productos WHERE
            REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                LOWER(categoria),
                'á','a'),
                'é','e'),
                'í','i'),
                'ó','o'),
                'ú','u'),
                'ü','u'
            ) LIKE ?""",
            (f"%{texto}%",),
        )
        return cursor.fetchall()

    elif operacion == "modificar":
        cursor.execute(
            """UPDATE inventario_productos SET nombre_producto =?, categoria =?, precio=?, unidades =?, descripcion =? WHERE id_producto =?""",
            datos,
        )
    elif operacion == "eliminar":
        cursor.execute(
            """DELETE FROM inventario_productos WHERE id_producto =?""", datos
        )
    else:
        print("Operación inválida.")
        conexion.close()
        return
    conexion.commit()
    conexion.close()


def agregar_producto():
    print("\nIngresando un nuevo producto...")
    producto = validaciones.validar_nombre(input("\nIngrese un producto: "))

    categoria = validaciones.validar_categoria(input("\nIngrese una categoría: "))

    precio = validaciones.validar_valor(input("\nIngrese precio: "))

    unidades = validaciones.validar_cantidad(
        input("\nIngrese la cantidad de unidades disponibles: ")
    )

    descripcion = validaciones.validar_informacion(
        input("\nIngrese la descripción del producto: ")
    )

    gestion_db("agregar", (producto, categoria, precio, unidades, descripcion))

    print(f"El producto '{producto}' ha sido agregado con éxito.")


def mostrar_producto():
    print("\nMostrando todos los productos:\n")
    resultado = gestion_db("mostrar", (1,))
    for producto in resultado:
        print(
            f"Id: {producto[0]} - Producto: {producto[1]} - Categoria: {producto[2]} - Precio: {producto[3]} - Unidades: {producto[4]} - Descripción: {producto[5]}"
        )


def buscar_producto():
    print("\nBúsqueda de productos")

    print(
        """
    Buscar por:
    1. ID
    2. Nombre
    3. Categoría
    """
    )

    opcion = input("Seleccione una opción (1-3): ")

    if opcion == "1":
        try:
            id_busqueda = int(input("\nIngrese el ID del producto: "))
        except ValueError:
            print("ID inválido.")
            return

        resultados = gestion_db("buscar_id", id_busqueda)

        if not resultados:
            print("No existe un producto con ese ID.")
            return

        producto = resultados[0]

        print(
            f"\nId: {producto[0]} - Producto: {producto[1]} - Categoria: {producto[2]} "
            f"- Precio: {producto[3]} - Unidades: {producto[4]} - Descripción: {producto[5]}"
        )
        if producto[4] < 50:
            print("//Las unidades del producto son escasas. Considere renovar stock//")
        return

    elif opcion == "2":
        termino = normalizar(input("\nIngrese nombre o parte del nombre: "))

        resultados = gestion_db("buscar_nombre", termino)

        if not resultados:
            print("No se encontraron productos.")
            return

        print("\nResultados encontrados:\n")
        for p in resultados:
            print(
                f"Id: {p[0]} - Producto: {p[1]} - Categoria: {p[2]} "
                f"- Precio: {p[3]} - Unidades: {p[4]} - Descripción: {p[5]}"
            )
        if p[4] < 50:
            print("//Las unidades del producto son escasas. Considere renovar stock//")
        return

    elif opcion == "3":
        categoria = normalizar(input("\nIngrese la categoría: "))

        resultados = gestion_db("buscar_categoria", categoria)

        if not resultados:
            print("No hay productos con esa categoría.")
            return

        print("\nProductos en esa categoría:\n")
        for p in resultados:
            print(
                f"Id: {p[0]} - Producto: {p[1]} - Categoria: {p[2]} "
                f"- Precio: {p[3]} - Unidades: {p[4]} - Descripción: {p[5]}"
            )
            if p[4] < 50:
                print(
                    "//Las unidades del producto son escasas. Considere renovar stock//"
                )

    else:
        print("Opción inválida.")


def modificar_producto():

    print("\nModificar un producto")
    print(
        """
        Modificar por:
        1. ID
        2. Nombre
        """
    )

    opcion = input("Seleccione una opción (1-2): ")

    if opcion == "1":
        try:
            id_busqueda = int(input("\nIngrese el ID del producto a modificar: "))
        except ValueError:
            print("Debe ingresar un número válido.")
            return

        resultado = gestion_db("buscar_id", id_busqueda)

        if not resultado:
            print("No existe un producto con ese ID.")
            return

        producto = resultado[0]

    elif opcion == "2":
        nombre = normalizar(input("\nIngrese el nombre del producto: "))
        resultados = gestion_db("buscar_nombre", nombre)

        if not resultados:
            print("No se encontraron productos con ese nombre.")
            return

        print("\nCoincidencias encontradas:")
        for p in resultados:
            print(
                f"{p[0]} - {p[1]} (Categoría: {p[2]}, Precio: {p[3]}, Unidades: {p[4]}, Descripción: {p[5]})"
            )

        try:
            id_seleccion = int(
                input("\nIngrese el ID exacto del producto a modificar: ")
            )
        except ValueError:
            print("Debe ingresar un número válido.")
            return

        resultado = gestion_db("buscar_id", id_seleccion)

        if not resultado:
            print("ID inválido.")
            return

        producto = resultado[0]

    else:
        print("Opción no válida.")
        return

    print("\nProducto actual:")
    print(f" ID: {producto[0]}")
    print(f" Nombre: {producto[1]}")
    print(f" Categoría: {producto[2]}")
    print(f" Precio: {producto[3]}")
    print(f" Unidades: {producto[4]}")
    print(f" Descripción: {producto[5]}")

    nuevo_nombre = input("\nNuevo nombre (enter para mantener): ")
    if nuevo_nombre.strip() == "":
        nuevo_nombre = producto[1]

    nueva_categoria = input("Nueva categoría (enter para mantener): ")
    if nueva_categoria.strip() == "":
        nueva_categoria = producto[2]

    try:
        nuevo_precio = input("Nuevo precio (enter para mantener): ")
        if nuevo_precio.strip() == "":
            nuevo_precio = producto[3]
        else:
            nuevo_precio = int(nuevo_precio)
    except ValueError:
        print("Precio inválido.")
        return
    try:
        nuevas_unidades = input("Cantidad de unidades (enter para mantener): ")
        if nuevas_unidades.strip() == "":
            nuevas_unidades = producto[4]
        else:
            nuevas_unidades = int(nuevas_unidades)
    except ValueError:
        print("Unidades inválidas.")
        return

    nueva_descripcion = input("Nueva descripción (enter para mantener): ")
    if nueva_descripcion.strip() == "":
        nueva_descripcion = producto[5]

    datos_actualizados = (
        nuevo_nombre,
        nueva_categoria,
        nuevo_precio,
        nuevas_unidades,
        nueva_descripcion,
        producto[0],
    )
    gestion_db("modificar", datos_actualizados)

    print("\nProducto modificado correctamente.")
    if nuevas_unidades < 50:
        print("//Las unidades del producto son escasas. Considere renovar stock//")


def eliminar_producto():

    print("\nEliminar un producto")
    print(
        """
        Eliminar por:
        1. ID
        2. Nombre
        """
    )

    opcion = input("Seleccione una opción (1-2): ")

    if opcion == "1":
        try:
            id_busqueda = int(
                input("\nIngrese el ID del producto que desea eliminar: ")
            )
        except ValueError:
            print("Debe ingresar un número válido.")
            return

        resultado = gestion_db("buscar_id", id_busqueda)

        if not resultado:
            print("No existe un producto con ese ID.")
            return

        producto = resultado[0]

        print("\nHa seleccionado el siguiente producto para eliminar:")
        print(f" ID: {producto[0]}")
        print(f" Nombre: {producto[1]}")
        print(f" Categoría: {producto[2]}")
        print(f" Precio: {producto[3]}")

        confirmar = input("\n¿Está seguro de eliminarlo? (si/no): ").lower()

        if confirmar == "si":
            gestion_db("eliminar", (id_busqueda,))
            print(f"\nProducto '{producto[1]}' eliminado correctamente.")
        else:
            print("\nEliminación cancelada.")

    elif opcion == "2":
        nombre = normalizar(input("\nIngrese el nombre del producto a eliminar: "))

        resultados = gestion_db("buscar_nombre", nombre)

        if not resultados:
            print("No se encontraron productos con ese nombre.")
            return

        print("\nCoincidencias encontradas:")
        for p in resultados:
            print(f"{p[0]} - {p[1]} (Categoría: {p[2]}, Precio: {p[3]})")

        try:
            id_eliminar = int(
                input("\nIngrese el ID exacto del producto que desea eliminar: ")
            )
        except ValueError:
            print("Debe ingresar un número válido.")
            return

        confirmar = input("¿Está seguro de eliminar este producto? (si/no): ").lower()
        if confirmar == "si":
            gestion_db("eliminar", (id_eliminar,))
            print("\nProducto eliminado correctamente.")
        else:
            print("\nEliminación cancelada.")


def salir_sistema_gestion():
    confirmar = input(
        "\n¿Está seguro de que desea salir del sistema? (si/no): "
    ).lower()

    if confirmar == "si":
        print("\nSaliendo...\tHasta pronto")
        return False

    else:
        print("\n Volviendo al menú...")


def normalizar(texto):
    texto = texto.strip().lower()
    reemplazos = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ü", "u"),
    )
    for acento, sin_acento in reemplazos:
        texto = texto.replace(acento, sin_acento)
    return texto
