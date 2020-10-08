from scene import *
from pathlib import Path
import ui

class MyScene(Scene):
	def setup(self):
		# load dirt texture
		dirt_img_fp = Path(__file__).parent.joinpath('dirt.png')
		dirt_img = ui.Image(str(dirt_img_fp))
		dirt_texture = Texture(dirt_img)
		
		# create map
		rows,cols = 100,100
		self.ground = Node(parent=self)
		for x in range(rows):
			for y in range(cols):
				tile = SpriteNode(dirt_texture, position=(x*32,y*32), size=(32,32))
				tile.selected = False
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
		for tile_node in self.ground.children:
			tile_node.position += location_diff
	
	def touch_ended(self, touch):
		# remove the previous selection
		for tile in self.ground.children:
			if tile.selected:
				for child in tile.children:
					if isinstance(child, ShapeNode):
						if child.is_selection:
							child.remove_from_parent()

			# find the cell at the touched location
			if tile.bbox.contains_point(touch.location):
				# draw a rect at the same position as tile
				rect = ui.Path.rect(
					*tile.position, 32, 32
				)
				rect.line_width = 1
				rect_node = ShapeNode(rect, stroke_color='white', fill_color='clear')
				rect_node.is_selection = True
				tile.selected = True
				tile.add_child(rect_node)
					

if __name__ == '__main__':
	run(MyScene(), show_fps=True)
