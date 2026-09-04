import simpy
import random

# ============================================================
# SIMULACIÓN DE UNA CAFETERÍA DE UN TECNOLÓGICO
# Librería utilizada: SimPy
# ============================================================

# Semilla para obtener resultados reproducibles
random.seed(10)


# ------------------------------------------------------------
# PROCESO DE UN ESTUDIANTE
# ------------------------------------------------------------
def estudiante(env, nombre, cafeteria, tiempo_atencion, estadisticas):

    llegada = env.now

    print(f"[{env.now:5.2f} min] {nombre} llega a la cafetería.")

    # El estudiante solicita ser atendido
    with cafeteria.request() as solicitud:

        yield solicitud

        inicio_atencion = env.now

        # Calcular tiempo que estuvo esperando
        tiempo_espera = inicio_atencion - llegada
        estadisticas["espera_total"] += tiempo_espera

        if tiempo_espera > estadisticas["mayor_espera"]:
            estadisticas["mayor_espera"] = tiempo_espera

        print(
            f"[{env.now:5.2f} min] {nombre} comienza a ser atendido. "
            f"Esperó {tiempo_espera:.2f} min."
        )

        # Tiempo que tarda en preparar el pedido
        tiempo_servicio = random.uniform(
            tiempo_atencion * 0.7,
            tiempo_atencion * 1.3
        )

        yield env.timeout(tiempo_servicio)

        estadisticas["atendidos"] += 1

        print(
            f"[{env.now:5.2f} min] {nombre} termina su compra. "
            f"Tiempo de atención: {tiempo_servicio:.2f} min."
        )


# ------------------------------------------------------------
# GENERADOR DE ESTUDIANTES
# ------------------------------------------------------------
def generar_estudiantes(
    env,
    cafeteria,
    cantidad_estudiantes,
    intervalo_llegada,
    tiempo_atencion,
    estadisticas
):

    for i in range(1, cantidad_estudiantes + 1):

        nombre = f"Estudiante {i}"

        env.process(
            estudiante(
                env,
                nombre,
                cafeteria,
                tiempo_atencion,
                estadisticas
            )
        )

        # Tiempo hasta que llega el siguiente estudiante
        intervalo = random.uniform(
            intervalo_llegada * 0.7,
            intervalo_llegada * 1.3
        )

        yield env.timeout(intervalo)


# ------------------------------------------------------------
# FUNCIÓN PRINCIPAL
# ------------------------------------------------------------
def simulacion():

    print("=" * 60)
    print("       SIMULACIÓN DE CAFETERÍA DEL TECNOLÓGICO")
    print("=" * 60)

    print("\nIngresa los datos de la cafetería.\n")

    # --------------------------------------------------------
    # ENTRADAS DEL USUARIO
    # --------------------------------------------------------

    while True:
        try:
            cantidad = int(
                input("Cantidad de estudiantes: ")
            )

            if cantidad > 0:
                break

            print("La cantidad debe ser mayor que 0.")

        except ValueError:
            print("Ingresa un número entero válido.")

    while True:
        try:
            empleados = int(
                input("Cantidad de empleados que atienden: ")
            )

            if empleados > 0:
                break

            print("Debe existir al menos un empleado.")

        except ValueError:
            print("Ingresa un número entero válido.")

    while True:
        try:
            intervalo = float(
                input(
                    "Intervalo promedio de llegada "
                    "entre estudiantes (minutos): "
                )
            )

            if intervalo > 0:
                break

            print("El intervalo debe ser mayor que 0.")

        except ValueError:
            print("Ingresa un número válido.")

    while True:
        try:
            tiempo_atencion = float(
                input(
                    "Tiempo promedio de atención "
                    "por estudiante (minutos): "
                )
            )

            if tiempo_atencion > 0:
                break

            print("El tiempo debe ser mayor que 0.")

        except ValueError:
            print("Ingresa un número válido.")

    while True:
        try:
            duracion = float(
                input(
                    "Duración de la simulación (minutos): "
                )
            )

            if duracion > 0:
                break

            print("La duración debe ser mayor que 0.")

        except ValueError:
            print("Ingresa un número válido.")

    # --------------------------------------------------------
    # CREAR ENTORNO DE SIMPY
    # --------------------------------------------------------

    env = simpy.Environment()

    # Número de empleados = capacidad del recurso
    cafeteria = simpy.Resource(
        env,
        capacity=empleados
    )

    # --------------------------------------------------------
    # ESTADÍSTICAS
    # --------------------------------------------------------

    estadisticas = {
        "atendidos": 0,
        "espera_total": 0,
        "mayor_espera": 0
    }

    # --------------------------------------------------------
    # INICIAR GENERADOR DE ESTUDIANTES
    # --------------------------------------------------------

    env.process(
        generar_estudiantes(
            env,
            cafeteria,
            cantidad,
            intervalo,
            tiempo_atencion,
            estadisticas
        )
    )

    # --------------------------------------------------------
    # EJECUTAR SIMULACIÓN
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("              INICIANDO SIMULACIÓN")
    print("=" * 60)

    env.run(until=duracion)

    # --------------------------------------------------------
    # CALCULAR RESULTADOS
    # --------------------------------------------------------

    if estadisticas["atendidos"] > 0:
        espera_promedio = (
            estadisticas["espera_total"]
            / estadisticas["atendidos"]
        )
    else:
        espera_promedio = 0

    estudiantes_no_atendidos = (
        cantidad - estadisticas["atendidos"]
    )

    # --------------------------------------------------------
    # MOSTRAR RESULTADOS
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("                 RESULTADOS")
    print("=" * 60)

    print(
        f"Estudiantes que llegaron:      {cantidad}"
    )

    print(
        f"Estudiantes atendidos:         "
        f"{estadisticas['atendidos']}"
    )

    print(
        f"Estudiantes no atendidos:      "
        f"{estudiantes_no_atendidos}"
    )

    print(
        f"Tiempo promedio de espera:     "
        f"{espera_promedio:.2f} minutos"
    )

    print(
        f"Mayor tiempo de espera:        "
        f"{estadisticas['mayor_espera']:.2f} minutos"
    )

    print(
        f"Empleados disponibles:         {empleados}"
    )

    print(
        f"Duración de simulación:        "
        f"{duracion:.2f} minutos"
    )

    # --------------------------------------------------------
    # ANÁLISIS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("                    ANÁLISIS")
    print("=" * 60)

    if espera_promedio < 3:
        print(
            "La cafetería presenta un buen tiempo de atención."
        )

    elif espera_promedio < 7:
        print(
            "La cafetería presenta un tiempo de espera moderado."
        )

    else:
        print(
            "La cafetería presenta tiempos de espera elevados."
        )

    if estudiantes_no_atendidos > 0:
        print(
            "Se recomienda aumentar el número de empleados "
            "o mejorar el tiempo de atención."
        )
    else:
        print(
            "La capacidad de atención es suficiente "
            "para la demanda simulada."
        )

    print("\nSimulación terminada.")


# ------------------------------------------------------------
# EJECUCIÓN DEL PROGRAMA
# ------------------------------------------------------------

