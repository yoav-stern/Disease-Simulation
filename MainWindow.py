import tkinter  # Import a graphics library
import matplotlib.pyplot as plt  # Import graph plotting library
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Import a function to make the graph run on a tkinter window
from matplotlib import style  # Library to change the look of the graph
from matplotlib import figure  # For graph implementation in tkinter
import random  # For random functionality
import math  # For the square root function
style.use('dark_background')  # Set the theme of the graph to be dark


class CPrediction:  # Prediction
    def __init__(self, predictionpopulation, beta, gamma):  # Set attributes
        self.population = predictionpopulation  # Set population
        self.s0 = predictionpopulation - 1  # Initial susceptible
        self.i0 = 1  # Initial infected
        self.r0 = 0  # Initial recovered
        self.susceptiblefunc = lambda b, s, i, p: (-b*s*i)/p  # The 3 differential equations
        self.infectedfunc = lambda b, g, s, i, p: (b*s*i)/p - g*i
        self.recoveredfunc = lambda g, i: g*i
        self.beta = beta  # Contact rate * probability of infection
        self.gamma = gamma  # Rate of recovery

    def eulers(self, t, deltat):  # Numerical solution using eulers method
        # Lists containing data to be plotted
        slist = []
        ilist = []
        rlist = []
        tlist = []
        end = False
        counter = 0

        while not end:  # Repeat until condition 'end' is met
            # Iterative formulas
            self.s0 = self.s0 + (self.susceptiblefunc(self.beta, self.s0, self.i0, self.population) * deltat)
            self.i0 = self.i0 + (self.infectedfunc(self.beta, self.gamma, self.s0, self.i0, self.population) * deltat)
            self.r0 = self.r0 + (self.recoveredfunc(self.gamma, self.i0) * deltat)
            t = t+deltat
            # Add the calculated values to their lists
            slist.append(self.s0)
            ilist.append(self.i0)
            rlist.append(self.r0)
            tlist.append(t)
            if self.i0 < self.population/100 and ilist[counter] < ilist[counter - 1]:  # If number of infected is decreasing and less then 1/100 then population, end calculation
                end = True
            counter += 1  # increment counter
        return tlist, slist, ilist, rlist  # Return the lists


class CShape:  # Contains geometrical properties and methods of a circle
    def __init__(self, xcoord, ycoord):  # Set attributes
        self.xcoord = xcoord  # Set x coordinate
        self.ycoord = ycoord  # Set y coordinate
        self.shape = canvas.create_oval(self.xcoord, self.ycoord, self.xcoord + 20, self.ycoord + 20, fill='green')  # Define the shape

    def move(self, movement):  # Method to allow the person to move
        xmove = random.randint(-movement, movement)  # Generate random distance for each person to move (within a range given from the user)
        ymove = random.randint(-movement, movement)
        position = canvas.coords(self.shape)  # Get the current coordinates of position
        # Set boundaries
        if position[0] < 10:  # If the new position is put of the boudries, chooose a different one in the oposite direction
            xmove = random.randint(0, movement)
        if position[1] < 10:
            ymove = random.randint(0, movement)
        if position[2] > 690:
            xmove = random.randint(-movement, 0)
        if position[3] > 690:
            ymove = random.randint(-movement, 0)

        canvas.move(self.shape, xmove, ymove)  # canvas.move moves the object by the value of the new coordinate
        canvas.update()  # Update the window
        self.xcoord = self.xcoord + xmove  # Update coordinates of object
        self.ycoord = self.ycoord + ymove


