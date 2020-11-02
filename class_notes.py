import sys

# OPERATION PRINT HELLO WORLD
PRINT_WORLD    = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4
PRINT_REGISTER = 5
ADD            = 6    

memory = []

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
        command_num = int(command, 10)
        memory.append(command_num)

# Program counter
pc = 0

registers = [0] * 8

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