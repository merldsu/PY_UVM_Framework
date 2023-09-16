import random

def get_load(): #This function returns Load instruction

	LISTFUNC3_LD=[0,1,2,4,5]
	OP_RV32=bin(3)[2:].zfill(7)
	FUNCT3=random.choice(LISTFUNC3_LD)
	RS1=bin(2)[2:].zfill(5)
	RD = random.randint(0,31)
	while RD==2:
		RD=random.randint(0,31)
	IMM_LD=random.randrange(0,511,4)
	while (IMM_LD+1073741824>4294967295 | IMM_LD+1073741824<2147483648):
		IMM_LD=random.randrange(0,511,4)
	sign=random.randint(0,1)
	if sign==1:
		binary = bin(IMM_LD)[2:].zfill(12)
		inverted = ''.join('1' if bit == '0' else '0' for bit in binary)
		negative = bin(int(inverted, 2) + 1)[2:]
		if negative=='1000000000000':
			negative_ld=negative.replace('1', '', 1)
		else:
			negative_ld=negative
		binary="0b"+negative_ld+RS1+bin(FUNCT3)[2:].zfill(3)+bin(RD)[2:].zfill(5)+OP_RV32
	else:
		binary="0b"+bin(IMM_LD)[2:].zfill(12)+RS1+bin(FUNCT3)[2:].zfill(3)+bin(RD)[2:].zfill(5)+OP_RV32
	LD="0b"+bin(int(binary,2))[2:].zfill(32)		
	return LD

def get_store(): #This function returns all store instruction

	LISTFUNC3_ST=[0,1,2]
	OP_RV32=bin(35)[2:].zfill(7)
	FUNCT3=random.choice(LISTFUNC3_ST)
	RS1=bin(2)[2:].zfill(5)
	RS2=random.randint(0,31)
	IMM_SW=random.randrange(0,511,4)
	while (IMM_SW+1073741824>4294967295 |IMM_SW+1073741824<2147483648):
		IMM_SW=random.randrange(0,511,4)
	sign=random.randint(0,1)
	if sign==1:
		binary = bin(IMM_SW)[2:].zfill(12)
		inverted = ''.join('1' if bit == '0' else '0' for bit in binary)
		negative = bin(int(inverted, 2) + 1)[2:]
		if negative=='1000000000000':
			negative_st=negative.replace('1', '', 1)
		else:
			negative_st=negative
		IMM1=negative_st[7:]
		IMM2=negative_st[:7]
		binary="0b"+IMM2+bin(RS2)[2:].zfill(5)+RS1+bin(FUNCT3)[2:].zfill(3)+IMM1+OP_RV32
	else:
		binary = bin(IMM_SW)[2:].zfill(12)
		IMM1=binary[7:]
		IMM2=binary[:7]
		binary="0b"+IMM2+bin(RS2)[2:].zfill(5)+RS1+bin(FUNCT3)[2:].zfill(3)+IMM1+OP_RV32
	ST="0b"+bin(int(binary,2))[2:].zfill(32)

	return ST
	
