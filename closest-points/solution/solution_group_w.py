import sys
import re
import math

input = sys.stdin.read()

# we define a point that has x and y coordinates
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


#### greedy algorithm implementation:
def dist(p1: Point, p2: Point): # euclidean distance
    return math.sqrt(
        ((p1.x-p2.x)**2)+((p1.y-p2.y)**2)
    )
    
def greedy_solution(points: list, n: int) -> float: 
    # defining the minimum as infinity since we need to compare it later 
    minimum = math.inf
    # the first point
    for i in range(n):
        # the second point to compare with the first
        for j in range(i+1,n):
            if dist(points[i],points[j]) < minimum:
                minimum = dist(points[i],points[j])
    return minimum

def closestInSlice(points: list, n: int, minimum):
    minimum_ = minimum

    for i in range(n):
        for j in range(i+1, min(11,n)):
            if dist(points[i], points[j]) < minimum_:
                minimum_ = dist(points[i], points[j])

    return minimum_
    
def divide_and_conquer(pX: list, pY: list, n: int) -> float:
    
    if n <= 3:
        return greedy_solution(pX, n)
    # we find the median on the axis to know where to split
    mid = n//2

    # spliting and sorting by y only to minimize the time
    left_x = pX[:mid]
    left_y = sorted(pX[:mid], key=lambda point: point.y) # can be optimised
    
    right_x = pX[mid:]
    right_y = sorted(pX[mid:], key=lambda point: point.y) # can be optimised
    
    min_left = divide_and_conquer(left_x, left_y, mid)
    min_right = divide_and_conquer(right_x, right_y, n-mid)

    minimum = min(min_left, min_right)

    #closest_x_mid = [pX[i] for i in range(n) if abs(pX[i].x - pX[mid].x) < minimum]
    closest_y_mid = [pY[i] for i in range(n) if abs(pY[i].x - pX[mid].x) < minimum]

    return closestInSlice(closest_y_mid, len(closest_y_mid), minimum)

def formatOutput(output):   # This function formats the output by rounding it too the 16 most important digits to match the answers in closest-pair-out.txt

    output_ = str(output)
    output_split = output_.split(".")
    if output_split[1] == "0":
        return output_split[0]
    elif len(output_) <= 16:
        return output_
    elif len(output_) > 16 and output_split[0] != "0":
        return str(round(output,16-len(output_split[0])-1))
    else:
        for i, c in enumerate(output_):

            if (c != "0" and c !=".") and i == 2:
                return str(round(output,15))
            elif c != "0" and c !=".":
                return str(round(output,13+i))


# we use regular expressions for skipping the intro text in the input files:
points = re.findall(r"[\w][^\S\r\n]+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)[^\S\r\n]+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)", input)

# we convert the points from string to type Point so we can sort them:
for i, v in enumerate(points):
    points[i] = Point(float(v[0]),float(v[1]))

# we sort points by x and y:
x_sorted = sorted(points, key=lambda point: point.x) # for a greedy algorithm
y_sorted = sorted(points, key=lambda point: point.y) # for the comparison of the points in borders

print(len(points), formatOutput(divide_and_conquer(x_sorted, y_sorted, len(points))))