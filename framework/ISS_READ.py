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


# Script for reading the Text file..

with open('ISS.txt') as infile, open('Iss.txt','w') as outfile:
  outfile.write(infile.read().replace("+" , ""))

#Here we make list to store the text file coloumns  
list_a = [] # Store Result from ISS
list_b = [] # Store INSTRUCTION from ISS
list_c = [] # Store PC from ISS
list_d = [] # Store INSTRUCTION ASSEMBLY from ISS

#Here we store the HEX value in list
d1 = [] # Result ISS in HEX
d2 = [] # INSTRUCTION in HEX
d3 = [] # PC in HEX
d4 = [] # INSTRUCTION ASSEMBLY in String

# The below script is coversion of text file into CSV file
logging.info("Convert HEX file into CSV (ISS_SIM)")  
iss = pd.read_csv('Iss.txt', sep=';', header=None, engine='python')
iss.columns=['Name']
iss = iss.stack().str.replace(',',':').unstack()
iss = iss.stack().str.replace(' ',',').unstack()
iss = iss.stack().str.replace(',,,,,,,,,',',,,').unstack()
iss = iss.stack().str.replace(',,,,,,,,,',',,,,,,,').unstack()
iss = iss['Name'].str.split(',', expand=True)
iss = iss.iloc[:,[2,3,8,10]]



list_a = iss.iloc[:,2];
for i in range (len(list_a)):
	c = list_a[i]
	d = "0x" + c
	d1.append(d)


list_b = iss.iloc[:,1];
for z in range (len(list_b)):
	c1 = list_b[z]
	d_1 = "0x" + c1
	d2.append(d_1)


list_c = iss.iloc[:,0];
for y in range (len(list_c)):
	c2 = list_c[y]
	d_2 = "0x" + c2
	d3.append(d_2)


list_d = iss.iloc[:,3];
for q in range (len(list_d)):
	c32 = list_d[q]
	d4.append(c32)
	



df_A=pd.DataFrame({'PC':d3,'INSTRUCTION':d2,'RESULT_ISS':d1,'INSTR_ASSEMBLY':d4})	
df_A.to_csv('ISS.csv',index=False)	

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logging.info('Running Conversion of Text file into CSV')


