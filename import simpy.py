import simpy
import random


def cliente(env, nombre, caja, tiempo_atencion, estadisticas):
    llegada = env.now

    print(f"[{env.now:.2f}] {nombre} llega a la fila.")

    with caja.request() as solicitud:
        yield solicitud

        inicio_atencion = env.now
        tiempo_espera = inicio_atencion - llegada

        estadisticas["espera"].append(tiempo_espera)

        print(
            f"[{env.now:.2f}] {nombre} comienza a ser atendido. "
            f"Esperó {tiempo_espera:.2f} minutos."
        )

        yield env.timeout(tiempo_atencion)

        fin_atencion = env.now
        tiempo_total = fin_atencion - llegada

        estadisticas["atendidos"] += 1
        estadisticas["tiempo_total"].append(tiempo_total)

        print(
            f"[{env.now:.2f}] {nombre} termina su atención."
        )


def generador_clientes(
    env,
    caja,
    numero_clientes,
    intervalo_llegadas,
    tiempo_atencion_min,
    tiempo_atencion_max,
    estadisticas
):
    for i in range(numero_clientes):

        tiempo_atencion = random.uniform(
            tiempo_atencion_min,
            tiempo_atencion_max
        )

        env.process(
            cliente(
                env,
                f"Cliente {i + 1}",
                caja,
                tiempo_atencion,
                estadisticas
            )
        )

        if i < numero_clientes - 1:
            tiempo_llegada = random.expovariate(
                1 / intervalo_llegadas
            )

            yield env.timeout(tiempo_llegada)


def main():

    print("=" * 60)
    print(" SIMULACIÓN DE UNA FILA DE ATENCIÓN")
    print("      Python + SimPy")
    print("=" * 60)

    print("\nIngrese los datos obtenidos durante su observación.\n")

    numero_clientes = int(
        input("Número de clientes a simular: ")
    )

    intervalo_llegadas = float(
        input("Tiempo promedio entre llegadas (minutos): ")
    )

    tiempo_atencion_min = float(
        input("Tiempo mínimo de atención (minutos): ")
    )

    tiempo_atencion_max = float(
        input("Tiempo máximo de atención (minutos): ")
    )

    numero_cajas = int(
        input("Número de cajas disponibles: ")
    )

    if numero_clientes <= 0:
        print("El número de clientes debe ser mayor que 0.")
        return

    if intervalo_llegadas <= 0:
        print("El intervalo de llegadas debe ser mayor que 0.")
        return

    if tiempo_atencion_min <= 0:
        print("El tiempo mínimo de atención debe ser mayor que 0.")
        return

    if tiempo_atencion_max < tiempo_atencion_min:
        print(
            "El tiempo máximo no puede ser menor "
            "que el tiempo mínimo."
        )
        return

    if numero_cajas <= 0:
        print("Debe existir al menos una caja.")
        return

    estadisticas = {
        "espera": [],
        "tiempo_total": [],
        "atendidos": 0
    }

    random.seed()

    env = simpy.Environment()

    caja = simpy.Resource(
        env,
        capacity=numero_cajas
    )

    env.process(
        generador_clientes(
            env,
            caja,
            numero_clientes,
            intervalo_llegadas,
            tiempo_atencion_min,
            tiempo_atencion_max,
            estadisticas
        )
    )

    print("\n" + "=" * 60)
    print("INICIANDO SIMULACIÓN")
    print("=" * 60 + "\n")

    env.run()

    print("\n" + "=" * 60)
    print("RESULTADOS DE LA SIMULACIÓN")
    print("=" * 60)

    espera = estadisticas["espera"]
    tiempo_total = estadisticas["tiempo_total"]

    promedio_espera = sum(espera) / len(espera)
    maximo_espera = max(espera)

    promedio_atencion = (
        sum(tiempo_total) / len(tiempo_total)
    )

    print(f"\nClientes atendidos: {estadisticas['atendidos']}")
    print(f"Tiempo promedio de espera: {promedio_espera:.2f} minutos")
    print(f"Tiempo máximo de espera: {maximo_espera:.2f} minutos")
    print(
        f"Tiempo promedio dentro del sistema: "
        f"{promedio_atencion:.2f} minutos"
    )

    print("\n" + "=" * 60)
    print("FIN DE LA SIMULACIÓN")
    print("=" * 60)


if __name__ == "__main__":
    main()
