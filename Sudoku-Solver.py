import itertools


class Cell:
    def __init__(self, num=None):
        """

        :param num:
        :type num: int
        """
        self.num = num if num >= 1 else None
        self.possible_values = set()

    def __str__(self):
        if self.num is not None:
            return str(self.num)
        return ''


class Board:
    def __init__(self, cells):
        """

        :param cells:
        :type cells: list[Cell | int]
        """
        self.cells = []
        for c in cells:
            if isinstance(c, Cell):
                self.cells.append(c)
            elif isinstance(c, int):
                self.cells.append(Cell(c))
            else:
                raise Exception("Invalid input, cells must be a list of integers or Cells")

        self.rows = [[] for _ in range(9)]
        self.cols = [[] for _ in range(9)]
        self.cubes = [[[] for _ in range(3)] for _ in range(3)]

        i = 0
        j = 0
        for cell in self.cells:
            # noinspection PyTypeChecker
            self.rows[i].append(cell)
            # noinspection PyTypeChecker
            self.cols[j].append(cell)
            self.cubes[int(i / 3)][int(j / 3)].append(cell)
            i = i + int((j + 1) / 9)
            j = (j + 1) % 9

    def solve(self):
        while True:
            flag = self._solve_rows() or self._solve_cols() or self._solve_cubes()
            if not flag:
                break
            self._set_possible_values()

    def _set_possible_values(self):
        i, j = 0, 0
        for cell in self.cells:
            if cell.num is None:
                for n in range(1, 10):
                    if n not in self.rows[i] and n not in self.cols[j] \
                            and n not in self.cubes[int(i / 3)][int(j / 3)]:
                        cell.possible_values.add(n)
            i = i + int((j + 1) / 9)
            j = (j + 1) % 9

    def _solve_cells(self):
        for c in self.cells:
            if len(c.possible_values) == 1 and c.num is None:
                c.num = list(c.possible_values)[0]

    def _solve_rows(self):
        flag = False
        for r in self.rows:
            for X in range(1, 10):
                for sub in itertools.combinations(r, X):
                    possible_values = set()
                    for cell in sub:
                        possible_values.union(cell.possible_values)
                    if len(possible_values) == X:
                        flag = True
                        others = set(r) - set(sub)
                        for cell in others:
                            cell.possible_values.remove()
        return flag

    def _solve_cols(self):
        flag = False
        for c in self.cols:
            for X in range(1, 10):
                for sub in itertools.combinations(c, X):
                    possible_values = set()
                    for cell in sub:
                        possible_values.union(cell.possible_values)
                    if len(possible_values) == X:
                        flag = True
                        others = set(c) - set(sub)
                        for cell in others:
                            cell.possible_values -= possible_values
        return flag

    def _solve_cubes(self):
        flag = False
        for r in self.cubes:
            for cube in r:
                for X in range(1, 10):
                    for sub in itertools.combinations(cube, X):
                        possible_values = set()
                        for cell in sub:
                            possible_values.union(cell.possible_values)
                        if len(possible_values) == X:
                            flag = True
                            others = set(cube) - set(sub)
                            for cell in others:
                                cell.possible_values -= possible_values
        return flag

    def __str__(self):
        cubes_separator_str = ('+' + '-' * 5) * 3 + '+'
        ret_str = cubes_separator_str + '\n'
        i = 0
        for row in self.rows:
            s = '|'
            j = 0
            for c in row:
                s += str(c) if str(c) != '' else ' '
                if j == 2:
                    s += '|'
                else:
                    s += ' '
                j = (j + 1) % 3
            ret_str += s + '\n'
            if i == 2:
                ret_str += cubes_separator_str + '\n'
            i = (i + 1) % 3

        return ret_str


if __name__ == '__main__':
    cs = [0, 1, 0, 0, 5, 3, 4, 0, 8, 8, 0, 0, 1, 9, 0, 3, 7, 0, 3, 7, 4, 6, 0, 0, 0, 0, 1, 0, 8, 6, 9, 0, 5, 2, 0, 0, 0,
          0, 7, 0, 8, 0, 6, 9, 3, 0, 4, 3, 2, 0, 7, 0, 1, 0, 7, 0, 5, 0, 0, 2, 0, 6, 9, 2, 6, 0, 5, 0, 9, 0, 3, 0, 4, 0,
          0, 0, 7, 6, 5, 0, 2]

    b = Board(cs)

    print(b)
