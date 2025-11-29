from estilos_programa import ERROR, OK, AVISO, INFO, NEGRITA

# en un archivo aparte creé variables para gestionar colorama de una manera más limpia

from validaciones import (
    validar_cantidad,
    validar_categoria,
    validar_informacion,
    validar_nombre,
    validar_valor,
)
import sqlite3


def inventario_db():

    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    print(OK + "Conexion abierta a la base de datos")
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


# producto_1 = ["Harina", "Almacen", 1000, 40, "Leudante"]
# producto_2 = ["Arroz", "Almacen", 1200, 45, "Parboli"]
# producto_3 = ["Leche", "Lacteos", 1350, 30, "Descremada"]
# producto_4 = ["Detergente", "Limpieza", 900, 80, "Rinde x5"]
# producto_5 = ["Atún ", "Conserva", 3500, 50, "Desmenuzado en Aceite"]
# mis productos precargados. los mismos de la preentrega
# (valores nuevos. agregados los atributos "unidades" y "descripción")

#  listado_productos = [producto_1, producto_2, producto_3, producto_4, producto_5]
# <<antiguo inventario con lista>>

#   Creé una función que gestiona sqlite3


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
        print(ERROR + "Operación inválida.")
        conexion.close()
        return
    conexion.commit()
    conexion.close()


def agregar_producto():
    print("\nIngresando un nuevo producto...")
    producto = validar_nombre(input("\nIngrese un producto: "))

    categoria = validar_categoria(input("\nIngrese una categoría: "))

    precio = validar_valor(input("\nIngrese precio: "))

    unidades = validar_cantidad(
        input("\nIngrese la cantidad de unidades disponibles: ")
    )

    descripcion = validar_informacion(input("\nIngrese la descripción del producto: "))

    gestion_db("agregar", (producto, categoria, precio, unidades, descripcion))

    print(OK + f"El producto '{producto}' ha sido agregado con éxito.")


def mostrar_producto():
    print(NEGRITA + "\nMostrando todos los productos:\n")
    resultado = gestion_db("mostrar", (1,))
    for producto in resultado:
        print(
            INFO
            + f"Id: {producto[0]} - Producto: {producto[1]} - Categoria: {producto[2]} - Precio: {producto[3]} - Unidades: {producto[4]} - Descripción: {producto[5]}"
        )


def buscar_producto():
    print(NEGRITA + "\nBúsqueda de productos")

    print(
        """
    Buscar por:
    1. ID
    2. Nombre
    3. Categoría
    """
    )

    opcion = input(NEGRITA + "Seleccione una opción (1-3): ")

    if opcion == "1":
        try:
            id_busqueda = int(input("\nIngrese el ID del producto: "))
        except ValueError:
            print("ID inválido.")
            return

        resultados = gestion_db("buscar_id", id_busqueda)

        if not resultados:
            print(ERROR + "No existe un producto con ese ID.")
            return

        producto = resultados[0]

        print(
            INFO
            + f"\nId: {producto[0]} - Producto: {producto[1]} - Categoria: {producto[2]} "
            f"- Precio: {producto[3]} - Unidades: {producto[4]} - Descripción: {producto[5]}"
        )
        if producto[4] < 50:
            print(
                AVISO
                + "   //Las unidades del producto son escasas. Considere renovar stock//"
            )
        return

    elif opcion == "2":
        termino = normalizar(input(NEGRITA + "\nIngrese nombre o parte del nombre: "))

        resultados = gestion_db("buscar_nombre", termino)

        if not resultados:
            print(ERROR + "No se encontraron productos.")
            return

        print(NEGRITA + "\nResultados encontrados:\n")
        for p in resultados:
            print(
                INFO + f"Id: {p[0]} - Producto: {p[1]} - Categoria: {p[2]} "
                f"- Precio: {p[3]} - Unidades: {p[4]} - Descripción: {p[5]}"
            )
        if p[4] < 50:
            print(
                AVISO
                + "   //Las unidades del producto son escasas. Considere renovar stock//"
            )
        return

    elif opcion == "3":
        categoria = normalizar(input("\nIngrese la categoría: "))

        resultados = gestion_db("buscar_categoria", categoria)

        if not resultados:
            print(ERROR + "No hay productos con esa categoría.")
            return

        print(NEGRITA + "\nProductos en esa categoría:\n")
        for p in resultados:
            print(
                INFO + f"Id: {p[0]} - Producto: {p[1]} - Categoria: {p[2]} "
                f"- Precio: {p[3]} - Unidades: {p[4]} - Descripción: {p[5]}"
            )
            if p[4] < 50:
                print(
                    AVISO
                    + "   //Las unidades del producto son escasas. Considere renovar stock//"
                )

    else:
        print(ERROR + "Opción inválida.")


