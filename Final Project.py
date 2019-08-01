from itertools import combinations
from statistics import mean

### Courses ###


class Course:
    
    def __init__(self, name):
        self.name = name
        self.prereq = None
        self.timecommit = 0
        # Takes the first two letters of the course name, which is the 
        # abbreviation of the college it belongs to
        self.college = name[0]+name[1] 
    
    # function for indicating the prerequisites for the given course
    def needs(self, node):
        self.prereq = node
    
    # function for indicating the overall workload of the course 
    # (readings, pre-class work, etc)
    def time(self, time):
        self.timecommit = time


### Setting up the courses ###

# Courses and names
cs110 = Course("cs110")
cs111 = Course("cs111")
cs112 = Course("cs112")
cs152 = Course("cs152")
cs156 = Course("cs156")
cs166 = Course("cs166")
ss110 = Course("ss110")
ss111 = Course("ss111")
ss144 = Course("ss144")
ss154 = Course("ss154")
ss142 = Course("ss142")

# Courses and time commitment
cs110.time(3)
cs111.time(2)
cs112.time(2)
cs152.time(4)
cs156.time(4)
ss110.time(1)
ss111.time(1)
ss144.time(2)
ss154.time(3)
cs166.time(4)
ss142.time(2)

# Courses and prerequisites (if any)
cs152.needs(cs110)
cs156.needs(cs110)
cs166.needs(cs112)
ss142.needs(ss110)
ss144.needs(ss111)
ss154.needs(ss111)


### Function for finding the element with the closest value to a certain target ###
# adapted from a code found on:
# https://www.geeksforgeeks.org/find-closest-number-array/
# to search from the workload averages (second elements in the tuples)

def findClosest(arr, n, target): 
  
    # Corner cases 
    if target <= arr[0][1]: 
        return arr[0][1] 
    if target >= arr[n - 1][1]: 
        return arr[n - 1][1]
  
    # Binary Search
    i = 0
    j = n
    mid = 0
    
    while i < j:
        # getting midpoint
        mid = (i + j) / 2
  
        if arr[mid] == target: 
            return arr[mid][1] 
  
        # If target is less than element, look to left
        if target < arr[mid][1]: 
  
            # If target is greater than previous to mid, return closest of two 
            if mid > 0 and target > arr[mid - 1][1]: 
                return getClosest(arr[mid - 1][1], arr[mid][1], target) 
  
            # Do it again for the other half
            j = mid 
          
        # Otherwise if target value is greater than mid
        else: 
            if mid < n - 1 and target < arr[mid + 1][1]: 
                return getClosest(arr[mid][1], arr[mid + 1][1], target) 
                  
            # Update i 
            i = mid + 1
          
    # Return the element left after search (the element closest to target)
    return arr[mid][1]
  
  
# Finding which element is closest by taking the distance
# from target (which is between val1 and val2)
def getClosest(val1, val2, target): 
  
    if target - val1 >= val2 - target: 
        return val2 
    else: 
        return val1 


### Scheduler ###
    
def schedule(list, taken):
    
    # Looking for the courses that can actually be taken in the next semester
    takeable = []
    for i in list:
        # if there are no prerequisites then we can examine
        if i.prereq == None:
            takeable.append(i)
        # if the prerequisites have already been taken then we can examine
        elif i.prereq in taken:
            takeable.append(i)
        # in the case that prerequisites for the course have not been taken,
        # the course will not be considered for the next semester
        
    groupings = []
    
    # get all unique combinations of courses (groups of 3)
    for combo in combinations(takeable, 3):
        groupings.append(combo)
    
    # put together the combinations along with the average 
    # work load for the given combination
    compile = []
    
    for combo in groupings:
        compile.append([combo, mean((combo[0].timecommit, 
        combo[1].timecommit, combo[2].timecommit))])
    
    # to sort the compile list using the second element of each list, 
    # which is the work load average
    def sort_w_work(element):
        return element[1]
    
    # sort
    compile.sort(key=sort_w_work)
    
    # compute the average of all the averages (the average work load 
    # of the entire pool of potential courses
    average = mean(n for _, n in compile)
    print "Average workload of all potential courses: {}".format(average)
    
    # use the findclosest function to identify which combination of courses 
    # produces a workload that is closest to the overall average 
    # (ensures workload is not too high, and not too low. 
    # too low would mean future semesters might have workloads skewed to be high)
    courses = findClosest(compile, len(compile), average)
    
    # get the combination of courses that is associated with the closest workload
    for each in compile:
        if courses in each:
            return each

    
# The list of courses I am interested in taking next semester    
list = [cs156, cs152, ss144, ss154, ss142, cs112, cs166, cs111]
# The list of courses I have already taken
taken = [ss110, ss111, cs110]

# Print the ideal course schedule
get = schedule(list, taken)
final = []
for i in get[0]:
    final.append(i.name)

print "Ideal course schedule for next semester: {}".format(final)
print "Workload of the course schedule: {}".format(get[1])
#%% md
## Explanation

The algorithm displayed takes as input a list of potential courses to take as well as a list of courses already taken by the student and returns a list of courses that the student should register for next semester. The way in which this happens is as follows:

