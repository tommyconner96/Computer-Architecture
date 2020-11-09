"""CPU functionality."""

import sys

# LDI = 0b10000010
# HLT = 0b00000001
# PRN = 0b01000111
# MUL = 0b10100010
# SP = 7  # stack pointer
LDI = 130
HLT = 1
PRN = 71
ADD = 160
SUB = 161
MUL = 162
DIV = 163
PUSH = 69
POP = 70
CALL = 80
RET = 17


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
        self.SP = 7
        self.pc = 0
        self.mar = 0
        self.mdr = 0
        self.ir = None
        self.fl = None
        self.running = False
        # self.ie = None
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[self.SP] = 256

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
                command_num = int(command, 2)
                self.ram[address] = command_num
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]
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
        self.ram[adr] = val

    def ALU_OPS(self, command):
        # ADD = 160
        # SUB = 161
        # MUL = 162
        # DIV = 163
        if command == 160:
            return "ADD"
        if command == 161:
            return "SUB"
        if command == 162:
            return "MUL"
        if command == 163:
            return "DIV"

    def run(self):
        running = self.running
        running = True
        while running:
            command = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # we will determine if operation is an ALU operation
            is_alu = (command >> 5) & 0b001 == 1
            if is_alu:
                op_type = self.ALU_OPS(command)
                # print(command)
                self.alu(op_type, operand_a, operand_b)
                self.pc += 3

            if command == HLT:
                running = False
                self.pc += 1
            elif command == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif command == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == PUSH:
                value_to_push = self.reg[operand_a]
                # move the stack pointer down
                self.reg[self.SP] -= 1
                # write the value to push, into the top of stack
                self.ram[self.reg[self.SP]] = value_to_push
                self.pc += 2
            elif command == POP:
                # Read the given register address
                # Read the value at the top of the stack
                # store that into the register given
                self.reg[operand_a] = self.ram[self.reg[self.SP]]
                # move the stack pointer back up
                self.reg[self.SP] += 1
                self.pc += 2
            elif command == CALL:
                # Push the return address onto the stack
                # Move the SP down
                self.reg[self.SP] -= 1
                # Write the value of the next line to return to in the code
                self.ram[self.reg[self.SP]] = self.pc + 2
                # Set the PC to whatever is given to us in the register
                self.pc = self.reg[operand_a]

            elif command == RET:
                # Pop the top of the stack and set the PC to the value of what was popped
                self.pc = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
