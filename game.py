from scene import *
from pathlib import Path
import ui


class MyScene(Scene):
    def setup(self):
        # load dirt texture
        dirt_img_fp = Path(__file__).parent.joinpath('assets/dirt.png')
        dirt_img = ui.Image(str(dirt_img_fp))
        dirt_texture = Texture(dirt_img)

        # create a Rect for tracking whats on screen
        screen_rect = ui.Path.rect(0, 0, self.size.w, self.size.h)
        screen_rect.line_width = 3
        self.screen_rect_node = ShapeNode(
            screen_rect, stroke_color='midnightblue', fill_color='clear')
        self.screen_rect_node.position = ((self.size.w / 2), (self.size.h / 2))
        self.add_child(self.screen_rect_node)

        # create map
        rows, cols = 100, 100
        self.tiles = [[0] * cols] * rows
        self.ground = Node(parent=self)
        for x in range(rows):
            for y in range(cols):
                tile = SpriteNode(
                    dirt_texture, position=(x * 32, y * 32), size=(32, 32))
                tile.selected = False
                self.tiles[x][y] = tile
                # check if tile would be visible
                if self.screen_rect_node.bbox.intersects(tile.bbox):
                    self.ground.add_child(tile)

    def did_change_size(self):
        pass

    def update(self):
        pass

    def touch_began(self, touch):
        pass

    def touch_moved(self, touch):
        # get the difference between previous touch location and current
        location_diff = touch.location - touch.prev_location

        # loop through all of our tiles and add the diff to their positions
        self.screen_rect_node.position += location_diff
        for x in range(len(self.tiles)):
            for y in range(x):
                tile = self.tiles[x][y]
                tile.position += location_diff
                if self.screen_rect_node.bbox.contains_rect(tile.bbox):
                    self.ground.add_child(tile)

        for tile_node in self.ground.children:
            tile_node.position += location_diff

    def touch_ended(self, touch):
        # remove the previous selection
        for tile in self.ground.children:
            if tile.selected:
                for child in tile.children:
                    if (isinstance(child, ShapeNode) and child.is_selection):
                        child.remove_from_parent()

            # find the cell at the touched location
            if tile.bbox.contains_point(touch.location):
                # draw a rect with the same size and position as tile
                rect = ui.Path.rect(*tile.position, 32, 32)
                rect.line_width = 1
                rect_node = ShapeNode(
                    rect, stroke_color='white', fill_color='clear')
                rect_node.is_selection = True
                tile.selected = True
                tile.add_child(rect_node)


if __name__ == '__main__':
    run(MyScene(), show_fps=True)
