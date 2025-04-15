
from settings import *
from timer import Timer


class Menu:
    def __init__(self, player, toggle_menu):

        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        # entries
        self.sell_options = list(self.player.item_inventory.keys())
        self.buy_options = list(self.player.seed_inventory.keys())
        self.options = {'sell': self.sell_options, 'buy': self.buy_options}
        self.setup()

        # movement
        self.buy_sell_index = 'sell'
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        text_surf = self.font.render(f'RM{self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(text_surf, text_rect)

    def setup(self):

        # create the text surfaces
        self.buy_text_surfs = []
        self.buy_total_height = 0

        for item in self.buy_options:
            text_surf = self.font.render(item, False, 'Black')
            self.buy_text_surfs.append(text_surf)
            self.buy_total_height += text_surf.get_height() + (self.padding * 2)

        self.buy_total_height += (len(self.buy_text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.buy_total_height / 2
        self.buy_rect = pygame.Rect(3 * (SCREEN_WIDTH / 4) - self.width / 2, self.menu_top, self.width, self.buy_total_height)

        # create the text surfaces
        self.sell_text_surfs = []
        self.sell_total_height = 0

        for item in self.sell_options:
            text_surf = self.font.render(item, False, 'Black')
            self.sell_text_surfs.append(text_surf)
            self.sell_total_height += text_surf.get_height() + (self.padding * 2)

        self.sell_total_height += (len(self.sell_text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.sell_total_height / 2
        self.sell_rect = pygame.Rect((SCREEN_WIDTH / 4) - self.width / 2, self.menu_top, self.width,
                                     self.sell_total_height)

        # buy / sell text surface
        self.buy_text = self.font.render('buy', False, 'Black')
        self.sell_text = self.font.render('sell', False, 'Black')

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.index = 0
                self.buy_sell_index = 'buy'
                self.timer.activate()

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.index = 0
                self.buy_sell_index = 'sell'
                self.timer.activate()

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                # get item
                current_item = self.options[self.buy_sell_index][self.index]

                # sell
                if self.buy_sell_index == 'sell':
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]

                # buy
                else:
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]

        # the values
        if self.index < 0:
            self.index = len(self.options[self.buy_sell_index]) - 1
        elif self.index > len(self.options[self.buy_sell_index]) - 1:
            self.index = 0

    def show_entry(self, text_surf, amount, top, selected, buy_sell):

        if buy_sell == 'sell':
            rect=self.sell_rect
        else:
            rect=self.buy_rect

        # background
        bg_rect = pygame.Rect(rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        # text
        text_rect = text_surf.get_rect(midleft=(rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright=(rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            if self.buy_sell_index == 'sell':  # sell
                pos_rect = self.sell_text.get_rect(midleft=(rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:  # buy
                pos_rect = self.buy_text.get_rect(midleft=(rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()

        for text_index, text_surf in enumerate(self.buy_text_surfs):
            top = self.buy_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index and self.buy_sell_index=='buy', 'buy')

        for text_index, text_surf in enumerate(self.sell_text_surfs):
            top = self.sell_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index and self.buy_sell_index=='sell', 'sell')