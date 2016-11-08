try:
	#Python 3
	import tkinter as tk
	from tkinter import ttk
	import queue
except Exception:
	#Python 2
	import Tkinter as tk
	import ttk
	from multiprocessing import Queue as queue
import sys
import glob
import serial as serial
import atexit
import struct
from PyCRC.CRCCCITT import CRCCCITT

LARGE_FONT = ("Verdana", 10)

class SwarmApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		#start tkinter
		tk.Tk.__init__(self, *args, **kwargs)

		#create a container to fit all the pages into
		container = tk.Frame(self)
		#make the window size 1000px by 800px
		self.geometry('1000x800')
		#fix the window size so that it cannot be resized
		self.resizable(width=False, height=False)
		#fill the container to the entire window size
		container.pack(side="top", fill="both", expand = True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		###########where all of the label variables are setup
		self.vehicle1Lat = tk.StringVar()
		self.vehicle2Lat = tk.StringVar()
		self.vehicle3Lat = tk.StringVar()
		self.vehicle1Long = tk.StringVar()
		self.vehicle2Long = tk.StringVar()
		self.vehicle3Long = tk.StringVar()
		self.vehicle1Alt = tk.StringVar()
		self.vehicle2Alt = tk.StringVar()
		self.vehicle3Alt = tk.StringVar()
		self.vehicle1Voltage = tk.StringVar()
		self.vehicle2Voltage = tk.StringVar()
		self.vehicle3Voltage = tk.StringVar()
		self.vehicle1Current = tk.StringVar()
		self.vehicle2Current = tk.StringVar()
		self.vehicle3Current = tk.StringVar()
		self.vehicle1Percent = tk.StringVar()
		self.vehicle2Percent = tk.StringVar()
		self.vehicle3Percent = tk.StringVar()
		self.vehicle1State = tk.StringVar()
		self.vehicle2State = tk.StringVar()
		self.vehicle3State = tk.StringVar()
		self.vehicle1Lat.set("Latitude: ")
		self.vehicle2Lat.set("Latitude: ")
		self.vehicle3Lat.set("Latitude: ")
		self.vehicle1Long.set("Longitude: ")
		self.vehicle2Long.set("Longitude: ")
		self.vehicle3Long.set("Longitude: ")
		self.vehicle1Alt.set("Altitude: ")
		self.vehicle2Alt.set("Altitude: ")
		self.vehicle3Alt.set("Altitude: ")
		self.vehicle1Voltage.set("Voltage: ")
		self.vehicle2Voltage.set("Voltage: ")
		self.vehicle3Voltage.set("Voltage: ")
		self.vehicle1Current.set("Current: ")
		self.vehicle2Current.set("Current: ")
		self.vehicle3Current.set("Current: ")
		self.vehicle1Percent.set("Battery Percent: ")
		self.vehicle2Percent.set("Battery Percent: ")
		self.vehicle3Percent.set("Battery Percent: ")
		self.vehicle1State.set("State: ")
		self.vehicle2State.set("State: ")
		self.vehicle3State.set("State: ")

		#setup the serial port
		try:
			self.uart = serial.Serial()
			self.uart.baudrate = 115200
		except:
			print("error creating serial object")

		self.frames = {}

		frame = StartPage(container, self)

		self.frames[StartPage] = frame

		frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

		#add exit handlers to execute when program is terminated
		atexit.register(self.serialExitHandler)

		#a serial buffer used to process incoming packets
		self.serialBuffer = []




	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

	def serialExitHandler(self):
		if self.uart.is_open:
			self.uart.close()
			print("closed serial port")
		else:
			print("no serial port needed to be closed")

	def readByte(self):
		if self.uart.is_open:
			if self.uart.in_waiting > 0:
				readByte = self.uart.read(size=1)
				self.serialBuffer.append(readByte)

	def processPackets(self):
		#only check for a valid packet if data is in the buffer
		if len(self.serialBuffer) >= 1:
			#check for start of packet A
			SOPA = struct.unpack('B', self.serialBuffer[0])
			if SOPA[0] != 172:
				print("Bad SOPA: %x" %SOPA[0])
				#if packet is not valid remove data from buffer
				del self.serialBuffer[0]
			#if start of packet A was present look for
			#start of packet B if there are 2 bytes present
			elif len(self.serialBuffer) >= 2:
				#check for start of packet B
				SOPB = struct.unpack('B', self.serialBuffer[1])
				if SOPB[0] != 50:
					print("Bad SOPB: ")
					#if packet is not valid remove all checked data
					del self.serialBuffer[0:1]
				#if start of packet was valid look to see if length data is present
				elif len(self.serialBuffer) >= 5:
					#if length data is present then wait until entire message is present
					length = struct.unpack('B', self.serialBuffer[3])
					print("length")
					print(length)
					if len(self.serialBuffer) >= (8 + length[0]):
						#check for a valid end of packet byte
						EOP = struct.unpack('B', self.serialBuffer[7+length[0]])
						print("EOP")
						print(EOP[0])
						if EOP[0] == 3:
							#calculate the packets crc (will implement at a later date)
							messageType = struct.unpack('B', self.serialBuffer[2])
							messagePayload = self.serialBuffer[5:(5+length[0])]
							#route the packet
							self.routePacket(messageType[0], messagePayload)
							#remove packet from buffer
							del self.serialBuffer[0:(8+length[0])]

						#if it was a bad packet delete the entire data worth of the
						else:
							del self.serialBuffer[0:(8 + length[0])]
							print("bad end of packet character %x" %EOP[0])

	def routePacket(self, messageType, payload):
		if messageType == 40:
			print("got NVdrones packet")
			temp = struct.unpack('B', payload[2])
			droneID = temp[0]
			temp = struct.unpack('B', payload[1])
			messageID = temp[0]
			if messageID == 11:
				#handle locality packet
				print("got locality packet")
				#try:
				latitude = struct.unpack('i', payload[3] + payload[4] + payload[5] + payload[6])
				longitude = struct.unpack('i', payload[7] + payload[8] + payload[9] + payload[10])
				altitude = struct.unpack('I', payload[11] + payload[12] + payload[13] + payload[14])

				latitudeFloat = latitude[0]/10000000.0
				longitudeFloat = longitude[0]/10000000.0
				altitudeFloat = altitude[0]/1000.0
				if droneID == 1:
					self.vehicle1Lat.set("Latitude: %f" %latitudeFloat)
					self.vehicle1Long.set("Longitude: %f " %longitudeFloat)
					self.vehicle1Alt.set("Altitude: %.1fm" %altitudeFloat)
				elif droneID == 2:
					self.vehicle2Lat.set("Latitude: %f" %latitudeFloat)
					self.vehicle2Long.set("Longitude: %f" %longitudeFloat)
					self.vehicle2Alt.set("Altitude: %.1fm" %altitudeFloat)
				elif droneID == 3:
					self.vehicle3Lat.set("Latitude: %f" %latitudeFloat)
					self.vehicle3Long.set("Longitude: %f" %longitudeFloat)
					self.vehicle3Alt.set("Altitude: %.1fm" %altitudeFloat)
				#except:
				#	print("bad payload information")
			elif messageID == 12:
				#handle power packet
				print("got power packet")
				voltage = struct.unpack('H', payload[3] + payload[4])
				current = struct.unpack('h', payload[5] + payload[6])
				percentage = struct.unpack('b', payload[7])
				voltageFloat = voltage[0]/1000.0
				currentFloat = current[0]/1000.0
				print(voltageFloat)
				if droneID == 1:
					self.vehicle1Voltage.set("Voltage: %.2fV" %voltageFloat)
					self.vehicle1Current.set("Current: %.2fA" %currentFloat)
					self.vehicle1Percent.set("Battery Percent: %i" %percentage[0])

				elif droneID == 2:
					self.vehicle2Voltage.set("Voltage: %.2fV" %voltageFloat)
					self.vehicle2Current.set("Current: %.2fA" %currentFloat)
					self.vehicle2Percent.set("Battery Percent: %i" %percentage[0])

				elif droneID == 3:
					self.vehicle3Voltage.set("Voltage: %.2fV" %voltageFloat)
					self.vehicle3Current.set("Current: %.2fA" %currentFloat)
					self.vehicle3Percent.set("Battery Percent: %i" %percentage[0])

			elif messageID == 15:
				print ("got state packet")
				state = struct.unpack('B', payload[3])
				stateList = ['Landed', 'Ready', 'Take Off', 'Taking Off', 'Holding', 'Waypoint', \
							'2D Vector', '3D Vector', 'Heading to LZ', 'Landing', 'RC Control', 'Changing Altitude']

				if droneID == 1:
					self.vehicle1State.set("State: " + stateList[state[0]])
				if droneID == 2:
					self.vehicle2State.set("State: " + stateList[state[0]])
				if droneID == 3:
					self.vehicle3State.set("State: " + stateList[state[0]])


				#except:
				#	print("bad payload information")





class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		self.controller = controller

		#create serial object to handle sending commands to swarm box
		self.v1Commands = vehicleCommands(1, controller.uart, controller)
		self.v2Commands = vehicleCommands(2, controller.uart, controller)
		self.v3Commands = vehicleCommands(3, controller.uart, controller)

		#create a Frame for the current Page
		tk.Frame.__init__(self, parent)



		##########create header container###################################
		headerWidget = tk.Frame(self, width=1000, height=400)
		headerWidget.pack(fill=tk.X)
		#create a label for the first vehicle
		vehicle1Label = tk.Label(headerWidget, text="Vehicle 1", font = LARGE_FONT)
		vehicle1Label.grid(row=1, column=0, pady= (30, 0), padx = (55, 52))

		#create a lable for the first vehicle
		vehicle2Label = tk.Label(headerWidget, text="Vehicle 2", font = LARGE_FONT)
		vehicle2Label.grid(row=1, column=1, pady=(30,0), padx = 52)

		#create a lable for the second vehicle
		vehicle3Label = tk.Label(headerWidget, text="Vehicle 3", font = LARGE_FONT)
		vehicle3Label.grid(row=1, column=2, pady=(30,0), padx = 52)

		ports = self.serial_ports()
		ports = ['ports closed'] + ports

		self.serialPort = ttk.Combobox(headerWidget, values=ports, state='readonly', )
		self.serialPort.grid(row=1, column=4, padx = 200, pady = (30, 0))
		self.serialPort.bind("<<ComboboxSelected>>", self.openPort)
		self.serialPort.current(0)



		############create a container for the command buttons#######################
		commandWidget = tk.Frame(self, width=1000, height=400)
		commandWidget.pack(fill = tk.X)

		commandButtonWidget1 = tk.Frame(commandWidget, width=125, height=400)
		commandButtonWidget1.grid(row=1, column = 1, padx = 20, pady = 0)
		launchButton1 = tk.Button(commandButtonWidget1, text = "Launch Vehicle", font = LARGE_FONT, command = self.v1Commands.launch, height = 1, width = 15)
		launchButton1.grid(row=1, column=1)

		armButton1 = tk.Button(commandButtonWidget1, text = "Arm", font = LARGE_FONT, command = self.v1Commands.arm, height = 1, width = 15)
		armButton1.grid(row=2, column=1)

		landButton1 = tk.Button(commandButtonWidget1, text = "Land Vehicle", font = LARGE_FONT, command = self.v1Commands.land, height = 1, width = 15)
		landButton1.grid(row=3, column=1)

		eLandButton1 = tk.Button(commandButtonWidget1, text = "E-Land Vehicle", font = LARGE_FONT, command = self.v1Commands.eLand, height = 1, width = 15)
		eLandButton1.grid(row=4, column=1)

		manualButton1 = tk.Button(commandButtonWidget1, text = "Start Manual Mode", font = LARGE_FONT, command = self.v1Commands.manualMode, height = 1, width = 15)
		manualButton1.grid(row=5, column=1)

		holdButton1 = tk.Button(commandButtonWidget1, text = "Loiter Mode", font = LARGE_FONT, command = self.v1Commands.hold, height = 1, width = 15)
		holdButton1.grid(row=6, column=1)

		disarmButton1 = tk.Button(commandButtonWidget1, text = "Disarm", font = LARGE_FONT, command = self.v1Commands.disarm, height = 1, width = 15)
		disarmButton1.grid(row=7, column=1)


		commandButtonWidget2 = tk.Frame(commandWidget, width=125, height=400)
		commandButtonWidget2.grid(row=1, column = 2, padx = 20, pady = 0)
		launchButton2 = tk.Button(commandButtonWidget2, text = "Launch Vehicle", font = LARGE_FONT, command = self.v2Commands.launch, height = 1, width = 15)
		launchButton2.grid(row=1, column=1)

		armButton2 = tk.Button(commandButtonWidget2, text = "Arm", font = LARGE_FONT, command = self.v2Commands.arm, height = 1, width = 15)
		armButton2.grid(row=2, column=1)

		landButton2 = tk.Button(commandButtonWidget2, text = "Land Vehicle", font = LARGE_FONT, command = self.v2Commands.land, height = 1, width = 15)
		landButton2.grid(row=3, column=1)

		eLandButton2 = tk.Button(commandButtonWidget2, text = "E-Land Vehicle", font = LARGE_FONT, command = self.v2Commands.eLand, height = 1, width = 15)
		eLandButton2.grid(row=4, column=1)

		manualButton2 = tk.Button(commandButtonWidget2, text = "Start Manual Mode", font = LARGE_FONT, command = self.v2Commands.manualMode, height = 1, width = 15)
		manualButton2.grid(row=5, column=1)

		holdButton2 = tk.Button(commandButtonWidget2, text = "Loiter Mode", font = LARGE_FONT, command = self.v2Commands.hold, height = 1, width = 15)
		holdButton2.grid(row=6, column=1)

		disarmButton2 = tk.Button(commandButtonWidget2, text = "Disarm", font = LARGE_FONT, command = self.v2Commands.disarm, height = 1, width = 15)
		disarmButton2.grid(row=7, column=1)

		commandButtonWidget3 = tk.Frame(commandWidget, width=125, height=400)
		commandButtonWidget3.grid(row=1, column = 3, padx = 20, pady = 0)
		launchButton3 = tk.Button(commandButtonWidget3, text = "Launch Vehicle", font = LARGE_FONT, command = self.v3Commands.launch, height = 1, width = 15)
		launchButton3.grid(row=1, column=1)

		armButton3 = tk.Button(commandButtonWidget3, text = "Arm", font = LARGE_FONT, command = self.v3Commands.arm, height = 1, width = 15)
		armButton3.grid(row=2, column=1)

		landButton3 = tk.Button(commandButtonWidget3, text = "Land Vehicle", font = LARGE_FONT, command = self.v3Commands.land, height = 1, width = 15)
		landButton3.grid(row=3, column=1)

		eLandButton3 = tk.Button(commandButtonWidget3, text = "E-Land Vehicle", font = LARGE_FONT, command = self.v3Commands.eLand, height = 1, width = 15)
		eLandButton3.grid(row=4, column=1)

		manualButton3 = tk.Button(commandButtonWidget3, text = "Start Manual Mode", font = LARGE_FONT, command = self.v3Commands.manualMode, height = 1, width = 15)
		manualButton3.grid(row=5, column=1)

		holdButton3 = tk.Button(commandButtonWidget3, text = "Loiter Mode", font = LARGE_FONT, command = self.v3Commands.hold, height = 1, width = 15)
		holdButton3.grid(row=6, column=1)

		disarmButton3 = tk.Button(commandButtonWidget3, text = "Disarm", font = LARGE_FONT, command = self.v3Commands.disarm, height = 1, width = 15)
		disarmButton3.grid(row=7, column=1)



		#create data status update section
		statusContainer = tk.Frame(self, width=1000, height=500)
		statusContainer.pack(fill = tk.X)


		status1Container = tk.Frame(statusContainer, width=150, height=500)
		status1Container.grid(row=3, column = 1, padx=(30, 180))

		vehicle1Label = tk.Label(status1Container, text="Vehicle 1", font = LARGE_FONT)
		vehicle1Label.grid(row=0, column=1, sticky=tk.W, pady = (20, 0))

		vehicle1BatteryVoltageLabel = tk.Label(status1Container, textvariable=controller.vehicle1Voltage, font = LARGE_FONT)
		vehicle1BatteryVoltageLabel.grid(row=1, column=1, sticky=tk.W)
		vehicle1BatteryCurrentLabel = tk.Label(status1Container, textvariable=controller.vehicle1Current, font = LARGE_FONT)
		vehicle1BatteryCurrentLabel.grid(row=2, column=1, sticky=tk.W)
		vehicle1BatteryPercentLabel = tk.Label(status1Container, textvariable=controller.vehicle1Percent, font = LARGE_FONT)
		vehicle1BatteryPercentLabel.grid(row=3, column=1, sticky=tk.W)
		vehicle1AltitudeLabel = tk.Label(status1Container, textvariable=controller.vehicle1Alt, font = LARGE_FONT)
		vehicle1AltitudeLabel.grid(row=4, column=1, sticky=tk.W)
		vehicle1LongLabel = tk.Label(status1Container, textvariable=controller.vehicle1Long, font = LARGE_FONT)
		vehicle1LongLabel.grid(row=5, column=1, sticky=tk.W)
		vehicle1LatLabel = tk.Label(status1Container, textvariable=controller.vehicle1Lat, font = LARGE_FONT)
		vehicle1LatLabel.grid(row=6, column=1, sticky=tk.W)
		vehicle1StateLabel = tk.Label(status1Container, textvariable=controller.vehicle1State, font = LARGE_FONT)
		vehicle1StateLabel.grid(row=7, column=1, sticky=tk.W)


		#create data status update section
		status2Container = tk.Frame(statusContainer, width=150, height=500)
		status2Container.grid(row=3, column = 2, padx=(0, 180))

		vehicle2Label = tk.Label(status2Container, text="Vehicle 2", font = LARGE_FONT)
		vehicle2Label.grid(row=0, column=1, sticky = tk.W, pady = (20, 0))

		vehicle2BatteryVoltageLabel = tk.Label(status2Container, textvariable=controller.vehicle2Voltage, font = LARGE_FONT)
		vehicle2BatteryVoltageLabel.grid(row=1, column=1, sticky=tk.W)
		vehicle2BatteryCurrentLabel = tk.Label(status2Container, textvariable=controller.vehicle2Current, font = LARGE_FONT)
		vehicle2BatteryCurrentLabel.grid(row=2, column=1, sticky=tk.W)
		vehicle2BatteryPercentLabel = tk.Label(status2Container, textvariable=controller.vehicle2Percent, font = LARGE_FONT)
		vehicle2BatteryPercentLabel.grid(row=3, column=1, sticky=tk.W)
		vehicle2AltitudeLabel = tk.Label(status2Container, textvariable=controller.vehicle2Alt, font = LARGE_FONT)
		vehicle2AltitudeLabel.grid(row=4, column=1, sticky=tk.W)
		vehicle2LongLabel = tk.Label(status2Container, textvariable=controller.vehicle2Long, font = LARGE_FONT)
		vehicle2LongLabel.grid(row=5, column=1, sticky=tk.W)
		vehicle2LatLabel = tk.Label(status2Container, textvariable=controller.vehicle2Lat, font = LARGE_FONT)
		vehicle2LatLabel.grid(row=6, column=1, sticky=tk.W)
		vehicle2StateLabel = tk.Label(status2Container, textvariable=controller.vehicle2State, font = LARGE_FONT)
		vehicle2StateLabel.grid(row=7, column=1, sticky=tk.W)

		#create data status update section
		status3Container = tk.Frame(statusContainer, width=150, height=500)
		status3Container.grid(row=3, column = 3, padx=(0, 200))

		vehicle3Label = tk.Label(status3Container, text="Vehicle 3", font = LARGE_FONT)
		vehicle3Label.grid(row=0, column=1, sticky = tk.W, pady = (20, 0))


		vehicle3BatteryVoltageLabel = tk.Label(status3Container, textvariable=controller.vehicle3Voltage, font = LARGE_FONT)
		vehicle3BatteryVoltageLabel.grid(row=1, column=1, sticky=tk.W)
		vehicle3BatteryCurrentLabel = tk.Label(status3Container, textvariable=controller.vehicle3Current, font = LARGE_FONT)
		vehicle3BatteryCurrentLabel.grid(row=2, column=1, sticky=tk.W)
		vehicle3BatteryPercentLabel = tk.Label(status3Container, textvariable=controller.vehicle3Percent, font = LARGE_FONT)
		vehicle3BatteryPercentLabel.grid(row=3, column=1, sticky=tk.W)
		vehicle3AltitudeLabel = tk.Label(status3Container, textvariable=controller.vehicle3Alt, font = LARGE_FONT)
		vehicle3AltitudeLabel.grid(row=4, column=1, sticky=tk.W)
		vehicle3LongLabel = tk.Label(status3Container, textvariable=controller.vehicle3Long, font = LARGE_FONT)
		vehicle3LongLabel.grid(row=5, column=1, sticky=tk.W)
		vehicle3LatLabel = tk.Label(status3Container, textvariable=controller.vehicle3Lat, font = LARGE_FONT)
		vehicle3LatLabel.grid(row=6, column=1, sticky=tk.W)
		vehicle3StateLabel = tk.Label(status3Container, textvariable=controller.vehicle3State, font = LARGE_FONT)
		vehicle3StateLabel.grid(row=7, column=1, sticky=tk.W)


		#####Position Controls#######################
		positionContainer = tk.Frame(self, width=1000, height=200)
		positionContainer.pack(fill = tk.X)

		position1Container = tk.Frame(positionContainer)
		position1Container.grid(row=1, column = 1, padx = (15, 85), sticky = tk.W)

		#altitude Entry
		alt1Label = tk.Label(position1Container, text="Vehicle 1 Altitude (m)", font = LARGE_FONT)
		alt1Label.grid(row=0, column=1, padx = (15, 10), pady = (50, 0), sticky = tk.W)
		self.altitude1Entry = tk.Entry(position1Container)
		self.altitude1Entry.grid(row=1, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		altitude1Button = tk.Button(position1Container, text = "Go to Altitude", font = LARGE_FONT, command = lambda: self.altitude(1), height = 1, width = 15)
		altitude1Button.grid(row=2, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)

		#vector Entry
		heading1Label = tk.Label(position1Container, text="Vehicle 1 Heading (Deg)", font = LARGE_FONT)
		heading1Label.grid(row=3, column=1, padx = (15, 10), pady = (40, 0), sticky = tk.W)
		self.heading1Entry = tk.Entry(position1Container)
		self.heading1Entry.grid(row=4, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		mag1Label = tk.Label(position1Container, text="Vehicle 1 Magnitude (m/s)", font = LARGE_FONT)
		mag1Label.grid(row=5, column=1, padx = (15, 10), pady = (0, 0), sticky = tk.W)
		self.mag1Entry = tk.Entry(position1Container)
		self.mag1Entry.grid(row=6, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		timeout1Label = tk.Label(position1Container, text="Vehicle 1 Timeout (s)", font = LARGE_FONT)
		timeout1Label.grid(row=7, column=1, padx = (15, 10), pady = (0, 0), sticky = tk.W)
		self.timeout1Entry = tk.Entry(position1Container)
		self.timeout1Entry.grid(row=8, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		vector1Button = tk.Button(position1Container, text = "Move", font = LARGE_FONT, command = lambda: self.vector(1), height = 1, width = 15)
		vector1Button.grid(row=9, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)

		position2Container = tk.Frame(positionContainer)
		position2Container.grid(row=1, column = 2, padx = (15, 85), sticky = tk.W)

		#altitude Entry
		alt2Label = tk.Label(position2Container, text="Vehicle 2 Altitude (m)", font = LARGE_FONT)
		alt2Label.grid(row=0, column=1, padx = (15, 10), pady = (50, 0), sticky = tk.W)
		self.altitude2Entry = tk.Entry(position2Container)
		self.altitude2Entry.grid(row=1, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		altitude2Button = tk.Button(position2Container, text = "Go to Altitude", font = LARGE_FONT, command = lambda: self.altitude(2), height = 1, width = 15)
		altitude2Button.grid(row=2, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)

		#vector Entry
		heading2Label = tk.Label(position2Container, text="Vehicle 2 Heading (Deg)", font = LARGE_FONT)
		heading2Label.grid(row=3, column=1, padx = (15, 10), pady = (40, 0), sticky = tk.W)
		self.heading2Entry = tk.Entry(position2Container)
		self.heading2Entry.grid(row=4, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		mag2Label = tk.Label(position2Container, text="Vehicle 2 Magnitude (m/s)", font = LARGE_FONT)
		mag2Label.grid(row=5, column=1, padx = (15, 10), pady = (0, 0), sticky = tk.W)
		self.mag2Entry = tk.Entry(position2Container)
		self.mag2Entry.grid(row=6, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		timeout2Label = tk.Label(position2Container, text="Vehicle 2 Timeout (s)", font = LARGE_FONT)
		timeout2Label.grid(row=7, column=1, padx = (15, 10), pady = (0, 0), sticky = tk.W)
		self.timeout2Entry = tk.Entry(position2Container)
		self.timeout2Entry.grid(row=8, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		vector2Button = tk.Button(position2Container, text = "Move", font = LARGE_FONT, command = lambda: self.vector(2), height = 1, width = 15)
		vector2Button.grid(row=9, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)

		position3Container = tk.Frame(positionContainer)
		position3Container.grid(row=1, column = 3, padx = (15, 85), sticky = tk.W)

		#altitude Entry
		alt3Label = tk.Label(position3Container, text="Vehicle 3 Altitude (m)", font = LARGE_FONT)
		alt3Label.grid(row=0, column=1, padx = (15, 10), pady = (50, 0), sticky = tk.W)
		self.altitude3Entry = tk.Entry(position3Container)
		self.altitude3Entry.grid(row=1, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		altitude3Button = tk.Button(position3Container, text = "Go to Altitude", font = LARGE_FONT, command = lambda:self.altitude(3), height = 1, width = 15)
		altitude3Button.grid(row=2, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)

		#vector Entry
		heading3Label = tk.Label(position3Container, text="Vehicle 3 Heading (Deg)", font = LARGE_FONT)
		heading3Label.grid(row=3, column=1, padx = (15, 10), pady = (40, 0), sticky = tk.W)
		self.heading3Entry = tk.Entry(position3Container)
		self.heading3Entry.grid(row=4, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		mag3Label = tk.Label(position3Container, text="Vehicle 3 Magnitude (m/s)", font = LARGE_FONT)
		mag3Label.grid(row=5, column=1, padx = (15, 10), pady = (0, 0), sticky = tk.W)
		self.mag3Entry = tk.Entry(position3Container)
		self.mag3Entry.grid(row=6, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		timeout3Label = tk.Label(position3Container, text="Vehicle 3 Timeout (s)", font = LARGE_FONT)
		timeout3Label.grid(row=7, column=1, padx = (15, 10), pady = (0, 0), sticky = tk.W)
		self.timeout3Entry = tk.Entry(position3Container)
		self.timeout3Entry.grid(row=8, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		vector3Button = tk.Button(position3Container, text = "Move", font = LARGE_FONT, command = lambda: self.vector(3), height = 1, width = 15)
		vector3Button.grid(row=9, column=1, pady = (0, 0), padx = (15, 0), sticky = tk.W)
		#vector 3ntry

	def altitude(self, vehicleNumber):
		if vehicleNumber == 1:
			altitude = int(self.altitude1Entry.get())
			self.v1Commands.altitude(altitude)
		elif vehicleNumber == 2:
			altitude = int(self.altitude2Entry.get())
			self.v2Commands.altitude(altitude)
		elif vehicleNumber == 3:
			altitude = int(self.altitude2Entry.get())
			self.v3Commands.altitude(altitude)


	def vector(self, vehicleNumber):
		if vehicleNumber == 1:
			heading = int(self.heading1Entry.get())
			magnitude = int(self.mag1Entry.get())
			timeout = int(self.timeout1Entry.get())
			self.v1Commands.vector(heading, magnitude, timeout)
		elif vehicleNumber == 2:
			heading = int(self.heading2Entry.get())
			magnitude = int(self.mag2Entry.get())
			timeout = int(self.timeout2Entry.get())
			self.v2Commands.vector(heading, magnitude, timeout)
		elif vehicleNumber == 3:
			heading = int(self.heading3Entry.get())
			magnitude = int(self.mag3Entry.get())
			timeout = sint(self.timeout3Entry.get())
			self.v3Commands.vector(heading, magnitude, timeout)








	def openPort(self, event):
		'''This gets executed when the serial drop
		down menu is updated.  It closes all serial
		ports, and opens the serial object on the new
		Serial Port Number'''
		#fetch the updated port number
		portName = self.serialPort.get()
		#if the serial port is currently open then close it
		if self.controller.uart.is_open:
			self.controller.uart.close()
		#if the serial port that was selected is 'ports closed'
		#then keep all serial ports closed
		if portName != 'ports closed':
			try:
				self.controller.uart.port = portName
				self.controller.uart.open()
				print("opened port"+portName)
			except:
				print("cannot open port")


	def serial_ports(self):
	    """ Lists serial port names

	        :raises EnvironmentError:
	            On unsupported or unknown platforms
	        :returns:
	            A list of the serial ports available on the system
	    """
	    if sys.platform.startswith('win'):
	        ports = ['COM%s' % (i + 1) for i in range(256)]
	    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
	        # this excludes your current terminal "/dev/tty"
	        ports = glob.glob('/dev/tty[A-Za-z]*')
	    elif sys.platform.startswith('darwin'):
	        ports = glob.glob('/dev/tty.*')
	    else:
	        raise EnvironmentError('Unsupported platform')

	    result = []
	    for port in ports:
	        try:
	            s = serial.Serial(port)
	            s.close()
	            result.append(port)
	        except (OSError, serial.SerialException):
	            pass
	    return result



class vehicleCommands():


	def __init__(self, vehicleNumber, serialObject, controller):
		self.senderID = 0
		self.currentFlightMode = 0
		self.serialObject = serialObject
		self.vehicleNumber = vehicleNumber
		self.controller = controller

		self.takeoffID = 1
		self.landID = 2
		self.eLandID = 3
		self.holdID = 4
		self.manualID = 5
		self.altID = 10
		self.localityID = 11
		self.powerID = 12
		self.disarmID = 13
		self.vectorID = 14
		self.stateID = 15
		self.startID = 16



	def launch(self):
		launchPacket = struct.pack('B', self.vehicleNumber)
		launchPacket += struct.pack('B', self.takeoffID)
		launchPacket += struct.pack('B', self.senderID)
		self.sendPacket(launchPacket, 3)
		print("launching vehicle: ")

	def land(self):
		landPacket = struct.pack('B', self.vehicleNumber)
		landPacket += struct.pack('B', self.landID)
		landPacket += struct.pack('B', self.senderID)
		self.sendPacket(landPacket, 3)
		print("landing vehicle: ")

	def eLand(self):
		eLandPacket = struct.pack('B', self.vehicleNumber)
		eLandPacket += struct.pack('B', self.eLandID)
		eLandPacket += struct.pack('B', self.senderID)
		self.sendPacket(eLandPacket, 3)
		print("landing vehicle: ")

	def arm(self):
		armPacket = struct.pack('B', self.vehicleNumber)
		armPacket += struct.pack('B', self.startID)
		armPacket += struct.pack('B', self.senderID)
		self.sendPacket(armPacket, 3)
		print("landing vehicle: ")

	def manualMode(self):
		manualModePacket = struct.pack('B', self.vehicleNumber)
		manualModePacket += struct.pack('B', self.manualID)
		manualModePacket += struct.pack('B', self.senderID)
		self.sendPacket(manualModePacket, 3)
		print("switched to manual mode")

	def hold(self):
		holdPacket = struct.pack('B', self.vehicleNumber)
		holdPacket += struct.pack('B', self.holdID)
		holdPacket += struct.pack('B', self.senderID)
		self.sendPacket(holdPacket, 3)

	def vector(self, heading, magnitude, timeout):
		heading = int(heading*100)
		timeout = int(timeout*1000)
		magnitude = int(magnitude*1000)
		vectorPacket = struct.pack('B', self.vehicleNumber)
		vectorPacket += struct.pack('B', self.vectorID)
		vectorPacket += struct.pack('B', self.senderID)
		vectorPacket += struct.pack('H', magnitude)
		vectorPacket += struct.pack('H', heading)
		vectorPacket += struct.pack('H', timeout)
		self.sendPacket(vectorPacket, 9)
		print("sending vector packet")

	def altitude(self, altitude):
		altPacket = struct.pack('B', self.vehicleNumber)
		altPacket += struct.pack('B', self.altID)
		altPacket += struct.pack('B', self.senderID)
		altPacket += struct.pack('f', float(altitude))
		print(altPacket)
		print("sending alt packet")
		self.sendPacket(altPacket, 7)

	def disarm(self):
		disarmPacket = struct.pack('B', self.vehicleNumber)
		disarmPacket += struct.pack('B', self.disarmID)
		disarmPacket += struct.pack('B', self.senderID)
		print("disarming")
		self.sendPacket(disarmPacket, 3)

	def sendPacket(self, payload, size):
		packet = ''
		SOPA = 172
		SOPB = 50
		RADIO_TYPE = 40
		packet = struct.pack('BBB', SOPA, SOPB, RADIO_TYPE)
		PayloadSizeA = size
		PayloadSizeB = 0
		packet += struct.pack('BB', PayloadSizeA, PayloadSizeB)
		packet += payload
		CRC = CRCCCITT().calculate(packet)
		packet += struct.pack('H', CRC)
		EOP = 3
		packet += struct.pack('B', EOP)
		#try:
		self.serialObject.write(packet)
		#print("Sending Packet: " + packet)
		#except:
		#	print("could not send serial")
		print("packet")


app = SwarmApp()
while 1:
	app.readByte()
	app.update()
	app.processPackets()
