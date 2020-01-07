import pygame


class KeyInput:
    def __init__(self):
        self.pressed = false_dictionary(key_names.values())
        self.last_pressed = false_dictionary(key_names.values())
        self.tapped = false_dictionary(key_names.values())

    def update_pressed(self):
        keys_pressed = pygame.key.get_pressed()
        for code, name in key_names.items():
            if keys_pressed[code]:
                self.pressed[name] = 1
            else:
                self.pressed[name] = 0

    def update_tapped(self):
        for name in self.pressed.keys():
            self.tapped[name] = self.pressed[name] - self.last_pressed[name]

    def update(self):
        self.last_pressed = dict(self.pressed)
        self.update_pressed()
        self.update_tapped()


def false_dictionary(keys, defualt=0):
    dic = {}
    for key in keys:
        dic[key] = defualt
    return dic


def invert_dict(dic):
    """ return an inverted dictionary. """
    new = {}
    for key, val in dic.items():
        if val in new:
            new[val].append(key)
        else:
            new[val] = [key]
    return new


key_names = {
    pygame.K_BACKSPACE: "BACKSPACE",
    pygame.K_CLEAR: "CLEAR",
    pygame.K_RETURN: "RETURN",
    pygame.K_PAUSE: "PAUSE",
    pygame.K_ESCAPE: "ESCAPE",
    pygame.K_SPACE: "SPACE",
    pygame.K_EXCLAIM: "EXCLAIM",
    pygame.K_QUOTEDBL: "QUOTEDBL",
    pygame.K_HASH: "HASH",
    pygame.K_DOLLAR: "DOLLAR",
    pygame.K_AMPERSAND: "AMPERSAND",
    pygame.K_QUOTE: "QUOTE",
    pygame.K_LEFTPAREN: "PARENTHESIS",
    pygame.K_RIGHTPAREN: "PARENTHESIS",
    pygame.K_ASTERISK: "ASTERISK",
    pygame.K_PLUS: "SIGN",
    pygame.K_COMMA: "COMMA",
    pygame.K_MINUS: "SIGN",
    pygame.K_PERIOD: "PERIOD",
    pygame.K_SLASH: "SLASH",
    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_COLON: "COLON",
    pygame.K_SEMICOLON: "SEMICOLON",
    pygame.K_LESS: "LESSTHAN",
    pygame.K_EQUALS: "EQUALS",
    pygame.K_GREATER: "GREATERTHAN",
    pygame.K_QUESTION: "MARK",
    pygame.K_AT: "AT",
    pygame.K_LEFTBRACKET: "BRACKET",
    pygame.K_BACKSLASH: "BACKSLASH",
    pygame.K_RIGHTBRACKET: "BRACKET",
    pygame.K_CARET: "CARET",
    pygame.K_UNDERSCORE: "UNDERSCORE",
    pygame.K_BACKQUOTE: "GRAVE",
    pygame.K_a: "A",
    pygame.K_b: "B",
    pygame.K_c: "C",
    pygame.K_d: "D",
    pygame.K_e: "E",
    pygame.K_f: "F",
    pygame.K_g: "G",
    pygame.K_h: "H",
    pygame.K_i: "I",
    pygame.K_j: "J",
    pygame.K_k: "K",
    pygame.K_l: "L",
    pygame.K_m: "M",
    pygame.K_n: "N",
    pygame.K_o: "O",
    pygame.K_p: "P",
    pygame.K_q: "Q",
    pygame.K_r: "R",
    pygame.K_s: "S",
    pygame.K_t: "T",
    pygame.K_u: "U",
    pygame.K_v: "V",
    pygame.K_w: "W",
    pygame.K_x: "X",
    pygame.K_y: "Y",
    pygame.K_z: "Z",
    pygame.K_UP: "UPARROW",
    pygame.K_DOWN: "DOWNARROW",
    pygame.K_LEFT: "LEFTARROW",
    pygame.K_RIGHT: "RIGHTARROW",
}
key_codes = invert_dict(key_names)

