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

import os
import time
from datetime import datetime 

def directory():
	dir_path = 'log/'
	if not os.path.exists(dir_path):
		os.mkdir(dir_path)
	dir_path = f'log/{os.getenv("Test","riscv_random_test")}/'	
		
	# scripting for saving dump file
	now = datetime.now()
	timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
	dir_path = os.path.join(dir_path,timestamp) 
	os.makedirs(dir_path)
	txt_file = os.path.join(dir_path, 'logging.txt')
	return txt_file, dir_path
	
def copy(dir_p):
	a = os.getcwd()
	os.system("cp *.csv "+a+"/"+dir_p)
	
def delete():
	os.remove('./INSTR_RV32.csv')
	os.remove('./DATA_RV32.csv')
	os.remove('./Iss.txt')
	os.remove('./ISS.txt')
	os.remove('./ISS.csv')
	os.remove('./dump.vcd')
	os.remove('./program.hex')
	os.remove('./RESULT_MONITOR.csv')
	os.remove('./Final_Results.csv')
	
def run(test):
	os.system(f"make {test}")
	
def main():
	read_text_file = open("Test.txt","r")
	for x in read_text_file:
		run(x)
		delete()
	read_text_file.close()
	
if __name__ == "__main__":
	main()	
