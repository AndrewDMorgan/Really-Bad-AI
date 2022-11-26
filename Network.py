import random


# the network class to deal with everything
class Network:

    # setting up the layers and weights
    def __init__(self, numInputs: int, numNodes: list, layerWeights: list = []) -> None:
        self.numNodes = numNodes
        self.numInputs = numInputs

        if layerWeights == []:
            self.layerWeights = []
            self.layerWeights.append([[0 for i in range(self.numInputs)] for i in range(self.numNodes[0])])
            
            i = 0
            for l in self.numNodes[1:]:
                self.layerWeights.append([[0 for i_ in range(len(self.layerWeights[i]))] for i__ in range(l)])
                i += 1
        else:
            self.layerWeights = layerWeights

    # inits with all values
    def Init(self, layerWeights: list, numInputs: int, numNodes: list) -> None:
        self.layerWeights = layerWeights
        self.numInputs = numInputs
        self.numNodes = numNodes
    
    # randomly mutates all the genes
    def Mutate(self, amp: float, minV: float, maxV: float) -> None:
        layerI = 0
        for layer in self.layerWeights:
            for nodeI in range(len(layer)):
                for weightI in range(len(layer[nodeI])):
                    self.layerWeights[layerI][nodeI][weightI] = min(max(self.layerWeights[layerI][nodeI][weightI] + random.uniform(-amp, amp), minV), maxV)
            layerI += 1
    
    # gets a new object with the mutations
    def GetMutated(self, amp: float, minV: float, maxV: float) -> object:
        newWeights = []

        layerI = 0
        for layer in self.layerWeights:
            newLayer = []
            for nodeI in range(len(layer)):
                newNode = []
                for weightI in range(len(layer[nodeI])):
                    newNode.append(self.layerWeights[layerI][nodeI][weightI])
                newLayer.append(newNode)
            newWeights.append(newLayer)
            layerI += 1

        newNet = Network(self.numInputs, self.numNodes, newWeights)
        newNet.Mutate(amp, minV, maxV)
        
        return newNet

    # getting the output
    def Calc(self, input: list) -> float:
        output = []
        for l in self.numNodes:
            output.append([0 for i in range(l)])
        
        layerI = 0
        for layer in self.layerWeights:
            for nodeI in range(len(layer)):
                sum = 0
                weightI = 0
                for weight in layer[nodeI]:
                    sum += input[weightI] * weight
                    weightI += 1
                
                output[layerI][nodeI] = sum
            input = output[layerI]
            layerI += 1
        
        return output[len(output) - 1]





# the random network to evolve from
baseNetwork = Network(1, [3, 3, 3, 1])

current = [-1, 10000000]

# evolving the network many times getting the best version each time
for evo in range(1000):
    # creating 50 copies with slight variations of the best ai (starting out with a random one)
    networks = []
    for i in range(50):
        newNet = baseNetwork.GetMutated(0.075, -99, 99)
        networks.append(newNet)
    
    # looping through the networks and getting the error
    i = 0
    closest = [-1, 10000000]  # index, error (heigher is worse)
    for network in networks:
        # getting the average error
        error  = abs( 1 - network.Calc([-1])[0])
        error += abs(     network.Calc([ 0])[0])
        error += abs(-1 - network.Calc([ 1])[0])

        if error < closest[1]:
            closest = [i, error]

        i += 1
    
    # checking if the new lowest is better or the same
    if closest[1] <= current[1]:
        baseNetwork = networks[closest[0]]
        current = closest


# checking the results using the ai sense -x is to hard to calculate
print("-1: ", network.Calc([-1]))
print("0: " , network.Calc([ 0]))
print("1: " , network.Calc([ 1]))
