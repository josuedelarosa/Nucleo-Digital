// Multiplicación: R0 * R1 -> R2

// Inicializar R2 a 0
@R2
M=0          // R2 = 0

// Comenzar el bucle
(LOOP_START)
@R1          // Cargar R1
D=M          // D = R1
@END         // Si R1 es 0, saltar a END
D;JEQ

// Sumar R0 a R2
@R2          // Cargar R2
D=M          // D = R2
@R0          // Cargar R0
D=D+A        // D = R2 + R0
@R2          // Dirección de R2
M=D          // Guardar nuevo valor en R2

// Decrementar R1
@R1          // Cargar R1
D=M          // D = R1
@1           // Cargar 1
D=D-A        // D = R1 - 1
@R1          // Dirección de R1
M=D          // Actualizar R1

@LOOP_START  // Volver al inicio del bucle
0;JMP

(END)        // Fin del programa
@END         // Detener el programa
0;JMP