class CHuman(CShape):  # Contains properties and methods of a human
    def __init__(self, xcoord, ycoord, state, probabilityofinfection):  # Set attributes of human
        super().__init__(xcoord, ycoord)  # Inherit x and y coordinates and all methods of CGeometry
        self.probabilityofinfection = probabilityofinfection  # Set the probability of infection
        self.state = state  # Set the SIR state
        self.daysinfected = 0  # Set the number of days infected

    def infected(self):  # Method to infect a person
        canvas.itemconfig(self.shape, fill='red')  # Change colour of person to red
        self.state = 'infected'  # Change the state
        global Inumber, Snumber
        Inumber += 1  # Increment by 1 the total number of people infected
        Snumber -= 1  # Decrement by 1 the total number of people susceptible

    def recover(self):  # Method to make a person recover
        canvas.itemconfig(self.shape, fill='blue')  # Change colour of person to blue
        self.state = 'recovered'  # Change the state
        global Rnumber, Inumber
        Rnumber += 1  # Increment by 1 the total number of people recovered
        Inumber -= 1  # Decrement by 1 the total number of people Infected

    def updateinfectionstatus(self):  # Update the number of days infected
        if self.state == 'infected':  # Increment the number of days a person has been infected for
            self.daysinfected += 1

    def checkstatus(self, neighbour, localinfectionradius, recoverytime):  # Check for infection or recovery
        randomnumber = random.randint(0, 100)
        distance = math.sqrt(((self.xcoord-neighbour.xcoord)**2)+((self.ycoord-neighbour.ycoord)**2))
        if self.daysinfected == recoverytime:  # If you have been infected for the time the user has entered
            self.recover()  # Recover
            self.daysinfected = 0  # To make sure the function no longer gets called
        elif self.state == 'infected' or self.state == 'recovered':  # If self is not susceptible then ignore
            pass
        elif distance <= localinfectionradius and neighbour.state == 'infected' and randomnumber < (self.probabilityofinfection * 100):
            self.infected()  # If the distance between between self and an infected person is less then the radius given by the user and probability of infection is met, call the infect method


class CWindow:  # Class for the entry window
    def __init__(self, master):
        self.master = master  # Set attributes: Labels, entries and buttons
        self.master.title("Entry window")
        self.master.configure(bg='black')
        self.populationlbl = tkinter.Label(master, text='Enter population:', bg='black', fg='white')
        self.populationlbl.grid(row=1)
        self.populationentry = tkinter.Entry(master)
        self.populationentry.grid(row=2, padx=10, pady=10)
        self.enterbutton = tkinter.Button(master, text='Enter all', command=self.buttonclick)
        self.enterbutton.grid(column=3, row=4, pady=20)
        self.infectiousnesslbl = tkinter.Label(master, text='Enter infection radius (in pixels):', bg='black', fg='white')
        self.infectiousnesslbl.grid(row=1, column=2)
        self.infectiousnessentry = tkinter.Entry(master)
        self.infectiousnessentry.grid(row=2, column=2, padx=10, pady=10)
        self.recoverylbl = tkinter.Label(master, text='Enter rate of recovery (in days):', bg='black', fg='white')
        self.recoverylbl.grid(row=3, column=0, padx=10)
        self.recoveryentry = tkinter.Entry(master)
        self.recoveryentry.grid(row=4, column=0, padx=10, pady=10)
        self.speedlbl = tkinter.Label(master, text='Enter movement radius (in pixels)', bg='black', fg='white')
        self.speedlbl.grid(row=3, column=2, padx=10)
        self.speedentry = tkinter.Entry(master)
        self.speedentry.grid(row=4, column=2, padx=10, pady=10)
        self.probabilitylbl = tkinter.Label(master, text=' Enter probability of infection:', bg='black', fg='white')
        self.probabilitylbl.grid(row=1, column=3)
        self.probabilityentry = tkinter.Entry(master)
        self.probabilityentry.grid(row=2, column=3)

    def buttonclick(self):  # Method for when the button is clicked
        global population, infectionradius, recoveryrate, movementradius, probability
        try:  # Check for valid data
            natural(self.populationentry.get())
            natural(self.infectiousnessentry.get())
            natural(self.recoveryentry.get())
            if not 0 <= float(self.probabilityentry.get()) <= 1 or int(self.speedentry.get()) >= 100:
                raise ValueError
        except ValueError:  # If data is not valid
            errorwindow = tkinter.Tk()  # Show invalid data window
            errorwindow.title('Invalid data')
            errorwindow.config(bg='black')
            errorlabel1 = tkinter.Message(errorwindow, text='Invalid data type, please make sure you have entered the correct data type:', bg='black', fg='white', font='Ariel, 10', width=307)
            errorlabel2 = tkinter.Label(errorwindow, text='        Probability - float between 1 and 0', bg='black', fg='white', font='Ariel, 10', width=34, anchor='w')
            errorlabel3 = tkinter.Message(errorwindow, text='   Population, Infection radius, Recovery - Positive integer \n Movement radius - Integer between 0 and 100', bg='black', fg='white', font='Ariel, 10', width=330, justify='center')
            errorlabel1.pack(), errorlabel2.pack(), errorlabel3.pack()
            errorwindow.mainloop()
        else:  # If data is valid
            population = int(self.populationentry.get())  # Save the inputted data
            infectionradius = int(self.infectiousnessentry.get())
            recoveryrate = int(self.recoveryentry.get())
            movementradius = int(self.speedentry.get())
            probability = float(self.probabilityentry.get())
            self.master.destroy()  # Close the window


