###############################################################################
## Decription: Generates a dataset of integer arithmetic expressions to be   ##
##             evaluated for an LLM                                          ##
## Last Modified: 16 Feb 2024                                                ##
###############################################################################

import numpy as np

class ArithDatasetGen():
    def __init__(self, num_samples, lower_bound, upper_bound):
        self.__num_samples = num_samples
        self.__lower_bound = lower_bound
        self.__upper_bound = upper_bound
        self.dataset = []

    def generate_sample(self):
        operands = np.random.randint(low=self.__lower_bound, high=self.__upper_bound,
                                 size = 4)
        expression = f"({operands[0]}*{operands[1]})+({operands[2]}*{operands[3]})"
        return expression
    def generate_new_dataset(self):
        self.dataset = []
        for i in range(self.__num_samples):
            self.dataset.append(self.generate_sample())
        return self.dataset

def main():
    datagen = ArithDatasetGen(num_samples = 10, lower_bound= 0, upper_bound= 100)
    datagen.generate_new_dataset()
    print(datagen.dataset)
    print(datagen.dataset[0].split(')')[0])

if __name__ == "__main__":
    main()