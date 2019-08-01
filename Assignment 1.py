import random
from prettytable import PrettyTable
import time

test0 = random.sample(xrange(1000), 1000)
test1 = random.sample(xrange(10000), 10000)
test2 = random.sample(xrange(100000), 100000)


def merge(left, center, right):
    sorted = []
    
    left.append(float("inf"))
    center.append(float("inf"))
    right.append(float("inf"))
    
    i = 0
    j = 0
    k = 0
    
    while len(sorted) < (len(left) + len(center) + len(right)) - 3:
        sorted.append(min(left[i], center[j], right[k]))
        if min(left[i], center[j], right[k]) == left[i]:
            i += 1
        elif min(left[i], center[j], right[k]) == center[j]:
            j += 1
        elif min(left[i], center[j], right[k]) == right[k]:
            k += 1
    return sorted

def threewaymergesort(arr):
    
    if len(arr) < 2:
        return arr
    if len(arr) % 3 == 0:
        m1 = len(arr) / 3
        m2 = len(arr) / 3 * 2
    else:
        m1 = len(arr) / 3 + 1
        m2 = len(arr) / 3 * 2 + 1
    
    left = arr[:m1]
    center = arr[m1:m2]
    right = arr[m2:]
    
    left = threewaymergesort(left)
    center = threewaymergesort(center)
    right = threewaymergesort(right)
    
    return merge(left, center, right)

start_time1 = time.time()

arr = [12, 11, 13, 5, 6, 7, 19, 200, 57, 2, 66, 18, 32, 74, 1, 28]
threewaymergesort(test0)

end_time1 = time.time()
totaltime1 = end_time1 - start_time1
print totaltime1

#referenced insertion sort code from GeeksforGeeks

def threewaymergeaug(left, center, right):
    sorted = []
    
    left.append(float("inf"))
    center.append(float("inf"))
    right.append(float("inf"))
    
    i = 0
    j = 0
    k = 0

    
    while len(sorted) < (len(left) + len(center) + len(right)) - 3:
        sorted.append(min(left[i], center[j], right[k]))
        if min(left[i], center[j], right[k]) == left[i]:
            i += 1
        elif min(left[i], center[j], right[k]) == center[j]:
            j += 1
        elif min(left[i], center[j], right[k]) == right[k]:
            k += 1
    return sorted


def insertionsort(arr):
    for i in range(1, len(arr)): 
        key = arr[i] 
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key 


def threewaymergesortaug(arr):
    
    if len(arr) < 2:
        return arr
    if len(arr) % 3 == 0:
        m1 = len(arr) / 3
        m2 = len(arr) / 3 * 2
    else:
        m1 = len(arr) / 3 + 1
        m2 = len(arr) / 3 * 2 + 1

    
    left = arr[:m1]
    center = arr[m1:m2]
    right = arr[m2:]

    
    if len(left) < 10:
        insertionsort(left)
    if len(center) < 10:
        insertionsort(center)
    if len(right) < 10:    
        insertionsort(right)
    else:
        left = threewaymergesortaug(left)
        center = threewaymergesortaug(center)
        right = threewaymergesortaug(right)
    
    return threewaymergeaug(left, center, right)

start_time2 = time.time()

arr = [12, 11, 13, 5, 6, 7, 19, 200, 57, 2, 66, 32, 18, 74, 1, 30, 76, 3]
threewaymergesortaug(test0)

end_time2 = time.time()
totaltime2 = end_time2 - start_time2
print totaltime2

def twowaymerge(left, right):
    sorted = []
    
    left.append(float("inf"))
    right.append(float("inf"))
    
    i = 0
    j = 0
    
    while len(sorted) < (len(left) + len(right)) - 2:
        sorted.append(min(left[i], right[j]))
        if min(left[i], right[j]) == left[i]:
            i += 1
        elif min(left[i], right[j]) == right[j]:
            j += 1
    return sorted


def twowaymergesort(arr):
    
    if len(arr) < 2:
        return arr
    else:
        m = len(arr) / 2
    
    left = arr[:m]
    right = arr[m:]
    
    left = twowaymergesort(left)
    right = twowaymergesort(right)
    
    return twowaymerge(left, right)


start_time3 = time.time()

arr = [12, 11, 13, 5, 6, 7, 19, 200, 57, 2, 66, 32, 18, 74, 1, 30, 76, 3]
twowaymergesort(test0)

end_time3 = time.time()
totaltime3 = end_time3 - start_time3
print totaltime3

t = PrettyTable(['Algorithm', 'Running time for 1000', 'Running time for 10000', 'Running time for 100000'])
t.add_row(['Merge Sort', 0.0145320892334,0.126022815704, 1.5960278511])
t.add_row(['3-way Merge Sort',0.00873994827271, 0.115930080414, 1.37388777733])
t.add_row(['Aug. 3-way Merge Sort', 0.00775289535522, 0.0856940746307, 1.11245012283])
print t
