import numpy as np

def diagon(sq_matrix):
    pattern = np.zeros(sq_matrix.shape)
    for i in range(1, len(sq_matrix)):
        if not np.array_equal(pattern[i][:i],sq_matrix[i][:i]):
            return False
    return True

f = open('matrix.txt')
lines = f.readlines()
M = np.array([list(map(float, i.split())) for i in lines])
f.close()

print(diagon(M))