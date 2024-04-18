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
