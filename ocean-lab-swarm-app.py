import tkinter as tk

LARGE_FONT = ("Verdana", 12)

class SwarmApp(tk.Tk):
	
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		container = tk.Frame(self)
		self.geometry('1000x750')
		self.resizable(width=False, height=False)
		container.pack(side="top", fill="both", expand = True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		frame = StartPage(container, self)

		self.frames[StartPage] = frame

		frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):
	
	def __init__(self, parent, controller):
		#set up all images used 
		self.forwardArrow = tk.PhotoImage(file="Media/forward arrow.gif")
		self.backArrow = tk.PhotoImage(file="Media/back arrow.gif")
		self.leftArrow = tk.PhotoImage(file="Media/left arrow.gif")
		self.rightArrow = tk.PhotoImage(file="Media/right arrow.gif")
		self.upArrow = tk.PhotoImage(file="Media/up arrow.gif")
		self.downArrow = tk.PhotoImage(file="Media/down arrow.gif")

		#create serial object to handle sending commands to swarm box
		self.vCommands = vehicleCommands()

		#create a Frame for the current Page
		tk.Frame.__init__(self, parent)
		
		####################################################################################
		#create a lable for the first vehicle
		vehicle1Label = tk.Label(self, text="Vehicle 1", font = LARGE_FONT)
		vehicle1Label.grid(row=1, column=3, pady=10)

		#create a container for the command buttons
		commandButtonWidget1 = tk.Frame(self, width=125, height=400)
		commandButtonWidget1.grid(row=2, column = 1)
		launchButton1 = tk.Button(commandButtonWidget1, text = "Launch Vehicle", font = LARGE_FONT, command = self.vCommands.launch, height = 1, width = 15)
		launchButton1.grid(row=1, column=1)

		hoverButton1 = tk.Button(commandButtonWidget1, text = "Hover Vehicle", font = LARGE_FONT, command = self.vCommands.hover, height = 1, width = 15)
		hoverButton1.grid(row=2, column=1)

		landButton1 = tk.Button(commandButtonWidget1, text = "Land Vehicle", font = LARGE_FONT, command = self.vCommands.land, height = 1, width = 15)
		landButton1.grid(row=3, column=1)

		#create horizontal position arrow container
		arrowWidget1 = tk.Frame(self, width=250, heigh=250)
		arrowWidget1.grid(row=2, column = 2, padx = 25)

		forwardButton1 = tk.Button(arrowWidget1, image = self.forwardArrow, font = LARGE_FONT, command = self.vCommands.forward, height = 68, width = 45)
		forwardButton1.grid(row=1, column=2)

		backButton1 = tk.Button(arrowWidget1, image = self.backArrow, font = LARGE_FONT, command = self.vCommands.back, height = 68, width = 45)
		backButton1.grid(row=3, column=2)

		leftButton1 = tk.Button(arrowWidget1, image = self.leftArrow, font = LARGE_FONT, command = self.vCommands.left, height = 45, width = 68)
		leftButton1.grid(row=2, column=1)

		rightButton1 = tk.Button(arrowWidget1, image = self.rightArrow, font = LARGE_FONT, command = self.vCommands.right, height = 45, width = 68)
		rightButton1.grid(row=2, column=3)

		#create up down arrow container
		upDownWidget1 = tk.Frame(self, width=150, height=500)
		upDownWidget1.grid(row=2, column = 3)

		upButton1 = tk.Button(upDownWidget1, image = self.upArrow, font = LARGE_FONT, command = self.vCommands.up, height = 76, width = 50)
		upButton1.grid(row=1, column=1)

		downButton1 = tk.Button(upDownWidget1, image = self.downArrow, font = LARGE_FONT, command = self.vCommands.down, height = 76, width = 50)
		downButton1.grid(row=2, column=1)

		#create data status update section
		status1Container = tk.Frame(self, width=150, height=500)
		status1Container.grid(row=2, column = 4, padx=(80, 0))

		vehicle1BatteryLabel = tk.Label(status1Container, text="Battery Voltage: 12.4V", font = LARGE_FONT)
		vehicle1BatteryLabel.grid(row=1, column=1, sticky=tk.W)
		vehicle1AltitudeLabel = tk.Label(status1Container, text="Altitude: 12m", font = LARGE_FONT)
		vehicle1AltitudeLabel.grid(row=2, column=1, sticky=tk.W)
		vehicle1LongLabel = tk.Label(status1Container, text="Longitude: -118.123432", font = LARGE_FONT)
		vehicle1LongLabel.grid(row=3, column=1, sticky=tk.W)
		vehicle1LatLabel = tk.Label(status1Container, text="Latitude: 35.234295", font = LARGE_FONT)
		vehicle1LatLabel.grid(row=4, column=1, sticky=tk.W)

		###############################################################################
		#create a lable for the first vehicle
		vehicle2Label = tk.Label(self, text="Vehicle 2", font = LARGE_FONT)
		vehicle2Label.grid(row=3, column=3, pady=10)

		#create a container for the command buttons
		commandButtonWidget2 = tk.Frame(self, width=125, height=400)
		commandButtonWidget2.grid(row=4, column = 1)
		launchButton2 = tk.Button(commandButtonWidget2, text = "Launch Vehicle", font = LARGE_FONT, command = self.vCommands.launch, height = 1, width = 15)
		launchButton2.grid(row=1, column=1)

		hoverButton2 = tk.Button(commandButtonWidget2, text = "Hover Vehicle", font = LARGE_FONT, command = self.vCommands.hover, height = 1, width = 15)
		hoverButton2.grid(row=2, column=1)

		landButton2 = tk.Button(commandButtonWidget2, text = "Land Vehicle", font = LARGE_FONT, command = self.vCommands.land, height = 1, width = 15)
		landButton2.grid(row=3, column=1)

		#create horizontal position arrow container
		arrowWidget2 = tk.Frame(self, width=250, heigh=250)
		arrowWidget2.grid(row=4, column = 2, padx = 25)

		forwardButton2 = tk.Button(arrowWidget2, image = self.forwardArrow, font = LARGE_FONT, command = self.vCommands.forward, height = 68, width = 45)
		forwardButton2.grid(row=1, column=2)

		backButton2 = tk.Button(arrowWidget2, image = self.backArrow, font = LARGE_FONT, command = self.vCommands.back, height = 68, width = 45)
		backButton2.grid(row=3, column=2)

		leftButton2 = tk.Button(arrowWidget2, image = self.leftArrow, font = LARGE_FONT, command = self.vCommands.left, height = 45, width = 68)
		leftButton2.grid(row=2, column=1)

		rightButton2 = tk.Button(arrowWidget2, image = self.rightArrow, font = LARGE_FONT, command = self.vCommands.right, height = 45, width = 68)
		rightButton2.grid(row=2, column=3)

		#create up down arrow container
		upDownWidget2 = tk.Frame(self, width=150, height=500)
		upDownWidget2.grid(row=4, column = 3)

		upButton2 = tk.Button(upDownWidget2, image = self.upArrow, font = LARGE_FONT, command = self.vCommands.up, height = 76, width = 50)
		upButton2.grid(row=1, column=1)

		downButton2 = tk.Button(upDownWidget2, image = self.downArrow, font = LARGE_FONT, command = self.vCommands.down, height = 76, width = 50)
		downButton2.grid(row=2, column=1)

		#create data status update section
		status2Container = tk.Frame(self, width=150, height=500)
		status2Container.grid(row=4, column = 4, padx=(80, 0))

		vehicle2BatteryLabel = tk.Label(status2Container, text="Battery Voltage: 12.4V", font = LARGE_FONT)
		vehicle2BatteryLabel.grid(row=1, column=1, sticky=tk.W)
		vehicle2AltitudeLabel = tk.Label(status2Container, text="Altitude: 12m", font = LARGE_FONT)
		vehicle2AltitudeLabel.grid(row=2, column=1, sticky=tk.W)
		vehicle2LongLabel = tk.Label(status2Container, text="Longitude: -118.123432", font = LARGE_FONT)
		vehicle2LongLabel.grid(row=3, column=1, sticky=tk.W)
		vehicle2LatLabel = tk.Label(status2Container, text="Latitude: 35.234295", font = LARGE_FONT)
		vehicle2LatLabel.grid(row=4, column=1, sticky=tk.W)

		###############################################################################
		#create a lable for the first vehicle
		vehicle3Label = tk.Label(self, text="Vehicle 3", font = LARGE_FONT)
		vehicle3Label.grid(row=5, column=3, pady=10)

		#create a container for the command buttons
		commandButtonWidget3 = tk.Frame(self, width=125, height=400)
		commandButtonWidget3.grid(row=6, column = 1)
		launchButton3 = tk.Button(commandButtonWidget3, text = "Launch Vehicle", font = LARGE_FONT, command = self.vCommands.launch, height = 1, width = 15)
		launchButton3.grid(row=1, column=1)

		hoverButton3 = tk.Button(commandButtonWidget3, text = "Hover Vehicle", font = LARGE_FONT, command = self.vCommands.hover, height = 1, width = 15)
		hoverButton3.grid(row=2, column=1)

		landButton3 = tk.Button(commandButtonWidget3, text = "Land Vehicle", font = LARGE_FONT, command = self.vCommands.land, height = 1, width = 15)
		landButton3.grid(row=3, column=1)

		#create horizontal position arrow container
		arrowWidget3 = tk.Frame(self, width=250, heigh=250)
		arrowWidget3.grid(row=6, column = 2, padx = 25)

		forwardButton3 = tk.Button(arrowWidget3, image = self.forwardArrow, font = LARGE_FONT, command = self.vCommands.forward, height = 68, width = 45)
		forwardButton3.grid(row=1, column=2)

		backButton3 = tk.Button(arrowWidget3, image = self.backArrow, font = LARGE_FONT, command = self.vCommands.back, height = 68, width = 45)
		backButton3.grid(row=3, column=2)

		leftButton3 = tk.Button(arrowWidget3, image = self.leftArrow, font = LARGE_FONT, command = self.vCommands.left, height = 45, width = 68)
		leftButton3.grid(row=2, column=1)

		rightButton3 = tk.Button(arrowWidget3, image = self.rightArrow, font = LARGE_FONT, command = self.vCommands.right, height = 45, width = 68)
		rightButton3.grid(row=2, column=3)

		#create up down arrow container
		upDownWidget3 = tk.Frame(self, width=150, height=500)
		upDownWidget3.grid(row=6, column = 3)

		upButton3 = tk.Button(upDownWidget3, image = self.upArrow, font = LARGE_FONT, command = self.vCommands.up, height = 76, width = 50)
		upButton3.grid(row=1, column=1)

		downButton3 = tk.Button(upDownWidget3, image = self.downArrow, font = LARGE_FONT, command = self.vCommands.down, height = 76, width = 50)
		downButton3.grid(row=2, column=1)

		#create data status update section
		status3Container = tk.Frame(self, width=150, height=500)
		status3Container.grid(row=6, column = 4, padx=(80, 0))

		vehicle3BatteryLabel = tk.Label(status3Container, text="Battery Voltage: 12.4V", font = LARGE_FONT)
		vehicle3BatteryLabel.grid(row=1, column=1, sticky=tk.W)
		vehicle3AltitudeLabel = tk.Label(status3Container, text="Altitude: 12m", font = LARGE_FONT)
		vehicle3AltitudeLabel.grid(row=2, column=1, sticky=tk.W)
		vehicle3LongLabel = tk.Label(status3Container, text="Longitude: -118.123432", font = LARGE_FONT)
		vehicle3LongLabel.grid(row=3, column=1, sticky=tk.W)
		vehicle3LatLabel = tk.Label(status3Container, text="Latitude: 35.234295", font = LARGE_FONT)
		vehicle3LatLabel.grid(row=4, column=1, sticky=tk.W)

class vehicleCommands():

	def launch(self):
		print("launching")

	def land(self):
		print("landing")

	def hover(slef):
		print("hover")

	def forward(self):
		print("moving forward")

	def back(self):
		print("moving back")

	def left(self):
		print("moving left")

	def right(self):
		print("moving right")

	def up(self):
		print("moving up")

	def down(self):
		print("moving down")



		
		

app = SwarmApp()
app.mainloop()