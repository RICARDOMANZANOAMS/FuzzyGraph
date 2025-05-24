class Node:
    def __init__(self, nameNode, CPUPowerCon, wirelessPowerCon):
        self.nameNode = nameNode
        self.CPUPowerCon = CPUPowerCon
        self.wirelessPowerCon = wirelessPowerCon
        self.energy = 100
    

    def calculateNodeEnergy(self):
        self.energy = self.energy - (self.CPUPowerCon+ self.wirelessPowerCon)
        


def calculateFuzzy(energy1, energy2):
    avg_energy = (energy1 + energy2) / 2
    if avg_energy >= 90:
        return 10
    elif avg_energy >= 80:
        return 20
    elif avg_energy >= 70:
        return 30
    elif avg_energy >= 60:
        return 40
    elif avg_energy >= 50:
        return 50
    elif avg_energy >= 60:
        return 60
    elif avg_energy > 20:
        return 80
    elif avg_energy > 0:
        return 100
   


class Graph:
    def __init__(self):
        self.adjacent_matrix = {}
        self.nodes = {}

    def addNode(self, nameNode, CPUPowerCon, wirelessPowerCon):
        if nameNode not in self.nodes:
            nodeObj = Node(nameNode, CPUPowerCon, wirelessPowerCon)
            nodeObj.calculateNodeEnergy()
            self.nodes[nameNode] = nodeObj
            self.adjacent_matrix[nameNode] = []

    def addConnection(self, node1Info, node2Info):
        node1Name, node1CPU, node1Wireless = node1Info
        node2Name, node2CPU, node2Wireless = node2Info

        self.addNode(node1Name, node1CPU, node1Wireless)
        self.addNode(node2Name, node2CPU, node2Wireless)

        node1Energy = self.nodes[node1Name].energy
        node2Energy = self.nodes[node2Name].energy

        valueWeight = calculateFuzzy(node1Energy, node2Energy)

        if node2Name not in [n[0] for n in self.adjacent_matrix[node1Name]]:
            self.adjacent_matrix[node1Name].append((node2Name, valueWeight))
        if node1Name not in [n[0] for n in self.adjacent_matrix[node2Name]]:
            self.adjacent_matrix[node2Name].append((node1Name, valueWeight))

    def findBestPath(self,node1,node2):
        nodes=self.adjacent_matrix.keys()
        predecessors={}
        costs={}
        for node in nodes:
            if node==node1:
                costs[node]=0
            else:
                costs[node]=999
            predecessors[node]=None
        count=0
        for i in range(0,len(nodes)):
            count=count+1
            updated = False
            for node, neighbors in self.adjacent_matrix.items():
                for neighbor, weight in neighbors:
                    if (costs[node]+weight)<costs[neighbor]:
                        costs[neighbor]=costs[node]+weight
                        predecessors[neighbor]=node
                        updated = True  # Change detected
            
            if not updated:
                print(count)
                print("predecessors")
                print(predecessors)   
                break  
       
        path = []
        current = node2
        while current is not None:
            path.insert(0, current)
            current = predecessors[current]
        print(path)


# Test
g = Graph()
A=('A', 10, 10)
B=('B', 30, 30)
C=('C', 10, 10)
D=('D', 30, 30)
E=('E', 40, 40)
F=('F', 20, 20)
G=('G', 1, 1)
g.addConnection(A, B)
g.addConnection(A, C)
g.addConnection(A, D)
g.addConnection(B, E)
g.addConnection(C, D)
g.addConnection(C, E)
g.addConnection(C, F)
g.addConnection(D,F)
g.addConnection(E, F)
g.addConnection(E, G)
g.addConnection(F, G)
g.findBestPath('A','G')



