import numpy as np

# Метод Сэвиджа
def savidj(var_crit):

    m = var_crit.shape[0]
    n = var_crit.shape[1]

    # Алгоритм
    # 1. Составить матрицу a[ij]=max_e[ij] - e[ij]
    sum_col = var_crit.max(axis=0)  # матрица максимумов по каждому столбцу

    a = np.zeros((m, n), dtype=int)

    i = 0
    while i < m:
        j = 0
        while j < n:
            a[i, j] = sum_col[j] - var_crit[i, j]
            j += 1
        i += 1

    # 2. Составить столбец, дополняющий матрицу var_crit, из max_a[ij]
    e_ir = a.max(axis=1)
    return e_ir.max()


# Метод Ходжа-Лемана
def hodj_leman(var_crit, v, q_array):

    m = var_crit.shape[0]
    n = var_crit.shape[1]

    # найти минимумы по строке
    min_row = var_crit.min(axis=1)

    e_ir = np.zeros(m, dtype=float)
    # 1. Составить столбец e_ir, дополняющий матрицу var_crit
    i = 0
    while i < m:
        e_ir[i] = v*sum(var_crit[i]*q_array) + (1-v)*min_row[i]
        i += 1
    return e_ir.max()


#print(savidj(np.array([[10, -2, 8], [-3, 5.2, 6], [7.5, 9, -1]], dtype=float)))
#print(savidj(np.array([[-50, -21, -23], [-33, -11, 15], [0, 5, 10]], dtype=float)))
#print(hodj_leman(np.array([[10, -2, 8], [-3, 5.2, 6], [7.5, 9, -1]], dtype=float), 0.5, [0.33 for i in range(3)]))
