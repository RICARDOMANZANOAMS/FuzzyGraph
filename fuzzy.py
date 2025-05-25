import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class Fuzzy:
    def __init__(self, inputVariables, outputVariables):
        self.rules = []
        self.ctrlInputs = {}
        self.ctrlOutputs = {}
        # Initialize input variables
        for variable in inputVariables:
            self.ctrlInputs[variable] = None
        # Initialize output variables
        for variable in outputVariables:
            self.ctrlOutputs[variable] = None
        self.controlSystem = None
        self.simulator = None

    def setRangeInput(self, variable, minVal, maxVal, step):
        variableRange = np.arange(minVal, maxVal + step, step)
        self.ctrlInputs[variable] = ctrl.Antecedent(variableRange, variable)

    def setRangeOutput(self, variable, minVal, maxVal, step):
        variableRange = np.arange(minVal, maxVal + step, step)
        self.ctrlOutputs[variable] = ctrl.Consequent(variableRange, variable)

    def defineRuleMF(self, variable, semanticLabel, fuzzRule, minVal, maxVal):
        if fuzzRule == "trig":
            if variable in self.ctrlInputs:
                universe = self.ctrlInputs[variable].universe
                self.ctrlInputs[variable][semanticLabel] = fuzz.trimf(universe, [minVal, (minVal + maxVal) / 2, maxVal])
            elif variable in self.ctrlOutputs:
                universe = self.ctrlOutputs[variable].universe
                self.ctrlOutputs[variable][semanticLabel] = fuzz.trimf(universe, [minVal, (minVal + maxVal) / 2, maxVal])
            else:
                raise ValueError(f"Variable '{variable}' not defined as input or output.")

    def addRule(self, antecedent, consequent):
        """
        antecedent: a ctrl.Antecedent or combination using & | operators
        consequent: a ctrl.Consequent membership, e.g. weight['high']
        """
        rule = ctrl.Rule(antecedent, consequent)
        self.rules.append(rule)

    def buildControlSystem(self):
        self.controlSystem = ctrl.ControlSystem(self.rules)
        self.simulator = ctrl.ControlSystemSimulation(self.controlSystem)

    def compute(self, input_values):
        """
        input_values: dict, e.g. {"power": 70, "cpu": 40}
        """
        if not self.simulator:
            raise RuntimeError("Control system not built. Call buildControlSystem() first.")
        for var, val in input_values.items():
            self.simulator.input[var] = val
        self.simulator.compute()
        outputs = {var: self.simulator.output[var] for var in self.ctrlOutputs}
        return outputs

    def showMembership(self, variable):
        if variable in self.ctrlInputs and self.ctrlInputs[variable] is not None:
            self.ctrlInputs[variable].view()
        elif variable in self.ctrlOutputs and self.ctrlOutputs[variable] is not None:
            self.ctrlOutputs[variable].view()
        else:
            raise ValueError(f"No input or output found for variable '{variable}'.")


# ----------- Usage example -----------

fz = Fuzzy(inputVariables=["batteryLevel","cpuPowerConsumption","wirelessPowerConsumption"], outputVariables=["weight"])

# Set input ranges
fz.setRangeInput("batteryLevel", 0, 100, 1)
fz.setRangeInput("cpuPowerConsumption", 0, 100, 1)
fz.setRangeInput("wirelessPowerConsumption", 0, 100, 1)


# Set output range
fz.setRangeOutput("weight", 1, 100, 1)

# Define input membership functions
fz.defineRuleMF("batteryLevel", "low", "trig", 0, 50)
fz.defineRuleMF("batteryLevel", "medium", "trig", 25, 75)
fz.defineRuleMF("batteryLevel", "high", "trig", 50, 100)

fz.defineRuleMF("cpuPowerConsumption", "low", "trig", 0, 50)
fz.defineRuleMF("cpuPowerConsumption", "medium", "trig", 30, 60)
fz.defineRuleMF("cpuPowerConsumption", "high", "trig", 50, 100)


fz.defineRuleMF("wirelessPowerConsumption", "low", "trig", 0, 50)
fz.defineRuleMF("wirelessPowerConsumption", "medium", "trig", 30, 60)
fz.defineRuleMF("wirelessPowerConsumption", "high", "trig", 50, 100)

# Define output membership functions
fz.defineRuleMF("weight", "low", "trig", 0, 50)
fz.defineRuleMF("weight", "medium", "trig", 30, 75)
fz.defineRuleMF("weight", "high", "trig", 50, 100)

# Define fuzzy rules connecting inputs to output
# Example rules:
fz.addRule(fz.ctrlInputs["batteryLevel"]["low"] & fz.ctrlInputs["cpuPowerConsumption"]["high"]& fz.ctrlInputs["wirelessPowerConsumption"]["high"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["medium"] & fz.ctrlInputs["cpuPowerConsumption"]["high"]& fz.ctrlInputs["wirelessPowerConsumption"]["high"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["high"] & fz.ctrlInputs["cpuPowerConsumption"]["high"]& fz.ctrlInputs["wirelessPowerConsumption"]["high"], fz.ctrlOutputs["weight"]["medium"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["low"] & fz.ctrlInputs["cpuPowerConsumption"]["medium"]& fz.ctrlInputs["wirelessPowerConsumption"]["high"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["low"] & fz.ctrlInputs["cpuPowerConsumption"]["low"]& fz.ctrlInputs["wirelessPowerConsumption"]["high"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["low"] & fz.ctrlInputs["cpuPowerConsumption"]["low"]& fz.ctrlInputs["wirelessPowerConsumption"]["medium"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["low"] & fz.ctrlInputs["cpuPowerConsumption"]["low"]& fz.ctrlInputs["wirelessPowerConsumption"]["low"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["medium"] & fz.ctrlInputs["cpuPowerConsumption"]["medium"]& fz.ctrlInputs["wirelessPowerConsumption"]["high"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["medium"] & fz.ctrlInputs["cpuPowerConsumption"]["low"]& fz.ctrlInputs["wirelessPowerConsumption"]["high"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["medium"] & fz.ctrlInputs["cpuPowerConsumption"]["low"]& fz.ctrlInputs["wirelessPowerConsumption"]["medium"], fz.ctrlOutputs["weight"]["high"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["medium"] & fz.ctrlInputs["cpuPowerConsumption"]["low"]& fz.ctrlInputs["wirelessPowerConsumption"]["low"], fz.ctrlOutputs["weight"]["medium"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["high"] & fz.ctrlInputs["cpuPowerConsumption"]["high"]& fz.ctrlInputs["wirelessPowerConsumption"]["medium"], fz.ctrlOutputs["weight"]["medium"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["high"] & fz.ctrlInputs["cpuPowerConsumption"]["medium"]& fz.ctrlInputs["wirelessPowerConsumption"]["medium"], fz.ctrlOutputs["weight"]["medium"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["high"] & fz.ctrlInputs["cpuPowerConsumption"]["low"]& fz.ctrlInputs["wirelessPowerConsumption"]["medium"], fz.ctrlOutputs["weight"]["medium"])
fz.addRule(fz.ctrlInputs["batteryLevel"]["high"] & fz.ctrlInputs["cpuPowerConsumption"]["low"]& fz.ctrlInputs["wirelessPowerConsumption"]["low"], fz.ctrlOutputs["weight"]["low"])


# Build and initialize control system
fz.buildControlSystem()

# Compute for given inputs
result = fz.compute({"batteryLevel": 99, "cpuPowerConsumption": 1, "wirelessPowerConsumption": 1})

print("Output weight:", result["weight"])
