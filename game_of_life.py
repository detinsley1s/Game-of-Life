#!/usr/bin/env python3

"""Game of Life
Programmed by Daniel Tinsley
Copyright 2016

The classic life simulation.
"""

import arcade


# dimensions of window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# dimensions of grid and tiles
GRID_DIMS = 100
TILE_DIMS = WINDOW_HEIGHT // GRID_DIMS


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, title='Game of Life')
        arcade.set_background_color(arcade.color.BLUE)
        self.grid = Grid()

    def on_draw(self):
        arcade.start_render()
        self.grid.draw()


class Tile:
    def __init__(self, x, y, dims, is_alive=False):
        self.x = x
        self.y = y
        self.dims = dims
        self.is_alive = is_alive


class Grid:
    def __init__(self):
        self.grid = []
        for row in range(GRID_DIMS):
            for col in range(GRID_DIMS):
                tile = Tile(
                    TILE_DIMS*col + TILE_DIMS//2,
                    TILE_DIMS*row + TILE_DIMS//2,
                    TILE_DIMS
                )
                self.grid.append(tile)

    def draw(self):
        for tile in self.grid:
            if tile.is_alive:
                color = arcade.color.BLACK
            else:
                color = arcade.color.WHITE
            arcade.draw_rectangle_filled(tile.x, tile.y, tile.dims, tile.dims, color)
            arcade.draw_rectangle_outline(tile.x, tile.y, tile.dims, tile.dims, arcade.color.BLACK)


def main():
    window = MainWindow()
    arcade.run()

if __name__ == '__main__':
    main()
