import pygame

from .vectors import Vector


class CompositeSprite:
    def __init__(self, sprites, anchors):
        self.sprites = sprites
        self.anchors = anchors

    def show(self, window_obj, pos, pos_anchor):
        base_name = pos_anchor.index("->")
        base_sprite = pos_anchor[:base_name]
        self.sprites[base_sprite].show(window_obj, pos)
        sprites_placed = {base_name}
        for anchor in self.anchors:
            pass


class Sprite:
    def __init__(self, sheet_filename, sheet_size):
        self.sprite_sheet = SpriteSheet(sheet_filename, sheet_size)
        self.image_sequences = {"DEFAULT": [(0, 0)]}
        self.current_sequence = None
        self.current_sequence_number = 0    # Image index in sequence
        self.time_since_last_image_change = 0

    def show(self, window_obj, pos, scale=1):
        image_number = self.image_sequences[self.current_sequence][self.current_sequence_number]
        self.sprite_sheet.draw(window_obj, image_number, pos, scale)

    def cycle_images(self, game_obj, sequence, change_period):

        if self.current_sequence != sequence:
            self.current_sequence = sequence
            self.current_sequence_number = 0

        elif self.time_since_last_image_change >= change_period:
            self.time_since_last_image_change = 0
            sequence_length = len(self.image_sequences[sequence])
            self.current_sequence_number = (self.current_sequence_number + 1) % sequence_length

        self.time_since_last_image_change += game_obj.dtime


class SpriteSheet:
    def __init__(self, filename, sheet_size):
        self.filename = filename
        self.sheet_size = sheet_size.copy()
        self.num_cells = self.sheet_size.x * self.sheet_size.y

        self.sheet_image = None
        self.scaled_image = None
        self.image_scale = None
        self.load_image()

        self.sheet_image_size = None
        self.image_size = None
        self.set_image_size()

        self.image_positions = []
        self.set_image_positions()

        self.handles = None
        self.load_handles()

    def load_image(self):
        self.sheet_image = pygame.image.load(self.filename).convert_alpha()

    def load_handles(self):
        extension_index = self.filename.rfind(".")
        filename_no_ext = self.filename[:extension_index]
        handle_file_name = filename_no_ext + "_handles.txt"
        try:
            handles_str = open(handle_file_name, "r").read()
            self.handles = eval(handles_str)
        except FileNotFoundError:
            print("NO HANDLE FILE FOR " + self.filename)
            self.handles = {}

    def set_scaled_image(self, window_obj, scale):
        self.image_scale = scale * window_obj.window_scale / min(self.image_size)
        new_size = (self.sheet_image_size * self.image_scale).rounded().tuple()
        self.scaled_image = pygame.transform.scale(self.sheet_image, new_size)

    def set_image_size(self):
        image_rect = self.sheet_image.get_rect()
        self.sheet_image_size = Vector(image_rect.width, image_rect.height)
        self.image_size = Vector(self.sheet_image_size.x / self.sheet_size.x,
                                 self.sheet_image_size.y / self.sheet_size.y)

    def set_image_positions(self):
        self.image_positions = {}
        for i in range(self.num_cells):
            key = (i % self.sheet_size.x, i // self.sheet_size.x)
            pos = Vector(key[0], key[1])
            pos.x *= self.image_size.x
            pos.y *= self.image_size.y
            self.image_positions[key] = pos

    def draw(self, window_obj, image_num, pos, scale=1):
        if scale != self.image_scale:
            self.set_scaled_image(window_obj, scale)

        sheet_pos = (self.image_positions[image_num] * self.image_scale).ceiled()
        sheet_size = (self.image_size * self.image_scale).floored()
        sheet_rect = sheet_pos.tuple() + sheet_size.tuple()

        display_pos = window_obj.display_pos(pos) - Vector(sheet_rect[2], sheet_rect[3]) / 2
        window_obj.window.blit(self.scaled_image, display_pos.tuple(), sheet_rect)
