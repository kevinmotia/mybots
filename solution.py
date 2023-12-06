import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
import numpy as np
#--------------------------------------------

#--------------------------------------------

class SOLUTION:
    def __init__(self, nextAvailableID, overallBot, continueOrNone, populationID):
        self.myID = nextAvailableID
        self.overallBot = int(overallBot)
        self.continueOrNone = continueOrNone
        self.populationID = int(populationID) # obtained from parallelHillClimber constructor
        self.weights = numpy.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        self.weights = self.weights * 2 - 1

        if self.continueOrNone == 'continue': 
            with open('weightsFiles/weights' + str(self.overallBot) + '_' + str(self.populationID) + '.txt', 'r') as pickleFile: # use botNumber
                self.weights = np.loadtxt(pickleFile)
                pickleFile.close()
            # second part of this block is in mutate() because constructor should not save. Only load.
        
        else:
            self.weights = np.random.rand(c.numSensorNeurons+1,c.numMotorNeurons)   
            self.weights = self.weights * 2 - 1    


    def Evaluate(self,directOrGUI):
        pass


    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length,width,height]) 
        pyrosim.End()


    def Generate_Body(self,xi,yi): 
# Start generating robot body and name the body file
        pyrosim.Start_URDF("bodyFiles/body"+str(xi)+str(yi)+".urdf")
#Torso
        pyrosim.Send_Cube(name="Torso", pos=[0+xi,0+yi,1] , size=[1,1,1])
# Upper Extremities
    #Back Leg
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0+xi,-0.5+yi,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0] , size=[0.2, 1, 0.2])
    #Front Leg
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0+xi,0.5+yi,1], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0] , size=[0.2, 1, 0.2])
    #Left Leg
        pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5+xi,0+yi,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0] , size=[1, 0.2, 0.2])       
    #Right Leg
        pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5+xi,0+yi,1], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0] , size=[1, 0.2, 0.2])   
# Lower Extremities
    #Back Lower Leg
        pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg" , parent= "BackLeg", child = "BackLowerLeg", type = "revolute", position = [0, -1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])   
    #Front Lower Leg
        pyrosim.Send_Joint( name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg", child = "FrontLowerLeg", type = "revolute", position = [0, 1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])
    #Left Lower Leg
        pyrosim.Send_Joint( name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg", child = "LeftLowerLeg", type = "revolute", position = [-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])
    #Right Lower Leg
        pyrosim.Send_Joint( name = "RightLeg_RightLowerLeg", parent= "RightLeg", child = "RightLowerLeg", type = "revolute", position = [1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])
        pyrosim.End()
        #exit() # uncommenting this allows you to see effects of code on body.urdf


    def Generate_Brain(self):
# Start neural network. Give 
        pyrosim.Start_NeuralNetwork("brainFiles/brain" + str(self.myID) + ".nndf") #changed from brain.nndf
# Upper Extremity Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")
# Lower Extremity Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RightLowerLeg")
# Upper Extremity Motor Neurons
        pyrosim.Send_Motor_Neuron( name = 9, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 10, jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 11, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 12, jointName = "Torso_RightLeg")
# Lower Extremity Motor Neurons
        pyrosim.Send_Motor_Neuron( name = 13, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 14, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 15, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 16, jointName = "RightLeg_RightLowerLeg")
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.weights[currentRow][currentColumn] )
        pyrosim.End()


    def Mutate(self): 
        randomRow = random.randint(0,c.numSensorNeurons - 1) #(0,2) represents 0th, 1st, and 2nd rows
        randomColumn = random.randint(0,c.numMotorNeurons - 1) #(0,1) represents 0th and 1st column
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1
        

    def Save_Weights(self):
        if self.continueOrNone == 'continue': # if 'continue', we've already loaded from this file. Edit the constructor to include this.
            with open('weightsFiles/weights' + str(self.overallBot) + '_' + str(self.populationID) + '.txt', 'w') as pickleFile: #let's use botNumber
                np.savetxt(pickleFile,self.weights)
                pickleFile.close()
        else:
            with open('weightsFiles/weights' + str(self.overallBot) + '_' + str(self.populationID) + '.txt', 'w') as pickleFile: # let's use botNumber, not botIndex swarmID*10+botIndex
                np.savetxt(pickleFile,self.weights)
                pickleFile.close()


    def Set_ID(self):
        self.myID

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Generate_Brain() 
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID)+ ' ' + str(self.overallBot) + ' ' + str(self.continueOrNone) + ' ' + str(self.populationID) +" &") # changed from "DIRECT" to directOrGUI... added " &"
    
    def Wait_For_Simulation_To_End(self):
        fitness_file_path = f"fitness{self.myID}.txt"
        while not os.path.exists(fitness_file_path):
            time.sleep(0.01)
        with open(fitness_file_path, 'r') as fitness_file:
            self.fitness = float(fitness_file.read())
        os.remove(fitness_file_path)
        while os.path.exists(fitness_file_path):
            os.remove(fitness_file_path)
            time.sleep(0.01)
