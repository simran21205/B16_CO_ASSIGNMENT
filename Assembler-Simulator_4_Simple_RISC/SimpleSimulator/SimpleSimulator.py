from sys import stdin
import fileinput
from matplotlib import pyplot

memory = []
f1 = stdin.read().split("\n")
'''with fileinput.input('test.txt') as f1:
    for i in f1:
        if(i!=""):
            memory.append(i)'''
for i in f1:
    if (i != ""):
        memory.append(i)

memory = memory + (256 - len(memory)) * [0]
pcl = []

def _8bit1(n):  # Function to convert a binary number to 8 bit binary number
      x = n
      num = 8 - len(x)
      return "0" * num + x
def _3bit(n):
    x=n
    num = 3 - len(x)
    return "0" * num + x
def _5bit(n):
    x=n[:5]
    num = 5 - len(x)
    return "0" * num + x
def binaryOfFraction(fraction):
    binary = str()
    while (fraction):
      fraction *= 2
      if (fraction >= 1):
        int_part = 1
        fraction -= 1
      else:
        int_part = 0
      binary += str(int_part)
    return binary

def frac_part(s):
    count = 1
    yo = 0
    for i in s:
        p = -1 *count
        yo += int(i) * pow(2,-1*count)
        count +=1
    return yo

def floatingPoint(real_no):
    int_str = bin(int(float(real_no)))[2 : ]
    fraction_str = binaryOfFraction(float(real_no) - int(float(real_no)))
    ind = int_str.index('1')
    exp_str = bin((len(int_str) - ind - 1))[2 : ]
    exp_str= _3bit(exp_str)
    mant_str = int_str[ind + 1 : ] + fraction_str
    mant_str = mant_str + ('0' * (5 - len(mant_str)))
    ieee_8=exp_str+ mant_str
    return ieee_8

def add(s):
    registers[reg[s[8:11]]] = registers[reg[s[2:5]]] + registers[reg[s[5:8]]]
    if (registers[reg[s[2:5]]] > max_val):
        registers[reg[s[2:5]]] = int(bin(int(registers[reg[s[2:5]]]))[2:][-16:], 2)
        cmp_value[0] = 1

def addf(s):
    a = _8bit1(bin(int(registers[reg[s[2:5]]]))[2:])
    exp1 = a[0:3]
    mantissa1 = a[3:8]
    exp_val1 = int(exp1, 2)
    ans1 = "1"+mantissa1
    d1 = int(ans1[:exp_val1+1],2)
    f1 = frac_part(ans1[exp_val1+1:])

    b = _8bit1(bin(int(registers[reg[s[5:8]]]))[2:])
    exp2 = b[0:3]
    mantissa2 = b[3:8]
    exp_val2 = int(exp2, 2)
    ans2 = "1"+mantissa2
    d2 = int(ans2[:exp_val2+1],2)
    f2 = frac_part(ans2[exp_val2+1:])

    yoo = floatingPoint(str(d1+f1+d2+f2))

    exp = yoo[0:3]
    mantissa = yoo[3:8]
    exp_val = int(exp, 2)
    ans = "1"+mantissa
    d = int(ans[:exp_val+1],2)
    f = frac_part(ans[exp_val+1:])
    registers[reg[s[8:11]]] = int(yoo,2)
    
    if (len(yoo)>8):
        cmp_value[0] = 1
        
def sub(s):
    registers[reg[s[8:11]]] = registers[reg[s[2:5]]] - registers[reg[s[5:8]]] 
    if registers[reg[s[2:5]]] < min_val:
        registers[reg[s[2:5]]] = 0
        cmp_value[0] = 1

def subf(s):
    a = _8bit1(bin(int(registers[reg[s[2:5]]]))[2:])
    exp1 = a[0:3]
    mantissa1 = a[3:8]
    exp_val1 = int(exp1, 2)
    ans1 = "1"+mantissa1
    d1 = int(ans1[:exp_val1+1],2)
    f1 = frac_part(ans1[exp_val1+1:])


    b = _8bit1(bin(int(registers[reg[s[5:8]]]))[2:])
    exp2 = b[0:3]
    mantissa2 = b[3:8]
    exp_val2 = int(exp2, 2)
    ans2 = "1"+mantissa2
    d2 = int(ans2[:exp_val2+1],2)
    f2 = frac_part(ans2[exp_val2+1:])    

    yoo = floatingPoint(str(d1+f1-d2-f2))

    exp = yoo[0:3]
    mantissa = yoo[3:8]
    exp_val = int(exp, 2)
    ans = "1"+mantissa
    d = int(ans[:exp_val+1],2)
    f = frac_part(ans[exp_val+1:])
    
    registers[reg[s[8:11]]] = int(yoo,2)
    
    if registers[reg[s[2:5]]] < min_val:
        registers[reg[s[2:5]]] = 0
        cmp_value[0] = 1
        
    if (len(yoo)>8 and d1+f1-d2-f2<0):
        cmp_value[0] = 1


def mul(s):
    registers[reg[s[8:11]]] = registers[reg[s[2:5]]] * registers[reg[s[5:8]]] 
    if registers[reg[s[8:11]]] > max_val:
        registers[reg[s[8:11]]] = int(bin(int(registers[reg[s[8:11]]]))[2:][-16:], 2)
        cmp_value[0] = 1


