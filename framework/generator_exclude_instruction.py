

def csr_exclude(csr_program,exclude_instructions): # This function exclude the instruction from riscv I extension (control & status register).
	status_csr=0
	for z in exclude_instructions: # Considering the user's request to exclude the specific CSR instruction, this involves excluding the particular CSR instruction provided by the user in the configuration file.
					
		if (z=="csrrw" and csr_program[19:22]=="001" and csr_program[27:34]=="1110011"):
			status_csr=1
		if (z=="csrrs" and csr_program[19:22]=="010" and csr_program[27:34]=="1110011"):
			status_csr=1
		if (z=="csrrc" and csr_program[19:22]=="011" and csr_program[27:34]=="1110011"):
			status_csr=1
		if (z=="csrrwi" and csr_program[19:22]=="101" and csr_program[27:34]=="1110011"):
			status_csr=1
		if (z=="csrrsi" and csr_program[19:22]=="110" and csr_program[27:34]=="1110011"):
			status_csr=1
		if (z=="csrrci" and csr_program[19:22]=="111" and csr_program[27:34]=="1110011"):
			status_csr=1
	
	return status_csr
	
	
def rv32imf_exclude(instruct_generated,exclude_instructions): # This function exclude the instruction from riscv instruction set architecture (rv32imf).
	status=0
	for y in exclude_instructions: # Considering the user's request to exclude the specific instruction, this involves excluding the particular instruction provided by the user in the configuration file.
					
		if (y=="auipc" and instruct_generated[27:34]=="0010111"):
			status=1
		if (y=="lb" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0000011"):
			status=1
		if (y=="lh" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0000011"):
			status=1
		if (y=="lw" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0000011"):
			status=1
		if (y=="lbu" and instruct_generated[19:22]=="100" and instruct_generated[27:34]=="0000011"):
			status=1
		if (y=="lhu" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0000011"):
			status=1
		if (y=="sb" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0100011"):
			status=1
		if (y=="sh" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0100011"):
			status=1
		if (y=="sw" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0100011"):
			status=1
		if (y=="slti" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0010011"):
			status=1
		if (y=="sltiu" and instruct_generated[19:22]=="011" and instruct_generated[27:34]=="0010011"):
			status=1
		if (y=="xori" and instruct_generated[19:22]=="100" and instruct_generated[27:34]=="0010011"):
			status=1
		if (y=="ori" and instruct_generated[19:22]=="110" and instruct_generated[27:34]=="0010011"):
			status=1
		if (y=="andi" and instruct_generated[19:22]=="111" and instruct_generated[27:34]=="0010011"):
			status=1
		if (y=="slli" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0010011"):
			status=1
		if (y=="srli" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0010011" and instruct_generated[2:9]=="0000000"):
			status=1
		if (y=="srai" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0010011" and instruct_generated[2:9]=="0100000"):
			status=1
		if (y=="add" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000000"):
			status=1
		if (y=="sub" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0100000"):
			status=1
		if (y=="sll" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0110011"):
			status=1
		if (y=="slt" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0110011"):
			status=1
		if (y=="sltu" and instruct_generated[19:22]=="011" and instruct_generated[27:34]=="0110011"):
			status=1
		if (y=="xor" and instruct_generated[19:22]=="100" and instruct_generated[27:34]=="0110011"):
			status=1
		if (y=="srl" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000000"):
			status=1
		if (y=="sra" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0100000"):
			status=1
		if (y=="or" and instruct_generated[19:22]=="110" and instruct_generated[27:34]=="0110011"):
			status=1
		if (y=="and" and instruct_generated[19:22]=="111" and instruct_generated[27:34]=="0110011"):
			status=1
		if (y=="mul" and instruct_generated[19:22]=="000" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
			status = 1
		if (y=="mulh" and instruct_generated[19:22]=="001" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
			status = 1
		if (y=="mulhsu" and instruct_generated[19:22]=="010" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
			status = 1
		if (y=="mulhu" and instruct_generated[19:22]=="011" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
			status = 1
		if (y=="div" and instruct_generated[19:22]=="100" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
			status = 1
		if (y=="divu" and instruct_generated[19:22]=="101" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
			status = 1
		if (y=="rem" and instruct_generated[19:22]=="110" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
			status = 1
		if (y=="remu" and instruct_generated[19:22]=="111" and instruct_generated[27:34]=="0110011" and instruct_generated[2:9]=="0000001"):
			status = 1
			
	return status
