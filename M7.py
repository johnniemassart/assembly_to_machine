import math

#Conversion class to convert assembly code into machine code
class Conversion:
    def __init__(self, operand, rd, rn, rm="optional"):
        self.operand = operand
        self.rd = rd
        self.rn = rn
        self.rm = rm
    
    #cond code - 1110 (all)
    def cond_code(self):
        return "1110"
    
    # op type - dependent on operand
    def op_type(self):
        if self.operand == "ADD" or self.operand == "SUB":
            if self.rm[0] == "r":
                return "000"
            if self.rm[0] == "#":
                return "001"
        elif self.operand == "MUL" or self.operand == "LSL" or self.operand == "ASR":
            return "000"
        elif self.operand == "MOV":
            if self.rn[0] == "r":
                return "000"
            if self.rn[0] == "#":
                return "001"
        elif self.operand == "LDR" or self.operand == "STR":
            if self.rm[0] == "#":
                return "010"
            elif self.rm[0] == "r":
                return "011"
            else:
                return "010"
    
    #remove leading r from rd
    def remove_rd_leading(self):
        if self.rd[0] == "r":
            return self.rd.replace("r", "")
    
    #remove leading r from rn
    def remove_rn_leading(self):
        if self.rn[0] == "r":
            return self.rn.replace("r", "")
        elif self.rn[0] == "#":
            return self.rn.replace("#", "")
    
    #remove leading r, # from rm
    def remove_rm_leading(self):
        if self.rm[0] == "r":
            return self.rm.replace("r", "")
        elif self.rm[0] == "#":
            return self.rm.replace("#", "")
    
    #op code value    
    def op_code(self):
        value = ""
        if self.operand == "ADD":
            value = "0100"
        elif self.operand == "SUB":
            value = "0010"
        elif self.operand == "MOV":
            value = "1101"
        elif self.operand == "MUL":
            value = "000"
        elif self.operand == "LSL":
            value = "1101"
        elif self.operand == "ASR":
            value = "1101"
        elif self.operand == "LDR":
            value = "1100"
        elif self.operand == "STR":
            value = "1100"
        return value
    
    #MUL a value - 0 (mul)
    def mult_a(self):
        return "0"
    
    #s value - 0 (all)
    def s(self):
        return "0"
    
    #LDR or STR L/S
    def l_s(self):
        if self.operand == "LDR":
            return "1"
        elif self.operand == "STR":
            return "0"
    
    # convert decimal to binary
    def dec_to_bn(self, dec):
        int_value = int(dec)
        str_value = ""
        while int_value > 0:
            if int_value % 2 == 0:
                str_value = "0" + str_value
            elif int_value % 2 != 0:
                str_value = "1" + str_value
            int_value = math.floor(int_value/2)
        if int_value == 0 and len(str_value) == 0:
            str_value = "0"
        return str_value

    #append zeros to binary conversion, if necessary
    def append_zeros(self, dec):
        binary = self.dec_to_bn(dec)
        while len(binary) % 4 != 0:
            binary = "0" + binary
        return binary
    
    #convert Rd value to binary
    def rd_conv(self):
        rd_leading = self.remove_rd_leading()
        return self.append_zeros(rd_leading)
    
    #convert Rn value to binary
    def rn_conv(self):
        rn_leading = self.remove_rn_leading()
        return self.append_zeros(rn_leading)
    
    # register format ADD, SUB
    def register_format(self):
        rm_leading = self.remove_rm_leading()
        reg_format_len = 12
        rm_bin = ""
        if len(self.dec_to_bn(rm_leading)) <= 4:
            rm_bin += self.append_zeros(rm_leading)
        else:
            rm_bin += self.dec_to_bn(rm_leading)
        add_zeros = reg_format_len - len(rm_bin)
        str_val = ""
        for i in range(0, add_zeros):
            str_val += "0"
        return str_val + rm_bin
    
    #MUL Rn - 0000
    def mul_rn_val(self):
        return "0000"
    
    #MUL Rs value 
    def mul_rs_conv(self):
        rs_leading = self.remove_rm_leading()
        return self.append_zeros(rs_leading)
    
    #MUL cd
    def mult_cd(self):
        return "1001"
    
    #MOV rn val - do not be confused with parameter naming
    def mov_rn(self):
        return "0000"
    
    #MOV register format
    def mov_register_format(self):
        register = self.rn_conv()
        register_len = 12
        add_zeros = register_len - len(register)
        str_val = ""
        for i in range(0, add_zeros):
            str_val += "0"
        return str_val + register
    
    #LSL rn val
    def lsl_asr_rn(self):
        return "0000"
    
    #LSL register format
    def lsl_asr_reg_format_w_reg(self):
        bit_7 = "0"
        s_r = "1"
        if self.operand == "LSL":
            shift_type = "00"
        elif self.operand == "ASR":
            shift_type = "10"
        rm_val = self.rn_conv()
        rs_val = self.append_zeros(self.remove_rm_leading())
        return f"{rs_val}{bit_7}{shift_type}{s_r}{rm_val}"
    
    #LDR, STR register format
    def ldr_str_reg_format(self):
        reg_len = 12
        str_val = ''
        if self.rm == "optional":
            for i in range(reg_len):
                str_val += "0"
            return str_val
        else:
            rm_leading = self.remove_rm_leading()
            rm_bin = self.append_zeros(rm_leading)
            reg_len = 12
            remaining_zeros = reg_len - len(rm_bin)
            str_val = ""
            for i in range(remaining_zeros):
                str_val += "0"
            return str_val + rm_bin
    
    #32 binary representation
    def bin_rep(self):
        if self.operand == "ADD" or self.operand == "SUB":
            return f"{self.cond_code()}{self.op_type()}{self.op_code()}{self.s()}{self.rn_conv()}{self.rd_conv()}{self.register_format()}"
        elif self.operand == "MUL":
            return f"{self.cond_code()}{self.op_type()}{self.op_code()}{self.mult_a()}{self.s()}{self.rd_conv()}{self.mul_rn_val()}{self.mul_rs_conv()}{self.mult_cd()}{self.rn_conv()}"
        elif self.operand == "MOV":
            return f"{self.cond_code()}{self.op_type()}{self.op_code()}{self.s()}{self.mov_rn()}{self.rd_conv()}{self.mov_register_format()}"
        elif self.operand == "LSL" or self.operand == "ASR":
            return f"{self.cond_code()}{self.op_type()}{self.op_code()}{self.s()}{self.lsl_asr_rn()}{self.rd_conv()}{self.lsl_asr_reg_format_w_reg()}"
        elif self.operand == "LDR" or self.operand == "STR":
            return f"{self.cond_code()}{self.op_type()}{self.op_code()}{self.l_s()}{self.rn_conv()}{self.rd_conv()}{self.ldr_str_reg_format()}"
    
    # hexidecimal dictionary for conversion
    def hex_dict(self):
        hex = {}
        j = 97
        for i in range(0, 16):
            hex[i] = i
            if i >= 10:
                hex[i] = chr(j)
                j += 1
        return hex
    
    # split binary conversion into groups of four
    def bin_four_split(self):
        val = ""
        val_list = []
        i = 1
        for element in self.bin_rep():
            val += element
            if i % 4 == 0:
                val_list.append(val)
                val = ""
            i = i + 1
        return val_list
    
    #convert binary groups of four to decimal value for each goup of four
    def bin_num_conv(self):
        bin_list = self.bin_four_split()
        str_list = []
        val = 0
        for bin in bin_list:
            for i, j in enumerate(bin):
                if i % 4 == 0 and j == "1":
                    val += 8
                if i % 4 == 1 and j == "1":
                    val += 4
                if i % 4 == 2 and j == "1":
                    val += 2
                if i % 4 == 3 and j == "1":
                    val += 1
            str_list.append(val)
            val = 0
        return str_list
    
    # convert decimal groups of four to hexidecimal
    def assembler_val(self):
        cont = self.bin_num_conv()
        hex = self.hex_dict()
        str_conv = ""
        for i in cont:
            for key, value in hex.items():
                if i == key:
                    str_conv += str(value)
        return str_conv
    

#read file into list
file_list = []
with open("./content.txt", "r") as file:
    file_list = file.read().splitlines()

#split file list accordingly
file_list_split = []
for item in file_list:
    file_list_split.append(item.replace(",", "").replace("[", "").replace("]", "").split())

#iterate through each command, store in variable
assembler_conversion = ""
for i in range(len(file_list_split)):
    testing = Conversion(*file_list_split[i])
    if i < (len(file_list) - 8):
        assembler_conversion += file_list[i] + "\t\t\t" + testing.assembler_val() + "\n"
    elif i < (len(file_list) - 2):
        assembler_conversion += file_list[i] + "\t\t" + testing.assembler_val() + "\n"
    else:
        assembler_conversion += file_list[i] + "\t" + testing.assembler_val() + "\n"

#write to file
with open("./assembler_conversion.txt", "w") as file:
    file.write(assembler_conversion)