def xor(s):
    registers[reg[s[8:11]]] = registers[reg[s[2:5]]] ^ registers[reg[s[5:8]]] 


def Or(s):
    registers[reg[s[8:11]]] = registers[reg[s[2:5]]] | registers[reg[s[5:8]]] 


def And(s):
    registers[reg[s[8:11]]] = registers[reg[s[2:5]]] & registers[reg[s[5:8]]] 


def movimm(s):
    registers[reg[s[:3]]] = int(s[3:], 2)

def movf(s):    
    registers[reg[s[:3]]] = float(int(s[3:], 2))

def rs(s):
    registers[reg[s[:3]]] = registers[reg[s[:3]]] >> int(s[3:], 2)
    if registers[reg[s[:3]]] > max_val:
        registers[reg[s[:3]]] = int(bin(int(registers[reg[s[:3]]]))[2:][-16:], 2)
        cmp_value[0] = 1

def ls(s):
    registers[reg[s[:3]]] = registers[reg[s[:3]]] << int(s[3:], 2)
    if registers[reg[s[:3]]] > max_val:
        registers[reg[s[0:3]]] = int(bin(int(registers[reg[s[:3]]]))[2:][-16:], 2)
        cmp_value[0] = 1

def Not(s):
    alpha = registers[reg[s[8:]]]
    new = _16bit(alpha)
    #print(alpha)
    x = ""
    for i in new:
        x += str(int(i) ^ 1)
    #print(x)
    num = int(x, 2)
    registers[reg[s[5:8]]] = num

def div(s):
    registers[0] = registers[reg[s[5:8]]] // registers[reg[s[8:11]]]
    registers[1] = registers[reg[s[5:8]]] % registers[reg[s[8:11]]]

def movreg(s):
    if reg[s[8:11]] != 7:
        registers[reg[s[8:11]]] = registers[reg[s[5:8]]]
    else:
        registers[reg[s[5:8]]] = int("".join(list(map(str, cmp_value))), 2)
        print("yo2")


def cmp(s):
    if registers[reg[s[5:8]]] == registers[reg[s[8:11]]]:
        cmp_value[3] = 1
    elif registers[reg[s[5:8]]] > registers[reg[s[8:11]]]:
        cmp_value[2] = 1
    else:
        cmp_value[1] = 1

def load(s):
    registers[reg[s[:3]]] = memory[int(s[3:], 2)]

def store(s):
    memory[int(s[3:], 2)] = registers[reg[s[:3]]]


def je(s):
    global pc
    if (cmp_value[3]) == 1:
        pc = int(s[3:], 2) - 1


def jlt(s):
    global pc
    if cmp_value[1] == 1:
        pc = int(s[3:], 2) - 1


def jgt(s):
    global pc
    if cmp_value[2] == 1:
        pc = int(s[3:], 2) - 1


def jmp(s):
    global pc
    pc = int(s[3:], 2) - 1


max_val = 65535
pc = 0
min_val = 0
reg = {"000": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}
cmp_value = [0, 0, 0, 0] # [[overflow],[less than],[greater than],[equal to]]
registers = [0, 0, 0, 0, 0, 0, 0, 0]  
opcode = {"10000": add, "10001": sub, "10110": mul, "11010": xor, "11011": Or, "11100": And, "10010": movimm,
          "11000": rs, "11001": ls, "10011": movreg, "10111": div, "11101": Not, "11110": cmp, "10100": load,
          "10101": store, "11111": jmp, "01100": jlt, "01101": jgt, "01111": je, "00000": addf,
          "00001": subf, "00010": movf}

def _8bit(n):  # Function to convert a binary number to 8 bit binary number
    x = bin(n)[2:]
    return "0" * (8 - len(x)) + x


def _16bit(n):  # Function to convert a binary number to 16 bit binary number
    x = bin(int(n))[2:]
    return "0" * (16 - len(x)) + x

def get_cmpval(l):
    x = ""
    for i in l:
        x += str(i)
    registers[7]=int(x,2)
    
old_pc = 0
while (memory[pc][:5] != "01010"):
    old_pc = pc
    pc2 = pc
    opcode[memory[pc][:5]](memory[pc][5:])
    if old_pc != pc:
        pc2 = pc
        pc = old_pc
    get_cmpval(cmp_value)
    if (memory[pc][:5] != "11110" and cmp_value[0] != 1 ):  # resets flag after instruction if the instruction is not compare or if there is no overflow
        registers[7] = 0
        cmp_value=[0, 0, 0, 0]
    print(_8bit(pc), end=" ")
    for i in registers[:7]:
        print(_16bit(i), end=" ")
    print("0" * 12, end="")
    for i in cmp_value:
        print(i, end="")
    print()
    if (registers[7] == 8):
        registers[7] = 0
        cmp_value=[0, 0, 0, 0]
        
    pcl.append(pc)
    pc = pc2
    pc = pc + 1

pcl.append(pc)
print(_8bit(pc), end=" ")
for i in registers[:7]:
    print(_16bit(i), end=" ")
print("0" * 12, end="")
for i in cmp_value:
    print(i, end="")
print()
x = range(len(pcl))
for i in memory:
    if (type(i) == type("a")):
        print(i)
    else:
        print(_16bit(i))
pyplot.scatter(x, pcl)
pyplot.xlabel("Cycle Number")
pyplot.ylabel("Program Counter")
pyplot.grid()
pyplot.show()
# assuming st has the instruction line in binary
