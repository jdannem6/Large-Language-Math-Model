###############################################################################
## Decription: Defines a class to take an arithmetic expression string and   ##
##             determine and return the atomic subexpression within it       ##
##             having highest precedence                                     ## 
## Last Modified: 8 March 2024                                               ##
###############################################################################
class PrecedenceEvaluator:
    def __init__(self):
        pass
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
        if add_idx != -1 and (sub_idx == -1 or add_idx < sub_idx):
            return self.__extract_operation(expression_str, add_idx)
        if sub_idx != -1:
            return self.__extract_operation(expression_str, sub_idx)

