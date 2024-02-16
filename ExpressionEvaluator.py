###############################################################################
## Decription: Takes a dataset of arithmetic expressions and processes it    ##
##             to create an alternative datset with the following            ##
##             properties:                                                   ##
##             1) Dataset is stored as a dictionary                          ##
##             2) Each key is the string form of the expression to be eval.  ##
##             3) Each key corresponds to another dictionary containing 3    ##
##                elements with:                                             ##
##                a) "eval_steps": a list of steps to solve the expression,  ##
##                   which terminates with the final step being the value    ##
##                b) "operator_counts": a string counting the total number   ##
##                   of occurences of each operator                          ##
##                c) "operand counts": a string detailing the total number   ##
##                    of occurences of each operand                          ##
## Last Modified: 16 Feb 2024                                                ##
###############################################################################

import numpy as np
from DatasetGenerator import ArithDatasetGen


class ExpressionEvaluator():
    def __init__(self, raw_dataset):
        self.__raw_dataset = raw_dataset
        self.__processed_dataset = {}
    """ Gets two operands from a string containing an atomic expression and 
        and returns them as an ordered pair"""
    def __get_operands(self, sub_expression):
        sub_expression = sub_expression.replace('(', "").replace(')', "")
        print(sub_expression)
        operand1 = int(sub_expression.split('*')[0])
        operand2 = int(sub_expression.split('*')[-1])
        return (operand1, operand2)
    
    """ Given an arithmetic expression, creates a ditionary mapping operator 
        and parentheses to the order in which they occur
        param[in] tokens: A list of tokens to count within the string. E.g.,
                          the operators or the operands to search for.
    """
    def __get_counts(self, tokens, raw_sample_str, count_operands=False):
        counts = {}
        for char in raw_sample_str:
            # Count the operators and parentheses
            if not count_operands:
                if char in tokens:
                    if char not in counts:
                        counts[char] = 1
                    else:
                        counts[char] = counts[char] + 1
            # Otherwise, count the operands
            else:
                if char not in tokens:
                    if char not in counts:
                        counts[char] = 1
                    else:
                        counts[char] = counts[char] + 1
        return counts
    """ Converts the string form describing the expression to a dictionary of 
        steps where each key is the step index and each value is the string
        describing the partially simplified expression for that step"""
    def __get_eval_steps(self, raw_sample_str):
        eval_steps = {}
        sub_expressions = [sub_exp + ')' for sub_exp in raw_sample_str.split(')') if sub_exp]
        sub_exp1 = sub_expressions[0] 
        sub_exp2 = sub_expressions[1].split('+')[-1]


        sub_exp1_operands = self.__get_operands(sub_exp1)
        sub_exp2_operands = self.__get_operands(sub_exp2)

        eval_steps[1] = f"{sub_exp1_operands[0]*sub_exp1_operands[1]}+{sub_exp2}"
        eval_steps[2] = f"{sub_exp1_operands[0]*sub_exp1_operands[1]}+{sub_exp2_operands[0]*sub_exp2_operands[1]}"
        eval_steps[3] = f"{sub_exp1_operands[0]*sub_exp1_operands[1]+sub_exp2_operands[0]*sub_exp2_operands[1]}"
        return eval_steps
    
    """ Generates the operator counts, operand counts, and the steps for a given 
        raw expression sample. Returns dictionary mapping the expression to 
        these three dictionaries """
    def process_sample(self, raw_sample_str):

        eval_steps =  self.__get_eval_steps(raw_sample_str)
        operator_tokens = [')', '(', '[', ']', '*', '+']
        operator_counts = self.__get_counts(operator_tokens, raw_sample_str, count_operands=False)
        operand_counts = self.__get_counts(operator_tokens, raw_sample_str, count_operands=True)

        return (eval_steps, operator_counts, operand_counts)
    
    """ Generates the dataset of arithmetic expressions with the steps to solve them """
    def process_dataset(self):
        for raw_sample in self.__raw_dataset:
            eval_steps, operator_counts, operand_counts = self.process_sample(raw_sample)
            self.__processed_dataset[raw_sample] = {"eval_steps": eval_steps,
                                                    "operator_counts": operator_counts,
                                                    "operand_counts": operand_counts}
        return self.__processed_dataset



def main():
    raw_datagen = ArithDatasetGen(num_samples=10 , lower_bound=0, upper_bound=5)
    raw_dataset = raw_datagen.generate_new_dataset()
    expression_evaluator = ExpressionEvaluator(raw_dataset)
    processed_dataset = expression_evaluator.process_dataset()
    print(processed_dataset)

if __name__ == "__main__":
    main()
