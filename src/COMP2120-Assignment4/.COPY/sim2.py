#!/usr/bin/env python3
#
# CPU simulator for COMP2120
#

opcode = ["ADD", "SUB", "NOT", "AND", "OR", "MOV", "LD", "ST", "B", "HLT",
	"PUSH", "POP", "CALL" , "RET"];

DO_NOT_SET_FLAG = 0
SET_FLAG = 1
RAM_SIZE=1024
RF_SIZE=32

import sys
import array as arr


class Register:
  def __init__(self, name, val):
    self.name=name
    self.val=val

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def puthex(val):
  return '{0:0{1}x}'.format(val,8)

def init_memory():
  global mem
  mem = arr.array('i', [])
  for x in range(0, RAM_SIZE):
    mem.append(0)

def init_RF():
  global RF
  RF = arr.array('i', [])
  for x in range(0, RF_SIZE):
    RF.append(0)

def init():
  global Register
  global Signal
  Register = {
    "PC"     : 0,
    "A"      : 0,
    "B"      : 0,
    "C"      : 0,
    "MAR"    : 0,
    "MBR"    : 0,
    "TEMP"   : 0,
    "SP"     : 0,
    "RFOUT1" : 0,
    "RFOUT2" : 0,
    "RFIN"   : 0,
    "IR"     : 0,
    "ZERO_FLAG" : 0
    }
  Signal = {
    "calc_addr"      : 0,
    "push_pop"       : 0,
    "incSP"          : 0,
    "decSP"          : 0,
    "MAR_to_TEMP"    : 0,
    "TEMP_to_MAR"    : 0,
    "branch"         : 0,
    "read_RF_port_1" : 0,
    "read_RF_port_2" : 0,
    "write_RF"       : 0,
    "src_of_S1"      : '',
    "dst_of_S1"      : '',
    "src_of_S2"      : '',
    "dst_of_S2"      : '',
    "src_of_D"       : '',
    "dst_of_D"       : '',
    "doalu"          : 0,
    "ALU_func"       : '',
    "move_via_S1"    : 0,
    "move_via_S2"    : 0,
    "move_via_D"     : 0,
    "read_memory"    : 0,
    "write_memory"   : 0,
    "dohalt"         : 0
    }
  init_memory()
  init_RF()

def reset():
  Register["PC"] = 0
  Register["SP"] = RAM_SIZE * 4

def incPC():
  Register["PC"] += 4
  if (debug):
    eprint("PC is increased by 4 (", puthex(Register["PC"]), ")")

def do_move_via_S1 (src, dst):
  Register[dst] = Register[src] 
  if (debug):
    eprint("Move via S1: ", dst, "<-", src, " (", puthex(Register[src]), ")")
    
def do_move_via_S2 (src, dst):
  Register[dst] = Register[src] 
  if (debug):
    eprint("Move via S2: ", dst, "<-", src, " (", puthex(Register[src]), ")")
    
def do_move_via_D (src, dst):
  Register[dst] = Register[src] 
  if (debug):
    eprint("Move via D: ", dst, "<-", src, " (", puthex(Register[src]), ")")

