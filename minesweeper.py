import random

class grid(object):
    def __init__(self, width=16, height=16, mines=40):
        self.width = width
        self.height = height
        self.mines = mines
        self.game_over = False
        mine_bool = [False]*(width*height - mines) + [True]*mines
        random.shuffle(mine_bool)
        self.grid = [[cell(row, column, mine=mine_bool.pop()) for column in range(width)] for row in range(height)]

    def clear_visited_cells(self):
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def show_all_cells(self):
        for row in self.grid:
            for cell in row:
                cell.hidden = False

    def explode(self):
        self.show_all_cells()
        self.game_over = True
        print self
        print 'You hit a bomb!'

    def select_cell(self, row, column):
        self.clear_visited_cells()
        self.player_cell_select(row, column)

    def player_cell_select(self, row, column):
        cell = self.grid[row][column]
        cell.hidden = False
        cell.visited = True
        if cell.mine:
            self.explode()

        neighbors = self.get_cell_neighbors(cell)
        mine_count = sum([1 for neighbor in neighbors if neighbor.mine])
        if not mine_count:
            for neighbor in neighbors:
                if not neighbor.visited:
                    self.player_cell_select(neighbor.row, neighbor.column)

    def get_cell_neighbors(self, cell):
        neighbors = []
        start_row, start_column = max(0, cell.row - 1), max(0, cell.column - 1)
        end_row, end_column = min(len(self.grid), cell.row + 2), min(len(self.grid[0]), cell.column + 2)
        for i in range(start_row, end_row):
            for j in range(start_column, end_column):
                neighbors.append(self.grid[i][j])
        return neighbors

    def get_mine_count(self, cell):
        neighbors = self.get_cell_neighbors(cell)
        mine_count = sum([1 for neighbor in neighbors if neighbor.mine])
        return mine_count

    def __repr__(self):
        out = ''
        out += '_'*self.width*2 + '\n'
        for row in self.grid:
            out += '|'
            for cell in row:
                if cell.hidden:
                    out += ' '
                elif cell.mine:
                    out += '*'
                else:
                    out += str(self.get_mine_count(cell))
                out += '|'
            out += '\n'
            out += '_'*self.width*2 + '\n'
        return out


class cell(object):
    def __init__(self, row, column, mine=False, hidden=True):
        self.hidden = hidden
        self.mine = mine
        self.row = row
        self.column = column
        self.visited = True

    def __repr__(self):
        return str((self.row, self.column, self.mine))

class game(object):
    pass

first_game = True
while True:
    if not first_game:
        new_s = raw_input('Want to start a new game?\n')
        if not new_s == 'y':
            break
    first_game = False

    new_grid = grid()
    while not new_grid.game_over:
        print new_grid
        p_select_s = raw_input('Select a new cell by row and column, like this: 3 5\n')
        coords = [int(x) for x in p_select_s.split()]
        new_grid.select_cell(*coords)



