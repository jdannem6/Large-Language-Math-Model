###############################################################################
## Decription: Generates a dataset of integer arithmetic expressions to be   ##
##             evaluated for an LLM                                          ##
## Last Modified: 11 March 2024                                              ##
###############################################################################

import numpy as np
import sympy as sp

class ExpressionGenerator:
    def __init__(self, num_samples=100, min_value=1, max_value=100, operators=['*', '/', '+', '-'], max_nesting=3):
        self.num_samples = num_samples
        self.min_value = min_value
        self.max_value = max_value
        self.operators = operators
        self.max_nesting = max_nesting
        # self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    def generate_operand(self):
        """Generate a single operand within the specified range."""
        return str(np.random.randint(self.min_value, self.max_value))
    def generate_operator(self):
        """Randomly select an operator."""
        return np.random.choice(self.operators)
    def needs_parentheses(self, prev_operator, current_operator, is_right):
        """Determine if parentheses are needed based on operator precedence and associativity."""
        if prev_operator is None or current_operator is None:
            return False
        if self.precedence[current_operator] > self.precedence[prev_operator]:
            return False  # Higher precedence operations don't need parentheses
        if self.precedence[current_operator] == self.precedence[prev_operator]:
            if current_operator == '^':  # '^' is right associative
                return not is_right  # Only add parentheses if it's the right operand in a previous '^' operation
            return False  # Same precedence but not '^', so no parentheses needed
        return True
    def generate_expression(self, nesting_level=0, prev_operator=None, is_right=False):
        """Generate an arithmetic expression, using parentheses only when mathematically necessary."""
        if nesting_level >= self.max_nesting:
            return self.generate_operand()
        expression = ""
        for i in range(np.random.randint(2, 4)):  # Determine number of parts in this expression
            current_operator = self.generate_operator() if i > 0 else None
            if i > 0:  # Add operator before every operand except the first one
                expression += f" {current_operator} "
            if nesting_level + 1 < self.max_nesting and np.random.choice([True, False]):
                sub_expr = self.generate_expression(nesting_level + 1, current_operator, i > 0)
                if i > 0 and self.needs_parentheses(prev_operator, current_operator, i < 2):
                    expression += f"({sub_expr})"
                else:
                    expression += sub_expr
            else:
                expression += self.generate_operand()
            prev_operator = current_operator
        return expression
    def generate_dataset(self):
        """Generates a dictionary containing indexed arithmetic expressions."""
        dataset = {}
        i = 0
        while i < self.num_samples:
            next_expression = self.generate_expression()
            # Only insert the expression in the dataset if there are no divide by zero issues
            try:
                expression = sp.sympify(next_expression)
                subexpr_result = str(float(expression.evalf()))
                # Since a result was obtained, its safe to add if it does already exist
                if next_expression not in dataset.values() and subexpr_result != "nan":
                    dataset[i] = next_expression
                    i += 1
            # if the expression string could not be evaluated, it has errors;
            # don't add to dataset
            except:
                continue
        return dataset
    

def main():
    # Generate a dataset with optimized logic for parentheses
    generator = ExpressionGenerator(num_samples=10, min_value=0, max_value=100, max_nesting=2)
    dataset = generator.generate_dataset()
    # Output a few samples from the optimized dataset
    samples = list(dataset.items())
    # for __, item in samples:
    #     print(item)
    
if __name__ == "__main__":
    main()