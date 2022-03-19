def isBalancedParenthesis(s):
    '''
    checks given string s has a pair of balanced parenthesis or not
    '''
    stack = []
    #used to match corresponding opening tag in stack
    closeToOpen = {
        ')':'(',
        '}':'{',
        ']':'[',
    }
    
    for item in s:
        if item in closeToOpen:
            if stack and stack[-1] == closeToOpen[item]:
                stack.pop()
            else:
                return False
        else:
            stack.append(item)
    return True if not stack else False