1. Filter out courses that cannot be taken next semester because the prerequisite course has not been already taken.
2. Create all the possible unique combinations of three courses.
3. Get the average workload for each combination.
3. Sort the list by workload.
4. Using binary search, find the combination of courses that produces a workload closest to the average workload of all the courses combined.
5. Return the combination of courses.

## Code once implemented
#%%
###
### Implemented Code
###

from itertools import combinations
from statistics import mean

### Courses ###


class Course:
    
    def __init__(self, name):
        self.name = name
        self.prereq = None
        self.timecommit = 0
        # Takes the first two letters of the course name, which is the 
        # abbreviation of the college it belongs to
        self.college = name[0]+name[1] 
    
    # function for indicating the prerequisites for the given course
    def needs(self, node):
        self.prereq = node
    
    # function for indicating the overall workload of the course 
    # (readings, pre-class work, etc)
    def time(self, time):
        self.timecommit = time


### Setting up the courses ###

# Courses and names
cs110 = Course("cs110")
cs111 = Course("cs111")
cs112 = Course("cs112")
cs152 = Course("cs152")
cs156 = Course("cs156")
cs166 = Course("cs166")
ss110 = Course("ss110")
ss111 = Course("ss111")
ss144 = Course("ss144")
ss154 = Course("ss154")
ss142 = Course("ss142")

# Courses and time commitment
cs110.time(3)
cs111.time(2)
cs112.time(2)
cs152.time(4)
cs156.time(4)
ss110.time(1)
ss111.time(1)
ss144.time(2)
ss154.time(3)
cs166.time(4)
ss142.time(2)

# Courses and prerequisites (if any)
cs152.needs(cs110)
cs156.needs(cs110)
cs166.needs(cs112)
ss142.needs(ss110)
ss144.needs(ss111)
ss154.needs(ss111)


### Function for finding the element with the closest value to a certain target ###
# adapted from a code found on:
# https://www.geeksforgeeks.org/find-closest-number-array/
# to search from the workload averages (second elements in the tuples)

def findClosest(arr, n, target): 
  
    # Corner cases 
    if target <= arr[0][1]: 
        return arr[0][1] 
    if target >= arr[n - 1][1]: 
        return arr[n - 1][1]
  
    # Binary Search
    i = 0
    j = n
    mid = 0
    
    while i < j:
        # getting midpoint
        mid = (i + j) / 2
  
        if arr[mid] == target: 
            return arr[mid][1] 
  
        # If target is less than element, look to left
        if target < arr[mid][1]: 
  
            # If target is greater than previous to mid, return closest of two 
            if mid > 0 and target > arr[mid - 1][1]: 
                return getClosest(arr[mid - 1][1], arr[mid][1], target) 
  
            # Do it again for the other half
            j = mid 
          
        # Otherwise if target value is greater than mid
        else: 
            if mid < n - 1 and target < arr[mid + 1][1]: 
                return getClosest(arr[mid][1], arr[mid + 1][1], target) 
                  
            # Update i 
            i = mid + 1
          
    # Return the element left after search (the element closest to target)
    return arr[mid][1]
  
  
# Finding which element is closest by taking the distance
# from target (which is between val1 and val2)
def getClosest(val1, val2, target): 
  
    if target - val1 >= val2 - target: 
        return val2 
    else: 
        return val1 


### Scheduler ###
    
def schedule(list, taken):
    
    # Looking for the courses that can actually be taken in the next semester
    takeable = []
    for i in list:
        # if there are no prerequisites then we can examine
        if i.prereq == None:
            takeable.append(i)
        # if the prerequisites have already been taken then we can examine
        elif i.prereq in taken:
            takeable.append(i)
        # in the case that prerequisites for the course have not been taken,
        # the course will not be considered for the next semester
        
    groupings = []
    
    # get all unique combinations of courses (groups of 3)
    for combo in combinations(takeable, 3):
        groupings.append(combo)
    
    # put together the combinations along with the average 
    # work load for the given combination
    compile = []
    
    for combo in groupings:
        compile.append([combo, mean((combo[0].timecommit, 
        combo[1].timecommit, combo[2].timecommit))])
    
    # to sort the compile list using the second element of each list, 
    # which is the work load average
    def sort_w_work(element):
        return element[1]
    
    # sort
    compile.sort(key=sort_w_work)
    
    # compute the average of all the averages (the average work load 
    # of the entire pool of potential courses
    average = mean(n for _, n in compile)
    print "Average workload of all potential courses: {}".format(average)
    
    # use the findclosest function to identify which combination of courses 
    # produces a workload that is closest to the overall average 
    # (ensures workload is not too high, and not too low. 
    # too low would mean future semesters might have workloads skewed to be high)
    courses = findClosest(compile, len(compile), average)
    
    # get the combination of courses that is associated with the closest workload
    for each in compile:
        if courses in each:
            return each

    
# The list of courses I am interested in taking next semester    
list = [cs156, cs152, ss144, ss154, ss142, cs112, cs166, cs111]
# The list of courses I have already taken
taken = [ss110, ss111, cs110]

# Print the ideal course schedule
get = schedule(list, taken)
final = []
for i in get[0]:
    final.append(i.name)

print "Ideal course schedule for next semester: {}".format(final)
print "Workload of the course schedule: {}".format(get[1])
