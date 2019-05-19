'''
ищет наименьшее из наибольших элементов рядков матрицы
'''
import numpy as np

f = open('matrix.txt')
M = np.array([list(map(float, i.split())) for i in f.readlines()])
f.close()

maxes = []
for row in M:
    maxes.append(max(row))

'''
maxes = np.zeros(len(M))
for i in len(M):
    maxes[i] = max(M[i])
'''

print(min(maxes))