def get_arthimetic(): #This function return all immediate and rtype Instructions

	LIST=[19,51,23,55]
	LISTF7 = [0, 32]
	opcode = random.choice(LIST)
	FUNCT3 = random.randint(0,7)
	RS1 = random.randint(0, 31)
	RS2 = random.randint(0, 31)
	RD = random.randint(0, 31)
	shamt = random.randint(0, 31)
	IMM = random.randrange(0, 511)
	while (RD == 2):
		RD = random.randint(0, 31)
	
	#In case of selection of Immidiate arthemetic instruction	
	if (opcode == 19):
		if(FUNCT3 == 5):
			FUNCT7 = random.choice(LISTF7)
			binary = "0b" + bin(FUNCT7)[2:].zfill(7) + bin(shamt)[2:].zfill(5) + bin(RS1)[2:].zfill(5) + bin(FUNCT3)[2:].zfill(3) + bin(RD)[2:].zfill(5) + bin(opcode)[2:].zfill(7)
		elif(FUNCT3 == 1):
			FUNCT7 = 0
			binary = "0b" + bin(FUNCT7)[2:].zfill(7) + bin(shamt)[2:].zfill(5) + bin(RS1)[2:].zfill(5) + bin(FUNCT3)[2:].zfill(3) + bin(RD)[2:].zfill(5) + bin(opcode)[2:].zfill(7)
		else:
			sign=random.randint(0,1)
			if sign==1:
				binary = bin(IMM)[2:].zfill(12)
				inverted = ''.join('1' if bit == '0' else '0' for bit in binary)
				negative = bin(int(inverted, 2) + 1)[2:]
				negative = bin(int(inverted, 2) + 1)[2:]
				if negative=='1000000000000':
					negative_ar=negative.replace('1', '', 1)
				else:
					negative_ar=negative
				binary = "0b" + negative_ar + bin(RS1)[2:].zfill(5) + bin(FUNCT3)[2:].zfill(3) + bin(RD)[2:].zfill(5) + bin(opcode)[2:].zfill(7)
			else:
				binary = "0b" + bin(IMM)[2:].zfill(12) + bin(RS1)[2:].zfill(5) + bin(FUNCT3)[2:].zfill(3) + bin(RD)[2:].zfill(5) + bin(opcode)[2:].zfill(7)
		ar_hex="0b"+bin(int(binary,2))[2:].zfill(32)
	
	#In case of selection of R-type arthemetic instruction	
	elif opcode==55:
		sign=random.randint(0,1)
		IMM_LUI=random.randint(0,524287)
		if sign==1:
			binary = bin(IMM_LUI)[2:].zfill(20)
			inverted = ''.join('1' if bit == '0' else '0' for bit in binary)
			negative = bin(int(inverted, 2) + 1)[2:]
			if negative=='1000000000000':
				negative_ar=negative.replace('1', '', 1)
			else:
				negative_ar=negative
			binary="0b"+negative_ar+bin(RD)[2:].zfill(5)+bin(opcode)[2:].zfill(7)
		else:
			binary="0b"+bin(IMM_LUI)[2:].zfill(20)+bin(RD)[2:].zfill(5)+bin(opcode)[2:].zfill(7)
		ar_hex="0b"+bin(int(binary,2))[2:].zfill(32)
		
	elif opcode==23:
		sign_auipc=random.randint(0,1)
		IMM_AUIPC=random.randint(0,524287)
		if sign_auipc==1:
			binary = bin(IMM_AUIPC)[2:].zfill(20)
			inverted = ''.join('1' if bit == '0' else '0' for bit in binary)
			negative = bin(int(inverted, 2) + 1)[2:]
			if negative=='1000000000000':
				negative_ar=negative.replace('1', '', 1)
			else:
				negative_ar=negative
			binary="0b"+negative_ar+bin(RD)[2:].zfill(5)+bin(opcode)[2:].zfill(7)
		else:
			binary="0b"+bin(IMM_AUIPC)[2:].zfill(20)+bin(RD)[2:].zfill(5)+bin(opcode)[2:].zfill(7)
		ar_hex="0b"+bin(int(binary,2))[2:].zfill(32)
	else:
		if(FUNCT3 == 0 or FUNCT3 == 5):
			FUNCT7 = random.choice(LISTF7)
		else:
			FUNCT7=0
		
		binary="0b"+bin(FUNCT7)[2:].zfill(7)+bin(RS2)[2:].zfill(5)+bin(RS1)[2:].zfill(5)+bin(FUNCT3)[2:].zfill(3)+bin(RD)[2:].zfill(5)+bin(opcode)[2:].zfill(7)
		ar_hex="0b"+bin(int(binary,2))[2:].zfill(32)
	
	return ar_hex

def fixed_brancheq(num_list): #Fixed Branch Program
	program1=['0x00C000EF','0x00150513','0x00950C63','0x00400493','0x00300513','0xFE9518E3','0x00530313','0x0063C863','0x00300313','0x00700393','0xFE7348E3','0x00900E13']
	program2=["0x00800193","0x00100213","0x00100293","0x404181b3","0xfe304ce3"]
	program3=["0x09000293","0x00000313","0x00100393","0x00638433","0x00038313","0x00040393","0xfe539ae3"]
	program4=['0x00C000EF','0x00150513','0x00950863','0x00400493','0x00300513','0xFE9518E3','0x00300313']
	program5=['0x00000493','0x00000413','0x00A00313','0x00645863','0x008484B3','0x00140413','0xFF5FF06F']
	program6=['0x00000413','0x00000493','0x00A00E13','0x01C40863','0x008484B3','0x00140413','0xFF5FF06F']
	program7=['0x00400413','0x00100493','0x00249493','0x00940663','0x00148493','0x408484B3','0x008484B3']
	program8=['0x00400413','0x00100493','0x00249493','0x00941663','0x00148493','0x408484B3','0x008484B3']
	program9=['0x00000493','0x00000413','0x00A00293','0x0082E863','0x008484B3','0x00140413','0xFF5FF06F']
	program10=['0x000404B3','0x00000533','0x000005B3','0x01400693','0x00B6FC63','0x0004A603','0x00C50533','0x00448493','0x00158593','0xFEDFF06F']
	main_list=[]
	branch_pg=[]
	for i in range(num_list):
		program_choice=random.randint(1,10)
		
		if program_choice==1:
			main_list.extend(program1)
		elif program_choice==2:
			main_list.extend(program2)
		elif program_choice==3:
			main_list.extend(program3)
		elif program_choice==4:
			main_list.extend(program4)
		elif program_choice==5:
			main_list.extend(program5)
		elif program_choice==6:
			main_list.extend(program6)
		elif program_choice==7:
			main_list.extend(program7)
		elif program_choice==8:
			main_list.extend(program8)
		elif program_choice==9:
			main_list.extend(program9)
		else:
			main_list.extend(program10)
			
	for x in range(len(main_list)):
		branch_pg.append("0b"+(bin(int(main_list[x],16))[2:].zfill(32)))
	
	return branch_pg

def M_extension():

	opcode=bin(51)[2:].zfill(7)
	RD=random.randint(0,31)
	while (RD == 2):
		RD = random.randint(0, 31)
	FUNCT3=random.randint(0,7)
	rs1=random.randint(0,31)
	rs2=random.randint(0,31)
	funct7=bin(1)[2:].zfill(7)
	binary = "0b" + funct7 + bin(rs2)[2:].zfill(5) + bin(rs1)[2:].zfill(5) + bin(FUNCT3)[2:].zfill(3) + bin(RD)[2:].zfill(5) + opcode
	hex="0b"+bin(int(binary,2))[2:].zfill(32)
	
	return hex
