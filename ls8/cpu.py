"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """
        * `PC`: Program Counter, address of the currently executing instruction
        * `IR`: Instruction Register, contains a copy of the currently executing instruction
        * `MAR`: Memory Address Register, holds the memory address we're reading or writing
        * `MDR`: Memory Data Register, holds the value to write or the value just read
        * `FL`: Flags, see below
        """        
        self.pc = 0
        self.mar = 0
        self.mdr = 0
        self.ir = None
        self.fl = None
        self.running = False
        # self.ie = None
        self.reg = [0] * 8
        self.ram = [0] * 256


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
    # def halt(self):
    #     self.running = False
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, adr):
        return self.ram[adr]

    def ram_write(self, val, adr):
        self.ram[val] = adr

    def run(self):
        running = self.running
        running = True

        while running:
            command = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if command == HLT:
                running = False
                self.pc += 1
            elif command == PRN:
                print(self.reg[operand_a])
                self.pc +=2
            elif command == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            else:
                running = False
        
