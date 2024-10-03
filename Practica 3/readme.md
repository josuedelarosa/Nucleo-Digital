Parte 1: MULT.asm

Descripción del Código de Multiplicación en Ensamblador
Este código realiza la multiplicación de dos valores almacenados en los registros R0 y R1 y guarda el resultado en el registro R2. La multiplicación se lleva a cabo mediante sumas repetitivas. A continuación, se explica el funcionamiento del código paso a paso:

1. Inicialización del Resultado (R2)
El valor del registro R2 se inicializa en 0, ya que se utilizará para almacenar el resultado acumulado de la multiplicación.

2. Inicio del Bucle de Multiplicación
Se marca la etiqueta (LOOP_START) para indicar el comienzo del bucle.
Se carga el valor de R1 y se verifica si es igual a 0. Si R1 es 0, se salta al final del programa, ya que no hay más sumas que realizar.
3. Suma Repetitiva para Multiplicar
El valor de R0 se suma al valor de R2. Esta suma se repite tantas veces como el valor en R1. Este proceso simula la multiplicación, ya que R0 se suma R1 veces.
Luego, el valor actualizado se almacena nuevamente en R2.
4. Decremento de R1
Cada vez que se realiza la suma, R1 se decrementa en 1 para llevar la cuenta de cuántas veces se ha realizado la suma.
Este proceso se repite hasta que R1 llegue a 0.
5. Repetición del Bucle
El bucle regresa a la etiqueta (LOOP_START) mientras R1 no sea igual a 0, repitiendo el proceso de sumar R0 a R2 y disminuir R1.
6. Finalización del Programa
Cuando R1 llega a 0, el flujo del programa salta a la etiqueta (END), donde el programa se detiene.
En Resumen
El código implementa una multiplicación utilizando sumas iterativas. R2 empieza en 0 y se incrementa con el valor de R0 tantas veces como indique el valor de R1. Esta técnica se conoce como multiplicación por sumas repetidas, donde R0 se agrega a sí mismo R1 veces. Al finalizar, R2 contiene el producto de R0 y R1.

Interpretación de las Instrucciones
La arquitectura Hack tiene dos tipos de instrucciones:

Instrucción A (Address): Utilizada para definir una dirección en la memoria.
Instrucción C (Compute): Utilizada para realizar operaciones aritméticas y lógicas, así como almacenamiento.
Cada instrucción está representada por 16 bits (es decir, 16 dígitos binarios).

Explicación General
Instrucciones A: Las instrucciones que comienzan con 000 son instrucciones A, que apuntan a una dirección específica en la memoria.
Instrucciones C: Las instrucciones que comienzan con 111 son instrucciones C, que realizan operaciones y cálculos.
Este conjunto de instrucciones refleja la lógica del programa ensamblador: inicializa R2, luego suma repetidamente R0 a R2 tantas veces como indique R1, y finalmente se detiene. El resultado son las instrucciones traducidas en lenguaje de máquina, listas para ser ejecutadas por la CPU Hack.

Parte 2: Programa en Fill.asm

Explicación del Código
Etiqueta de inicio (START): Define el inicio del programa, utilizado como referencia para el bucle principal.

Verificar el Estado del Teclado:

@KBD apunta a la dirección del teclado.
D=M carga el valor actual del teclado.
@FILL indica la etiqueta para llenar la pantalla.
D;JNE hace un salto a FILL si el valor de D es diferente de cero, lo cual indica que una tecla está siendo presionada.
Vaciar la Pantalla (si ninguna tecla está presionada):

@SCREEN apunta a la dirección de inicio de la pantalla (ubicada en 16384).
D=A guarda la dirección en D para iterar.
(CLEAR_LOOP) es el bucle que se repite hasta que todas las direcciones de la pantalla están en 0.
A=D selecciona la dirección actual.
M=0 limpia esa dirección.
D=D+1 incrementa la dirección.
@CLEAR_LOOP y D-A;JLT aseguran que el bucle continúe hasta llegar al final de la pantalla (ENDSCREEN).
Llenar la Pantalla (si una tecla está presionada):

(FILL) es la etiqueta de llenado.
El proceso es similar al bucle de limpieza, pero llena cada dirección de la pantalla con -1 (M=-1), que representa todos los bits en 1.
Etiqueta (ENDSCREEN):

@24576 apunta a la dirección justo después del área de la pantalla (16384 + 8192), utilizada como límite para los bucles de llenado y limpieza.
Bucle Infinito:

Al final de cada bucle (CLEAR_LOOP o FILL_LOOP), el programa regresa a la etiqueta (START) para verificar el estado del teclado continuamente.
Este código asegura que, cuando una tecla está presionada, la pantalla se llene completamente, y cuando no hay teclas presionadas, la pantalla se vacíe. El bucle principal verifica constantemente el estado del teclado para actualizar la pantalla en consecuencia.

Explicación General
Este código se divide en secciones que manipulan la pantalla y la entrada del teclado:

Inicializa direcciones específicas para la pantalla y el teclado.
Utiliza instrucciones condicionales para verificar valores en la memoria y tomar decisiones.
Realiza bucles basados en las comparaciones para llenar o vaciar la pantalla.
Al final, vuelve al inicio para mantener el programa en ejecución continua.
Este flujo es similar al programa Fill, que verifica si una tecla está presionada para decidir si llenar o vaciar la pantalla. El programa está diseñado para ser cíclico, ejecutándose continuamente para mantener actualizada la pantalla según el estado del teclado.

