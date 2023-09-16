# Copyright 2023 MERL-DSU

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import logging
import os


# Script for reading the Text file..
#if (testname == "riscv_csr_test"):
with open('ISS.txt') as infile, open('Iss.txt','w') as outfile:
  outfile.write(infile.read().replace("+" , ""))

#Here we make list to store the text file coloumns  
list_a = [] # Store Result from ISS
list_b = [] # Store INSTRUCTION from ISS
list_c = [] # Store PC from ISS
list_d = [] # Store INSTRUCTION ASSEMBLY from ISS
list_cr = []
list_x = []


#Here we store the HEX value in list
d1 = [] # Result ISS in HEX
d2 = [] # INSTRUCTION in HEX
d3 = [] # PC in HEX
d4 = [] # INSTRUCTION ASSEMBLY in String
d5 = [] # C_R
d6 = [] # REG NAME


logging.info("Convert HEX file into CSV (ISS_SIM)")  
iss = pd.read_csv('Iss.txt', sep=';', header=None, engine='python')
iss.columns=['Name']
iss = iss.stack().str.replace(' ',',').unstack()
iss = iss.stack().str.replace(':',',').unstack()
iss = iss.stack().str.replace(',,,,,,,,,',',').unstack()
iss = iss.stack().str.replace(',,,,,,',',').unstack()
iss = iss.stack().str.replace(',,,',',').unstack()
iss = iss.stack().str.replace(',,',',').unstack()
iss = iss.stack().str.replace(',,',',').unstack()
iss = iss['Name'].str.split(',', expand=True)
iss = iss.iloc[:,[2,3,4,6,7,8]]




list_a = iss.iloc[:,2]; # C_R
for i in range (len(list_a)):
	c = list_a[i]
	d1.append(c)



list_b = iss.iloc[:,1]; # Instructions
for z in range (len(list_b)):
	c1 = list_b[z]
	d_1 = "0x" + c1
	d2.append(d_1)



list_c = iss.iloc[:,0];
for y in range (len(list_c)): # Program counter
	c2 = list_c[y]
	d_2 = "0x" + c2
	d3.append(d_2)



list_d = iss.iloc[:,3]; # Results
for q in range (len(list_d)):
	c32 = list_d[q]
	h_1 = "0x" + c32
	d4.append(h_1)

	
list_cr = iss.iloc[:,4];
for cr in range (len(list_cr)): # instruction name
	CR = list_cr[cr]
	CR_1 = CR
	d5.append(CR)
	
list_x = iss.iloc[:,5];
for x in range (len(list_x)): # REG name
	X = list_x[x]
	X_1 = X
	d6.append(X_1)


df_A=pd.DataFrame({'PC':d3,'INSTRUCTION':d2,'RESULT_ISS':d4,'INSTR_ASSEMBLY':d5,'C_R':d1,'REG':d6})

for x in range(len(df_A['C_R'])):
	if ((df_A['C_R'][x]) == 'c'):
		df_A.drop([x], inplace=True)
	else:
		pass

df_A = df_A.reset_index(drop=True)

testname = os.getenv("Test","riscv_load_test")

if (testname == 'riscv_csr_test'): 
	for x11 in range(len(df_A['REG'])):
		if ((df_A['REG'][x11])) == 'x0' and ((df_A['C_R'][x11]) == 'r'):
			df_A.drop([x11], inplace=True)
		else:
			pass
	df_A = df_A.reset_index(drop=True)

# Remove unncessary coloumn
filename = 'removed_data.csv'
if os.path.isfile(filename):	
	df_Rem_CSV = pd.read_csv('removed_data.csv')
	df_REM_CSV = df_Rem_CSV['PC'].tolist()
	
	index = 0
	
	while index < len((df_A['PC'])):
		element = (df_A['PC'])[index]
		
		if element in df_REM_CSV:
			df_A.drop([index], inplace=True)
		else:
			index += 1
			
		df_A = df_A.reset_index(drop=True)
else:
	pass

df_A.to_csv('ISS.csv',index=False)


	

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logging.info('Running Conversion of Text file into CSV')
