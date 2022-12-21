import sys
import re
import numpy as np

class Alignment:
    def __init__(self, penaltyMatrixFile: str, gap_penalty: int):
        self.gap_penalty = gap_penalty

        # Read in input-file line for line
        with open(penaltyMatrixFile, "r")  as file:
            lines = [line.strip().split("\r")[0] for line in file] 
        
        self.matrix = [] 

        for line in lines:
            if not line.startswith("#"):
                self.matrix.append(re.split('\s\s|\s', line)) # split by either one whitespace or two

        self.index = self.matrix[0]
        self.matrix = self.matrix[1:]

        for i in range(len(self.matrix)):
            self.matrix[i] = self.matrix[i][1:]
            self.matrix[i] = list(map(int, self.matrix[i]))
        
        self.matrix = np.array(self.matrix)

    def look_up(self, s1:str, s2:str) -> int:
        """
        Perform look_up in penalty matrix
        """
        index1 = self.index.index(s1)
        index2 = self.index.index(s2)
        return self.matrix[index1][index2]

    def parsePath(self, path_matrix, s1, s2):
        """
        function to return the actual alignment of the inputs 
        by travesing the path that got us to the optimal alignment score 
        (the value in the lower right corner of the matrix).
        """
        
        current_index = [len(s1),len(s2)] # start in the lower right corner (the optimal aligment score)

        # we need seperate index because the input strings can be different lengths
        counter_s1 = 0
        counter_s2 = 0
        out_s1 = ""
        out_s2 = ""


        while True: 
            _index = path_matrix[current_index[0],current_index[1]] # index to prior value

            if _index is None: # Break out if we are at 0,0
                break

            # Checks if the path taken is diagonal, vertical or horizontal from each point
            diagonal = current_index[0]-1 == _index[0] and current_index[1]-1 == _index[1]
            vertical = current_index[0] == _index[0] and current_index[1]-1 == _index[1]
            horizontal = current_index[0]-1 == _index[0] and current_index[1] == _index[1]

            if diagonal: # add no gap
                out_s1 = out_s1 + s1[(-1-counter_s1)]
                out_s2 = out_s2 + s2[(-1-counter_s2)]
                
                counter_s1 += 1
                counter_s2 += 1

            elif vertical: # add gap to s1
                out_s1 = out_s1+ "-"
                out_s2 = out_s2 + s2[(-1-counter_s2)]

                counter_s2 += 1

            elif horizontal: # add gap to s2
                out_s1 = out_s1 + s1[(-1-counter_s1)]
                out_s2 = out_s2 + "-"

                counter_s1 += 1

            current_index = _index

        return out_s1[::-1], out_s2[::-1] # reverse both strings


    def construct_matrix(self, s1: str, s2: str):
        """
        Construct the accumalitive minimal penalty matrix (aka optimal score) for a given input.
        """

        # Cache-matrix we use to store intermediate results
        matrix = np.zeros((len(s1)+1,len(s2)+1)) # +1 to make room for the penalties
        
        # Replace the first row and column in the matrix
        matrix[0] = np.array(list(map(lambda x:x*(self.gap_penalty), range(len(s2)+1)))) # row
        matrix[:, 0] = np.array(list(map(lambda x:x*(self.gap_penalty), range(len(s1)+1)))) # column

        # instantiate matrix we use to store index's of the optimal alignment so we can 
        # backtrace once the matrix is calculated, and construct the strings:
        path_matrix = np.zeros((len(s1)+1,len(s2)+1), dtype=object)
        path_matrix[0] = [(0,i-1) for i in range(len(s2)+1)] 
        path_matrix[:, 0] = [(i-1,0) for i in range(len(s1)+1)]
        path_matrix[0,0] = None
        
        # Construct optimal score matrix
        for i in range(1,len(s1)+1):
            for j in range(1,len(s2)+1):
                
                # look-up values and store their index
                diagonal_value = (matrix[i-1,j-1]+self.look_up(s1[i-1], s2[j-1]),[i-1,j-1])
                vertical_value = (matrix[i, j-1]+self.gap_penalty,[i, j-1])
                horizontal_value = (matrix[i-1, j]+self.gap_penalty,[i-1,j])

                # Sort diagnoal, vertical and horizontal value by most optimal choice
                solutions = sorted([
                    diagonal_value,
                    vertical_value,
                    horizontal_value
                ],key=lambda x:x[0], reverse=True)

                matrix[i, j] = solutions[0][0] # Get the best choice
                path_matrix[i,j] = tuple(solutions[0][1]) # Get index of best choice
        
        out_s1 , out_s2 = self.parsePath(path_matrix, s1, s2)

        return int(matrix[len(s1),len(s2)]), out_s1, out_s2


def read_input():
    """
    Read and parse input from file
    """
    si = sys.stdin
    lines = [line.strip().split("\r")[0] for line in si]
    
    data = {}
    
    for i in range(len(lines)):
        if lines[i].startswith('>'):
            name = lines[i].split(" ")[0].replace(">","")
            data[name] = ""
        else:
            data[name] += lines[i]
            
    return data


if __name__ == "__main__":
    matrix = Alignment("data/BLOSUM62.txt", gap_penalty=-4)
    data = read_input()
    # Order used to compare with HbB_FASTAs-out.txt
    #keys = ["Human","Spider","Cow","Horse","Trout", "Pig","Human-sickle","Deer","Lamprey","Rockcod","Sea-Cucumber","Gull","Gorilla"]
    keys = list(data.keys())
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            penalty, s1, s2 = matrix.construct_matrix(data[keys[i]], data[keys[j]])

            print(f'{keys[i]}--{keys[j]}: {penalty}\n{s1}\n{s2}')
    