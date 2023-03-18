# Test=riscv_load_test Iteration=1000

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import cocotb
from cocotb import random
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge ,Timer,RisingEdge,ClockCycles
import pyuvm
import os
from pyuvm import*
import logging
from datetime import datetime 
import shutil
import time
import subprocess
from subprocess import run



#IMPORT THE SYSTEM PATH TO LINK DIFFERENT PY FILE
from pathlib import Path
import sys
sys.path.insert(0, str(Path("..").resolve()))


# importing all classes

#from Scripts import *
import Script as sp 
from BFM_RV32 import *
from SEQUENCER import *
from GENERATOR import *
from ISS_WHISPER import ISS_SIM
from DRIVER import *
from MONITOR import *
from SCOREBOARD import Scoreboard
from COVERAGE import *

# DEFINING BASE TESTER

		
class PYUVM_ENV(uvm_env):
	

	
	def build_phase(self):
		
		
		self.tester = BaseTester.create("tester",self)
		self.sequencer = Sequencer("sequencer",self)
		self.driver = DRIVER("driver",self)
		self.monitor = MONITOR("monitor",self)
		self.iss_whi = ISS_SIM("iss_whi",self)
		self.scoreboard = Scoreboard("scoreboard",self)
		self.coverage= Coverage("coverage",self)
		
		self.cmd_fifo_seq = uvm_tlm_fifo("cmd_fifo_seq",self)	
		self.cmd_fifo_seq_mon = uvm_tlm_fifo("cmd_fifo_seq_mon",self)

		
	def connect_phase(self):
		self.logger.info("PY_UVM Environment Execution")
		self.sequencer.pp_Driver.connect(self.cmd_fifo_seq.put_export)
		self.driver.gp_Sequencer.connect(self.cmd_fifo_seq.get_export)
		
		
		self.sequencer.pp_Monitor.connect(self.cmd_fifo_seq_mon.put_export)
		self.monitor.gp_Sequencer.connect(self.cmd_fifo_seq_mon.get_export)
		

class BaseTester(uvm_component):
		
	def build_phase(self):
		pass
		
		
	def start_of_simulation_phase(self):
		pass
		
	async def run_phase(self):
		
		await self.bfm.start_tasks()
		
		
		
									
class RV32_Tester(BaseTester):
	def build_phase(self):
		self.logger.info("**********RV32 Tester Build phase*********")
		
		self.Generator = Generator("Generator",self)
		self.bfm = RV32_BFM()
		
		
		ConfigDB().set(None,"*","bfm",self.bfm)
		ConfigDB().set(None,"*","GENR",self.Generator)


@pyuvm.test()			
class RandomTest(uvm_test):

	def build_phase(self):
		self.logger.info("*********PY_TEST Decorator Build Phase*********")
		uvm_factory().set_type_override_by_type(BaseTester,RV32_Tester)
		self.env = PYUVM_ENV("env",self)
		
		
	def end_of_elaboration_phase(self):
		self.txt,self.dir_p = sp.directory()
		formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
		file_handler = logging.FileHandler(self.txt, mode="w")
		stream_handler = logging.StreamHandler()
		file_handler.setFormatter(formatter)
		stream_handler.setFormatter(formatter)
		self.add_logging_handler_hier(file_handler)
		self.add_logging_handler_hier(stream_handler)
		self.remove_streaming_handler_hier()
		seed = cocotb.RANDOM_SEED
		dir_path = f'log/{os.getenv("Test","riscv_random_test")}/'
		self.logger.info(f"Test Name : {os.getenv('Test','riscv_random_test')} , Number of Instructions : {os.getenv('Iteration','10')} , Random Seed Number : {seed} \n")

	def final_phase(self):
		sp.copy(self.dir_p)


		


				
