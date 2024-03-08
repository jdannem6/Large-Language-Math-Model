###############################################################################
## Decription: Defines a class to take an arithmetic expression string and   ##
##             determine and return the atomic subexpression within it       ##
##             having highest precedence                                     ## 
## Last Modified: 8 March 2024                                               ##
###############################################################################
class PrecedenceEvaluator:
    def __init__(self):
        pass

    def __extract_operation(self, expression_str, op_idx):
        start = op_idx - 1
        while start > 0 and expression_str[start].isdigit():
            start -= 1
        end = op_idx + 1
        while end < len(expression_str) and expression_str[end].isdigit():
            end += 1
        return expression_str[start:end+1]
    
    def __determine_nested_levels(self, expression_str):
        nested_levels_list = []
        nested_level = 0
        i = 0
        while i < len(expression_str):
            if expression_str[i] == '(':
                nested_levels_list.append(("", nested_level, i))
                nested_level += 1
            elif expression_str[i] == ')':
                nested_level -= 1
                start_index = None
                for j in range(len(nested_levels_list) - 1, -1, -1):
                    if nested_levels_list[j][1] == nested_level:
                        start_index = nested_levels_list[j][2]
                        nested_levels_list[j] = (expression_str[start_index + 1:i], nested_level, start_index)
                        break
            i += 1
        return nested_levels_list
    
    def __extract_parenth_expr(self, expression_str):
        nested_levels_list = self.__determine_nested_levels(expression_str)
        if not nested_levels_list:
            return ""
        highest_nested = max(nested_levels_list, key=lambda x: x[1])
        return highest_nested[0]
    
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

