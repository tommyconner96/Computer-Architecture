import sys

PRINT_WORLD    = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4
PRINT_REGISTER = 5
ADD            = 6    
PUSH           = 7
POP            = 8
CALL           = 9   
RET            = 10  

memory = [0] * 256

# LOAD A PROGRAM INTO MEMORY
def load_program():
    if len(sys.argv) != 2:
        print("Wrong number of arguments, please pass file name")
        sys.exit(1) 

    memory_address = 0
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
            command_num = int(command, 10)
            memory[memory_address] = command_num
            memory_address += 1

# Program counter
pc = 0

registers = [0] * 8

SP = 7
# registers[SP] == the current top of our stack
registers[SP] = 256

load_program()

running = True
while running:

    # Read a command from memory
    # at the current PC location 
    command = memory[pc]
    if command == PRINT_WORLD:
        print("Hello World")
        pc += 1
    
    elif command == HALT:
        running = False
        pc += 1
    
    elif command == PRINT_NUM:
        # Take a look at the next line in memory
        value = memory[pc + 1]
        # print that value 
        print(value)
        pc += 2
    
    elif command == SAVE:
        # Get the value we are saving
        value = memory[pc + 1]
        reg_address = memory[pc + 2]
        # Store the value at the correct register
        registers[reg_address] = value
        pc += 3
    
    elif command == PRINT_REGISTER:
        # get the address of register to print
        reg_address = memory[pc + 1]
        print(registers[reg_address])
        pc += 2
    
    elif command == ADD:
        reg_addr_1 = memory[pc + 1]
        reg_addr_2 = memory[pc + 2]

        # Retrieve the values in both registers
        val1 = registers[reg_addr_1]
        val2 = registers[reg_addr_2]

        # Add and store result in reg_addr_1
        registers[reg_addr_1] = val1 + val2

        pc += 3
    
    elif command == PUSH:
        # Read the given register address
        reg_address = memory[pc + 1]
        value_to_push = registers[reg_address]
        # move the stack pointer down
        registers[SP] -= 1
        # write the value to push, into the top of stack
        memory[registers[SP]] = value_to_push
        pc += 2
    
    elif command == POP:
        # Read the given register address
        reg_address = memory[pc + 1]
        # Read the value at the top of the stack
        # store that into the register given
        registers[reg_address] = memory[registers[SP]]
        # move the stack pointer back up
        registers[SP] += 1
        pc += 2
    
    elif command == CALL:
        # Push the return address onto the stack
        # Move the SP down
        registers[SP] -= 1
        # Write the value of the next line to return to in the code
        memory[registers[SP]] = pc + 2
        # Set the PC to whatever is given to us in the register
        reg_num = memory[pc + 1]
        print(memory[-10:])
        pc = registers[reg_num]

    elif command == RET:
        # Pop the top of the stack and set the PC to the value of what was popped
        pc = memory[registers[SP]]
        registers[SP] += 1