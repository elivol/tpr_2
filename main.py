from tkinter import *
from tkinter import ttk, messagebox
from funcs import *

root = Tk()


class MainWindow():

    def __init__(self):

        # Виджет шапка
        fra = Frame(root, bg='#dcf7dc')
        header = Label(fra, text='Выберите параметры матрицы и метод решения', bg='#dcf7dc')
        header.grid(row=0, column=0, columnspan=4, rowspan=2)
        fra.grid(row=0, column=0, columnspan=4, rowspan=2)

        # Выпадающие листы с размерностью матрицы
        entry = [i for i in range(2, 11, 1)]
        crit_l = Label(root, text='Количество критериев F')
        crit = ttk.Combobox(root, values=entry, height=8, width=10, state='readonly')
        crit.set(entry[0])

        var_l = Label(root, text='Количество вариантов E')
        var = ttk.Combobox(root, values=entry, height=8, width=10, state='readonly')
        var.set(entry[0])

        # Выбор метода
        meth_l = Label(root, text='Выберите метод')

        methods = ['Метод Сэвиджа', 'Метод Ходжа-Лемана']
        m_lst = ttk.Combobox(root, values=methods, height=2, state='readonly')
        m_lst.set(methods[0])

        # Кнопка
        do_btn = Button(root, text='Далее', bg='#dcf7dc')

        # Расположение виджетов в окне и их отображение
        crit_l.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        var_l.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        crit.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        var.grid(row=3, column=2, columnspan=2, padx=5, pady=5)
        meth_l.grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        m_lst.grid(row=4, column=2, columnspan=1, padx=5, pady=5)
        do_btn.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        def full_matrix(event):
            InputMatrix(int(var.get()), int(crit.get()), m_lst.current())

        # Связывание виджета, события и функции
        do_btn.bind('<Button-1>', full_matrix)


