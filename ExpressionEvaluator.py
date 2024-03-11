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
## Last Modified: 8 March 2024                                               ##
###############################################################################

import sympy as sp
import numpy as np
from DatasetGenerator import ArithDatasetGen
from PrecedenceEvaluator import PrecedenceEvaluator
import re # Needed for extracting operands and operators from regular 
          # expressions
import math



"""
    Searches for numbers within an arithmetic expression string that are written in scientific notation
    (e.g., 2.541e-05) and converts those numbers to a string form that doesn't use scientific notation.
"""

def convert_sci_notation_terms(expression):

    # Regular expression to find numbers in scientific notation
    sci_notation_regex = r'\b\d+\.?\d*[eE][+-]?\d+\b'

    def replace_sci_notation(match):
        # Convert the scientific notation number to decimal
        # and format it to remove trailing zeros
        number = float(match.group())
        return '{:f}'.format(number).rstrip('0').rstrip('.')

    # Use re.sub() to replace all occurrences of scientific notation in the expression
    return re.sub(sci_notation_regex, replace_sci_notation, expression)


class ExpressionEvaluator():
    def __init__(self, raw_dataset):
        self.__raw_dataset = raw_dataset
        self.__processed_dataset = {}
        self.precedence_eval = PrecedenceEvaluator()

    """ Converts a list of symbol occurrences to a dictionary giving
        the total number of occurences for each symbol. Used for 
        determing operator and operand counts """
    def __convert_to_count_dict(self, list_of_occurrences):
        counts_dict = {}
        for symbol in list_of_occurrences:
            # Set count to 1 for any symbol the first time its occurred
            if symbol not in counts_dict:
                counts_dict[symbol] = 1
            # Increment count for subsequent encounters of symbol
            else:
                counts_dict[symbol] += 1
        return counts_dict
    
    """ Creates a dictionary mapping each operand to the number of times it 
        occurs within the expression """
    def __get_operand_counts(self, expression_str):
        # Create a pattern to define the format of the operands in the 
        # arithmetic string
        operand_pattern = r'\b\d+\b' #\b - word break, \d a digit
        operands_in_expression = re.findall(operand_pattern, expression_str)

        ## Get the total numer of counts for all the operators in the 
        ## expression
        operand_counts = self.__convert_to_count_dict(operands_in_expression)
        return operand_counts
    
    """ Creates a dictionary mapping each operator (including parenthesis) 
        to the number of times it  occurs within the expression """
    def __get_operator_counts(self, expression_str):
        # Create a pattern to define the format of operators to serach
        # for in the string
        operator_pattern = r'[\^\*/\+\-\(\)]'
        operators_in_expression = re.findall(operator_pattern, expression_str)
        ## Get the total numer of counts for all the operators in the 
        ## expression
        operator_counts = self.__convert_to_count_dict(operators_in_expression)
        return operator_counts       
    """ Simple helper function to determine if expression is fully simplified
        based on whether operators still exist within it """
    def __is_solved(self, expression_str):
        # Create a pattern to define the format of operators to search
        # for in the string
        operator_pattern = r'[\^\*/\+\-\(\)]'
        operators_in_expr = re.findall(operator_pattern, expression_str)
        # Expression is solved if there are no operators left in string or for negative numbers
        # if there is just one with a constant expression (a negative number)
        expression_is_solved = len(operators_in_expr) == 0 or \
                               "-" in expression_str  and \
                                 self.precedence_eval.is_constant(expression_str)
        return expression_is_solved
    
    """ Converts the string form describing the expression to a dictionary of 
        steps where each key is the step index and each value is the string
        describing the partially simplified expression for that step"""
    def __get_eval_steps(self, expression_str):
        eval_steps = {}
        i = 0
        # print("\n\n\nOriginal expression:", expression_str)
        while not self.__is_solved(expression_str):
            self.precedence_eval.was_add_or_sub = False
            self.precedence_eval.was_double_negative = False
            # Determine the highest precedence subexpression within the
            # expression string
            next_subexpr, start_idx, end_idx = \
                self.precedence_eval.next_subexpression(expression_str)
            # Solve the atomic subexpression
            # print("expression so far:", expression_str)
            # print("sub expression:", next_subexpr)
            subexp = sp.sympify(next_subexpr)
            subexpr_result = str(float(subexp.evalf())) # float needed due to sympys unnecessary precision
            ## Substitute the result back into the original expression
            # Add addition character back into the expression if there was a double negative
            # or if there was an addition or subtraction operation with the first operand being negative
            addition_char = ""
            if (self.precedence_eval.was_add_or_sub and start_idx != 0)\
                or self.precedence_eval.was_double_negative:
                addition_char = "+"
            expression_str = expression_str[:start_idx] + addition_char + subexpr_result \
                            + expression_str[end_idx+1:]
            # Convert any values in from scientific notation to standard form
            expression_str = convert_sci_notation_terms(expression_str)

            eval_steps[i] = expression_str
            i +=1
        return eval_steps
    """ Generates the operator counts, operand counts, and the steps for a given 
        raw expression sample. Returns dictionary mapping the expression to 
        these three dictionaries """
    def process_sample(self, raw_sample_str):
        eval_steps =  self.__get_eval_steps(raw_sample_str)
        operator_counts = self.__get_operator_counts(raw_sample_str)
        operand_counts = self.__get_operand_counts(raw_sample_str)

        return (eval_steps, operator_counts, operand_counts)
    """ Generates the dataset of arithmetic expressions with the steps to solve them """
    def process_dataset(self):
        for raw_sample in self.__raw_dataset:
            # raw_sample = raw_sample.replace(" ", "")
            print(raw_sample)
            eval_steps, operator_counts, operand_counts = self.process_sample(raw_sample)
            self.__processed_dataset[raw_sample] = {"eval_steps": eval_steps,
                                                    "operator_counts": operator_counts,
                                                    "operand_counts": operand_counts}
        return self.__processed_dataset

def main():
    raw_datagen = ArithDatasetGen(num_samples=10 , lower_bound=0, upper_bound=5)
    # raw_dataset = raw_datagen.generate_new_dataset()
    # raw_dataset  = ["9*1-5*5+(2-8*4-8*11-(2-2*10))"]
    raw_dataset = ["5-10*0+7+1+10*7*3+(7*8)*4+7"]
    expression_evaluator = ExpressionEvaluator(raw_dataset)

    # print(f"original expression: {test_expression}")
    processed_dataset = expression_evaluator.process_dataset()
    for expression in raw_dataset:
        eval_steps = list(processed_dataset[expression]['eval_steps'].values())
        computed_result = float(eval_steps[-1])
        sympy_expression = sp.sympify(expression)
        true_result = float(sympy_expression.evalf())
        # assert type(computed_result) == type(true_result)
        print("True result: ", true_result)
        print("computed result:", computed_result)
        print("True result: ", true_result)
        print("computed result:", computed_result)
    print(processed_dataset)

# original_expressions = processed_dataset.keys()
    
#     # Check that all the computed results are near their true values
#     all_results_close = True
#     debug_mode = True
#     num_right = 0
#     for expression in original_expressions:




if __name__ == "__main__":
    main()