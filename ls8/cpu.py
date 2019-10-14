"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = self.reg[0]
    
    def __repr__(self):
        return f"ram: {self.ram} \n reg: {self.reg}"
    
    def ram_read(self, addy):
        return self.ram[addy]
    
    def ram_write(self, value, addy):
        self.ram[addy] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
       
        print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        opp_a = self.ram[self.pc + 1]
        opp_b = self.ram[self.pc + 2]

        print(f"opp_a: {opp_a} opp_b: {opp_b}")

        running = True

        while running:
            IR = self.ram[self.pc]
            print(f"ir: {IR}, pc: {self.pc}")
            
            if IR == HLT:
                running = False
            
            elif IR == LDI:
                self.reg[opp_a] = opp_b
                self.pc += 2
            
            elif IR == PRN:
                print(self.reg[opp_a])
                self.pc += 1

            else:
                print(f"{IR}")
                sys.exit(1)
            
            self.pc += 1