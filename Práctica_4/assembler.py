import os
import sys
class HackFileProcessor:
    """Procesa archivos de ensamblador Hack.

    Maneja la lectura y limpieza de los comandos de ensamblador para su traducción.
    """

    def __init__(self, filename: str):
        """Inicializa y procesa el archivo de ensamblador."""
        self.current_instruction = ""
        self.line_number = -1
        self.instructions = self._clean_file(filename)

    def _clean_file(self, filename: str):
        """Lee el archivo, elimina espacios en blanco y comentarios, y devuelve una lista limpia de comandos."""
        with open(filename, 'r') as file:
            cleaned_lines = []
            for line in file:
                # Elimina comentarios y espacios en blanco, solo agrega líneas no vacías
                clean_line = line.split("//")[0].strip()
                if clean_line:
                    cleaned_lines.append(clean_line.replace(" ", ""))
            return cleaned_lines

    def has_more_instructions(self) -> bool:
        """Verifica si quedan más comandos por procesar."""
        return self.line_number + 1 < len(self.instructions)

    def advance(self) -> None:
        """Avanza al siguiente comando."""
        self.line_number += 1
        self.current_instruction = self.instructions[self.line_number]

    def reset(self) -> None:
        """Reinicia el puntero de instrucciones al inicio."""
        self.current_instruction = ""
        self.line_number = -1

    def instruction_type(self) -> str:
        """Determina si la instrucción actual es un comando A, C o L (etiqueta)."""
        if self.current_instruction.startswith("@"):
            return "A_COMMAND"
        elif self.current_instruction.startswith("("):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def get_symbol(self) -> str:
        """Extrae el símbolo o número de una instrucción A o L."""
        if self.instruction_type() == "A_COMMAND":
            return self.current_instruction[1:]
        if self.instruction_type() == "L_COMMAND":
            return self.current_instruction[1:-1]
        return ""

    def get_dest(self) -> str:
        """Extrae el destino en una instrucción C."""
        if "=" in self.current_instruction:
            return self.current_instruction.split("=")[0]
        return ""

    def get_comp(self) -> str:
        """Extrae la parte de computación de una instrucción C."""
        parts = self.current_instruction.split("=")
        comp_part = parts[-1]  # Maneja el caso cuando no hay dest
        return comp_part.split(";")[0]

    def get_jump(self) -> str:
        """Extrae la parte de salto en una instrucción C."""
        if ";" in self.current_instruction:
            return self.current_instruction.split(";")[1]
        return ""


class BinaryTranslator:
    """Convierte los mnemónicos del ensamblador Hack en instrucciones binarias."""

    def __init__(self):
        """Inicializa las tablas de traducción para los mnemónicos."""
        self.dest_table = {
            "": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"
        }
        self.comp_table = {
            "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "M": "1110000",
            "!D": "0001101", "!A": "0110001", "!M": "1110001", "-D": "0001111", "-A": "0110011", "-M": "1110011",
            "D+1": "0011111", "A+1": "0110111", "M+1": "1110111", "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
            "D+A": "0000010", "D+M": "1000010", "D-A": "0010011", "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
            "D&A": "0000000", "D&M": "1000000", "D|A": "0010101", "D|M": "1010101"
        }
        self.jump_table = {
            "": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
        }

    def translate_dest(self, mnemonic: str) -> str:
        """Convierte el mnemónico de destino a binario."""
        return self.dest_table.get(mnemonic, "000")

    def translate_comp(self, mnemonic: str) -> str:
        """Convierte el mnemónico de computación a binario."""
        return self.comp_table.get(mnemonic, "0101010")

    def translate_jump(self, mnemonic: str) -> str:
        """Convierte el mnemónico de salto a binario."""
        return self.jump_table.get(mnemonic, "000")


class SymbolTable:
    """Administra los símbolos y sus direcciones en el ensamblador Hack."""

    def __init__(self):
        """Inicializa la tabla con los símbolos predefinidos."""
        self.symbol_table = {
            "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,
            "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15, "SCREEN": 16384, "KBD": 24576,
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4
        }

    def add_symbol(self, symbol: str, address: int) -> None:
        """Agrega un nuevo símbolo y su dirección a la tabla."""
        self.symbol_table[symbol] = address

    def contains_symbol(self, symbol: str) -> bool:
        """Verifica si el símbolo ya está en la tabla."""
        return symbol in self.symbol_table

    def get_address(self, symbol: str) -> int:
        """Devuelve la dirección asociada con el símbolo."""
        return self.symbol_table.get(symbol, -1)


def hack_assembler():
    """Función principal para ensamblar el código Hack a binario."""

    if len(sys.argv) != 2:
        print("Sigue la estructura: python HackAssembler.py [archivo.asm]")
        return

    input_file = sys.argv[1]
    processor = HackFileProcessor(input_file)
    symbol_table = SymbolTable()

    # Primera pasada: Registra las etiquetas en la tabla de símbolos
    rom_address = 0
    while processor.has_more_instructions():
        processor.advance()
        if processor.instruction_type() == "L_COMMAND":
            label = processor.get_symbol()
            symbol_table.add_symbol(label, rom_address)
        else:
            rom_address += 1

    # Segunda pasada: Traduce las instrucciones a binario
    processor.reset()
    translator = BinaryTranslator()
    output_file = input_file.replace(".asm", ".hack")
    with open(output_file, "w") as hack_file:
        ram_address = 16
        while processor.has_more_instructions():
            processor.advance()
            if processor.instruction_type() == "A_COMMAND":
                symbol = processor.get_symbol()
                if symbol.isdigit():
                    address = int(symbol)
                elif symbol_table.contains_symbol(symbol):
                    address = symbol_table.get_address(symbol)
                else:
                    address = ram_address
                    symbol_table.add_symbol(symbol, address)
                    ram_address += 1
                hack_file.write(format(address, "016b") + "\n")
            elif processor.instruction_type() == "C_COMMAND":
                comp = translator.translate_comp(processor.get_comp())
                dest = translator.translate_dest(processor.get_dest())
                jump = translator.translate_jump(processor.get_jump())
                hack_file.write("111" + comp + dest + jump + "\n")


if __name__ == "__main__":
    hack_assembler()