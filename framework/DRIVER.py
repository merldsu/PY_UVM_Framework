# Copyright [2023] [MERL-DSU]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cocotb, pyuvm
from cocotb.triggers import ClockCycles
from pyuvm import *
from cocotb.queue import Queue, QueueEmpty
from pyuvm import utility_classes
from cocotb.triggers import Timer, FallingEdge, RisingEdge


class DRIVER(uvm_driver):

	def build_phase(self):
		self.logger.info("**********Driver Execution**********")
		
		self.bfm=ConfigDB().get(self,"","bfm")
		self.gp_Sequencer = uvm_blocking_get_port("gp_Sequencer",self)

		
	async def run_phase(self):
		self.raise_objection()
		self.logger.info("**********Driver Sustained********** ")
		
		
		await RisingEdge(self.bfm.dut.clk)
		await self.bfm.reset_m(0)
		#self.bfm.start_tasks()
		self.logger.info("Instruction & Data is dispatch to RTL by BFM (***Driver***)")
		while True:
			
			send_pc , send_instr = await self.gp_Sequencer.get()
			if (send_pc =="0xFFFFFFFF" and send_instr =="0xFFFFFFFF"):
				await RisingEdge(self.bfm.dut.clk)
				await self.bfm.reset_m(1)
			else:
				await self.bfm.send_values_bfm(send_pc , send_instr)
			


