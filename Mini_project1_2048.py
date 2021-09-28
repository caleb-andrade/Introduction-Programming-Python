def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = [0 for i in range(len(line))]
    j = 0
    for x in line:
        if x != 0:
            result[j] = x
            j += 1
    for i in range(len(list(result))-1):
        if result[i] == result[i+1]:
            result[i] = result[i] + result[i+1]
            result.pop(i+1)
            result.append(0)
    return result
            
