#!/usr/bin/env python3

"""Game of Life
Programmed by Daniel Tinsley
Copyright 2016

The classic life simulation.
"""

from random import randint
import sge


# dimensions of window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# grid and tile dimensions
GRID_DIMS = 100
TILE_DIMS = WINDOW_HEIGHT // GRID_DIMS


class Game(sge.dsp.Game):
    """This class handles most parts of the game which work globally.

    Subclass of sge.dsp.Game

    Methods:
    event_close
    event_key_press
    event_mouse_button_press
    """

    def event_key_press(self, key, char):
        """Detect when a key is pressed on the keyboard.

        Overrides method from superclass sge.dsp.game

        Parameters:
        key -- the identifier string of the key that was pressed
        char -- the Unicode character associated with the key press
        """
        if key == 'escape':
            self.event_close()
        elif key == 'r':
            grid.randomize()
        elif key == 's':
            grid.grid_is_alive = not grid.grid_is_alive
        elif key == 'c':
            grid.clear()

    def event_close(self):
        """Close the application."""
        self.end()

    def event_mouse_button_press(self, button):
        """Detect when a mouse button is pressed.

        Overrides method from superclass sge.dsp.Game

        Parameter:
        button -- the identifier string of the mouse button that was
                  pressed
        """
        # x, y are switched because grid coords differ from list coords
        # Grid coords use the Cartesian system, unlike lists
        mouse_x_loc = int(sge.mouse.get_y() // TILE_DIMS)
        mouse_y_loc = int(sge.mouse.get_x() // TILE_DIMS)

        if 0 <= mouse_y_loc < GRID_DIMS and 0 <= mouse_x_loc < GRID_DIMS:
            if button == 'left':
                grid.change_cell(mouse_x_loc, mouse_y_loc)


class Room(sge.dsp.Room):
    """This class stores the settings and objects found in a level.

    Subclass of a sge.dsp.Room

    Method:
    event_step
    """

    def event_step(self, time_passed, delta_mult):
        """Do level processing once each frame.

        Overrides method from superclass sge.dsp.Room

        Parameters:
        time_passed -- the total milliseconds that have passed during
                       the last frame
        delta_mult -- what speed and movement should be multiplied by
                      this frame due to delta timing
        """
        # Display the instructions
        sge.game.project_text(
            LABEL_FONT, 'MOUSE', WINDOW_WIDTH - 137, 147,
            color=sge.gfx.Color('black'), halign='left', valign='middle'
        )
        sge.game.project_text(
            INSTRUCTIONS_FONT, 'Left Click: Add Tiles', WINDOW_WIDTH - 177,
            197, color=sge.gfx.Color('black'), halign='left', valign='middle'
        )
        sge.game.project_text(
            LABEL_FONT, 'KEYBOARD', WINDOW_WIDTH - 155, WINDOW_HEIGHT - 287,
            color=sge.gfx.Color('black'), halign='left', valign='middle'
        )
        sge.game.project_text(
            INSTRUCTIONS_FONT, 'C: Clear Board', WINDOW_WIDTH - 177,
            WINDOW_HEIGHT - 237, color=sge.gfx.Color('black'), halign='left',
            valign='middle'
        )
        sge.game.project_text(
            INSTRUCTIONS_FONT, 'R: Randomize Board', WINDOW_WIDTH - 177,
            WINDOW_HEIGHT - 207, color=sge.gfx.Color('black'), halign='left',
            valign='middle'
        )
        sge.game.project_text(
            INSTRUCTIONS_FONT, 'S: Start Animation', WINDOW_WIDTH - 177,
            WINDOW_HEIGHT - 177, color=sge.gfx.Color('black'), halign='left',
            valign='middle'
        )
        sge.game.project_text(
            INSTRUCTIONS_FONT, 'Esc: Exit Game', WINDOW_WIDTH - 177,
            WINDOW_HEIGHT - 147, color=sge.gfx.Color('black'), halign='left',
            valign='middle'
        )

        # Draw the cells that are alive and determine which will
        # continue living or will die
        for tile in grid.grid:
            if grid.grid_is_alive:
                alive = grid.get_total_neighbors(tile.x, tile.y)
                col = tile.x // TILE_DIMS
                row = tile.y // TILE_DIMS
                if tile.is_alive and (alive < 2 or alive > 3) or (
                        not tile.is_alive and alive == 3):
                    grid.change_cell(row, col)
        for idx, tile in enumerate(grid.grid):
            sge.game.project_sprite(tile.sprite, 0, tile.x, tile.y)
            grid.grid[idx].changed = False


class Tile(sge.dsp.Object):
    """This class is responsible for the individual tiles.

    Subclass of sge.dsp.Object

    Instance variables:
    changed -- boolean denoting if the cell changed its status during
               a single life stage
    is_alive -- boolean denoting if the cell is living
    """

    def __init__(self, x, y, is_alive=False, changed=False):
        """Determine the screen placement and sprite for the tile.

        Calls the superclass' constructor method to form the tile

        Parameters:
        x -- the x coordinate on a Cartesian plane of the tile
        y -- the y coordinate on a Cartesian plane of the tile
        is_alive -- boolean denoting if the cell is living
        changed -- boolean denoting if the cell changed its status
                   during a single life stage
        """
        self.is_alive = is_alive
        self.changed = changed
        sprite = ALIVE_SPRITE if self.is_alive else DEAD_SPRITE
        super().__init__(x, y, sprite=sprite)


class Grid:
    """This class is responsible for the grid and its functions.

    Methods:
    change_cell
    clear
    get_total_neighbors
    randomize

    Instance variables:
    grid -- list that contains the cell locations and sprites
    grid_is_alive -- boolean that denotes if the grid is running
    """

    def __init__(self):
        """Initialize the instance variables and prepare the grid."""
        self.grid_is_alive = False
        self.grid = []
        for row in range(GRID_DIMS):
            for col in range(GRID_DIMS):
                tile = Tile(TILE_DIMS*col, TILE_DIMS*row)
                self.grid.append(tile)

    def change_cell(self, mouse_x_loc, mouse_y_loc):
        """Change the cell from alive to dead or vice versa.

        Parameters:
        mouse_x_loc -- the x coordinate of the changed cell
        mouse_y_loc -- the y coordinate of the changed cell
        """
        actual_loc = mouse_x_loc*GRID_DIMS + mouse_y_loc
        self.grid[actual_loc] = Tile(
            mouse_y_loc*TILE_DIMS, mouse_x_loc*TILE_DIMS,
            not self.grid[actual_loc].is_alive, True
        )

    def get_total_neighbors(self, x_loc, y_loc):
        """Get the total neighbors that are alive in all 8 directions.

        Parameters:
        x_loc -- the x coordinate of the cell
        y_loc -- the y coordinate of the cell
        """
        total = 0
        col = x_loc // TILE_DIMS
        row = y_loc // TILE_DIMS
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if (i, j) != (row, col):
                    i %= GRID_DIMS
                    j %= GRID_DIMS
                    if self.grid[i*GRID_DIMS + j].changed:
                        if not self.grid[i*GRID_DIMS + j].is_alive:
                            total += 1
                    else:
                        if self.grid[i*GRID_DIMS + j].is_alive:
                            total += 1
        return total

    def randomize(self):
        """Randomize placement of living cells on the grid."""
        for row in range(GRID_DIMS):
            for col in range(GRID_DIMS):
                if randint(0, 2) == 1:
                    self.change_cell(col, row)

    def clear(self):
        """Clear the grid and stop it from running."""
        for row in range(GRID_DIMS):
            for col in range(GRID_DIMS):
                self.grid[col*GRID_DIMS + row].is_alive = True
                self.change_cell(col, row)
        self.grid_is_alive = False


# Construct a Game object so the game can begin
Game(
    width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
    window_text='Game of Life by Dan Tinsley',
    grab_input=True, collision_events_enabled=False
)

# Create the font
INSTRUCTIONS_FONT = sge.gfx.Font(name='fonts/horta.ttf', size=25)
LABEL_FONT = sge.gfx.Font(name='fonts/horta.ttf', size=36, underline=True)

# Create the sprites and tiles
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

# Instantiate the grid for gameplay
grid = Grid()

# Instantiate the board with a specified background color
BACKGROUND = sge.gfx.Background([], sge.gfx.Color("gray"))
sge.game.start_room = Room([], background=BACKGROUND)

# Make the mouse cursor visible for usage in the game
sge.game.mouse.visible = True

if __name__ == '__main__':
    sge.game.start()
