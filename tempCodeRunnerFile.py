for k in range(9):
            if (i, j) != (i, k):
                neighbours.append((i, k))
            if (k, j) != (i, j):
                neighbours.append((k, j))