def natural(entrynumber):  # Check if input is a natural number
    if int(entrynumber) < 0:
        raise ValueError


def animate():  # Plot data
    DaysPassed.append(DayCounter)  # Update x values
    S.append(Snumber)  # Update the list containing number of susceptible people for each cycle
    I.append(Inumber)  # Update the list containing number of infected people for each cycle
    R.append(Rnumber)  # Update the list containing number of recovered people for each cycle
    plt.cla()  # Clear the axes
    plt.xlabel('Time / days')  # X-axis label
    plt.ylabel('Number of people')  # Y-axis label
    ax.plot(DaysPassed, S, 'g', label='Susceptible')  # Plot the points
    ax.plot(DaysPassed, I, 'r', label='Infected')
    ax.plot(DaysPassed, R, 'b', label='Recovered')
    handles, labels = ax.get_legend_handles_labels()  # Show labels
    ax.legend(labels)
    Environmentwindow.update_idletasks()  # To make the animation a little smoother


def mergesort(arr):  # Merge sort algorithm
    if len(arr) <= 1:  # Base case
        return arr
    middle = int(len(arr)/2)  # Split array into 2
    left = mergesort(arr[:middle])  # Call mergesort for the left and right arrays
    right = mergesort(arr[middle:])
    result = []
    leftpointer, rightpointer = 0, 0
    while leftpointer < len(left) and rightpointer < len(right):  # While you havent reached the end of an array
        if left[leftpointer] <= right[rightpointer]:  # If an element is bigger then the other
            result.append(left[leftpointer])  # Add elemnt to result
            leftpointer += 1  # Increment pointer
        else:
            result.append(right[rightpointer])  # Add elemnt to result
            rightpointer += 1   # Increment pointer

    result += left[leftpointer:]  # Add remaining values to the result array
    result += right[rightpointer:]
    return result


def getpeak(array):  # Get the position of the largest number in an array
    maximum = array[0]
    maxposition = 0
    for i in range(1, len(array)):  # Search through the whole array
        if array[i] > maximum:  # If current element is greater then maximum
            maximum = array[i]  # Set a new maximum
            maxposition = i  # Get the position of the maximum
    return maxposition


# initialise global variables
population, infectionradius, recoveryrate, movementradius, probability = 0, 0, 0, 0, 0

# create the entry window
root = tkinter.Tk()
EntryWindowMain = CWindow(root)
root.mainloop()

# create environment
Environmentwindow = tkinter.Tk()
Environmentwindow.title('Simulation')
canvas = tkinter.Canvas(Environmentwindow, height='700', width='700', bg='black')

# Setting up the graph data
Snumber = population
Inumber = 0
Rnumber = 0
DaysPassed = []
S = []
I = []
R = []

# to make the people move
populationList = []
for x in range(population):  # Create the requested number of people and add them to a list
    person = CHuman(random.randint(0, 700), random.randint(0, 700), 'susceptible', probability)
    populationList.append(person)

populationList[0].infected()  # infect the first person

fig = plt.figure(figsize=(7, 7))  # Create the graph
ax = fig.add_subplot(1, 1, 1)
plt.ion()  # Activate interactive mode
dataPlot = FigureCanvasTkAgg(fig, master=Environmentwindow)  # To enable the graph to be drawn on a tkinter window
dataPlot.draw()  # Draw graph
dataPlot.get_tk_widget().pack(side=tkinter.RIGHT)  # Draw graph on the right side of the window

# Initialise simulation variables
SimulationComplete = False
DayCounter = 0

while not SimulationComplete:  # Repeat until no one is infected anymore
    animate()  # Plot the data
    DayCounter += 1  # Increment the number of days passed since the start of the simulation
    for person in populationList:  # For every person in the list
        person.move(movementradius)  # Call the move method
        person.updateinfectionstatus()  # Call updateinfectionstatus method
        for x in range(population):
            person.checkstatus(populationList[x], infectionradius, recoveryrate)  # Check for infection or recovery
        canvas.pack(side=tkinter.LEFT)  # Display the simulation on the right side of the window
    if Snumber + Rnumber == population:  # If no one is infected
        SimulationComplete = True  # End the simulation
        Environmentwindow.destroy()  # Destroy the simulation window

