import Calculations
import time
import values
import _thread as thread
import Conventional
from gui import carGUI
from random import randint
from Car import Car
from Intersection import Intersection
import IntersectionThread
# import server
# import client

# Initialize array to contain cars
carList = []
IntersectionList = []


def simulation(gui):
    # Initialize instance of intersection
    currIntersection_1 = Intersection(length=40, wid=40, posX=490, posY=200, gui=gui)
    currIntersection_2 = Intersection(length=40, wid=40, posX=1020, posY=500, gui=gui)
    currIntersection_3 = Intersection(length=40, wid=40, posX=1020, posY=200, gui=gui)
    currIntersection_4 = Intersection(length=40, wid=40, posX=490, posY=500, gui=gui)
    IntersectionList.append(currIntersection_1)
    IntersectionList.append(currIntersection_2)
    IntersectionList.append(currIntersection_3)
    IntersectionList.append(currIntersection_4)

    for i in range(len(IntersectionList)):
        gui.drawIndicationLines(IntersectionList[i])

    elapsedTime = 0                                         # initialize time in seconds
    runSim = True                                           # bool to stop simulation

    # Begin simulation:
    while(runSim):

        gui.update()

        # Determine what kind of simulation we're running
        if(gui.CheckVar.get() == 1):
            values.conventionalSimFlag = True
        else:
            values.conventionalSimFlag = False

        # Remove processed cars from the intersection list
        for i in range(len(IntersectionList)):
            cleanList(carList, gui, IntersectionList[i])

        # Check to see if we should end simulation
        """
        if(elapsedTime > values.simluationTime):
            runSim = False
        """                              # if time condition is true runSim to false
        elapsedTime += values.timeInterval                  # increment 100 mili second

        # Update the intersection containers and values
        for i in range(len(IntersectionList)):
            update_intersection(IntersectionList[i], elapsedTime)

        # Check if this is a conventional simulation
        if(values.conventionalSimFlag):
            for i in range(len(IntersectionList)):
                # thread.start_new_thread(run_conventional, (IntersectionList[i], gui))
                run_conventional(IntersectionList[i], gui)
                # interThread = IntersectionThread.interThread(IntersectionList[i],)

        # Check if this is an optimized simulation
        else:
            interThreads = []
            for i in range(len(IntersectionList)):
                # run_opt = thread.__init__(run_optimized, (IntersectionList[i], gui, carList))
                # run_opt.start()
                # interThreads.append(run_opt)
                # interThread = IntersectionThread.InterThread(IntersectionList[i], gui, carList)
                # interThread.start()
                # interThreads.append(interThread)
                run_optimized(IntersectionList[i], gui, carList)

            '''
            for i in range(len(interThreads)):
                interThreads[i].join()
            '''

            # interThreads.clear()

        # Update the positions of the cars
        update_positions(gui)

        # Generate new cars
        generate_cars(gui, elapsedTime)

        # Call server communications
        # server_send_packet()

        # Sleep the while loop
        time.sleep(.01)

    generate_statistics()


def run_optimized(intersection, gui, carList):
    timeStart = time.time()             # START TIME

    Calculations.collisionDetection(intersection.queueX, intersection.queueY, gui, intersection, carList)

    timeEnd = time.time()

    # Call the delay update function
    update_car_delay((timeEnd - timeStart))


def run_conventional(intersection, gui):
    timeStart = time.time()             # START TIME
    Conventional.stopSign(intersection.queueX, intersection.queueY, gui, intersection)

    timeEnd = time.time()               # END TIME

    # Call the delay update function
    update_car_delay((timeEnd - timeStart))


def update_intersection(intersection, elapsedTime):
        timeStart = time.time()         # START TIME

        intersection.updateIntersectionContainers(carList, elapsedTime)
        intersection.restoreVelocities(carList)

        timeEnd = time.time()           # END TIME

        # Call the delay update function
        update_car_delay((timeEnd - timeStart))


def update_positions(gui):
        timeStart = time.time()         # START TIME

        # Update the positions of the cars in the list
        for i in range(0, len(carList)):
            carList[i].updatePosition(values.timeInterval)

        # Update GUI
        gui.moveCars(carList, values.timeInterval)

        timeEnd = time.time()           # END TIME

        # Call the delay update function
        update_car_delay((timeEnd - timeStart))


def generate_cars(gui, elapsedTime):
        timeStart = time.time()         # START TIME

        if(True):       # not values.conventionalStoppedX and not values.conventionalStoppedY):
            if(elapsedTime % values.carGenerationModulo is 0):
                # Generate two cars
                for i in range(1, 3):
                    rand = randint(0, 3)
                    if(rand == 0 or rand == 1 or rand == 2):
                        newCar = randomCarGenerator(gui, True, i)
                        carList.append(newCar)

        timeEnd = time.time()           # END TIME

        # Call the delay update function
        update_car_delay((timeEnd - timeStart))


