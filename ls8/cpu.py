"""CPU functionality."""

import sys

# LDI = 0b10000010
# HLT = 0b00000001
# PRN = 0b01000111
# MUL = 0b10100010
SP = 7  # stack pointer
LDI = 130
HLT = 1
PRN = 71
MUL = 162
PUSH = 69
POP = 70


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
        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        # program = []
        # LOAD A PROGRAM INTO MEMORY
        print(sys.argv)
        if len(sys.argv) != 2:
            print("Wrong number of arguments, please pass file name")
            sys.exit(1)

        with open(sys.argv[1]) as f:
            for line in f:
                # Split the line on the comment character (#)
                line_split = line.split('#')
                # Extract the command from the split line
                # It will be the first value in our split line
                command = line_split[0].strip()
                if command == '':
                    continue
                # specify that the number is base 10
                command_num = int(command, 2)
                # print(command_num)
                # program.append(command_num)
                self.ram[address] = command_num
                address +=1

        # REVISIT IF WE GET AN INFINITE LOOP. DAY 3 lecture  1:10 for reference
            # for instruction in program:
            #     self.ram[address] = instruction
            #     address += 1
            # print(program)
            # return program
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
        # if adr >= 0 and adr < len(self.ram):
        return self.ram[adr]
        # else:
        #     print("error")
        #     return -1

    def ram_write(self, val, adr):
        self.ram[adr] = val

    def run(self):
        running = self.running
        running = True

        while running:
            command = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(operand_a, operand_b)
            # print(command)
            if command == HLT:
                running = False
                self.pc += 1
            elif command == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif command == LDI:
                # print(operand_a, operand_b)
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            elif command == PUSH:
                value_to_push = self.reg[operand_a]
                # move the stack pointer down
                self.reg[SP] -= 1
                # write the value to push, into the top of stack
                self.ram[self.reg[SP]] = value_to_push
                self.pc += 2
            elif command == POP:
                # Read the given register address
                # Read the value at the top of the stack
                # store that into the register given
                self.reg[operand_a] = self.ram[self.reg[SP]]
                # move the stack pointer back up
                self.reg[SP] += 1
                self.pc += 2
