import json
from datetime import datetime

ARCHIVO_DATOS = "registros_pedidos.json"

PRODUCTOS = [
    "Gorra",
    "Polo",
    "Hoodie",
    "Chompa",
    "Casaca",
    "Jean",
    "Otra prenda"
]

TIPOS_TRABAJO = [
    "Bordado",
    "DTF",
    "Venta sin personalizar"
]

ORIGEN_PRENDA = [
    "Tienda",
    "Cliente"
]

ESTADOS = [
    "Cotizado",
    "Confirmado",
    "En producción",
    "Terminado",
    "Entregado"
]


def cargar_datos():
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("⚠️ El archivo está dañado. Se iniciará vacío.")
        return []


def guardar_datos(registros):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(registros, archivo, indent=4, ensure_ascii=False)


def pedir_texto_obligatorio(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("❌ Este campo es obligatorio.")


def pedir_texto_opcional(mensaje):
    return input(mensaje).strip()


def pedir_celular(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and len(valor) >= 8:
            return valor
        print("❌ Ingresa un número de celular válido.")


def pedir_entero_obligatorio(mensaje):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor > 0:
                return valor
            print("❌ Debe ser mayor que 0.")
        except ValueError:
            print("❌ Ingresa un número válido.")


def pedir_decimal_obligatorio(mensaje):
    while True:
        try:
            valor = float(input(mensaje).strip())
            if valor >= 0:
                return round(valor, 2)
            print("❌ Debe ser mayor o igual a 0.")
        except ValueError:
            print("❌ Ingresa un número válido.")


def pedir_decimal_opcional(mensaje, valor_defecto=0.0):
    valor = input(mensaje).strip()
    if valor == "":
        return round(valor_defecto, 2)

    try:
        numero = float(valor)
        if numero >= 0:
            return round(numero, 2)
        print("❌ Debe ser mayor o igual a 0. Se usará el valor por defecto.")
        return round(valor_defecto, 2)
    except ValueError:
        print("❌ Número inválido. Se usará el valor por defecto.")
        return round(valor_defecto, 2)


def pedir_opcion_lista(mensaje, opciones, permitir_vacio=False, valor_defecto=None):
    while True:
        print(f"\n{mensaje}")
        for i, opcion in enumerate(opciones, start=1):
            print(f"{i}. {opcion}")

        if permitir_vacio:
            texto = f"Elige una opción (Enter = {valor_defecto}): "
        else:
            texto = "Elige una opción: "

        valor = input(texto).strip()

        if permitir_vacio and valor == "":
            return valor_defecto

        try:
            indice = int(valor)
            if 1 <= indice <= len(opciones):
                return opciones[indice - 1]
            print("❌ Opción inválida.")
        except ValueError:
            print("❌ Ingresa un número válido.")


def generar_id(registros):
    if not registros:
        return 1
    return max(r["id"] for r in registros) + 1


def recalcular_saldo(registro):
    registro["saldo_pendiente"] = round(registro["precio_cotizado"] - registro["adelanto"], 2)


def mostrar_registro(registro, indice=None):
    encabezado = f"REGISTRO {indice + 1}" if indice is not None else "REGISTRO"
    print(f"\n========== {encabezado} ==========")
    print(f"ID: {registro['id']}")
    print(f"Fecha de registro: {registro['fecha_registro']}")
    print(f"Nombre: {registro['nombre']}")
    print(f"Apellido: {registro['apellido'] if registro['apellido'] else '-'}")
    print(f"Celular: {registro['celular']}")
    print(f"Producto: {registro['producto']}")
    print(f"Tipo de trabajo: {registro['tipo_trabajo']}")
    print(f"Origen de la prenda: {registro['origen_prenda']}")
    print(f"Cantidad: {registro['cantidad']}")
    print(f"Detalles del diseño: {registro['detalles_diseno'] if registro['detalles_diseno'] else '-'}")
    print(f"Precio cotizado: S/ {registro['precio_cotizado']:.2f}")
    print(f"Adelanto: S/ {registro['adelanto']:.2f}")
    print(f"Saldo pendiente: S/ {registro['saldo_pendiente']:.2f}")
    print(f"Estado: {registro['estado']}")
    print(f"Fecha probable: {registro['fecha_probable'] if registro['fecha_probable'] else '-'}")
    print(f"Observación: {registro['observacion'] if registro['observacion'] else '-'}")


def registrar_cotizacion(registros):
    print("\n========== NUEVA COTIZACIÓN ==========")

    nombre = pedir_texto_obligatorio("Nombre: ")
    apellido = pedir_texto_opcional("Apellido (opcional): ")
    celular = pedir_celular("Celular: ")
    producto = pedir_opcion_lista("Producto:", PRODUCTOS)
    tipo_trabajo = pedir_opcion_lista("Tipo de trabajo:", TIPOS_TRABAJO)
    origen_prenda = pedir_opcion_lista(
        "Origen de la prenda:",
        ORIGEN_PRENDA,
        permitir_vacio=True,
        valor_defecto="Tienda"
    )
    cantidad = pedir_entero_obligatorio("Cantidad: ")
    detalles_diseno = pedir_texto_opcional("Detalles del diseño (opcional): ")
    precio_cotizado = pedir_decimal_obligatorio("Precio cotizado total: S/ ")
    adelanto = pedir_decimal_opcional("Adelanto (opcional, Enter = 0): S/ ", 0.0)
    fecha_probable = pedir_texto_opcional("Fecha probable (opcional): ")
    observacion = pedir_texto_opcional("Observación (opcional): ")

    if adelanto > precio_cotizado:
        print("❌ El adelanto no puede ser mayor al precio cotizado.")
        return

    registro = {
        "id": generar_id(registros),
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "nombre": nombre,
        "apellido": apellido,
        "celular": celular,
        "producto": producto,
        "tipo_trabajo": tipo_trabajo,
        "origen_prenda": origen_prenda,
        "cantidad": cantidad,
        "detalles_diseno": detalles_diseno,
        "precio_cotizado": precio_cotizado,
        "adelanto": adelanto,
        "saldo_pendiente": round(precio_cotizado - adelanto, 2),
        "estado": "Cotizado",
        "fecha_probable": fecha_probable,
        "observacion": observacion
    }

    registros.append(registro)
    guardar_datos(registros)
    print("✅ Cotización registrada correctamente.")


def ver_todos_los_registros(registros):
    if not registros:
        print("\nNo hay registros todavía.")
        return

    for i, registro in enumerate(registros):
        mostrar_registro(registro, i)


def buscar_registros(registros):
    if not registros:
        print("\nNo hay registros todavía.")
        return

    print("\n========== BUSCAR REGISTRO ==========")
    print("1. Buscar por nombre o apellido")
    print("2. Buscar por celular")
    print("3. Buscar por ID")
    opcion = input("Elige una opción: ").strip()

    encontrados = []

    if opcion == "1":
        texto = input("Escribe nombre o apellido: ").strip().lower()
        for i, registro in enumerate(registros):
            nombre = registro.get("nombre", "")
            apellido = registro.get("apellido", "")
            nombre_completo = f"{nombre} {apellido}".lower()
            if texto in nombre_completo:
                encontrados.append((i, registro))

    elif opcion == "2":
        texto = input("Escribe celular: ").strip()
        for i, registro in enumerate(registros):
            if texto in registro["celular"]:
                encontrados.append((i, registro))

    elif opcion == "3":
        try:
            id_buscar = int(input("Ingresa el ID: ").strip())
            for i, registro in enumerate(registros):
                if registro["id"] == id_buscar:
                    mostrar_registro(registro, i)
                    return
            print("❌ No se encontró el registro.")
            return
        except ValueError:
            print("❌ ID inválido.")
            return

    else:
        print("❌ Opción inválida.")
        return

    if not encontrados:
        print("❌ No se encontraron registros.")
        return

    for i, registro in encontrados:
        mostrar_registro(registro, i)


def cambiar_estado(registros):
    if not registros:
        print("\nNo hay registros todavía.")
        return

    print("\n========== CAMBIAR ESTADO ==========")
    for i, registro in enumerate(registros):
        print(
            f"{i + 1}. {registro['nombre']} {registro['apellido']} | "
            f"{registro['producto']} | {registro['estado']}"
        )

    try:
        indice = int(input("Número del registro: ").strip()) - 1
    except ValueError:
        print("❌ Ingresa un número válido.")
        return

    if not (0 <= indice < len(registros)):
        print("❌ Número inválido.")
        return

    nuevo_estado = pedir_opcion_lista("Nuevo estado:", ESTADOS)
    registros[indice]["estado"] = nuevo_estado
    guardar_datos(registros)
    print("✅ Estado actualizado correctamente.")


def registrar_pago(registros):
    if not registros:
        print("\nNo hay registros todavía.")
        return

    print("\n========== REGISTRAR PAGO ==========")
    for i, registro in enumerate(registros):
        print(
            f"{i + 1}. {registro['nombre']} {registro['apellido']} | "
            f"{registro['producto']} | Saldo: S/ {registro['saldo_pendiente']:.2f}"
        )

    try:
        indice = int(input("Número del registro: ").strip()) - 1
    except ValueError:
        print("❌ Ingresa un número válido.")
        return

    if not (0 <= indice < len(registros)):
        print("❌ Número inválido.")
        return

    monto = pedir_decimal_obligatorio("Monto que está pagando ahora: S/ ")

    if monto > registros[indice]["saldo_pendiente"]:
        print("❌ El pago no puede ser mayor al saldo pendiente.")
        return

    registros[indice]["adelanto"] = round(registros[indice]["adelanto"] + monto, 2)
    recalcular_saldo(registros[indice])

    if registros[indice]["adelanto"] > 0 and registros[indice]["estado"] == "Cotizado":
        registros[indice]["estado"] = "Confirmado"

    guardar_datos(registros)
    print("✅ Pago registrado correctamente.")


def editar_registro(registros):
    if not registros:
        print("\nNo hay registros todavía.")
        return

    print("\n========== EDITAR REGISTRO ==========")
    for i, registro in enumerate(registros):
        print(
            f"{i + 1}. {registro['nombre']} {registro['apellido']} | "
            f"{registro['producto']} | Estado: {registro['estado']}"
        )

    try:
        indice = int(input("Número del registro a editar: ").strip()) - 1
    except ValueError:
        print("❌ Ingresa un número válido.")
        return

    if not (0 <= indice < len(registros)):
        print("❌ Número inválido.")
        return

    registro = registros[indice]

    print("\nDeja vacío y presiona Enter para mantener el valor actual.\n")

    nuevo_nombre = input(f"Nombre [{registro['nombre']}]: ").strip()
    if nuevo_nombre:
        registro["nombre"] = nuevo_nombre

    nuevo_apellido = input(f"Apellido [{registro['apellido']}]: ").strip()
    if nuevo_apellido:
        registro["apellido"] = nuevo_apellido

    nuevo_celular = input(f"Celular [{registro['celular']}]: ").strip()
    if nuevo_celular:
        if nuevo_celular.isdigit() and len(nuevo_celular) >= 8:
            registro["celular"] = nuevo_celular
        else:
            print("❌ Celular inválido. Se mantiene el valor actual.")

    print(f"\nProducto actual: {registro['producto']}")
    registro["producto"] = pedir_opcion_lista(
        "Producto:",
        PRODUCTOS,
        permitir_vacio=True,
        valor_defecto=registro["producto"]
    )

    print(f"\nTipo de trabajo actual: {registro['tipo_trabajo']}")
    registro["tipo_trabajo"] = pedir_opcion_lista(
        "Tipo de trabajo:",
        TIPOS_TRABAJO,
        permitir_vacio=True,
        valor_defecto=registro["tipo_trabajo"]
    )

    print(f"\nOrigen actual: {registro['origen_prenda']}")
    registro["origen_prenda"] = pedir_opcion_lista(
        "Origen de la prenda:",
        ORIGEN_PRENDA,
        permitir_vacio=True,
        valor_defecto=registro["origen_prenda"]
    )

    nueva_cantidad = input(f"Cantidad [{registro['cantidad']}]: ").strip()
    if nueva_cantidad:
        try:
            cantidad_int = int(nueva_cantidad)
            if cantidad_int > 0:
                registro["cantidad"] = cantidad_int
            else:
                print("❌ Cantidad inválida. Se mantiene el valor actual.")
        except ValueError:
            print("❌ Cantidad inválida. Se mantiene el valor actual.")

    nuevos_detalles = input(f"Detalles del diseño [{registro['detalles_diseno']}]: ").strip()
    if nuevos_detalles:
        registro["detalles_diseno"] = nuevos_detalles

    nuevo_precio = input(f"Precio cotizado [{registro['precio_cotizado']}]: ").strip()
    if nuevo_precio:
        try:
            precio_float = float(nuevo_precio)
            if precio_float >= 0:
                registro["precio_cotizado"] = round(precio_float, 2)
            else:
                print("❌ Precio inválido. Se mantiene el valor actual.")
        except ValueError:
            print("❌ Precio inválido. Se mantiene el valor actual.")

    nuevo_adelanto = input(f"Adelanto [{registro['adelanto']}]: ").strip()
    if nuevo_adelanto:
        try:
            adelanto_float = float(nuevo_adelanto)
            if adelanto_float >= 0:
                registro["adelanto"] = round(adelanto_float, 2)
            else:
                print("❌ Adelanto inválido. Se mantiene el valor actual.")
        except ValueError:
            print("❌ Adelanto inválido. Se mantiene el valor actual.")

    nueva_fecha_probable = input(f"Fecha probable [{registro['fecha_probable']}]: ").strip()
    if nueva_fecha_probable:
        registro["fecha_probable"] = nueva_fecha_probable

    nueva_observacion = input(f"Observación [{registro['observacion']}]: ").strip()
    if nueva_observacion:
        registro["observacion"] = nueva_observacion

    print(f"\nEstado actual: {registro['estado']}")
    registro["estado"] = pedir_opcion_lista(
        "Estado:",
        ESTADOS,
        permitir_vacio=True,
        valor_defecto=registro["estado"]
    )

    if registro["adelanto"] > registro["precio_cotizado"]:
        print("❌ El adelanto no puede ser mayor al precio cotizado. No se guardaron los cambios.")
        return

    recalcular_saldo(registro)
    guardar_datos(registros)
    print("✅ Registro editado correctamente.")


def ver_resumen(registros):
    if not registros:
        print("\nNo hay registros todavía.")
        return

    total_registros = len(registros)
    total_cotizado = sum(r["precio_cotizado"] for r in registros)
    total_cobrado = sum(r["adelanto"] for r in registros)
    total_pendiente = sum(r["saldo_pendiente"] for r in registros)

    conteo_estados = {estado: 0 for estado in ESTADOS}
    for registro in registros:
        conteo_estados[registro["estado"]] += 1

    conteo_tipos = {}
    for registro in registros:
        tipo = registro["tipo_trabajo"]
        conteo_tipos[tipo] = conteo_tipos.get(tipo, 0) + 1

    print("\n========== RESUMEN ==========")
    print(f"Total de registros: {total_registros}")
    print(f"Total cotizado: S/ {total_cotizado:.2f}")
    print(f"Total cobrado: S/ {total_cobrado:.2f}")
    print(f"Total pendiente: S/ {total_pendiente:.2f}")

    print("\nEstados:")
    for estado, cantidad in conteo_estados.items():
        print(f"- {estado}: {cantidad}")

    if conteo_tipos:
        tipo_mas_registrado = max(conteo_tipos, key=conteo_tipos.get)
        print(f"\nTipo de trabajo más registrado: {tipo_mas_registrado}")


def eliminar_registro(registros):
    if not registros:
        print("\nNo hay registros todavía.")
        return

    print("\n========== ELIMINAR REGISTRO ==========")
    for i, registro in enumerate(registros):
        print(f"{i + 1}. {registro['nombre']} {registro['apellido']} | {registro['producto']}")

    try:
        indice = int(input("Número del registro a eliminar: ").strip()) - 1
    except ValueError:
        print("❌ Ingresa un número válido.")
        return

    if not (0 <= indice < len(registros)):
        print("❌ Número inválido.")
        return

    registro = registros[indice]
    confirmar = input(
        f"¿Seguro que quieres eliminar a {registro['nombre']} {registro['apellido']}? (s/n): "
    ).strip().lower()

    if confirmar != "s":
        print("❌ Eliminación cancelada.")
        return

    eliminado = registros.pop(indice)
    guardar_datos(registros)
    print(f"✅ Registro eliminado: {eliminado['nombre']} {eliminado['apellido']}")


def mostrar_menu():
    print("\n===================================================")
    print(" SISTEMA DE COTIZACIÓN Y SEGUIMIENTO DE PEDIDOS ")
    print("===================================================")
    print("1. Registrar nueva cotización")
    print("2. Buscar cliente")
    print("3. Ver todos los registros")
    print("4. Editar registro")
    print("5. Registrar pago")
    print("6. Cambiar estado")
    print("7. Ver resumen")
    print("8. Eliminar registro")
    print("9. Salir")


def main():
    registros = cargar_datos()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            registrar_cotizacion(registros)
        elif opcion == "2":
            buscar_registros(registros)
        elif opcion == "3":
            ver_todos_los_registros(registros)
        elif opcion == "4":
            editar_registro(registros)
        elif opcion == "5":
            registrar_pago(registros)
        elif opcion == "6":
            cambiar_estado(registros)
        elif opcion == "7":
            ver_resumen(registros)
        elif opcion == "8":
            eliminar_registro(registros)
        elif opcion == "9":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    main()