class InputMatrix():

    method = 0  # Метод (по-умолчанию 0 - Сэвидж)
    col = 2
    row = 2
    matrix_entry = []

    def __init__(self, row, col, method):

        # Установка свойств класса
        self.col = col
        self.row = row
        self.method = method

        # Создание дочернего окна
        win = Toplevel(root, relief='raised')
        win.title('Ввод матрицы и коэффициентов')

        # Виджет шапка
        fra = Frame(win, bg='#dcf7dc')
        header = Label(fra, text='Заполните матрицу', bg='#dcf7dc')
        header.grid(row=0, column=(self.col+1)//2, rowspan=2)
        fra.grid(row=0, column=0, columnspan=self.col+1, rowspan=2)

        # Лейблы для столбцов и строк
        crits_l = [Label(win, text='F['+ str(i+1) + ']') for i in range(self.col)]
        vars_l = [Label(win, text='E[' + str(i+1) + ']') for i in range(self.row)]

        # Поля ввода для столбцов и строк матрицы
        self.matrix_entry = [[Entry(win, width=8) for i in range(self.col)] for j in range(self.row)]

        # Отображение лейблов критериев и вариантов
        for i in range(self.col):
            crits_l[i].grid(row=2, column=i+1)
        for i in range(self.row):
            vars_l[i].grid(row=3+i, column=0)

        # Отображение полей ввода матрицы
        for i in range(self.row):
            for j in range(self.col):
                self.matrix_entry[i][j].grid(row=3+i, column=1+j, padx=3, pady=3)

        # Вывод дополнительных полей, если метод Ходжа-Лемана
        if self.method == 1:
            # Создание леблов для вероятности и параметра v
            header_q_l = Label(win, text='Введите вероятность для каждого критерия', bg='#dcf7dc')
            q_l = [Label(win, text='q[' + str(i + 1) + ']') for i in range(self.col)]
            v_l = Label(win, text='Степень доверия v', bg='#dcf7dc')

            # Создание полей ввода
            q_entry = [Entry(win, width=8) for i in range(self.col)]  # вероятность каждого критерия
            v_entry = Entry(win, width=8)  # параметр v

            # Отображение леблов и полей
            header_q_l.grid(row=3+self.row, column=0, columnspan=self.col+1)
            for i in range(self.col):
                q_l[i].grid(row=3+self.row+1, column=i+1)
                q_entry[i].grid(row=3+self.row+2, column=i+1)
            v_l.grid(row=3+self.row+3, column=0, columnspan=self.col+1)
            v_entry.grid(row=3+self.row+4, column=(self.col+1)//2)

        # Кнопка и ее отображение в окне win
        do_btn = Button(win, text='Далее', bg='#dcf7dc')
        do_btn.grid(row=3+self.row+5, column=(1+self.col)//2, pady=5)

        def show_solution_savidj(event):
            matrix = np.zeros((self.row, self.col), dtype=float)

            for i in range(self.row):
                for j in range(self.col):
                    if self.matrix_entry[i][j].get():
                        try:
                            matrix[i, j] = float(self.matrix_entry[i][j].get())
                        except ValueError:
                            messagebox.showwarning("Ошибка", "Данные введены неверно!")
                            return
                    else:
                        messagebox.showwarning("Ошибка", "Данные введены неверно!")
                        return
            if self.method == 0:
                SolutionSavidj(matrix)

        # Связывание виджета, события и функции
        do_btn.bind('<Button-1>', show_solution_savidj)


class SolutionSavidj():

    matrix = None

    def __init__(self, matrix):

        # Установка свойств
        self.matrix = matrix

        # Решение задачи:
        solution = savidj(matrix)
        col_a = solution[0].shape[1]
        row_a = solution[0].shape[0]

        # Создание дочернего окна
        win = Toplevel(root, relief='raised')
        win.title('Вывод решения')

        # Виджет шапка
        fra = Frame(win, width=200, height=20, bg='#dcf7dc')
        header = Label(fra, text='Решение по методу Сэвиджа', bg='#dcf7dc', justify='center')

        # Создание трех вреймов для отображения результата и промежуточных шагов
        fra1 = Frame(win, width=100, height=20)
        fra2 = Frame(win, width=100, height=20)
        fra3 = Frame(win, width=200, height=20)

        header.grid()
        fra.grid(row=0, column=0, columnspan=col_a+2, padx=3)


        # ШАГ 1
        #  В первый фрейм выводим матрицу а[ij]

        # Леблы
        step_1 = Label(win, text='Шаг 1', bg='#dcf7dc')
        step_2 = Label(win, text='Шаг 2', bg='#dcf7dc')
        step_3 = Label(win, text='Шаг 3', bg='#dcf7dc')
        matrix_a_l = Label(win, text='Построим матрицу a[ij], \nвычисленную по формуле \nmax(max(e[ij]) - e[ij]):')
        matrix_a_res = [[Label(win, text=str(el)) for el in row] for row in solution[0]]
        column_e_l = Label(win, text='Дополним матрицу a[ij] столбцом e[ir], \nвычисленным по формуле \nmax(a[ij]):')
        column_e_res = [Label(win, text=str(el)) for el in solution[1]]
        result_l = Label(win, text='Результатом решения является(-ются) наименьший(-е) элемент(ы) столбца e[ir]:')
        result = solution[2]

        # Сепараторы(разделители контента)
        sep1 = ttk.Separator(win, orient='vertical')
        sep2 = ttk.Separator(win, orient='horizontal')
        sep3 = ttk.Separator(win, orient='horizontal')


        # Отображение содержимого
        step_1.grid(row=1, column=0, pady=3)

        matrix_a_l.grid(row=2, column=0, pady=3, columnspan=col_a+2)
        sep1.grid(row=1, column=col_a+3, rowspan=row_a+2, sticky='ns')
        for i in range(row_a):
            for j in range(col_a):
                matrix_a_res[i][j].grid(row=i+3, column=j, pady=3)

        step_2.grid(row=1, column=col_a+4)
        column_e_l.grid(row=2, column=col_a+4, columnspan=col_a+5)
        for i in range(row_a):
            column_e_res[i].grid(row=i+3, column=col_a+4)

        sep2.grid(row=row_a+4, column=0, columnspan=col_a+2, sticky='ew')
        sep3.grid(row=row_a+4, column=col_a+2, columnspan=col_a+7, sticky='ew')

        step_3.grid(row=row_a+5, column=0, columnspan=2)
        result_l.grid(row=row_a+6, column=0, columnspan=col_a+7)
        Label(win, text='Значение функции: Z = '+str(result[0][0])).grid(row=row_a+7, column=0, columnspan=col_a+7)
        Label(win, text='Варианты, выбранные в ходе решения задачи методом Сэвиджа:').grid(row=row_a+8, column=0, columnspan=col_a+7)
        for i in range(len(result)):
            Label(win, text='E['+str(result[i][1])+'] =').grid(row=row_a+i+9, column=0)
            Label(win, text=str(result[i][0])).grid(row=row_a+i+9, column=1)



win = MainWindow()
root.mainloop()
