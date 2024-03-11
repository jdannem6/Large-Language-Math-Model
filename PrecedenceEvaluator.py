###############################################################################
## Decription: Defines a class to take an arithmetic expression string and   ##
##             determine and return the atomic subexpression within it       ##
##             having highest precedence                                     ## 
## Last Modified: 9 March 2024                                               ##
###############################################################################
import re
class PrecedenceEvaluator:
    def __init__(self):
        self.__last_subexpr_start = 0
        self.__last_subexpr_end = 0
        self.__operators = ["^", "*", "/", "+", "-"]


    def __extract_operation(self, expression_str, op_idx, add_paren_offset = True):
        start = op_idx - 1
        while start > 0 and (expression_str[start].isdigit() 
                             or expression_str[start] == ".") :
            start -= 1

        end = op_idx + 1
        first_char = end
        # For negative operands, skip past the first character
        if expression_str[first_char] == "-":
            end +=1
        while end < len(expression_str) and  (expression_str[end].isdigit()
                                              or expression_str[end] == "."):
            end += 1
        # Determine if first operand is negative
        is_first_op_neg = False
        if expression_str[start] == "-":
            is_first_op_neg = True 
        # If this negative sign is actaully a subtraction, operand is not neg.
        if (start - 1) > 0 and expression_str[start - 1] not in self.__operators:
            operator = expression_str[op_idx]
            if operator not in ["+", "-"]:

                is_first_op_neg = False
            else:
                self.was_add_or_sub = True


        # Index finding loops go one index past last digit; come back one
        # Note: there is no need to come back one if first operand is negative
        if start != 0 and not is_first_op_neg:
            start +=1
        end -= 1
        # Store the start and end index if needed later for substitution
        # purposes. For parenthesis expressions, add the index to the 
        # index of first parenthessis
        """" Adds 1 to both to account for skipped beginning parenthesis. 
             the add_paren_offset prevents this from being added multiple
             times"""
        len_start_paren = 0
        if add_paren_offset:
            len_start_paren = 1
        if self.__is_parenth_operation:
            self.__last_subexpr_end = self.__last_subexpr_start + end + \
                            len_start_paren
            self.__last_subexpr_start = self.__last_subexpr_start + start + \
                                        len_start_paren

        if not self.__is_parenth_operation:
            self.__last_subexpr_start = start
            self.__last_subexpr_end = end


        sub_exp = expression_str[start:end+1]
        return sub_exp
    
    def __determine_nested_levels(self, expression_str):
        nested_levels_list = []
        nested_level = 0
        i = 0
        end_index = -1 # We don't know where subexpression ends until reaching
                       # the terminating parenthesis
        while i < len(expression_str):
            if expression_str[i] == '(':
                start_idx = i
                end_idx = -1
                nested_levels_list.append(("", nested_level, start_idx, end_idx))
                nested_level += 1
            elif expression_str[i] == ')':
                nested_level -= 1
                start_index = None
                for j in range(len(nested_levels_list) - 1, -1, -1):
                    if nested_levels_list[j][1] == nested_level:
                        start_index = nested_levels_list[j][2]
                        end_index = i
                        nested_levels_list[j] = (expression_str[start_index:end_index+1], nested_level, start_index, end_index)
                        break
            i += 1
        return nested_levels_list

    def __extract_parenth_expr(self, expression_str):
        nested_levels_list = self.__determine_nested_levels(expression_str)
        if not nested_levels_list:
            return ""
        most_nested_exp = max(nested_levels_list, key=lambda x: x[1])
        # Store where the parenthesis expression occurs within the string
        start_idx = most_nested_exp[2]
        end_idx = most_nested_exp[3]
        self.__last_subexpr_start = start_idx
        self.__last_subexpr_end = end_idx
        return most_nested_exp[0]
    
    """ Determines if double negative exists in given expression """
    def __has_double_negative(self, expression_str):
        match = re.search(r'-\s*-\s*\d+(\.\d+)?', expression_str)
        if match:
            return True
        else:
            return False
    """ Locates any subexpressions having double negatives in front of an operand
        E.g., 5 - -2. and returns the two indices locating it within the 
        expression. Used to sub cases like --2 for +2
    """
    def __extract_double_negative(self, expression_str):
        match = re.search(r'-\s*-\s*\d+(\.\d+)?', expression_str)
        if match:
            # Extracting the match without spaces for clarity and calculating indices
            extracted = match.group(0).replace(" ", "")
            start =  match.start()
            end = match.end() - 1
            len_start_paren = 1
            """ Refactor this. At the very least, come back and provide names to
                the constants """
            if self.__is_parenth_operation:
                self.__last_subexpr_end = self.__last_subexpr_start + end -1\
                                
                self.__last_subexpr_start = self.__last_subexpr_start + start + \
                                            len_start_paren + 1
            else:
                self.__last_subexpr_start = start
                self.__last_subexpr_end = end
            return extracted
        else:
            return ""
    def __extract_exponentiation(self, expression_str):
        idx = expression_str.find('^')
        if idx != -1:
            return self.__extract_operation(expression_str, idx)
        return ""

    def __extract_mult_divis(self, expression_str):
        mult_idx = expression_str.find('*')
        div_idx = expression_str.find('/')
        if mult_idx == -1 and div_idx == -1:
            return ""
        if mult_idx != -1 and (div_idx == -1 or mult_idx < div_idx):
            return self.__extract_operation(expression_str, mult_idx)
        if div_idx != -1:
            return self.__extract_operation(expression_str, div_idx)
        
    def __extract_add_sub(self, expression_str):
        add_idx = expression_str.find('+')
        sub_idx = expression_str.find('-')
        if add_idx == -1 and sub_idx == -1:
            return ""
        # Perform the math operation if it exist and comes before the
        # the subtraction (if exists) of if the "subtraction" is actually 
        # a negative number
        if add_idx != -1 and (sub_idx == -1 or add_idx < sub_idx or \
                              self.is_constant(self.__extract_operation(expression_str, sub_idx, 
                                                                        add_paren_offset=False))):
            return self.__extract_operation(expression_str, add_idx, add_paren_offset = True)
        # Otherwise perform the subtraction operation
        if sub_idx != -1:
            # If the expression is a subtraction operation, return it
            sub_expr =  self.__extract_operation(expression_str, sub_idx, add_paren_offset=True)
            if not self.is_constant(sub_expr):
                return sub_expr
            # Otherwise if the extracted operation is actually just a negative
            # constant, search for other subtraction operations
            else:
                next_sub_idx = expression_str.find('-', sub_idx + 1)
                while (self.is_constant(sub_expr) and next_sub_idx != -1):
                    sub_expr = self.__extract_operation(expression_str, next_sub_idx, 
                                                        add_paren_offset=False)
                return sub_expr

    """
    Determines if a given string subexpression represents only a constant. 
    """
    def is_constant(self, sub_expr):

        # Remove surrounding parentheses if they exist
        if sub_expr.startswith("(") and sub_expr.endswith(")"):
            sub_expr= sub_expr[1:-1]

        # Check if the subexpression matches the pattern of a negative constant
        if sub_expr.startswith("-"):
            # Check if the rest of the subexpression is a valid number (integer or float)
            sub_expr = sub_expr[1:]
        try:
            float(sub_expr)
            return True  # The subexpression is a valid negative constant
        except ValueError:
            return False  # The subexpression is not a valid number, hence not a negative constant


    """ Returns the highest precedence subexpression and the start and 
        end index at which it occurs within the expression string"""
    def next_subexpression(self, expression_str):
        # Flag to track whether the operation is parenthesis operation. This  
        # is only necessary for tracking indices properly for parenthesis expressions
        self.__is_parenth_operation = False
        if '(' in expression_str or ')' in expression_str:
            # Get the highest precedence parenthesis-enclosed subexpression
            # This subexpression may contain more than one operations;
            # determine its highest precedence operations within it
            # using EMDAS rules 
            self.__is_parenth_operation = True
            sub_exp = self.__extract_parenth_expr(expression_str)
            # Remove outer parenthesis from the extracted expression and pass it
            # to the next functions
            expression_str = sub_exp[1:-1]
        # Search for any double negatives
        if self.__has_double_negative(expression_str):
            sub_exp = self.__extract_double_negative(expression_str)
            # Set flag to replace double negative with + in the 
            # Expression Evaluator
            self.was_double_negative = True
        elif '^' in expression_str:
            sub_exp = self.__extract_exponentiation(expression_str)
        elif '*' in expression_str or '/' in expression_str:
            sub_exp = self.__extract_mult_divis(expression_str)
        elif '+' in expression_str or '-' in expression_str:
            sub_exp = self.__extract_add_sub(expression_str)
        # Otherwise, if the subexpression is a postive or negative constant
        # Remove the parenthesis from the expression
        if (self.is_constant(sub_exp)) and self.__is_parenth_operation:
            if sub_exp.startswith("(") and sub_exp.endswith(")"):
                sub_exp= sub_exp[1:-1]
            " Revisit this; not sure why this fixed issue"
            if sub_exp.startswith("-"):
                self.__last_subexpr_start -=1
                self.__last_subexpr_end +=1
        return (sub_exp, self.__last_subexpr_start, self.__last_subexpr_end)
        
def main():
    expression = "(3+(2+3+3^4))*(3+2)"
    print("original expression:", expression)
    my_pe = PrecedenceEvaluator()
    result_str = my_pe.next_subexpression(expression)
    print(result_str)

if __name__ == "__main__":
    main()
