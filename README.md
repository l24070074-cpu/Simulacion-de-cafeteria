Simulación de una fila de atención con Python y SimPy Descripción del proyecto Este proyecto consiste en la simulación de un sistema de atención formado por una fila de clientes y una o varias cajas. El programa fue desarrollado en Python utilizando la librería SimPy y está basado en la observación de un sistema real realizada durante el trabajo de campo. El programa funciona completamente mediante la terminal y no utiliza una interfaz gráfica. Objetivo El objetivo de la simulación es representar el comportamiento de los clientes dentro de una fila de atención y analizar los tiempos de espera y atención. Datos de entrada El programa solicita al usuario los siguientes datos:

Número de clientes a simular.
Tiempo promedio entre llegadas de los clientes.
Tiempo mínimo de atención.
Tiempo máximo de atención.
Número de cajas disponibles. Los datos deben corresponder a la información obtenida durante la observación del sistema real. Funcionamiento del algoritmo El programa crea un entorno de simulación utilizando SimPy. Cada cliente representa una entidad del sistema. Cuando un cliente llega, solicita utilizar una caja. Si todas las cajas están ocupadas, el cliente debe esperar en la fila. Cuando una caja queda disponible, el cliente comienza su atención. Al terminar, libera la caja y abandona el sistema. El programa registra los tiempos de espera y los tiempos que los clientes permanecen dentro del sistema. Resultados Al finalizar la simulación, el programa muestra en la terminal:
Número de clientes atendidos.
Tiempo promedio de espera.
Tiempo máximo de espera.
Tiempo promedio dentro del sistema. Requisitos Para ejecutar el programa es necesario tener instalado:
Python 3
SimPy 4.1.2 Para instalar SimPy se utiliza:
pip install simpy
``
## Ejecución
Desde una terminal ubicada en la carpeta del proyecto se ejecuta:
```bash
python simulacion_caja.py
El programa solicitará los datos de entrada y posteriormente ejecutará la simulación. Tecnologías utilizadas

Python
SimPy
GitHub
Terminal Integrantes Integrante 1:** ______________________________ Integrante 2:** ______________________________ Conclusión La simulación permite representar mediante un modelo computacional el comportamiento de un sistema real de atención. A partir de los datos obtenidos durante la observación de campo es posible analizar los tiempos de espera y atención de los clientes y observar el comportamiento del sistema bajo diferentes condiciones.
