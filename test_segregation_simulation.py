"""Tests for the Square and Grid classes used in segregation_simulation"""

__author__ = "Ellen Whalen"

from segregation_simulation import Square
from segregation_simulation import Grid
import pytest


def test_x_o_count():
    dim = 20
    new_grid = Grid(dim, 50, 70)

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

    assert red_count == 50
    assert blue_count == 70

   