def randomCarGenerator(LiveGUI, twoCars, Direction):
    timeStart = time.time()         # TIME START

    if(not twoCars):
        direction = randint(1, 2)
    else:
        direction = Direction

    velocity = values.maxVelocity
    ID = randomIDGenerator()

    if(direction == 1):
        # Generate a horizontally traveling car
        car = Car(length=5, width=5, velocityX=velocity, velocityY=0, startX=0, startY=IntersectionList[0].positionY, ID=ID, direction="horizontal", startTime=time.time())
        LiveGUI.drawCar(direction, ID, dirNumber=0)
        carList.append(car)

        ID = randomIDGenerator()
        car = Car(length=5, width=5, velocityX=velocity, velocityY=0, startX=0, startY=IntersectionList[1].positionY, ID=ID, direction="horizontal", startTime=time.time())
        LiveGUI.drawCar(direction, ID, dirNumber=1)
    elif(direction == 2):
        # Generate a vertically traveling car in the first Y Lane
        car = Car(length=5, width=5, velocityX=0, velocityY=velocity, startX=IntersectionList[0].positionX, startY=0, ID=ID, direction="vertical", startTime=time.time())
        LiveGUI.drawCar(direction, ID, dirNumber=0)
        carList.append(car)

        # Generate a vertically travelling car in the second Y Lane
        ID = randomIDGenerator()
        car = Car(length=5, width=5, velocityX=0, velocityY=velocity, startX=IntersectionList[1].positionX, startY=0, ID=ID, direction="vertical", startTime=time.time())
        LiveGUI.drawCar(direction, ID, dirNumber=1)


    timeEnd = time.time()           # TIME END

    # Call the delay update function
    update_car_delay((timeEnd - timeStart))

    return car


def generate_statistics():
    if(values.conventionalSimFlag):
        size_conv = len(values.conventional_times)
        sum_conv = 0
        for i in range(0, size_conv):
            sum_conv = sum_conv + values.conventional_times[i]

        avg_conv = sum_conv / size_conv

        sum_conv_calc_times = 0
        for i in range(0, len(values.conventional_calculation_times)):
            sum_conv_calc_times += values.conventional_calculation_times[i]

        avg_conv_calc_times = sum_conv_calc_times / len(values.conventional_calculation_times)

        print("CONVENTIONAL AVERAGE: ", avg_conv)
        print("CONVENTIONAL AVERAGE CALCULATION TIME: ", avg_conv_calc_times)

    else:
        size_opt = len(values.optimized_times)
        sum_opt = 0
        for i in range(0, size_opt):
            sum_opt = sum_opt + values.optimized_times[i]

        avg_opt = sum_opt / size_opt

        sum_opt_calc_times = 0
        for i in range(0, len(values.optimized_calculation_times)):
            sum_opt_calc_times += values.optimized_calculation_times[i]

        avg_opt_calc_times = sum_opt_calc_times / len(values.optimized_calculation_times)

        print("OPTIMIZED AVERAGE: ", avg_opt)
        print("OPTIMIZED AVERAGE CALCULATION TIME: ", avg_opt_calc_times)


def randomIDGenerator():
    timeStart = time.time()         # TIME START

    # Generate a Unique ID
    generateID = True
    while(generateID):
        generateID = False
        ID = randint(0, 10000)
        for i in range(0, len(carGUI.carIDs)):
            if ID == carGUI.carIDs[i]:
                generateID = True

    timeEnd = time.time()           # END TIME

    # Call the delay update function
    update_car_delay((timeEnd - timeStart))

    return ID


def cleanList(carList, gui, currIntersection):

    deleteList = []

    for i in range(len(carList)):

        """ If the cars x position is greate than the interesection X width then remove it """
        if((carList[i].positionX > 1500) or (carList[i].positionY > 1500)):

            if(values.conventionalSimFlag and not carList[i].timeStamped):
                # print("THIS CARS POSITION IS: ", carList[i].positionX, carList[i].positionY)
                values.conventional_times.append(time.time() - carList[i].startTime - carList[i].calculationTime)
                values.conventional_calculation_times.append(carList[i].calculationTime)
                carList[i].timeStamped = True

            elif(not values.conventionalSimFlag and not carList[i].timeStamped):
                # print("THIS CARS POSITION IS: ", carList[i].positionX, carList[i].positionY)
                values.optimized_times.append(time.time() - carList[i].startTime - carList[i].calculationTime)
                values.optimized_calculation_times.append(carList[i].calculationTime)
                carList[i].timeStamped = True
                deleteList.append(carList[i])

    for i in range(len(deleteList)):
        gui.deleteCar(deleteList[i])
        carList.remove(deleteList[i])


def update_car_delay(time):
    # timeStart = time.time()         # TIME START

    for i in range(0, len(carList)):
        carList[i].calculationTime += time

    # timeEnd = time.time()           # TIME END

    # Call the delay update function
    # update_car_delay((timeEnd - timeStart))
