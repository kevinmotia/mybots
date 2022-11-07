from solution import SOLUTION 
import constants as c
import copy
import os
import glob
import pybullet as p
#------------------------------------
class PARALLEL_HILL_CLIMBER:
    def __init__(self):
       # os.system("rm brain*.nndf") # step 82 parallelHC
        #os.system("rm fitness*.txt") # step 83 parallelHC
        self.parents = {}

        # This block is for manyBots
        # Start with ID of 0, and check if a brain.nndf file has already occurred. Purpose of this code block is to determine the initial ID after possible prev ParallelHC
    


        numberOfBrainFiles = len(glob.glob("brainFiles/brain*.nndf"))

        if os.path.exists('bestBrains.txt'):
            fp = open('bestBrains.txt', 'r') 
            lines = fp.readlines()
            cleanLines = []
            for entry in lines:
                cleanLines.append(entry.replace('\n',''))
            cleanLines = list(map(int, cleanLines))
            print('Here are bestBrains entries:',cleanLines)
            fp.close()


            self.nextAvailableID = max(cleanLines) + 1
            for i in range(numberOfBrainFiles):
                if os.path.exists('brainFiles/brain'+str(self.nextAvailableID)+'.nndf'):
                    self.nextAvailableID += 1


        else:
            self.nextAvailableID = 0      # we should make it start at something that already exists so the code can iterate to an ID that doesn't exist yet.
            for i in range(numberOfBrainFiles): 
                if os.path.exists("brainFiles/brain"+ str(self.nextAvailableID) + ".nndf"):  
                    self.nextAvailableID += 1

        for i in range(c.populationSize): # this for loop says that there will be 1 file that will be overwritten/evolved per parent. 
            self.parents[i] = SOLUTION(self.nextAvailableID) 
            self.nextAvailableID = self.nextAvailableID + 1

    def Evolve(self): 
        self.Evaluate(self.parents)
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print() # uncommented call to parallelHC print method ... step 107 parallelHC
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in range (len(self.parents)): 
            self.children[i] = copy.deepcopy(self.parents[i])
            self.nextAvailableID = self.nextAvailableID + 1
            


    def Mutate(self):
        for i in range(len(self.children)): # len(self.children) iterates through empty keys too?
            self.children[i].Mutate()

    def Print(self): 
        print('\n')
        for key in range(len(self.parents)):
            print('parents fitness =',self.parents[key].fitness, 'children fitness=',self.children[key].fitness)
        print('\n')

    def Select(self): 
        for key in range(len(self.parents)):
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]
        
    def Show_Best(self):
        overKey = 0                             
        bestFitness = self.parents[0].fitness 
        for i in range(len(self.parents)):
            if self.parents[i].fitness < bestFitness:
                bestFitness = self.parents[i].fitness
                overKey = i
        self.parents[overKey].Start_Simulation("DIRECT") #Shows best single robot sim in GUI
        

        # Write best brain file ID to bestBrains.txt
        bestIDFile = open("bestBrains.txt", "a") 
        bestIDFile.write(str(self.parents[overKey].myID))       
        bestIDFile.write('\n')                              #Write delimiter after brain ID
        bestIDFile.close
        
#--------------------------------------------------------------------------------------------------------------
        # write bestFitness to a file....... only use one of the following blocks at a time

        noObstacleFile = open("emptyEnv_fitnesses.txt", "a")      # Use this one if empty environment.
        noObstacleFile.write(str(bestFitness))
        noObstacleFile.write('\n')
        noObstacleFile.close

        #obstacleFile = open("obstacleEnv_fitnesses", "a")    # Use this if obstacle environment.
        #obstacleFile.write(str(xCoordinateOfLinkZero))
        #obstacleFile.write('\n')
        #obstacleFile.close
        

    #----------------------------------------------------------------------------------------------------------

    def Evaluate(self, solutions):
        for i in range(len(solutions)):
            solutions[i].Start_Simulation("DIRECT") #step 69 parallelHC -- GUI -> DIRECT
        for i in range(len(solutions)):            #step 72 parallelHC... uncomment to activate Parallelism, comment to deactivate Parallelism
            solutions[i].Wait_For_Simulation_To_End()