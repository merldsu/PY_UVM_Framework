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
import cocotb 



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
	os.system("cp *.txt "+a+"/"+dir_p)
	os.system("cp *.log "+a+"/"+dir_p)
	
def delete():
	os.remove('./INSTR_RV32.csv')
	os.remove('./DATA_RV32.csv')
	os.remove('./Iss.txt')
	os.remove('./ISS.txt')
	os.remove('./ISS.csv')
	#os.remove('./dump.fst')
	os.remove('./program.hex')
	os.remove('./RESULT_MONITOR.csv')
	os.remove('./Final_Results.csv')
	os.remove('./exec.log')
	filename = 'removed_data.csv'
	if os.path.isfile(filename):
		os.remove('./removed_data.csv')
	else:
		pass
		

def over_all_report(info):
	
	folder_path = 'log/'
	file_path = os.path.join(folder_path, "over_all_report.txt")
	
	if not os.path.exists(file_path):
		with open(file_path, "a") as file:
			file.write(" " * 8 + "\t\t\t######### This is the report of overall Test that execute #########\n\n")
			file.write("   Date\t\tTime\t\t Test_Name\t\t Number_of_Instructions\t\t Random_Seed_Number\t\t Test_Status\n")
			
			
	with open(file_path, "a") as file:
		file.write(info + "\n")
	
def run(test):
	os.system(f"make {test}")
	
def print1():
	read_text_files = open("log/Coverage/coverage_summary.txt","r")
	for x in read_text_files:
		print(x)
	read_text_files.close()
	
def main():
	#rep()
	read_text_file = open("Test.txt","r")
	for x in read_text_file:
		run(x)
		delete()
	read_text_file.close()
	print1()
	
if __name__ == "__main__":
	main()	
