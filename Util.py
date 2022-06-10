import numpy as np

def local_max(arr, N = 2, strict = False):
    '''find local maximums of an array where local is defined as M points on either side, if strict is true
    then it will follow this process exactly if strict is false it will also count local maxes that are at least
    one space from the edge if they satisfy the requirement within the remaining array'''
    local_maxs = []
    M = int(N/2)
    
    #loop through the array
    if not strict:
        i = 1

    else:
        i = M

    indexes = []
    
    while i < len(arr) - 1:
        
        iterate = 1
        #flag
        local_max = True
        
        for j in range(M):
            try:
                #will make index error when your with M of the edges so except index error
                if arr[i] < arr[i + j]:
                    local_max = False
                    iterate = j
                    break

            except IndexError:
                if strict:
                    #reproduce old behaviour
                    local_max = False
                    break
                #other wise search in the other direction
                
            try:
                if arr[i] < arr[i - j]:
                    local_max = False
                    break

            except IndexError:
                if strict:
                    local_max = False
                    break

            
        if local_max:
            local_maxs.append(arr[i])
            indexes.append(i)
            
        i += iterate
        
    return np.array(local_maxs), np.array(indexes)