collisionrate = (population/(700*700)) * (movementradius/2) * infectionradius  # Calculate collision rate
betavalue = collisionrate * probability  # Calculate beta value
gammavalue = 1/recoveryrate  # Calculate gamma vAlue

Isorted = mergesort(I)  # Sort the I array
# Stats page
message = ('Population: ', str(population), '\n Infection radius: ', str(infectionradius), '\n Movement radius: ', str(movementradius), '\n Recovery rate: ', str(recoveryrate), '\n Probability of infection: ', str(probability))
StatsPage = tkinter.Tk()  # Create statistics page
StatsPage.title('Statistics')
StatsPage.config(bg='black')
prediction = CPrediction(population, betavalue, gammavalue)  # Create prediction
time, psusceptible, pinfected, precovered = prediction.eulers(0, 0.5)
Parameters1 = tkinter.Label(StatsPage, text='The parameters entered are:', bg='black', fg='white')  # Set labels
Parameters2 = tkinter.Label(StatsPage, text="".join(message), bg='black', fg='white')
PredictedPeak1 = tkinter.Label(StatsPage, text='Predicted peak:', bg='black', fg='white')
PredictedPeak2 = tkinter.Label(StatsPage, text=math.ceil(mergesort(pinfected)[len(pinfected)-1]), bg='black', fg='white')  # Find peak value of pinfected
PeakInfected1 = tkinter.Label(StatsPage, text='Actual peak:', bg='black', fg='white')
PeakInfected2 = tkinter.Label(StatsPage, text=Isorted[len(I)-1], bg='black', fg='white')  # Largest number in the I array
PeakInfected3 = tkinter.Label(StatsPage, text='Actual day of peak:', bg='black', fg='white')
PeakInfected4 = tkinter.Label(StatsPage, text=math.ceil(DaysPassed[getpeak(I)]), bg='black', fg='white')  # Find the day which the peak is reached
Recovered1 = tkinter.Label(StatsPage, text='Total number of people infected and recovered: ', bg='black', fg='white')
Recovered2 = tkinter.Label(StatsPage, text=Rnumber, bg='black', fg='white')
Peakday1 = tkinter.Label(StatsPage, text='Predicted day of peak: ', bg='black', fg='white')
Peakday2 = tkinter.Label(StatsPage, text=math.ceil(time[getpeak(pinfected)]), bg='black', fg='white')  # Find the day which the peak is reached
Days1 = tkinter.Label(StatsPage, text='Total number of days passed: ', bg='black', fg='white')
Days2 = tkinter.Label(StatsPage, text=DayCounter, bg='black', fg='white')
fig2 = figure.Figure(figsize=(7, 7))  # Create a graph figure
axs = fig2.subplots(2)  # split the figure into 2
dataPlot = FigureCanvasTkAgg(fig2, master=StatsPage)  # To enable the graph to be drawn on a tkinter window
axs[0].plot(time, psusceptible, 'g')  # Plot predicted graph
axs[0].plot(time, pinfected, 'r')
axs[0].plot(time, precovered, 'b')
axs[0].set_title('Predicted with Eulers method:')
axs[1].plot(DaysPassed, S, 'g', label='Susceptible')  # Plot graph of actual results
axs[1].plot(DaysPassed, I, 'r', label='Infected')
axs[1].plot(DaysPassed, R, 'b', label='Recovered')
axs[1].set_title('Actual result:')
dataPlot.draw()  # Draw graph
dataPlot.get_tk_widget().pack(side=tkinter.RIGHT)
Parameters1.pack(), Parameters2.pack(), PredictedPeak1.pack(), PredictedPeak2.pack(), Peakday1.pack(), Peakday2.pack(), PeakInfected1.pack()
PeakInfected2.pack(), PeakInfected3.pack(), PeakInfected4.pack(), Recovered1.pack(), Recovered2.pack(), Days1.pack(), Days2.pack()  # Display lables
StatsPage.mainloop()

Environmentwindow.mainloop()  # Run the window
