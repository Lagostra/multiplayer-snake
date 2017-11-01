import pygame


class List(pygame.Surface):

    def __init__(self, position, dimensions, data, text_map, background_colour=(255, 255, 255), selected_colour=(0, 255, 0),
                 text_colour=(0, 0, 0), font='Arial', font_size=20, outline=(1, (0, 0, 0)), pad=0.4):
        super().__init__(dimensions)
        self.position = position
        self.data = data
        self.text_map = text_map

        self.background_colour = background_colour
        self.selected_colour = selected_colour
        self.text_colour = text_colour
        self.font = pygame.font.SysFont(font, font_size)
        self.outline = outline
        self.pad = pad

        self.selected_item = None
        self.scroll_offset = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not (self.position[0] < x < self.position[0] + self.get_width()
                        and self.position[1] < y < self.position[1] + self.get_height()):
                    continue
                if event.button == 4:
                    self.scroll_offset -= 10
                elif event.button == 5:
                    self.scroll_offset += 10
                elif event.button == 1:
                    index = int((y + self.scroll_offset)/(self.font.get_linesize()*(1 + 2*self.pad)))
                    if 0 <= index < len(self.data):
                        self.selected_item = self.data[index]

                upper_limit = max(len(self.data) * (self.font.get_linesize() * (1 + 2*self.pad)) - self.get_height(), 0)
                if self.scroll_offset < 0:
                    self.scroll_offset = 0
                elif self.scroll_offset > upper_limit:
                    self.scroll_offset = upper_limit

    def render(self):
        self.fill(self.background_colour)

        if self.outline:
            pygame.draw.rect(self, self.outline[1], (0, 0, self.get_width(), self.get_height()), self.outline[0])

        ls = self.font.get_linesize()
        for i in range(len(self.data)):
            if 0 <= (i + 1) * (ls * (1 + 2*self.pad)) - self.scroll_offset \
                    and i * (ls * (1 + 2*self.pad)) - self.scroll_offset <= self.get_height():
                y = i * (ls * (1 + 2*self.pad)) - self.scroll_offset
                if self.data[i] == self.selected_item:
                    pygame.draw.rect(self, self.selected_colour, (self.outline[0],
                                                                  y + 1,
                                                                  self.get_width() - 2*self.outline[0],
                                                                  ls * (1 + 2*self.pad) - 1))

                label = self.font.render(self.text_map(self.data[i]), True, self.text_colour)
                self.blit(label, (ls * self.pad, y + ls * self.pad))

                y = (i + 1) * (ls * (1 + 2*self.pad))
                pygame.draw.line(self, (0, 0, 0), (0, y - self.scroll_offset), (self.get_width(), y - self.scroll_offset))