def do_read_RF_port1():
  reg = (Register["IR"]//65536)%256
  Register["RFOUT1"] = RF[reg]
  if (debug):
    eprint("Read RF Port 1 -- R", reg, " (", puthex(Register["RFOUT1"]), ")")

def do_read_RF_port2():
  reg = (Register["IR"]%65536)//256
  Register["RFOUT2"] = RF[reg]
  if (debug):
    eprint("Read RF Port 2 -- R", reg, " (", puthex(Register["RFOUT2"]), ")")

def do_write_RF():
  reg = Register["IR"]%256
  RF[reg] = Register["RFIN"]
  if (debug):
    eprint("Write RF -- R", reg, " (", puthex(Register["RFIN"]), ")")

def ALU_COPY():
  Register["C"] = Register["A"]
  if (debug):
    eprint("ALU (COPY)")

def ALU_ADD():
  Register["C"] = Register["A"] + Register["B"]
  if (debug):
    eprint("ALU (ADD)")

def ALU_SUB():
  Register["C"] = Register["A"] - Register["B"]
  if (debug):
    eprint("ALU (SUB)")

def ALU_AND():
  Register["C"] = Register["A"] & Register["B"]
  if (debug):
    eprint("ALU (AND)")

def ALU_OR():
  Register["C"] = Register["A"] | Register["B"]
  if (debug):
    eprint("ALU (OR)")

def ALU_NOT():
  Register["C"] = ~Register["A"]
  if (debug):
    eprint("ALU (NOT)")

def ALU_operation (opcode, setflag):
  switcher = {
    "OP_COPY": ALU_COPY,
    "OP_ADD" : ALU_ADD,
    "OP_SUB" : ALU_SUB,
    "OP_AND" : ALU_AND,
    "OP_OR"  : ALU_OR,
    "OP_NOT" : ALU_NOT
    }
  func = switcher.get(opcode)
  func()
  if (setflag==1):
    if (Register["C"]==0):
      Register["ZERO_FLAG"] = 1
    else:
      Register["ZERO_FLAG"] = 0
    if (debug):
      eprint("Zero Flag Set to ", Register["ZERO_FLAG"])

def do_read_memory():
  addr = Register["MAR"]//4
  Register["MBR"] = mem[addr]
  if (debug):
    eprint("Read Memory at ", puthex(Register["MAR"]), " (", puthex(Register["MBR"]), ")")

def do_write_memory():
  addr = Register["MAR"]//4
  mem[addr] = Register["MBR"] 
  if (debug):
    eprint("Write Memory at ", puthex(Register["MAR"]), " (", puthex(Register["MBR"]), ")")

def do_incSP():
  Register["SP"] += 4
  if (debug):
    eprint("SP increased to ", puthex(Register["SP"]))

def do_decSP():
  Register["SP"] -= 4
  if (debug):
    eprint("SP decreased to ", puthex(Register["SP"]))

def do_MAR_to_TEMP():
  Register["TEMP"] = Register["MAR"]
  if (debug):
    eprint("Move MAR to TEMP")

def do_TEMP_to_MAR():
  Register["MAR"] = Register["TEMP"]
  if (debug):
    eprint("Move TEMP to MAR")

def fetch():
  if (debug):
    eprint("-------------------------------------------")
    eprint("Instruction Fetch")
    eprint("-------------------------------------------")
  do_move_via_S1("PC", "A")
  ALU_operation("OP_COPY", DO_NOT_SET_FLAG)
  do_move_via_D("C", "MAR")
  addr = Register["MAR"]//4
  Register["IR"] = mem[addr]
  if (debug):
    eprint("Read Instruction at ", puthex(Register["MAR"]), " (", puthex(Register["IR"]), ")")
  incPC()

def set_HALT():
  Signal["dohalt"] = 1

def set_ADD():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 1
  Signal["read_RF_port_2"] = 1
  Signal["write_RF"] = 1
  Signal["src_of_S1"] = "RFOUT1"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = "RFOUT2"
  Signal["dst_of_S2"] = "B"
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "RFIN"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_ADD"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 1
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_SUB():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 1
  Signal["read_RF_port_2"] = 1
  Signal["write_RF"] = 1
  Signal["src_of_S1"] = "RFOUT1"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = "RFOUT2"
  Signal["dst_of_S2"] = "B"
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "RFIN"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_SUB"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 1
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_AND():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 1
  Signal["read_RF_port_2"] = 1
  Signal["write_RF"] = 1
  Signal["src_of_S1"] = "RFOUT1"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = "RFOUT2"
  Signal["dst_of_S2"] = "B"
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "RFIN"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_AND"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 1
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_OR():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 1
  Signal["read_RF_port_2"] = 1
  Signal["write_RF"] = 1
  Signal["src_of_S1"] = "RFOUT1"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = "RFOUT2"
  Signal["dst_of_S2"] = "B"
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "RFIN"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_OR"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 1
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_NOT():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 1
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 1
  Signal["src_of_S1"] = "RFOUT1"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "RFIN"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_NOT"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_MOVE():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 1
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 1
  Signal["src_of_S1"] = "RFOUT1"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "RFIN"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_COPY"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_LD():
  Signal["calc_addr"] = 1
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 0
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 1
  Signal["src_of_S1"] = "MBR"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "RFIN"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_COPY"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 1
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_ST():
  Signal["calc_addr"] = 1
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 1
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 0
  Signal["src_of_S1"] = "RFOUT1"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "MBR"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_COPY"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 1
  Signal["dohalt"] = 0

def set_BR():
  Signal["calc_addr"] = 1
  Signal["push_pop"] = 0
  Signal["incSP"] = 0
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 1
  Signal["read_RF_port_1"] = 0
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 0
  Signal["src_of_S1"] = ""
  Signal["dst_of_S1"] = ""
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = ""
  Signal["dst_of_D"] = ""
  Signal["doalu"] = 0
  Signal["ALU_func"] = ""
  Signal["move_via_S1"] = 0
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 0
  Signal["read_memory"] = 0
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_PUSH():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 1
  Signal["incSP"] = 0
  Signal["decSP"] = 1
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 1
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 0
  Signal["src_of_S1"] = "RFOUT1"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "MBR"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_COPY"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 1
  Signal["dohalt"] = 0

def set_POP():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 1
  Signal["incSP"] = 1
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 0
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 1
  Signal["src_of_S1"] = "MBR"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "RFIN"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_COPY"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 1
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def set_CALL():
  Signal["calc_addr"] = 1
  Signal["push_pop"] = 1
  Signal["incSP"] = 0
  Signal["decSP"] = 1
  Signal["MAR_to_TEMP"] = 1
  Signal["TEMP_to_MAR"] = 1
  Signal["branch"] = 1
  Signal["read_RF_port_1"] = 0
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 0
  Signal["src_of_S1"] = "PC"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "MBR"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_COPY"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 0
  Signal["write_memory"] = 1
  Signal["dohalt"] = 0

def set_RET():
  Signal["calc_addr"] = 0
  Signal["push_pop"] = 1
  Signal["incSP"] = 1
  Signal["decSP"] = 0
  Signal["MAR_to_TEMP"] = 0
  Signal["TEMP_to_MAR"] = 0
  Signal["branch"] = 0
  Signal["read_RF_port_1"] = 0
  Signal["read_RF_port_2"] = 0
  Signal["write_RF"] = 0
  Signal["src_of_S1"] = "MBR"
  Signal["dst_of_S1"] = "A"
  Signal["src_of_S2"] = ""
  Signal["dst_of_S2"] = ""
  Signal["src_of_D"] = "C"
  Signal["dst_of_D"] = "PC"
  Signal["doalu"] = 1
  Signal["ALU_func"] = "OP_COPY"
  Signal["move_via_S1"] = 1
  Signal["move_via_S2"] = 0
  Signal["move_via_D"] = 1
  Signal["read_memory"] = 1
  Signal["write_memory"] = 0
  Signal["dohalt"] = 0

def decode():
  opcode = Register["IR"]//16777216;
  switcher = {
    0 : set_ADD,
    1 : set_SUB,
    2 : set_NOT,
    3 : set_AND,
    4 : set_OR,
    5 : set_MOVE,
    6 : set_LD,
    7 : set_ST,
    8 : set_BR,
    9 : set_HALT,
    10: set_PUSH,
    11: set_POP,
    12: set_CALL,
    13: set_RET
    }
  func=switcher.get(opcode)
  func()
  if (debug):
    eprint("-------------------------------------------")
    eprint("Instruction Decode")
    eprint("-------------------------------------------")
  
def execute():
  if (debug):
    eprint("-------------------------------------------")
    eprint("Instruction Execute")
    eprint("-------------------------------------------")
  if (Signal["dohalt"]):
    return
  if (Signal["calc_addr"]):
    do_move_via_S1("PC", "A")
    ALU_operation("OP_COPY", DO_NOT_SET_FLAG)
    do_move_via_D("C","MAR")
    do_read_memory()
    do_move_via_S1("MBR","A")
    ALU_operation("OP_COPY", DO_NOT_SET_FLAG)
    do_move_via_D("C","MAR")
    incPC()
  if (Signal["MAR_to_TEMP"]):
    do_MAR_to_TEMP()
  if (Signal["push_pop"]):
    if(Signal["decSP"]):
      do_decSP()
    do_move_via_S1("SP", "A")
    ALU_operation("OP_COPY", DO_NOT_SET_FLAG)
    do_move_via_D("C", "MAR")
    if (Signal["incSP"]):
      do_incSP()
  if (Signal["read_memory"]):
    do_read_memory()
  if (Signal["read_RF_port_1"]):
    do_read_RF_port1()
  if (Signal["read_RF_port_2"]):
    do_read_RF_port2()
  if (Signal["move_via_S1"]):
    do_move_via_S1(Signal["src_of_S1"],Signal["dst_of_S1"])
  if (Signal["move_via_S2"]):
    do_move_via_S1(Signal["src_of_S2"],Signal["dst_of_S2"])
  if (Signal["doalu"]):
    ALU_operation(Signal["ALU_func"],SET_FLAG)
  if (Signal["move_via_D"]):
    do_move_via_D(Signal["src_of_D"], Signal["dst_of_D"])
  if (Signal["write_RF"]):
    do_write_RF()
  if (Signal["write_memory"]):
    do_write_memory()
  if (Signal["TEMP_to_MAR"]):
    do_TEMP_to_MAR()
  if (Signal["branch"]): 
    condition_code = Register["IR"]//65536%256
    if (condition_code == 0):  #unconditional branch
      branch_taken = 1
    elif (condition_code == 1): #branch if zero
      branch_taken = Register["ZERO_FLAG"]
    elif (condition_code == 2): #branch if not zero
      branch_taken = not Register["ZERO_FLAG"]
    if (branch_taken):
      do_move_via_S1("MAR", "A")
      ALU_operation("OP_COPY", DO_NOT_SET_FLAG)
      do_move_via_D("C","PC")

def read_program(fn):
  global nword
  i = 0
#  f = open(fn, "r")
  try:
    with open(fn, "r") as f:
      for x in f:
        mem[i] = int(x,16)
        i = i + 1
      nword=i
  except IOError:
    eprint("Cannot read file ", fn)
    exit()

def dump_memory():
  eprint("Content of Memory:")
  for x in range(0,nword):
    eprint(puthex(mem[x]))

def dump_register(n):
  eprint("Content of the first ", n, " registers:")
  for x in range(0,n):
    eprint(puthex(RF[x]))

def disassemble():
  addr = mem[Register["PC"]//4]
  IR = Register["IR"]
  op = IR//16777216
  s1 = (IR//65536)%256
  s2 = (IR%65536)//256
  d = IR%256
  if (op < 6): #ALU operations
    if ((op!=2) and (op!=5)):
      eprint(opcode[op], " R", s1, ", R", s2, ", R", d)
    else:
      eprint(opcode[op], " R", s1, ", R", d)
  elif (op == 11): # pop
    eprint(opcode[op], " R", d)
  elif (op == 6) : # ld
    eprint(opcode[op], puthex(addr), ", R", d)
  elif (op == 10): # push
    eprint(opcode[op], " R", s1)
  elif (op == 7): #st
    eprint(opcode[op], " R", s1, ", ", puthex(addr))
  elif (op == 8): #br
    condition_code = (IR//65536)%256
    if (condition_code==0):
      opcodebr="BR"
    elif (condition_code==1):
      opcodebr="BZ"
    else:
      opcodebr="BNZ"
    eprint(opcodebr, puthex(addr))
  elif (op == 12): #call
    eprint(opcode[op], puthex(addr))
  else:
    eprint(opcode[op])

def usage():
  eprint("Usage: python3 ./prog1.py progname OR python3 ./prog1.py -d progname")

def main():
  global debug
  debug = 0
  argc = len(sys.argv)
  if (argc == 1):
    usage()
    exit()
  if (sys.argv[1][0]=='-'):
    if (argc == 2):
      usage()
      exit()
    filename=sys.argv[2]
    if (sys.argv[1][1]=='d'):
      debug = 1
    else:
      usage()
      exit()
  else:
    debug = 0
    filename=sys.argv[1] 
  init()
  read_program(filename)
  dump_memory()
  reset()
  while(not Signal["dohalt"]):
    if (debug):
      eprint ("Executing PC at ", puthex(Register["PC"]))
    fetch()
    decode()
    if (debug):
      eprint("IR = ", puthex(Register["IR"]))
      disassemble()
    execute()
    if (debug):
      dump_register(14)
      input("Press Enter to Continue")
  eprint("Final Result:")
  dump_register(14)
  dump_memory()
main()
