import pygame


class Button(pygame.Surface):

    def __init__(self, position, dimensions, text=None, background_colour=(255, 255, 255),
                 text_colour=(0,0,0), font='Arial', font_size=20, background_image=None, outline=(1, (0, 0, 0)),
                 click_handlers=[]):
        super().__init__(dimensions)
        self.position = position

        self.text = text
        self.background_colour = background_colour
        self.text_colour = text_colour
        self.font = pygame.SysFont(font, font_size)
        self.background_image = background_image
        self.outline = outline
        self.click_handlers = click_handlers

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if self.position[0] < x < self.position[0] + self.get_width() \
                        and self.position[1] < y < self.position[1] + self.get_height():
                    for handler in self.click_handlers:
                        handler()

    def render(self):
        if self.background_image:
            pass
            # Render background image
        else:
            self.fill(self.background_colour)

        pygame.draw.rect(self, self.outline[1], (0, 0, self.get_width(), self.get_height()), self.outline[0])

        label = self.font.render(self.text, True, self.text_colour)
        self.blit(label, ((self.get_width() - label.get_width())/2, (self.get_height() - label.get_height()) / 2))