def modificar_producto():

    print(NEGRITA + "\nModificar un producto")
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
            print(ERROR + "Debe ingresar un número válido.")
            return

        resultado = gestion_db("buscar_id", id_busqueda)

        if not resultado:
            print(ERROR + "No existe un producto con ese ID.")
            return

        producto = resultado[0]

    elif opcion == "2":
        nombre = normalizar(input("\nIngrese el nombre del producto: "))
        resultados = gestion_db("buscar_nombre", nombre)

        if not resultados:
            print(ERROR + "No se encontraron productos con ese nombre.")
            return

        print(NEGRITA + "\nCoincidencias encontradas:")
        for p in resultados:
            print(
                INFO
                + f"{p[0]} - {p[1]} (Categoría: {p[2]}, Precio: {p[3]}, Unidades: {p[4]}, Descripción: {p[5]})"
            )

        try:
            id_seleccion = int(
                input("\nIngrese el ID exacto del producto a modificar: ")
            )
        except ValueError:
            print(ERROR + "Debe ingresar un número válido.")
            return

        resultado = gestion_db("buscar_id", id_seleccion)

        if not resultado:
            print(ERROR + "ID inválido.")
            return

        producto = resultado[0]

    else:
        print(ERROR + "Opción inválida.")
        return

    print(NEGRITA + "\nProducto actual:")
    print(INFO + f" ID: {producto[0]}")
    print(INFO + f" Nombre: {producto[1]}")
    print(INFO + f" Categoría: {producto[2]}")
    print(INFO + f" Precio: {producto[3]}")
    print(INFO + f" Unidades: {producto[4]}")
    print(INFO + f" Descripción: {producto[5]}")

    nuevo_nombre = input("\nNuevo nombre (enter para mantener): ")
    if nuevo_nombre.strip() == "":
        nuevo_nombre = producto[1]

    nueva_categoria = input("\nNueva categoría (enter para mantener): ")
    if nueva_categoria.strip() == "":
        nueva_categoria = producto[2]

    nuevo_precio = input("\nNuevo precio (enter para mantener): ")
    if nuevo_precio.strip() == "":
        nuevo_precio = producto[3]
    else:
        nuevo_precio = validar_valor(nuevo_precio)

    nuevas_unidades = input("\nCantidad de unidades (enter para mantener): ")
    if nuevas_unidades.strip() == "":
        nuevas_unidades = producto[4]
    else:
        nuevas_unidades = validar_cantidad(nuevas_unidades)

    nueva_descripcion = input("\nNueva descripción (enter para mantener): ")
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

    print(OK + "\nProducto modificado correctamente.")
    if nuevas_unidades < 50:
        print(
            AVISO
            + "   //Las unidades del producto son escasas. Considere renovar stock//"
        )


def eliminar_producto():

    print(NEGRITA + "\nEliminar un producto")
    print(
        """
        Eliminar por:
        1. ID
        2. Nombre
        """
    )

    opcion = input(NEGRITA + "Seleccione una opción (1-2): ")

    if opcion == "1":
        try:
            id_busqueda = int(
                input(NEGRITA + "\nIngrese el ID del producto que desea eliminar: ")
            )
        except ValueError:
            print(ERROR + "Debe ingresar un número válido.")
            return

        resultado = gestion_db("buscar_id", id_busqueda)

        if not resultado:
            print(ERROR + "No existe un producto con ese ID.")
            return

        producto = resultado[0]

        print(NEGRITA + "\nHa seleccionado el siguiente producto para eliminar:")
        print(INFO + f" ID: {producto[0]}")
        print(INFO + f" Nombre: {producto[1]}")
        print(INFO + f" Categoría: {producto[2]}")
        print(INFO + f" Precio: {producto[3]}")

        confirmar = input(AVISO + "\n¿Está seguro de eliminarlo? (si/no): ").lower()

        if confirmar == "si" or confirmar == "s":
            gestion_db("eliminar", (id_busqueda,))
            print(OK + f"\nProducto '{producto[1]}' eliminado correctamente.")
        else:
            print(NEGRITA + "\nEliminación cancelada.")

    elif opcion == "2":
        nombre = normalizar(
            input(NEGRITA + "\nIngrese el nombre del producto a eliminar: ")
        )

        resultados = gestion_db("buscar_nombre", nombre)

        if not resultados:
            print(ERROR + "No se encontraron productos con ese nombre.")
            return

        print(NEGRITA + "\nCoincidencias encontradas:")
        for p in resultados:
            print(INFO + f"{p[0]} - {p[1]} (Categoría: {p[2]}, Precio: {p[3]})")

        try:
            id_eliminar = int(
                input(
                    NEGRITA + "\nIngrese el ID exacto del producto que desea eliminar: "
                )
            )
        except ValueError:
            print(ERROR + "Debe ingresar un número válido.")
            return

        confirmar = input(
            AVISO + "¿Está seguro de eliminar este producto? (si/no): "
        ).lower()
        if confirmar == "si":
            gestion_db("eliminar", (id_eliminar,))
            print(OK + "\nProducto eliminado correctamente.")
        else:
            print(INFO + "\nEliminación cancelada.")


def salir_sistema_gestion():
    confirmar = input(
        AVISO + "\n¿Está seguro de que desea salir del sistema? (si/no): "
    ).lower()

    if confirmar == "si" or confirmar == "s":
        print(OK + NEGRITA + "\nSaliendo..." + OK + "\tHasta pronto")
        return False

    else:
        print(NEGRITA + "\n Volviendo al menú...")


# definí una función que normalicé el ingreso de datos del usuario para evitar incompatibilidades
# con la base de datos.
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
