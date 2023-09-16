import random

def csrtest(excluded_csr,implemented_csr,extension,privileged_mode): # This function is responsible to generate the CSR instructions
	
	csr_num=[]
	if len(privileged_mode)==0: # # If user dont want privileged mode than this if will get execute
		excluded_csr_names=["minstret", "mhpmcounter3", "mhpmcounter4", "mhpmcounter5", "mhpmcounter6", "mcycleh", "minstreth", "mhpmcounter3h", "mhpmcounter4h", "mhpmcounter5h", "mhpmcounter6h", "mstatus", "mie", "mtvec", "mcountinhibit", "mhpmevent3", "mhpmevent4", "mhpmevent5", "mhpmevent6", "mscratch", "mepc", "mcause", "mtval", "mip", "tselect", "tdata1", "tdata2", "mcycle", "misa", "mvendorid","marchid", "mimpid", "mhartid"] # The list contains all the names of CSR number wich generator provides
		
		implemented_csr_names= ['hgeie', 'mcounteren', 'micect', 'mrac', 'mcpc', 'mpmc', 'mfdht', 'mfdhs', 'mitcnt0', 'mitb0', 'mitctl0', 'mitcnt1', 'mitb1', 'mitctl1', 'miccmect', 'mdccmect', 'mcgc', 'mfdc', 'mscause', 'mdeau', 'meivt', 'meipt', 'meicpct', 'meicidpl', 'meicurpl', 'mdseac', 'meihap', 'cycle', 'cycleh', 'hcontext', 'hcounteren', 'hedeleg', 'henvcfg', 'henvcfgh', 'hgatp', 'hgeip', 'hideleg', 'hie', 'hip', 'hpmcounter10', 'hpmcounter10h', 'hpmcounter11', 'hpmcounter11h', 'hpmcounter12', 'hpmcounter12h', 'hpmcounter13', 'hpmcounter13h', 'hpmcounter14', 'hpmcounter14h', 'hpmcounter15', 'hpmcounter15h', 'hpmcounter16','hpmcounter16h', 'hpmcounter17', 'hpmcounter17h', 'hpmcounter18', 'hpmcounter18h', 'hpmcounter19', 'hpmcounter19h', 'hpmcounter20', 'hpmcounter20h', 'hpmcounter21', 'hpmcounter21h', 'hpmcounter22', 'hpmcounter22h', 'hpmcounter23', 'hpmcounter23h', 'hpmcounter24', 'hpmcounter24h', 'hpmcounter25', 'hpmcounter25h', 'hpmcounter26', 'hpmcounter26h', 'hpmcounter27', 'hpmcounter27h', 'hpmcounter28', 'hpmcounter28h', 'hpmcounter29', 'hpmcounter29h', 'hpmcounter3', 'hpmcounter30', 'hpmcounter30h', 'hpmcounter31', 'hpmcounter31h', 'hpmcounter3h', 'hpmcounter4', 'hpmcounter4h', 'hpmcounter5', 'hpmcounter5h', 'hpmcounter6', 'hpmcounter6h', 'hpmcounter7', 'hpmcounter7h', 'hpmcounter8', 'hpmcounter8h', 'hpmcounter9', 'hpmcounter9h', 'hstatus', 'htimedelta', 'htimedeltah', 'htinst', 'htval', 'hvip','instret', 'instreth', 'mbase', 'mbound', 'mdbase', 'mdbound', 'medeleg', 'menvcfg', 'menvcfgh', 'mhpmcounter10', 'mhpmcounter10h', 'mhpmcounter11', 'mhpmcounter11h', 'mhpmcounter12', 'mhpmcounter12h', 'mhpmcounter13', 'mhpmcounter13h', 'mhpmcounter14', 'mhpmcounter14h', 'mhpmcounter15', 'mhpmcounter15h', 'mhpmcounter16', 'mhpmcounter16h', 'mhpmcounter17', 'mhpmcounter17h', 'mhpmcounter18', 'mhpmcounter18h', 'mhpmcounter19', 'mhpmcounter19h', 'mhpmcounter20', 'mhpmcounter20h', 'mhpmcounter21', 'mhpmcounter21h', 'mhpmcounter22', 'mhpmcounter22h', 'mhpmcounter23', 'mhpmcounter23h', 'mhpmcounter24', 'mhpmcounter24h', 'mhpmcounter25', 'mhpmcounter25h', 'mhpmcounter26', 'mhpmcounter26h', 'mhpmcounter27', 'mhpmcounter27h', 'mhpmcounter28', 'mhpmcounter28h', 'mhpmcounter29', 'mhpmcounter29h', 'mhpmcounter30', 'mhpmcounter30h', 'mhpmcounter31', 'mhpmcounter31h', 'mhpmcounter7', 'mhpmcounter7h', 'mhpmcounter8', 'mhpmcounter8h', 'mhpmcounter9', 'mhpmcounter9h', 'mhpmevent10',"mhpmevent11", "mhpmevent12", "mhpmevent13", "mhpmevent14", "mhpmevent15", "mhpmevent16", "mhpmevent17", "mhpmevent18", "mhpmevent19", "mhpmevent20", "mhpmevent21", "mhpmevent22", "mhpmevent23", "mhpmevent24", "mhpmevent25", "mhpmevent26", "mhpmevent27", "mhpmevent28", "mhpmevent29", "mhpmevent30", "mhpmevent31", "mhpmevent7", "mhpmevent8", "mhpmevent9",'mibase', 'mibound', 'mideleg', 'mintstatus', 'mnxti', 'mscratchcsw', 'mscratchcswl', 'mseccfg', 'mseccfgh', 'mstatush', 'mtinst', 'mtval2', 'mtvt', 'pmpaddr0', 'pmpaddr1', 'pmpaddr10', 'pmpaddr11', 'pmpaddr12', 'pmpaddr13', 'pmpaddr14', 'pmpaddr15', 'pmpaddr2', 'pmpaddr3', 'pmpaddr4', 'pmpaddr5', 'pmpaddr6', 'pmpaddr63', 'pmpaddr7', 'pmpaddr8', 'pmpaddr9', 'pmpcfg0', 'pmpcfg1', 'pmpcfg14', 'pmpcfg15', 'pmpcfg2', 'pmpcfg3', 'satp', 'scause', 'scontext', 'scounteren', 'sedeleg', 'senvcfg', 'sepc', 'sideleg', 'sie', 'sintstatus', 'sip', 'snxti', 'sscratch', 'sscratchcsw', 'sscratchcswl', 'sstatus', 'stval', 'stvec', 'stvt', 'tdata3', 'time', 'timeh', 'ucause', 'uepc', 'uie', 'uintstatus', 'uip', 'unxti', 'uscratch', 'uscratchcsw', 'uscratchcswl', 'ustatus', 'utval', 'utvec', 'utvt', 'vl', 'vsatp', 'vscause', 'vsepc', 'vsie', 'vsip', 'vsscratch', 'vsstatus', 'vstart', 'vstval', 'vstvec', 'vtype', 'vxrm', 'vxsat'] # The list includes the names of all CSR numbers that the generator provides in case the user requests any of them		
		
		if len(implemented_csr)!=0: # Checking if the provided CSR number to include in CSR instruction is supported by the generator or not
			matched = False
			for x in implemented_csr:
				if x in implemented_csr_names:
					matched = True
					break
			if matched:
				pass
			else:
				raise AssertionError('The given csr number name is not supported by the generator(***Generator***)')
		else:
			pass
			
		if len(excluded_csr)!=0: # Checking if the provided CSR number to exclude from CSR instruction is supported by the generator or not
			matched = False
			for x in excluded_csr:
				if x in excluded_csr_names:
					matched = True
					break
			if matched:
				pass
			else:
				raise AssertionError('The given csr number name is not supported by the generator(***Generator***)')
		else:
			pass
			
		opcode_csr=bin(115)[2:].zfill(7)
		RD_csr=random.randint(0,31)
		while (RD_csr == 2):
			RD_csr = random.randint(0, 31)
		csr_list=[0xb02,0xb03,0xb04,0xb05,0xb06,0xb80,0xb82,0xb83,0xb84,0xb85,0xb86,0x300,0x304,0x305,0x320,0x323,0x324,0x325,0x326,0x340,0x341,0x342,0x343,0x344,0x7a0,0x7a1,0x7a2,0xb00,0x301,0xf11,0xf12,0xf13,0xf14] #This list contains the CSR number in hex
		
		for x in extension:	
			if (x=='RV32F'): #Appending floating CSR numbers if user add F-extension in the configuration file
				csr_list.append(0x001) #fflags
				csr_list.append(0x002) #frm
				csr_list.append(0x003) #fcsr
				
				for x in excluded_csr: # Excluding the floating CSR number if the user want to exclude some of them after adding F-extension in the configuration file

					if x=="fflags":
						csr_list.remove(0x001)
					if x=="frm":
						csr_list.remove(0x002)
					if x=="fcsr":
						csr_list.remove(0x003)
				
		for x in excluded_csr: # Excluding the CSR numbers which generator supports if the user ask for it in the configuration file
			if x=="minstret":
				csr_list.remove(0xb02)
			if x=="mhpmcounter3":
				csr_list.remove(0xb03)
			if x=="mhpmcounter4":
				csr_list.remove(0xb04)
			if x=="mhpmcounter5":
				csr_list.remove(0xb05)
			if x=="mhpmcounter6":
				csr_list.remove(0xb06)
			if x=="mcycleh":
				csr_list.remove(0xb80)
			if x=="minstreth":
				csr_list.remove(0xb82)
			if x=="mhpmcounter3h":
				csr_list.remove(0xb83)
			if x=="mhpmcounter4h":
				csr_list.remove(0xb84)
			if x=="mhpmcounter5h":
				csr_list.remove(0xb85)
			if x=="mhpmcounter6h":
				csr_list.remove(0xb86)
			if x=="mstatus":
				csr_list.remove(0x300)
			if x=="mie":
				csr_list.remove(0x304)
			if x=="mtvec":
				csr_list.remove(0x305)
			if x=="mcountinhibit":
				csr_list.remove(0x320)
			if x=="mhpmevent3":
				csr_list.remove(0x323)
			if x=="mhpmevent4":
				csr_list.remove(0x324)
			if x=="mhpmevent5":
				csr_list.remove(0x325)
			if x=="mhpmevent6":
				csr_list.remove(0x326)
			if x=="mscratch":
				csr_list.remove(0x340)
			if x=="mepc":
				csr_list.remove(0x341)
			if x=="mcause":
				csr_list.remove(0x342)
			if x=="mtval":
				csr_list.remove(0x343)
			if x=="mip":
				csr_list.remove(0x344)
			if x=="tselect":
				csr_list.remove(0x7a0)
			if x=="tdata1" or x=="mcontrol":
				csr_list.remove(0x7a1)
			if x=="tdata2":
				csr_list.remove(0x7a2)
			if x=="mcycle":
				csr_list.remove(0xb00)
			if x=="misa":
				csr_list.remove(0x301)
			if x=="mvendorid":
				csr_list.remove(0xf11)
			if x=="marchid":
				csr_list.remove(0xf12)
			if x=="mimpid":
				csr_list.remove(0xf13)
			if x=="mhartid":
				csr_list.remove(0xf14)	
		
		for x in implemented_csr: # Including the non standard CSR number if the user ask for it in the configuration file
			if x=="hgeie":
				csr_list.append(0x607)
			if x=="mcounteren":
				csr_list.append(0x306)
			if x=="micect":
				csr_list.append(0x7f0)
			if x=="mrac":
				csr_list.append(0x7c0)
			if x=="mcpc":
				csr_list.append(0x7c2)
			if x=="mpmc":
				csr_list.append(0x7c6)
			if x=="mfdht":
				csr_list.append(0x7ce)
			if x=="mfdhs":
				csr_list.append(0x7cf)
			if x=="mitcnt0":
				csr_list.append(0x7d2)
			if x=="mitb0":
				csr_list.append(0x7d3)
			if x=="mitctl0":
				csr_list.append(0x7d4)
			if x=="mitcnt1":
				csr_list.append(0x7d5)
			if x=="mitb1":
				csr_list.append(0x7d6)
			if x=="mitctl1":
				csr_list.append(0x7d7)
			if x=="miccmect":
				csr_list.append(0x7f1)
			if x=="mdccmect":
				csr_list.append(0x7f2)
			if x=="mcgc":
				csr_list.append(0x7f8)
			if x=="mfdc":
				csr_list.append(0x7f9)
			if x=="mscause":
				csr_list.append(0x7ff)
			if x=="mdeau":
				csr_list.append(0xbc0)
			if x=="meivt":
				csr_list.append(0xbc8)
			if x=="meipt":
				csr_list.append(0xbc9)
			if x=="meicpct":
				csr_list.append(0xbca)
			if x=="meicidpl":
				csr_list.append(0xbcb)
			if x=="meicurpl":
				csr_list.append(0xbcc)
			if x=="mdseac":
				csr_list.append(0xfc0)
			if x=="meihap":
				csr_list.append(0xfc8)
			if x=="cycle":
				csr_list.append(0xc00)
			if x=="cycleh":
				csr_list.append(0xc80)
			if x=="hcontext":
				csr_list.append(0x6a8)
			if x=="hcounteren":
				csr_list.append(0x606)
			if x=="hedeleg":
				csr_list.append(0x602)
			if x=="henvcfg":
				csr_list.append(0x60a)
			if x=="henvcfgh":
				csr_list.append(0x61a)
			if x=="hgatp":
				csr_list.append(0x680)
			if x=="hgeip":
				csr_list.append(0xe12)
			if x=="hideleg":
				csr_list.append(0x603)
			if x=="hie":
				csr_list.append(0x604)
			if x=="hip":
				csr_list.append(0x644)
			if x=="hpmcounter10":
				csr_list.append(0xc0a)
			if x=="hpmcounter10h":
				csr_list.append(0xc8a)
			if x=="hpmcounter11":
				csr_list.append(0xc0b)
			if x=="hpmcounter11h":
				csr_list.append(0xc8b)
			if x=="hpmcounter12":
				csr_list.append(0xc0c)
			if x=="hpmcounter12h":
				csr_list.append(0xc8c)
			if x=="hpmcounter13":
				csr_list.append(0xc0d)
			if x=="hpmcounter13h":
				csr_list.append(0xc8d)
			if x=="hpmcounter14":
				csr_list.append(0xc0e)
			if x=="hpmcounter14h":
				csr_list.append(0xc8e)
			if x=="hpmcounter15":
				csr_list.append(0xc0f)
			if x=="hpmcounter15h":
				csr_list.append(0xc8f)
			if x=="hpmcounter16":
				csr_list.append(0xc10)
			if x=="hpmcounter16h":
				csr_list.append(0xc90)
			if x=="hpmcounter17":
				csr_list.append(0xc11)
			if x=="hpmcounter17h":
				csr_list.append(0xc91)
			if x=="hpmcounter18":
				csr_list.append(0xc12)
			if x=="hpmcounter18h":
				csr_list.append(0xc92)
			if x=="hpmcounter19":
				csr_list.append(0xc13)
			if x=="hpmcounter19h":
				csr_list.append(0xc93)
			if x=="hpmcounter20":
				csr_list.append(0xc14)
			if x=="hpmcounter20h":
				csr_list.append(0xc94)
			if x=="hpmcounter21":
				csr_list.append(0xc15)
			if x=="hpmcounter21h":
				csr_list.append(0xc95)
			if x=="hpmcounter22":
				csr_list.append(0xc16)
			if x=="hpmcounter22h":
				csr_list.append(0xc96)
			if x=="hpmcounter23":
				csr_list.append(0xc17)
			if x=="hpmcounter23h":
				csr_list.append(0xc97)
			if x=="hpmcounter24":
				csr_list.append(0xc18)
			if x=="hpmcounter24h":
				csr_list.append(0xc98)
			if x=="hpmcounter25":
				csr_list.append(0xc19)
			if x=="hpmcounter25h":
				csr_list.append(0xc99)
			if x=="hpmcounter26":
				csr_list.append(0xc1a)
			if x=="hpmcounter26h":
				csr_list.append(0xc9a)
			if x=="hpmcounter27":
				csr_list.append(0xc1b)
			if x=="hpmcounter27h":
				csr_list.append(0xc9b)
			if x=="hpmcounter28":
				csr_list.append(0xc1c)
			if x=="hpmcounter28h":
				csr_list.append(0xc9c)
			if x=="hpmcounter29":
				csr_list.append(0xc1d)
			if x=="hpmcounter29h":
				csr_list.append(0xc9d)
			if x=="hpmcounter3":
				csr_list.append(0xc03)
			if x=="hpmcounter30":
				csr_list.append(0xc1e)
			if x=="hpmcounter30h":
				csr_list.append(0xc9e)
			if x=="hpmcounter31":
				csr_list.append(0xc1f)
			if x=="hpmcounter31h":
				csr_list.append(0xc9f)
			if x=="hpmcounter3h":
				csr_list.append(0xc83)
			if x=="hpmcounter4":
				csr_list.append(0xc04)
			if x=="hpmcounter4h":
				csr_list.append(0xc84)
			if x=="hpmcounter5":
				csr_list.append(0xc05)
			if x=="hpmcounter5h":
				csr_list.append(0xc85)
			if x=="hpmcounter6":
				csr_list.append(0xc06)
			if x=="hpmcounter6h":
				csr_list.append(0xc86)
			if x=="hpmcounter7":
				csr_list.append(0xc07)
			if x=="hpmcounter7h":
				csr_list.append(0xc87)
			if x=="hpmcounter8":
				csr_list.append(0xc08)
			if x=="hpmcounter8h":
				csr_list.append(0xc88)
			if x=="hpmcounter9":
				csr_list.append(0xc09)
			if x=="hpmcounter9h":
				csr_list.append(0xc89)
			if x=="hstatus":
				csr_list.append(0x600)
			if x=="htimedelta":
				csr_list.append(0x605)
			if x=="htimedeltah":
				csr_list.append(0x615)
			if x=="htinst":
				csr_list.append(0x64a)
			if x=="htval":
				csr_list.append(0x643)
			if x=="hvip":
				csr_list.append(0x645)
			if x=="instret":
				csr_list.append(0xc02)
			if x=="instreth":
				csr_list.append(0xc82)
			if x=="mbase":
				csr_list.append(0x380)
			if x=="mbound":
				csr_list.append(0x381)
			if x=="mdbase":
				csr_list.append(0x384)
			if x=="mdbound":
				csr_list.append(0x385)
			if x=="medeleg":
				csr_list.append(0x302)
			if x=="menvcfg":
				csr_list.append(0x30a)
			if x=="menvcfgh":
				csr_list.append(0x31a)
			if x=="mhpmcounter10":
				csr_list.append(0xb0a)
			if x=="mhpmcounter10h":
				csr_list.append(0xb8a)
			if x=="mhpmcounter11":
				csr_list.append(0xb0b)
			if x=="mhpmcounter11h":
				csr_list.append(0xc93)
			if x=="mhpmcounter12":
				csr_list.append(0xb0c)
			if x=="mhpmcounter12h":
				csr_list.append(0xb8c)
			if x=="mhpmcounter13":
				csr_list.append(0xb0d)
			if x=="mhpmcounter13h":
				csr_list.append(0xb8d)
			if x=="mhpmcounter14":
				csr_list.append(0xb0e)
			if x=="mhpmcounter14h":
				csr_list.append(0xb8e)
			if x=="mhpmcounter15":
				csr_list.append(0xb0f)
			if x=="mhpmcounter15h":
				csr_list.append(0xb8f)
			if x=="mhpmcounter16":
				csr_list.append(0xb10)
			if x=="mhpmcounter16h":
				csr_list.append(0xb90)
			if x=="mhpmcounter17":
				csr_list.append(0xb11)
			if x=="mhpmcounter17h":
				csr_list.append(0xb91)
			if x=="mhpmcounter18":
				csr_list.append(0xb12)
			if x=="mhpmcounter18h":
				csr_list.append(0xb92)
			if x=="mhpmcounter19":
				csr_list.append(0xb13)
			if x=="mhpmcounter19h":
				csr_list.append(0xb93)
			if x=="mhpmcounter20":
				csr_list.append(0xb14)
			if x=="mhpmcounter20h":
				csr_list.append(0xb94)
			if x=="mhpmcounter21":
				csr_list.append(0xb15)
			if x=="mhpmcounter21h":
				csr_list.append(0xb95)
			if x=="mhpmcounter22":
				csr_list.append(0xb16)
			if x=="mhpmcounter22h":
				csr_list.append(0xb96)
			if x=="mhpmcounter23":
				csr_list.append(0xb17)
			if x=="mhpmcounter23h":
				csr_list.append(0xb97)
			if x=="mhpmcounter24":
				csr_list.append(0xb18)
			if x=="mhpmcounter24h":
				csr_list.append(0xb98)
			if x=="mhpmcounter25":
				csr_list.append(0xb19)
			if x=="mhpmcounter25h":
				csr_list.append(0xb99)
			if x=="mhpmcounter26":
				csr_list.append(0xb1a)
			if x=="mhpmcounter26h":
				csr_list.append(0xb9a)
			if x=="mhpmcounter27":
				csr_list.append(0xb1b)
			if x=="mhpmcounter27h":
				csr_list.append(0xb9b)
			if x=="mhpmcounter28":
				csr_list.append(0xb1c)
			if x=="mhpmcounter28h":
				csr_list.append(0xb9c)
			if x=="mhpmcounter29":
				csr_list.append(0xb1d)
			if x=="mhpmcounter29h":
				csr_list.append(0xb9d)
			if x=="mhpmcounter30":
				csr_list.append(0xb1e)
			if x=="mhpmcounter30h":
				csr_list.append(0xb9e)
			if x=="mhpmcounter31":
				csr_list.append(0xb1f)
			if x=="mhpmcounter31h":
				csr_list.append(0xb9f)
			if x=="mhpmcounter7":
				csr_list.append(0xb07)
			if x=="mhpmcounter7h":
				csr_list.append(0xb87)
			if x=="mhpmcounter8":
				csr_list.append(0xb08)
			if x=="mhpmcounter8h":
				csr_list.append(0xb88)
			if x=="mhpmcounter9":
				csr_list.append(0xb09)
			if x=="mhpmcounter9h":
				csr_list.append(0xb89)
			if x=="mhpmevent10":
				csr_list.append(0x32a)
			if x=="mhpmevent11":
				csr_list.append(0x32b)
			if x=="mhpmevent12":
				csr_list.append(0x32c)
			if x=="mhpmevent13":
				csr_list.append(0x32d)
			if x=="mhpmevent14":
				csr_list.append(0x32e)
			if x=="mhpmevent15":
				csr_list.append(0x32f)
			if x=="mhpmevent16":
				csr_list.append(0x330)
			if x=="mhpmevent17":
				csr_list.append(0x331)
			if x=="mhpmevent18":
				csr_list.append(0x332)
			if x=="mhpmevent19":
				csr_list.append(0x333)
			if x=="mhpmevent20":
				csr_list.append(0x334)
			if x=="mhpmevent21":
				csr_list.append(0x335)
			if x=="mhpmevent22":
				csr_list.append(0x336)
			if x=="mhpmevent23":
				csr_list.append(0x337)
			if x=="mhpmevent24":
				csr_list.append(0x338)
			if x=="mhpmevent25":
				csr_list.append(0x339)
			if x=="mhpmevent26":
				csr_list.append(0x33a)
			if x=="mhpmevent27":
				csr_list.append(0x33b)
			if x=="mhpmevent28":
				csr_list.append(0x33c)
			if x=="mhpmevent29":
				csr_list.append(0x33d)
			if x=="mhpmevent30":
				csr_list.append(0x33e)
			if x=="mhpmevent31":
				csr_list.append(0x33f)
			if x=="mhpmevent7":
				csr_list.append(0x327)
			if x=="mhpmevent8":
				csr_list.append(0x328)
			if x=="mhpmevent9":
				csr_list.append(0x329)
			if x=="mibase":
				csr_list.append(0x382)
			if x=="mibound":
				csr_list.append(0x383)
			if x=="mideleg":
				csr_list.append(0x303)
			if x=="mintstatus":
				csr_list.append(0x346)
			if x=="mnxti":
				csr_list.append(0x345)
			if x=="mscratchcsw":
				csr_list.append(0x348)
			if x=="mscratchcswl":
				csr_list.append(0x349)
			if x=="mseccfg":
				csr_list.append(0x747)
			if x=="mseccfgh":
				csr_list.append(0x757)
			if x=="mstatush":
				csr_list.append(0x310)
			if x=="mtinst":
				csr_list.append(0x34a)
			if x=="mtval2":
				csr_list.append(0x34b)
			if x=="mtvt":
				csr_list.append(0x307)
			if x=="pmpaddr0":
				csr_list.append(0x3b0)
			if x=="pmpaddr1":
				csr_list.append(0x3b1)
			if x=="pmpaddr10":
				csr_list.append(0x3ba)
			if x=="pmpaddr11":
				csr_list.append(0x3bb)
			if x=="pmpaddr12":
				csr_list.append(0x3bc)
			if x=="pmpaddr13":
				csr_list.append(0x3bd)
			if x=="pmpaddr14":
				csr_list.append(0x3be)
			if x=="pmpaddr15":
				csr_list.append(0x3bf)
			if x=="pmpaddr2":
				csr_list.append(0x3b2)
			if x=="pmpaddr3":
				csr_list.append(0x3b3)
			if x=="pmpaddr4":
				csr_list.append(0x3b4)
			if x=="pmpaddr5":
				csr_list.append(0x3b5)
			if x=="pmpaddr6":
				csr_list.append(0x3b6)
			if x=="pmpaddr63":
				csr_list.append(0x3ef)
			if x=="pmpaddr7":
				csr_list.append(0x3b7)
			if x=="pmpaddr8":
				csr_list.append(0x3b8)
			if x=="pmpaddr9":
				csr_list.append(0x3b9)
			if x=="pmpcfg0":
				csr_list.append(0x3a0)
			if x=="pmpcfg1":
				csr_list.append(0x3a1)
			if x=="pmpcfg14":
				csr_list.append(0x3ae)
			if x=="pmpcfg15":
				csr_list.append(0x3af)
			if x=="pmpcfg2":
				csr_list.append(0x3a2)
			if x=="pmpcfg3":
				csr_list.append(0x3a3)
			if x=="satp":
				csr_list.append(0x180)
			if x=="scause":
				csr_list.append(0x142)
			if x=="scontext":
				csr_list.append(0x5a8)
			if x=="scounteren":
				csr_list.append(0x106)
			if x=="sedeleg":
				csr_list.append(0x102)
			if x=="senvcfg":
				csr_list.append(0x10a)
			if x=="sepc":
				csr_list.append(0x141)
			if x=="sideleg":
				csr_list.append(0x103)
			if x=="sie":
				csr_list.append(0x104)
			if x=="sintstatus":
				csr_list.append(0x146)
			if x=="sip":
				csr_list.append(0x144)
			if x=="snxti":
				csr_list.append(0x145)
			if x=="sscratch":
				csr_list.append(0x140)
			if x=="sscratchcsw":
				csr_list.append(0x148)
			if x=="sscratchcswl":
				csr_list.append(0x149)
			if x=="sstatus":
				csr_list.append(0x100)
			if x=="stval":
				csr_list.append(0x143)
			if x=="stvec":
				csr_list.append(0x105)
			if x=="stvt":
				csr_list.append(0x107)
			if x=="tdata3":
				csr_list.append(0x7a3)
			if x=="time":
				csr_list.append(0xc01)
			if x=="timeh":
				csr_list.append(0xc81)
			if x=="ucause":
				csr_list.append(0x042)
			if x=="uepc":
				csr_list.append(0x041)
			if x=="uie":
				csr_list.append(0x004)
			if x=="uintstatus":
				csr_list.append(0x046)
			if x=="uip":
				csr_list.append(0x044)
			if x=="unxti":
				csr_list.append(0x045)
			if x=="uscratch":
				csr_list.append(0x040)
			if x=="uscratchcsw":
				csr_list.append(0x048)
			if x=="uscratchcswl":
				csr_list.append(0x049)
			if x=="ustatus":
				csr_list.append(0x000)
			if x=="utval":
				csr_list.append(0x043)
			if x=="utvec":
				csr_list.append(0x005)
			if x=="utvt":
				csr_list.append(0x007)
			if x=="vl":
				csr_list.append(0xc20)
			if x=="vsatp":
				csr_list.append(0x280)
			if x=="vscause":
				csr_list.append(0x242)
			if x=="vsepc":
				csr_list.append(0x241)
			if x=="vsie":
				csr_list.append(0x204)
			if x=="vsip":
				csr_list.append(0x244)
			if x=="vsscratch":
				csr_list.append(0x240)
			if x=="vsstatus":
				csr_list.append(0x200)
			if x=="vstart":
				csr_list.append(0x008)
			if x=="vstval":
				csr_list.append(0x243)
			if x=="vstvec":
				csr_list.append(0x205)
			if x=="vtype":
				csr_list.append(0xc21)
			if x=="vxrm":
				csr_list.append(0x00a)
			if x=="vxsat":
				csr_list.append(0x009)
		
				
		csr=random.choice(csr_list)
		if csr==0xf11 or csr==0xf12 or csr==0xf13 or csr==0xf14 or csr==0xfc8 or csr==0xfc0 or csr==0xc00 or csr==0xf13 or csr==0xe12 or csr==0xc03 or csr==0xc1f or csr==0xc9f or csr==0xc83 or csr==0xc04 or csr==0xc84 or csr==0xc02 or csr==0xc82 or csr==0xf15 or csr==0xc01 or csr==0xc81 or csr==0xc20 or csr==0xc21:
			FUNCT3_csr=random.randint(2,7)
			while (FUNCT3_csr == 4 or FUNCT3_csr == 5):
				FUNCT3_csr = random.randint(2,7)
			rs1_csr=0
			
		else:
			if csr== 0x7c2:
				rs1_csr=0
			else:
				rs1_csr=random.randint(0,31)
			FUNCT3_csr=random.randint(1,7)
			while (FUNCT3_csr == 4):
				FUNCT3_csr = random.randint(2,7)
		
		binary_csr = "0b" + bin(csr)[2:].zfill(12) + bin(rs1_csr)[2:].zfill(5) + bin(FUNCT3_csr)[2:].zfill(3) + bin(RD_csr)[2:].zfill(5) + opcode_csr
		hex_csr="0b"+bin(int(binary_csr,2))[2:].zfill(32)
	
	else: # If user want privileged mode than this else will get execute
		opcode_csr=bin(115)[2:].zfill(7)
		RD_csr=random.randint(0,31)
		while (RD_csr == 2):
			RD_csr = random.randint(0, 31)
		for x in privileged_mode:
			if x=="machine_mode": # If user want machine mode in privilged mode this CSR numbers will be get included in the list
				csr_num.extend([0xb02,0xb03,0xb04,0xb05,0xb06,0xb80,0xb82,0xb83,0xb84,0xb85,0xb86,0x300,0x304,0x305,0x320,0x323,0x324,0x325,0x326,0x340,0x341,0x342,0x343,0x344,0xb00,0x301,0xf11,0xf12,0xf13,0xf14])
			if x=="user_mode": # If user want user mode in privilged mode this CSR numbers will be get included in the list
				csr_num.extend([0x042, 0x041, 0x004, 0x046, 0x044, 0x045, 0x040, 0x048, 0x049, 0x000, 0x043, 0x005, 0x007])
			if x=="supervisor_mode": # If user want supervisor mode in privilged mode this CSR numbers will be get included in the list
				csr_num.extend([0x180, 0x142, 0x5a8, 0x106, 0x102, 0x10a, 0x141, 0x103, 0x104, 0x146, 0x144, 0x145, 0x140, 0x148, 0x149, 0x100, 0x143, 0x105, 0x107])
			
		csr=random.choice(csr_num)
		if csr==0xf11 or csr==0xf12 or csr==0xf13 or csr==0xf14 or csr==0xfc8 or csr==0xfc0 or csr==0xc00 or csr==0xf13 or csr==0xe12 or csr==0xc03 or csr==0xc1f or csr==0xc9f or csr==0xc83 or csr==0xc04 or csr==0xc84 or csr==0xc02 or csr==0xc82 or csr==0xf15 or csr==0xc01 or csr==0xc81 or csr==0xc20 or csr==0xc21:
			FUNCT3_csr=random.randint(2,7)
			while (FUNCT3_csr == 4 or FUNCT3_csr == 5):
				FUNCT3_csr = random.randint(2,7)
			rs1_csr=0
			
		else:
			if csr== 0x7c2:
				rs1_csr=0
			else:
				rs1_csr=random.randint(0,31)
			FUNCT3_csr=random.randint(1,7)
			while (FUNCT3_csr == 4):
				FUNCT3_csr = random.randint(2,7)
		
		binary_csr = "0b" + bin(csr)[2:].zfill(12) + bin(rs1_csr)[2:].zfill(5) + bin(FUNCT3_csr)[2:].zfill(3) + bin(RD_csr)[2:].zfill(5) + opcode_csr
		hex_csr="0b"+bin(int(binary_csr,2))[2:].zfill(32)
	return hex_csr
