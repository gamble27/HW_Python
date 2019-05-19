import numpy as np


def diagon(matrix):
    error = np.linalg.LinAlgError
    if matrix.ndim != 2:
        return error
    if not all([len(matrix) == len(matrix[i]) for i in range(len(matrix))]):
        return error
    i = 0
    while i < len(matrix):
        if matrix[i, i] == 0 and i < len(matrix)-1:
            matrix[i], matrix[i+1] = matrix[i+1], matrix[i]
        else:
            for j in range(i+1, len(matrix)):
                matrix[j] -= (matrix[j, i]/matrix[i, i]) * matrix[i]
            i += 1
    return matrix

f = open('matrix.txt')
lines = f.readlines()
M = np.array([list(map(float, i.split())) for i in lines])
M1 = np.array([list(map(float, i.split())) for i in lines])
f.close()

N = diagon(M)
# f = open('res.txt','w')
# print(*N, sep='\n', file=f)
# f.close()
print((N==M1).all())