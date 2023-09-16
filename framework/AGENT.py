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



import cocotb
import pyuvm
from pyuvm import*

from SEQUENCER import *
from DRIVER import *
from MONITOR import *

# Define the uvm_agent class

class agent(uvm_agent):
	def build_phase(self):
		pass

# Agent for Swerv Framework
class Swerv_agent(agent):

	def build_phase(self):
		self.sequencer = Swerv_Sequencer("sequencer",self)
		self.driver = DRIVER_SWERV("driver",self)
		self.monitor_swerv = MONITOR_SWERV("monitor_swerv",self)
		
		self.cmd_fifo_seq = uvm_tlm_fifo("cmd_fifo_seq",self)	
		
		
	def connect_phase(self):
	
		self.logger.info("PY_UVM SWERV-AGENT Execution")
		
		self.sequencer.pp_Driver.connect(self.cmd_fifo_seq.put_export)
		self.driver.gp_Sequencer.connect(self.cmd_fifo_seq.get_export)		
