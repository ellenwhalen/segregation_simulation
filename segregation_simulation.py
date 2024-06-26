import random as r
import graphics as g



class Square:
    _name: str
    _has_moved: bool

    def __init__(self, name: str):
        self._name = name
        self._has_moved = False
    
    @property
    def name(self):
        return self._name
    
    @property
    def has_moved(self):
        return self._has_moved
    
    def set_name(self, new_name: str):
        """Sets the name of the square."""
        self._name = new_name 

    def __str__(self):
        return "'" + self.name + "'"
    
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

class Grid:
    _dim: int 
    _grid: list[list[Square]]
    _round: int
    _win: g.GraphWin
    _similar: int
    _red_squares: int
    _blue_squares: int

    def __init__(self, dim, empty, percent_red, similar): 
        if empty == 100:
            raise ValueError("Empty percent must be lower than 100.")
        if empty == 0:
            raise ValueError("Empty percent must be higher than 0.")
        self._dim = dim
        self._grid = []
        self._round = 0
        self._win = g.GraphWin("Segregation Simulation", 800, 800, autoflush=False)
        self.win.setBackground("lightgray")
        self.win.setCoords(0, 0, self.dim, self.dim)
        self._similar = similar

        total_squares = self.dim * self.dim
        squares_to_fill = round(total_squares - (total_squares * (empty/100)))
        self._red_squares = round(squares_to_fill * (percent_red/100))
        self._blue_squares = squares_to_fill - self.red_squares

        # initializing grid to Squares with name ''
        for i in range(self.dim):
            row = [Square('')]
            for j in range(self.dim - 1):
                row += [Square('')]
            self._grid.append(row)
        
        # inserting X's representing red squares
        i = 0
        while i < self.red_squares:
            row = r.randint(1, dim)
            col = r.randint(1, dim)
            if (self._grid[row - 1][col - 1]).name == '': 
                self.place_char(row - 1, col - 1, "X")
                i += 1
        
        # inserting O's representing blue squares
        i = 0
        while i < self.blue_squares:
            row = r.randint(1, dim)
            col = r.randint(1, dim)
            if (self._grid[row - 1][col - 1]).name == '': 
                self.place_char(row - 1, col - 1, "O")
                i += 1

    @property
    def grid(self):
        return self._grid
    
    @property
    def dim(self):
        return self._dim
    
    @property
    def round(self):
        return self._round
    
    @property
    def win(self):
        return self._win
    
    @property
    def similar(self):
        return self._similar
    
    @property
    def red_squares(self):
        return self._red_squares
    
    @property
    def blue_squares(self):
        return self._blue_squares

    def place_char(self, row: int, col: int, char: str):
        """Places an 'X', 'O' or '' on the grid."""
        if char != 'X' and char != 'O' and char != '':
            raise ValueError("Squares can only be named 'X', 'O' or ''.")

        (self._grid[row][col]).set_name(char) 

    def is_square_satisfied(self, row: int, col: int) -> bool:
        """Checks to see if a Square at [row][col] is satisfied."""
        box_around_square = Box(row, col, self._dim)
        square_name = self.grid[row][col].name
        num_similar = 0
        for i in box_around_square.row_range():
            for j in box_around_square.col_range():
                if self.grid[i][j].name == '' or self.grid[i][j].name == square_name:
                    num_similar += 1
        percent_similar = ((num_similar - 1)/(box_around_square.total_range() - 1)) * 100
        # ^need to subtract 1 from both num_similar and total_range to avoid counting the square we're checking
        if percent_similar >= self.similar:
            return True
        return False

    def is_grid_satisfied(self) -> bool:
        """Checks to see if the grid is satisfied. If not, takes one round of steps."""
        # making sure all squares start out not having the has_moved attribute
        for i in range(self.dim):
            for j in range(self.dim):
                self.grid[i][j]._has_moved = False
        
        grid_is_satisfied = True
        for i in range(self.dim):
            for j in range(self.dim):
                if self.grid[i][j].name != '':      # skip empty squares
                    square_satisfied = self.is_square_satisfied(i, j)
                    if square_satisfied == False:   
                        grid_is_satisfied = False   
                        if self.grid[i][j].has_moved == False:  
                            square_moving = self.grid[i][j]    
                            self.move_square(i, j)              
                            square_moving._has_moved = True
        self._round += 1
        self.draw_grid()
        return grid_is_satisfied

    def move_square(self, row: int, col: int):
        """Moves one square to a random empty space in the grid."""
        square_moved = False
        while square_moved == False:
            new_row = r.randint(1, self.dim) - 1
            new_col = r.randint(1, self.dim) - 1
            if self.grid[new_row][new_col].name == '':
                this_empty_square = self.grid[new_row][new_col]
                self.grid[new_row][new_col] = self.grid[row][col]
                self.grid[row][col] = this_empty_square
                square_moved = True
    
    def draw_grid(self):
        """Draws the grid."""
        for i in range(self.dim):
            line = g.Line(g.Point(0, i), g.Point(self.dim, i))
            line.draw(self.win)
            line = g.Line(g.Point(i, 0), g.Point(i, self.dim))
            line.draw(self.win)
        for row in range(self.dim):
            for col in range(self.dim):
                square = g.Rectangle(g.Point(col, row), g.Point(col + 1, row + 1))
                if self.grid[row][col].name == "X":
                    square.setFill("red")
                elif self.grid[row][col].name == "O":
                    square.setFill("blue")
                else:
                    square.setFill("lightgray")
                square.draw(self.win)
        g.update(5)


DIM = 20            # Dimension of the grid
EMPTY = 10          # Percent of the grid left empty
PERCENT_RED = 50    # Percent of squares that are red 
SIMILAR = 30        # Percent similarity that squares will tolerate



my_grid = Grid(DIM, EMPTY, PERCENT_RED, SIMILAR)

grid_satisfied = False
while grid_satisfied == False:
    grid_satisfied = my_grid.is_grid_satisfied()


print("It took " + str(my_grid.round) + " rounds to satisfy all squares.")
my_grid.win.getMouse()
my_grid.win.close()
