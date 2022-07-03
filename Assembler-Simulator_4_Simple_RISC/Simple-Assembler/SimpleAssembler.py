from sys import stdin

try:
  l=[]
  f1=stdin.read().split("\n")
  for i in f1:
    if(i!=""):
      l.append(i+"\n")
    else:
      l.append("\n")
  xx=len(l)-1
  while(True):
    if(l[xx]=="\n"):
      l=l[:xx]
      xx=xx-1
    else:
      break
  opcode = {"add": ("10000", "RRR"),"sub": ("10001", 'RRR'),"mov": ("10010", 'R$', "10011", 'RR'),"ld": ("10100", "Rm"),
              "st": ("10101", "Rm"),"mul": ("10110", "RRR"),"div": ("10111", "RR"),"rs": ("11000", "R$"),
              "ls": ("11001", "R$"),"xor": ("11010", "RRR"),"or": ("11011", "RRR"),"and": ("11100", "RRR"),
              "not": ("11101", "RR"),"cmp": ("11110", "RR"),"jmp": ("11111", "m"),"jlt": ("01100", "m"),
              "jgt": ("01101", "m"),"je": ("01111", "m"),"hlt": ("01010", "F")}
  registers = {"R0": "000","R1": "001","R2": "010","R3": "011","R4": "100","R5": "101","R6": "110","FLAGS": "111"}
  var_dict = {}  # Stores the variable name with the memory address allocated to the variable
  label_dict  = {} #Stores the variable name with the memory address allocated to the label
  instruction_count = 0
  line_count=1
  l2 = []
  out=[]
  error=False
  def _8bit(n):  # Function to convert a binary number to 8 bit binary number
      x = bin(n)[2:]
      num = 8 - len(x)
      return "0" * num + x
  def inst_to_bin(instruction_list):
      global line_count
      global error
      binary_instruction = ""
      # getting opcode
      if instruction_list[0] in opcode.keys():
          if instruction_list[0] != "mov":
              binary_instruction = binary_instruction + opcode[instruction_list[0]][0]
          else:
              if instruction_list[2][0] == "$":
                  binary_instruction += opcode[instruction_list[0]][0]
              else:
                  binary_instruction += opcode[instruction_list[0]][2]
          if instruction_list[0] != "mov": # getting type and values accordingly
              if opcode[instruction_list[0]][1] == "RRR":  # type A
                if len(instruction_list) == 4 and instruction_list[1] in registers.keys() and instruction_list[2] in registers.keys() and instruction_list[3] in registers.keys():
                  
                  if registers[instruction_list[1]] != "111" and registers[instruction_list[2]] != "111" and registers[instruction_list[3]] != "111":
                    binary_instruction = binary_instruction + "00" + registers[instruction_list[1]] + registers[instruction_list[2]] + registers[instruction_list[3]]
                    out.append(binary_instruction)
                  else:
                    error = True
                    print("[ERROR] Illegal use of FLAGS register at line "+str(line_count))
                else: 
                  error =  True
                  print("[ERROR] Invalid Syntax at line "+str(line_count))
              elif opcode[instruction_list[0]][1] == "Rm":  # type D
                if len(instruction_list) == 3 and instruction_list[1] in registers.keys():  
                  if registers[instruction_list[1]] != "111":
                    if instruction_list[2] in var_dict.keys():
                      binary_instruction = binary_instruction + registers[instruction_list[1]] + var_dict[instruction_list[2]]
                      out.append(binary_instruction)
                    elif instruction_list[2] in label_dict.keys():
                      error = True
                      print("[ERROR] Label Misused as Variable at line "+str(line_count))
                    else:
                      error = True
                      print("[ERROR] Use of undefined variable at line "+str(line_count))
                  else:
                    error = True
                    print("[ERROR] Illegal use of FLAGS register at line "+str(line_count)) 
                else:
                  error = True
                  print("[ERROR] Invalid Syntax at line "+str(line_count))
              elif opcode[instruction_list[0]][1] == "R$":  # type B            
                  if len(instruction_list) == 3 and instruction_list[1] in registers.keys() and instruction_list[2][1:].isdigit():
                    if 0 <= int(instruction_list[2][1:]) <= 255:                  
                      if registers[instruction_list[1]] != "111":           
                        binary_instruction = binary_instruction + registers[instruction_list[1]] + _8bit(int(instruction_list[2][1:]))
                        out.append(binary_instruction)
                      else:
                        error = True
                        print("[ERROR] Illegal use of FLAGS register at line " +str(line_count))  
                    else:
                      error = True
                      print("[ERROR] Illegal immediate value at line " +str(line_count))                    
                  else:  
                    error =  True
                    print("[ERROR] Invalid Syntax at line " +str(line_count))
              elif opcode[instruction_list[0]][1] == "RR":  # type C
                if len(instruction_list) == 3 and instruction_list[1] in registers.keys() and instruction_list[2] in registers.keys():
                  if registers[instruction_list[1]] != "111" and registers[instruction_list[2]] != "111":
                    binary_instruction = binary_instruction + "00000" + registers[instruction_list[1]] + registers[instruction_list[2]]
                    out.append(binary_instruction)
                  else:
                    error = True
                    print("[ERROR] Illegal use of FLAGS register at line "+str(line_count))   
                else:
                  error =  True
                  print("[ERROR] Invalid Syntax at line "+str(line_count))
              elif opcode[instruction_list[0]][1] == "m":  # type E
                if instruction_list[1] in label_dict:
                  binary_instruction = binary_instruction + "000" + label_dict[instruction_list[1]]
                  out.append(binary_instruction)
                elif(instruction_list[1] in var_dict):
                  error=True
                  print("[ERROR] Variable Misused as Label at line "+str(line_count))
                else:
                  error = True
                  print("[ERROR] Label Undefined at line "+str(line_count))
              elif opcode[instruction_list[0]][1] == "F":  # type F
                    binary_instruction = binary_instruction + "0" * 11
                    out.append(binary_instruction)
          else:
                if instruction_list[2][0] == "$":
                    if len(instruction_list) == 3 and instruction_list[1] in registers.keys() and instruction_list[2][1:].isdigit():
                        if 0 <= int(instruction_list[2][1:]) <= 255:
                            if registers[instruction_list[1]] != "111":
                                binary_instruction = binary_instruction + registers[instruction_list[1]] + _8bit(int(instruction_list[2][1:]))
                                out.append(binary_instruction)
                            else:
                                error = True
                                print("[ERROR] Illegal use of FLAGS register at line "+str(line_count))
                        else:
                            error = True
                            print("[ERROR] Illegal Immediate Value at line "+str(line_count))
                    else:
                        error =  True
                        print("[ERROR] Invalid Syntax at line "+str(line_count))
                else:
                    if instruction_list[1] in registers and instruction_list[2] in registers:
                        if registers[instruction_list[1]] != "111":
                            binary_instruction = binary_instruction + "00000" + registers[instruction_list[1]] + registers[instruction_list[2]]
                            out.append(binary_instruction)
                        else:
                            error = True
                            print("[ERROR] Illegal use of FLAGS register at line " +str(line_count))
                    else:
                        error =  True
                        print("[ERROR] Invalid Syntax at line " +str(line_count))
      else:
          print("[ERROR] Invalid Operation Call at line " +str(line_count))
          error=True
  line_count1=1
  for i in l:  # Gives final list of instructions without empty lines
        if i != '\n\n':
            l2.append(i)
            if (i.strip().split()[0] in opcode):  # Count of the total number of instructions excluding var and label declerations
                instruction_count += 1
            elif (i.strip().split()[0][-1] == ":"):  # identifying a label declaration
                if (i.strip().split()[0][:-1] not in label_dict):
                    if i.strip().split()[0][:-1] not in opcode.keys():
                        label_dict[i.strip().split()[0][:-1]] = _8bit(instruction_count)
                        instruction_count += 1
                    elif(not error):
                        error = True
                        print("[ERROR] Invalid Label Name at line",line_count1)
                elif(not error):
                    error=True
                    print("[ERROR] Label redeclared at line",line_count1)
        line_count1+=1
  hlt_chk=l2[-1].strip().split()
  if(len(hlt_chk)==2):                                     #Checking that program ends with halt statement
        if(hlt_chk[0][-1]==":" and hlt_chk[1]=="hlt"):
            pass
        else:
            print("[ERROR] Halt statement not used at EOF") 
            error=True
  elif(len(hlt_chk)==1):
        if(hlt_chk[0]!="hlt"):
            print("[ERROR] Halt statement not used at EOF")
            error=True
        elif(hlt_chk[0]=="hlt"):
            pass
        else:
            print("[ERROR] Halt statement not used at EOF")
            error=True
  else:
        print("[ERROR] Halt statement not used at EOF")
        error=True
  pre_var_dec=True
  line_count2=1
  for i in l[:-1]:
        if(i!='\n\n'):
            if(error):
                break
            tempvar = i.strip().split()
            if (tempvar[0] == "var" and pre_var_dec):  # identifying a variable declaration
                varflag=True
                lll=tempvar[1].split("_")
                for i in lll:
                    if(not i.isalnum()):
                        varflag=False
                if(not varflag):
                    print("[ERROR] Invalid Variable Name at line",line_count2)
                    error=True
                    break
                elif (tempvar[1] not in var_dict):
                    var_dict[tempvar[1]] = _8bit(instruction_count)
                    instruction_count += 1
                else:
                    print("[ERROR] Variable redeclared at line",line_count2)   #[ERROR] Redecleration of same variable
                    error=True
                    break
            elif(tempvar[0] == "var" and not pre_var_dec):
                print("[ERROR] Variable declared at line" ,line_count2,"instead of at the start")  #[ERROR] Variable not declared at the start 
                error=True
                break
            else:
                pre_var_dec=False
            if(tempvar[0]=="hlt"):
                print("[ERROR] Halt statement used before termination at line",line_count2) #[ERROR] Halt statement used before EOF
                error=True
                break
            elif(tempvar[0][-1]==":" and len(tempvar)==2 and tempvar[1]=="hlt"):
                error=True
                print("[ERROR] Halt statement used before termination at line",line_count2) #[ERROR] Halt stament used before EOF as a label
                break
        line_count2+=1
  for i in l:         #Line count handled
    if(i!='\n\n'):
      if(error):
        break
      instruction_list = i.strip().split()# getting opcode
      if (instruction_list[0] != "var" and instruction_list[0][-1] != ":"):
        inst_to_bin(instruction_list)
      elif (instruction_list[0][-1] == ":"):
          labelflag=True
          ll2 = instruction_list[0][:-1].split("_")
          for i in ll2:
            if(not i.isalnum()):
              labelflag=False
          if(not labelflag):
            print("[ERROR] Invalid Label Name at line",line_count)
            error=True
            break
          elif len(instruction_list)>=2:
            inst_to_bin((instruction_list[1:]))
          else:
            print("[ERROR] Empty Label")
            error=True
            break
    line_count=line_count+1
  if(not error):
    for i in out:
      print(i)
except:
  print("[ERROR]Invalid Input File Format")
