"""Tests for the Square and Grid classes used in segregation_simulation"""

__author__ = "Ellen Whalen"

from segregation_simulation import Square
from segregation_simulation import Grid
import pytest

def test_calc_square_colors():
    dim = 20
    empty = 10
    percent_red = 50
    similar = 30
    a_grid = Grid(dim, empty, percent_red, similar)
    assert a_grid.blue_squares == 180
    assert a_grid.red_squares == 180

    dim = 40
    empty = 20
    percent_red = 60
    similar = 40
    my_other_grid = Grid(dim, empty, percent_red, similar)
    assert my_other_grid.red_squares == 768
    assert my_other_grid.blue_squares == 512


def test_x_o_count():
    dim = 20
    empty = 10
    percent_red = 50
    similar = 30
    new_grid = Grid(dim, empty, percent_red, similar)

    red_count = 0
    for i in range(dim):
        for j in range(dim):
            if new_grid._grid[i][j].name == "X":
                red_count += 1
    
    blue_count = 0
    for i in range(dim):
        for j in range(dim):
            if new_grid._grid[i][j].name == "O":
                blue_count += 1

    assert red_count == 180
    assert blue_count == 180

def test_weird_init_corner_cases():
    dim = 20
    empty = 100
    percent_red = 50
    similar = 30
    with pytest.raises(ValueError) as excinfo:  
        Grid(dim, empty, percent_red, similar)
    assert str(excinfo.value) == "Empty percent must be lower than 100." 

    empty = 0
    with pytest.raises(ValueError) as excinfo:  
        Grid(dim, empty, percent_red, similar)
    assert str(excinfo.value) == "Empty percent must be higher than 0." 
    

def test_is_grid_satisfied():
    dim = 20
    empty = 30
    percent_red = 100
    similar = 30
    red_grid = Grid(dim, empty, percent_red, similar)
    # it takes 1 round (the starting round of checking) to organize a 100% red or blue grid
    satisfied = red_grid.is_grid_satisfied()
    assert satisfied == True
    assert red_grid.round == 1           
    percent_red = 0
    blue_grid = Grid(dim, empty, percent_red, similar)
    satisfied = blue_grid.is_grid_satisfied()
    assert satisfied == True
    assert blue_grid.round == 1

def test_place_char():
    grid = Grid(20, 10, 50, 30)
    grid.place_char(10, 17, 'X')
    assert grid.grid[10][17].name == 'X'
    grid.place_char(10, 17, 'O')
    assert grid.grid[10][17].name == 'O'
    grid.place_char(0, 0, '')
    assert grid.grid[0][0].name == ''
    with pytest.raises(ValueError) as excinfo:
        grid.place_char(4, 5, '!')
    assert str(excinfo.value) == "Squares can only be named 'X', 'O' or ''."

def test_is_square_satisfied():
    grid = Grid(20, 10, 50, 30)
    grid.place_char(0, 0, 'O')
    grid.place_char(0, 1, 'O')
    grid.place_char(1, 1, '')
    grid.place_char(1, 0, 'X')
    assert grid.is_square_satisfied(0, 0) == True
    grid.place_char(0, 1, 'X')
    grid.place_char(1, 1, 'X')
    assert grid.is_square_satisfied(0, 0) == False
    grid = Grid(20, 10, 50, 50)
    grid.place_char(1, 1, 'X')
    grid.place_char(0, 1, 'X')
    grid.place_char(0, 0, '')
    grid.place_char(1, 0, 'X')
    grid.place_char(2, 0, 'X')
    grid.place_char(2, 1, 'O')
    grid.place_char(2, 2, 'O')
    grid.place_char(1, 2, 'O')
    grid.place_char(0, 2, 'O')
    assert grid.is_square_satisfied(1, 1) == True
    grid.place_char(1, 0, 'O')
    assert grid.is_square_satisfied(1, 1) == False


def test_move_square():
    # takes a while to run - made the grid 10x10 so there's slightly fewer
    # squares for it to check at random
    grid = Grid(10, 10, 100, 30) # grid starts out 100% red
    grid.place_char(0, 0, '')
    grid.move_square(1, 1)
    assert grid.grid[0][0].name == 'X'
    assert grid.grid[1][1].name == ''