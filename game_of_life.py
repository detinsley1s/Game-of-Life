#!/usr/bin/env python3

"""Game of Life
Programmed by Daniel Tinsley
Copyright 2016

The classic life simulation.
"""

import sge


# dimensions of window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# grid and tile dimensions
GRID_DIMS = 100
TILE_DIMS = WINDOW_HEIGHT // GRID_DIMS


class Game(sge.dsp.Game):
    def event_key_press(self, key, char):
        if key == 'escape':
            self.event_close()

    def event_close(self):
        self.end()

    def event_mouse_button_press(self, button):
        mouse_x_loc = int(sge.mouse.get_y() // TILE_DIMS)
        mouse_y_loc = int(sge.mouse.get_x() // TILE_DIMS)
        if 0 <= mouse_y_loc < GRID_DIMS and 0 <= mouse_x_loc < GRID_DIMS:
            if button == 'left':
                grid.change_cell(mouse_x_loc, mouse_y_loc)


class Room(sge.dsp.Room):
    def event_step(self, time_passed, delta_mult):
        for tile in grid.grid:
            alive, dead = grid.get_total_neighbors(tile.x, tile.y)
            col = tile.x // TILE_DIMS
            row = tile.y // TILE_DIMS
            if tile.is_alive and (
                    alive < 2 or alive > 3) or (
                    not tile.is_alive and dead == 3):
                grid.change_cell(row, col)
            sge.game.project_sprite(tile.sprite, 0, tile.x, tile.y)


class Tile(sge.dsp.Object):
    def __init__(self, x, y, is_alive=False):
        self.is_alive = is_alive
        sprite = ALIVE_SPRITE if self.is_alive else DEAD_SPRITE
        super().__init__(x, y, sprite=sprite)


class Grid:
    def __init__(self):
        self.grid = []
        for row in range(GRID_DIMS):
            for col in range(GRID_DIMS):
                tile = Tile(
                    TILE_DIMS*col,
                    TILE_DIMS*row
                )
                self.grid.append(tile)

    def change_cell(self, mouse_x_loc, mouse_y_loc):
        actual_loc = mouse_x_loc*GRID_DIMS + mouse_y_loc
        self.grid[actual_loc] = Tile(
            mouse_y_loc*TILE_DIMS, mouse_x_loc*TILE_DIMS,
            not self.grid[actual_loc].is_alive
        )

    def get_total_neighbors(self, x, y):
        total_live = 0
        total_dead = 0
        col = x // TILE_DIMS
        row = y // TILE_DIMS
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if (i, j) != (row, col):
                    i %= GRID_DIMS
                    j %= GRID_DIMS
                    if self.grid[i*GRID_DIMS + j].is_alive:
                        total_live += 1
                    else:
                        total_dead += 1
        return total_live, total_dead


Game(
    width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
    window_text='Game of Life by Dan Tinsley',
    grab_input=True, collision_events_enabled=False
)

DEAD_SPRITE = (
    sge.gfx.Sprite(width=TILE_DIMS, height=TILE_DIMS, origin_x=0, origin_y=0)
)
ALIVE_SPRITE = (
    sge.gfx.Sprite(width=TILE_DIMS, height=TILE_DIMS, origin_x=0, origin_y=0)
)

DEAD_SPRITE.draw_rectangle(
    0, 0, DEAD_SPRITE.width, DEAD_SPRITE.height,
    outline=sge.gfx.Color("black"), fill=sge.gfx.Color("white")
)
ALIVE_SPRITE.draw_rectangle(
    0, 0, ALIVE_SPRITE.width, ALIVE_SPRITE.height,
    outline=sge.gfx.Color("black"), fill=sge.gfx.Color("black")
)

grid = Grid()

BACKGROUND = sge.gfx.Background([], sge.gfx.Color("blue"))
sge.game.start_room = Room([], background=BACKGROUND)

sge.game.mouse.visible = True

if __name__ == '__main__':
    sge.game.start()
