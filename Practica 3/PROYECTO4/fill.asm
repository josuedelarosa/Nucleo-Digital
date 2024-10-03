// Fill.asm
// Programa que llena o vacía la pantalla dependiendo de si el botón está presionado

(START)
    @KBD       // Dirección del teclado
    D=M        // D = valor del teclado (0 si no se presiona, distinto de 0 si se presiona)
    @FILL      // Si el valor del teclado no es 0, saltar a FILL
    D;JNE

    // Vaciar la pantalla
    @SCREEN    // Dirección de la pantalla
    D=A        // D = Dirección de la pantalla (empezar desde el inicio)
    @ENDSCREEN // Dirección de fin de pantalla
(CLEAR_LOOP)
    A=D
    M=0        // Poner 0 en cada dirección (vaciar la pantalla)
    D=D+1      // Incrementar dirección
    @CLEAR_LOOP
    D-A;JLT    // Repetir hasta que se llegue al final de la pantalla

    @START     // Vuelve al inicio para comprobar el estado del teclado
    0;JMP

(FILL)
    // Llenar la pantalla
    @SCREEN    // Dirección de la pantalla
    D=A        // D = Dirección de la pantalla (empezar desde el inicio)
    @ENDSCREEN // Dirección de fin de pantalla
(FILL_LOOP)
    A=D
    M=-1       // Poner 1 en cada dirección (llenar la pantalla)
    D=D+1      // Incrementar dirección
    @FILL_LOOP
    D-A;JLT    // Repetir hasta que se llegue al final de la pantalla

    @START     // Vuelve al inicio para comprobar el estado del teclado
    0;JMP

(ENDSCREEN)
    @24576     // Dirección justo después del final de la pantalla (SCREEN + 8192, ya que SCREEN = 16384)
