###############################################################################
## Decription: Defines a class to take an arithmetic expression string and   ##
##             determine and return the atomic subexpression within it       ##
##             having highest precedence                                     ## 
## Last Modified: 8 March 2024                                               ##
###############################################################################
class PrecedenceEvaluator:
    def __init__(self):
        pass
    def __extract_add_sub(self, expression_str):
        add_idx = expression_str.find('+')
        sub_idx = expression_str.find('-')
        if add_idx == -1 and sub_idx == -1:
            return ""
        if add_idx != -1 and (sub_idx == -1 or add_idx < sub_idx):
            return self.__extract_operation(expression_str, add_idx)
        if sub_idx != -1:
            return self.__extract_operation(expression_str, sub_idx)

