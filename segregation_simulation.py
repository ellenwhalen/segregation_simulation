import random as r

DIM = 20
EMPTY = 10
PERCENT_RED = 50
SIMILAR = 30

total_squares = DIM * DIM
squares_to_fill = round(total_squares - (total_squares * (EMPTY/100)))
red_squares = round(squares_to_fill * (PERCENT_RED/100))
blue_squares = squares_to_fill - red_squares

class Agent:
    _row = int
    _col = int
    _name = str
    _dim = int
    _grid = list[list[str]]
    _satisfied = bool
    _moving = bool

    def __init__(self, row: int, col: int, name: str, dim: int, grid: list[list[str]]):
        _row = row
        _col = col
        _name = name
        _dim = dim
        _grid = grid
        _satisfied = True
        _moving = False

    @property
    def row(self):
        return self._row
    
    @property
    def col(self):
        return self._col
    
    @property
    def name(self):
        return self._name
    
    @property
    def dim(self):
        return self._dim
    
    @property
    def grid(self):
        return self._grid
    
    @property
    def satisfied(self):
        return self._satisfied
    
    @property
    def moving(self):
        return self._moving
    
    def is_satisfied(self):
        """Checks to see if the Agent is satisfied in its current postiion."""
        box = Box(self.row, self.col, self.dim)
        number_similar = 0
        for i in box.row_range():
            for j in box.col_range():
                if grid[i][j] == self.name:     # minor bug here - need to also count "" in satisfied count
                    number_similar += 1
        percent_similar = ((number_similar - 1)/(box.total_range() - 1)) * 100  # need to sub 1 from both to omit counting self
        if percent_similar >= SIMILAR:
            self._satisfied = True
        else:
            self._satisfied = False
            self._moving = True

    def move(self, row, col):
        """Moves the Agent to a new row and col position."""
        self._row = row
        self._col = col

    def __str__(self):
        return "R: " + str(row) + " C: " + str(col) 
        


class Box:
    _min_row = int
    _max_row = int
    _min_col = int
    _max_col = int

    def __init__(self, row: int, col: int, dim: int):
        self._min_row = max(0, row - 1)
        self._max_row = min(dim - 1, row + 1)
        self._min_col = max(0, col - 1)
        self._max_col = min(dim - 1, col + 1)
    
    @property
    def min_row(self):
        return self._min_row
    
    @property
    def max_row(self):
        return self._max_row
    
    @property
    def min_col(self):
        return self._min_col
    
    @property
    def max_col(self):
        return self._max_col
    
    def row_range(self):   
        """Returns the range from min_row to max_row."""
        return range(self.min_row, self.max_row + 1)
    
    def col_range(self):
        """Returns the range from min_col to max_col."""
        return range(self.min_col, self.max_col + 1)
    
    def total_range(self):
        """Returns the total number of squares in the Box."""
        total = 0
        for i in self.row_range():
            for j in self.col_range():
                total += 1
        return total
    

grid = []
for i in range(DIM):
    grid.append([""] * DIM)

i = 0
while i < red_squares:
    row = r.randint(1, DIM)
    col = r.randint(1, DIM)
    if grid[row - 1][col - 1] == "": 
        placeholder_agent = Agent(row - 1, col - 1, "X", DIM, grid)
        grid[row - 1][col - 1] = placeholder_agent
        i += 1

i = 0
while i < blue_squares:
    row = r.randint(1, DIM)
    col = r.randint(1, DIM)
    if grid[row - 1][col - 1] == "": 
        placeholder_agent = Agent(row - 1, col - 1, "O", DIM, grid)
        grid[row - 1][col - 1] = placeholder_agent
        i += 1

print(grid)

""" 
test_agent = Agent(0, 0, DIM, grid)
print(test_agent.name)
print(test_agent.satisfied)

print(test_agent)
"""

"""
for i in range(DIM):
    for j in range(DIM):
        if grid[i][j] != "":
            placeholder_agent = Agent(i, j, DIM, grid)
            agent_grid[i][j] = placeholder_agent
             """

print(grid[0][0])

