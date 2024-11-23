'''
on 7 discard down to 7 resources
road can start on other people's properties
'''

import sys, pygame
import random
import math

pygame.init()

scrn_width = 800
scrn_height = 600

dx = scrn_width / 800

scrn = pygame.display.set_mode((scrn_width, scrn_height))

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), int(12 * dx))

black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
light_blue = (51, 153, 255)
brick_color = (186, 28, 15)
wood_color = (33, 84, 16)
green = (0, 255, 0)
yellow = (255, 255, 0)
sheep_color = (153, 255, 102)
wheat_color = (242, 207, 12)
stone_color = (187, 192, 185)
white = (255, 255, 255)

player_one_color = (60, 220, 170)
player_two_color = (43, 27, 191)
player_three_color = (255, 0, 0)
player_four_color = (251, 3, 255)

player_colors = (player_one_color, player_two_color, player_three_color,
                 player_four_color, (0, 0, 0))

tile_size_mod = 40 * dx


def dif_mess(msg, color, x, y):
    mess = font.render(msg, True, color)
    scrn.blit(mess, [x, y])


def stock_mess(msg, color, x, y, size):
    font = pygame.font.Font(pygame.font.get_default_font(), int(size * dx))
    mess = font.render(msg, True, color)
    scrn.blit(mess, [x, y])


class Game:
    def __init__(self):

        self.tile_types = [
            "hills", "hills", "hills", "hills", "forest", "forest", "forest",
            "forest", "mountain", "mountain", "mountain", "mountain", "fields",
            "fields", "fields", "fields", "pasture", "pasture", "pasture",
            "pasture"
        ]
        self.tile_values = [
            10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 5, 4, 3, 8, 5, 6, 11
        ]

        self.nearby_points_mod = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0),
                                  (1, 1), (0, 1), (-1, 1)]

        self.tiles = [
            Tile((3, 1)),
            Tile((5, 1)),
            Tile((7, 1)),
            Tile((2, 3)),
            Tile((4, 3)),
            Tile((6, 3)),
            Tile((8, 3)),
            Tile((1, 5)),
            Tile((3, 5)),
            Tile((5, 5)),
            Tile((7, 5)),
            Tile((9, 5)),
            Tile((2, 7)),
            Tile((4, 7)),
            Tile((6, 7)),
            Tile((8, 7)),
            Tile((3, 9)),
            Tile((5, 9)),
            Tile((7, 9))
        ]
        self.all_corners = [(1, 5), (1, 6), (2, 3), (2, 4), (2, 7), (2, 8),
                            (3, 1), (3, 2), (3, 5), (3, 6), (3, 9), (3, 10),
                            (4, 0), (4, 3), (4, 4), (4, 7), (4, 8), (4, 11),
                            (5, 1), (5, 2), (5, 5), (5, 6), (5, 9), (5, 10),
                            (6, 0), (6, 3), (6, 4), (6, 7), (6, 8), (6, 11),
                            (7, 1), (7, 2), (7, 5), (7, 6), (7, 9), (7, 10),
                            (8, 0), (8, 3), (8, 4), (8, 7), (8, 8), (8, 11),
                            (9, 1), (9, 2), (9, 5), (9, 6), (9, 9), (9, 10),
                            (10, 3), (10, 4), (10, 7), (10, 8), (11, 5),
                            (11, 6)]

        self.resource_list = ("brick", "wood", "stone", "wheat", "wool")

        self.cards = [
            "knight", "knight", "knight", "knight", "knight", "knight",
            "knight", "knight", "knight", "knight", "knight", "knight",
            "knight", "knight", "victory point", "victory point",
            "victory point", "victory point", "victory point", "double road",
            "double road", "year of plenty", "year of plenty", "monopoly",
            "monopoly"
        ]

        self.settlement_button = Stock_buttons(
            (scrn_width / 10 * 7), (scrn_height / 10 * 8), (scrn_width / 12),
            (scrn_height / 11))

        self.road_button = Stock_buttons(
            (scrn_width / 10 * 9), (scrn_height / 10 * 8), (scrn_width / 12),
            (scrn_height / 11))

        self.card_button = Stock_buttons(
            (scrn_width / 10 * 9), (scrn_height / 10 * 9), (scrn_width / 12),
            (scrn_height / 11))

        self.city_button = Stock_buttons(
            (scrn_width / 10 * 7), (scrn_height / 10 * 9), (scrn_width / 12),
            (scrn_height / 11))

        self.trade_button = Stock_buttons(
            (scrn_width / 10 * 5), (scrn_height / 10 * 8), (scrn_width / 10),
            (scrn_height / 11))

        self.card_play_button = Stock_buttons(
            (scrn_width / 10 * 5), (scrn_height / 10 * 9), (scrn_width / 10),
            (scrn_height / 11))

        self.end_turn = Stock_buttons(
            (scrn_width / 10 * 8), (scrn_height / 10 * 8), (scrn_width / 12),
            (scrn_height / 12))

        self.trade_menu = Stock_buttons((scrn_width / 32), (scrn_height / 12),
                                        (scrn_width / 11 * 7),
                                        (scrn_height / 12 * 10))

        self.trade_accept = Stock_buttons(
            (scrn_width / 9 * 3), (scrn_height / 14 * 11), (scrn_width / 9),
            (scrn_height / 14))

        self.intro_buttons = [
            Stock_buttons(scrn_width / 5, scrn_height / 7 * 4, scrn_width / 4,
                          scrn_height / 14),
            Stock_buttons(scrn_width / 5, scrn_height / 7 * 5, scrn_width / 4,
                          scrn_height / 14),
            Stock_buttons(scrn_width / 5, scrn_height / 7 * 6, scrn_width / 4,
                          scrn_height / 14),
            Stock_buttons(scrn_width / 2, scrn_height / 7 * 4, scrn_width / 24,
                          scrn_height / 24),
            Stock_buttons(scrn_width / 20 * 12, scrn_height / 7 * 4,
                          scrn_width / 24, scrn_height / 24)
        ]

        self.vic_button = Stock_buttons(
            (scrn_width / 18 * 7), (scrn_height / 10 * 9), (scrn_width / 10),
            (scrn_height / 11))

        self.intro_screen = True
        self.game_active = False
        self.tutorial_active = False

        self.trade_active = False
        self.trade_buttons = []
        self.trade_values = []
        for i in range(20):
            self.trade_buttons.append(Button())
        for i in range(10):
            self.trade_values.append(Trade_values())
        self.trade_select_buttons = [
            Stock_buttons(scrn_width / 22 * 10, scrn_height / 7 * 6,
                          scrn_width / 24, scrn_height / 24),
            Stock_buttons(scrn_width / 20 * 12, scrn_height / 7 * 6,
                          scrn_width / 24, scrn_height / 24)
        ]
        self.trading_player = 0

        self.settlement_placement_active = False
        self.active_settlements = []
        self.settlement_locations = []
        self.available_settlement_locations = [(1, 5), (1, 6), (2, 3), (2, 4),
                                               (2, 7), (2, 8), (3, 1), (3, 2),
                                               (3, 5), (3, 6), (3, 9), (3, 10),
                                               (4, 0), (4, 3), (4, 4), (4, 7),
                                               (4, 8), (4, 11), (5, 1), (5, 2),
                                               (5, 5), (5, 6), (5, 9), (5, 10),
                                               (6, 0), (6, 3), (6, 4), (6, 7),
                                               (6, 8), (6, 11), (7, 1), (7, 2),
                                               (7, 5), (7, 6), (7, 9), (7, 10),
                                               (8, 0), (8, 3), (8, 4), (8, 7),
                                               (8, 8), (8, 11), (9, 1), (9, 2),
                                               (9, 5), (9, 6), (9, 9), (9, 10),
                                               (10, 3), (10, 4), (10, 7),
                                               (10, 8), (11, 5), (11, 6)]

        self.city_placement_active = False
        self.active_cities = []
        self.city_locations = []

        self.road_placement_active = False
        self.active_roads = []
        self.road_locations = []
        self.road_start = None
        self.road_end = None

        self.players = []
        self.active_player = 1
        self.robber_active = False

        self.harbor_choices = self.border_check()
        self.active_harbors = []
        self.harbor_count = 7

        self.vic_calc_active = False
        self.vic_exit = Stock_buttons(int(490 * dx), int(60 * dx),
                                      int(15 * dx), int(15 * dx))
        self.vic_buttons = []
        self.vic_settlement = 0
        self.vic_city = 0
        self.vic_road = 0
        self.vic_army = 0

        self.robber_locations = []

        for tile in range(len(self.tiles)):
            self.robber_locations.append(self.tiles[tile].tile_locations[0])

        for i in range(self.harbor_count):
            self.active_harbors.append(Harbor(self.harbor_choices))
            self.harbor_choices.remove(self.active_harbors[i].harbor_position)
            self.harbor_choices.remove(
                (self.active_harbors[i].harbor_position[1],
                 self.active_harbors[i].harbor_position[0]))

        self.double_road = False
        self.road_counter = 0

        self.robber_location = 9

        self.resource_trade1 = [0, 0, 0, 0, 0]
        self.resource_trade2 = [0, 0, 0, 0, 0]

        self.turn_counter = 1

        self.player_count = 2

    #controls for the opening screen
    def intro_screen_controls(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for i in range(len(self.intro_buttons)):
                    if pos[0] >= self.intro_buttons[i].x and pos[0] <= (
                            self.intro_buttons[i].x +
                            self.intro_buttons[i].width
                    ) and pos[1] >= self.intro_buttons[i].y and pos[1] <= (
                            self.intro_buttons[i].y +
                            self.intro_buttons[i].height):
                        #game start
                        if i == 0:
                            self.intro_screen = False

                            for j in range(self.player_count + 1):
                                self.players.append(Player())
                            self.start_rounds = self.player_count * 2 - 1
                            self.players[-1].resources = [99, 99, 99, 99, 99]

                            for m in range(len(self.players) - 1):
                                self.vic_buttons.append(
                                    Stock_buttons(
                                        int((90 * (m + 1) + 40) * dx),
                                        int(200 * dx), int(20 * dx),
                                        int(20 * dx)))

                            for h in range(len(self.players) - 1):
                                self.vic_buttons.append(
                                    Stock_buttons(
                                        int((90 * (h + 1) + 40) * dx),
                                        int(240 * dx), int(20 * dx),
                                        int(20 * dx)))

                            self.game_active = True
                        #tutorial start
                        if i == 1:
                            self.intro_screen = False
                            self.tutorial_active = True
                            print("Tutorial is in progress: " +
                                  str(self.tutorial_active))
                        #quit out
                        if i == 2:

                            pygame.quit()
                            quit()

                        #decrease player count
                        if i == 3 and self.player_count > 2:

                            self.player_count -= 1

                        #increase player count
                        if i == 4 and self.player_count < 4:

                            self.player_count += 1

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.robber_active == True:
                    for tiles in range(len(self.robber_locations)):
                        if pos[0] >= (
                            (self.robber_locations[tiles][0] * tile_size_mod) +
                            (tile_size_mod) - 12 * dx) and pos[0] <= (
                                (self.robber_locations[tiles][0] *
                                 tile_size_mod) +
                                (tile_size_mod) + 12 * dx) and pos[1] >= (
                                    (self.robber_locations[tiles][1] *
                                     tile_size_mod) + (tile_size_mod / 2) -
                                    (12 * dx)) and pos[1] <= (
                                        (self.robber_locations[tiles][1] *
                                         tile_size_mod) + (tile_size_mod / 2) +
                                        (12 * dx)):
                            self.robber_location = (tiles)
                            self.robber_active = False

                elif self.robber_active == False:
                    #___BUTTONS ON THE RIGHT SIDE OF SCREEN
                    if pos[0] >= self.settlement_button.x and pos[0] <= (
                            self.settlement_button.x +
                            self.settlement_button.width
                    ) and pos[1] >= self.settlement_button.y and pos[1] <= (
                            self.settlement_button.y +
                            self.settlement_button.height):

                        if self.settlement_placement_active == False:
                            self.settlement_placement_active = True
                            print(self.settlement_placement_active)
                        elif self.settlement_placement_active == True:
                            self.settlement_placement_active = False
                            print(self.settlement_placement_active)

                    if pos[0] >= self.road_button.x and pos[0] <= (
                            self.road_button.x + self.road_button.width
                    ) and pos[1] >= self.road_button.y and pos[1] <= (
                            self.road_button.y + self.road_button.height):

                        if self.road_placement_active == False:
                            self.road_placement_active = True
                            print(self.road_placement_active)
                        elif self.road_placement_active == True:
                            self.road_placement_active = False
                            print(self.road_placement_active)

                    if pos[0] >= self.city_button.x and pos[0] <= (
                            self.city_button.x + self.city_button.width
                    ) and pos[1] >= self.city_button.y and pos[1] <= (
                            self.city_button.y + self.city_button.height):

                        if self.city_placement_active == False:
                            self.city_placement_active = True
                            print(self.city_placement_active)
                        elif self.city_placement_active == True:
                            self.city_placement_active = False
                            print(self.city_placement_active)

                    if pos[0] >= self.trade_button.x and pos[0] <= (
                            self.trade_button.x + self.trade_button.width
                    ) and pos[1] >= self.trade_button.y and pos[1] <= (
                            self.trade_button.y + self.trade_button.height):
                        self.trade_active = True

                    if pos[0] >= self.card_button.x and pos[0] <= (
                            self.card_button.x + self.card_button.width
                    ) and pos[1] >= self.card_button.y and pos[1] <= (
                            self.card_button.y + self.card_button.height):
                        if self.players[
                                self.active_player -
                                1].resources[2] > 0 and self.players[
                                    self.active_player -
                                    1].resources[3] > 0 and self.players[
                                        self.active_player -
                                        1].resources[4] > 0:
                            card_draw = random.choice(self.cards)
                            self.players[self.active_player -
                                         1].card_hand.append(card_draw)
                            self.players[self.active_player -
                                         1].resources[2] -= 1
                            self.players[self.active_player -
                                         1].resources[3] -= 1
                            self.players[self.active_player -
                                         1].resources[4] -= 1
                            self.cards.remove(card_draw)
                            print("You've drawn " + str(card_draw))
                        else:
                            print("You cannot afford a development card")

                    if pos[0] >= self.card_play_button.x and pos[0] <= (
                            self.card_play_button.x +
                            self.card_play_button.width
                    ) and pos[1] >= self.card_play_button.y and pos[1] <= (
                            self.card_play_button.y +
                            self.card_play_button.height):
                        self.card()

                    if pos[0] >= self.end_turn.x and pos[0] <= (
                            self.end_turn.x + self.end_turn.width
                    ) and pos[1] >= self.end_turn.y and pos[1] <= (
                            self.end_turn.y + self.end_turn.height):

                        self.turn()

                    if pos[0] >= self.vic_button.x and pos[0] <= (
                            self.vic_button.x + self.vic_button.width
                    ) and pos[1] >= self.vic_button.y and pos[1] <= (
                            self.vic_button.y + self.vic_button.height):
                        self.vic_calc_active = True

                    #___DOUBLE ROAD RESOURCE CARD___
                    if self.double_road == True:
                        for i in range(len(self.all_corners)):
                            if pos[0] >= (
                                (self.all_corners[i][0] * tile_size_mod) - 5
                            ) and pos[0] <= (
                                (self.all_corners[i][0] * tile_size_mod) + 5
                            ) and pos[1] >= (
                                (self.all_corners[i][1] * tile_size_mod) - 5
                            ) and pos[1] <= (
                                (self.all_corners[i][1] * tile_size_mod) + 5):
                                if self.road_counter < 3:
                                    self.road_placement(pos)
                                    self.road_counter += 1
                                elif self.road_counter >= 3:
                                    self.road_placement(pos)
                                    self.double_road = False
                                    self.road_counter = 0
                                    self.players[self.active_player -
                                                 1].resources[0] += 2
                                    self.players[self.active_player -
                                                 1].resources[1] += 2

                    #___SETTLEMENT PLACEMENT___
                    elif self.settlement_placement_active == True:
                        nearby_tiles = []
                        valid_placement = True
                        if self.players[
                                self.active_player -
                                1].settlement_cap > 0 and self.players[
                                    self.active_player -
                                    1].resources[0] >= 1 and self.players[
                                        self.active_player -
                                        1].resources[1] >= 1 and self.players[
                                            self.active_player - 1].resources[
                                                4] >= 1 and self.players[
                                                    self.active_player -
                                                    1].resources[3] >= 1:
                            for i in range(len(self.all_corners)):
                                if pos[0] >= (
                                    (self.all_corners[i][0] *
                                     tile_size_mod) - 5) and pos[0] <= (
                                         (self.all_corners[i][0] *
                                          tile_size_mod) + 5) and pos[1] >= (
                                              (self.all_corners[i][1] *
                                               tile_size_mod) -
                                              5) and pos[1] <= (
                                                  (self.all_corners[i][1] *
                                                   tile_size_mod) + 5):

                                    for n in range(len(
                                            self.nearby_points_mod)):
                                        if (self.all_corners[i][0] +
                                                self.nearby_points_mod[n][0],
                                                self.all_corners[i][1] +
                                                self.nearby_points_mod[n][1]
                                            ) in self.settlement_locations:
                                            print(
                                                "Invalid settlement location")
                                            valid_placement = False

                                    if self.all_corners[
                                            i] in self.settlement_locations:
                                        print("Already Active")
                                        valid_placement = False

                                    elif valid_placement == True:
                                        self.settlement_locations.append(
                                            self.all_corners[i])

                                        for k in range(len(self.tiles)):
                                            for j in range(6):
                                                if self.all_corners[
                                                        i] == self.tiles[
                                                            k].tile_locations[
                                                                j]:
                                                    nearby_tiles.append(k)

                                        self.active_settlements.append(
                                            Settlement(self.all_corners[i],
                                                       self.active_player,
                                                       nearby_tiles))
                                        self.players[self.active_player -
                                                     1].settlement_cap -= 1
                                        self.players[self.active_player -
                                                     1].settlement_count += 1
                                        self.players[self.active_player -
                                                     1].resources[0] -= 1
                                        self.players[self.active_player -
                                                     1].resources[1] -= 1
                                        self.players[self.active_player -
                                                     1].resources[3] -= 1
                                        self.players[self.active_player -
                                                     1].resources[4] -= 1
                                        self.settlement_placement_active = False

                                        if self.all_corners[
                                                i] in self.available_settlement_locations:
                                            self.available_settlement_locations.remove(
                                                self.all_corners[i])

                                        for n in range(
                                                len(self.nearby_points_mod)):
                                            if (
                                                    self.all_corners[i][0] +
                                                    self.nearby_points_mod[n]
                                                [0], self.all_corners[i][1] +
                                                    self.nearby_points_mod[n]
                                                [1]
                                            ) in self.available_settlement_locations:
                                                self.available_settlement_locations.remove(
                                                    (self.all_corners[i][0] +
                                                     self.nearby_points_mod[n]
                                                     [0],
                                                     self.all_corners[i][1] +
                                                     self.nearby_points_mod[n]
                                                     [1]))

                                        if len(self.active_settlements) < (
                                                self.player_count * 2):
                                            for tiles in range(len(
                                                    self.tiles)):
                                                if tiles in self.active_settlements[
                                                        -1].nearby_tiles:
                                                    if self.tiles[
                                                            tiles].tile_type == "hills":
                                                        self.players[
                                                            self.
                                                            active_settlements[
                                                                -1].
                                                            settlement_owner -
                                                            1].resources[
                                                                0] += 1
                                                    elif self.tiles[
                                                            tiles].tile_type == "forest":
                                                        self.players[
                                                            self.
                                                            active_settlements[
                                                                -1].
                                                            settlement_owner -
                                                            1].resources[
                                                                1] += 1
                                                    elif self.tiles[
                                                            tiles].tile_type == "mountain":
                                                        self.players[
                                                            self.
                                                            active_settlements[
                                                                -1].
                                                            settlement_owner -
                                                            1].resources[
                                                                2] += 1
                                                    elif self.tiles[
                                                            tiles].tile_type == "fields":
                                                        self.players[
                                                            self.
                                                            active_settlements[
                                                                -1].
                                                            settlement_owner -
                                                            1].resources[
                                                                3] += 1
                                                    elif self.tiles[
                                                            tiles].tile_type == "pasture":
                                                        self.players[
                                                            self.
                                                            active_settlements[
                                                                -1].
                                                            settlement_owner -
                                                            1].resources[
                                                                4] += 1

                        elif self.players[self.active_player -
                                          1].settlement_cap <= 0:
                            print("You cannot place anymore settlements")
                            self.settlement_placement_active = False

                        elif self.players[
                                self.active_player -
                                1].resources[0] < 1 or self.players[
                                    self.active_player -
                                    1].resources[1] < 1 or self.players[
                                        self.active_player -
                                        1].resources[4] < 1 or self.players[
                                            self.active_player -
                                            1].resources[3] < 1:
                            print("You cannot afford to build a settlement")
                            self.settlement_placement_active = False

                    #___ACTIVATES ROAD PLACEMENT___
                    elif self.road_placement_active == True:
                        if self.players[
                                self.active_player -
                                1].road_cap > 0 and self.players[
                                    self.active_player -
                                    1].resources[0] >= 1 and self.players[
                                        self.active_player -
                                        1].resources[1] >= 1:
                            self.road_placement(pos)

                        elif self.players[self.active_player -
                                          1].road_cap <= 0:
                            print("You cannot place anymore roads")
                            self.road_placement_active = False

                        elif self.players[self.active_player -
                                          1].resources[0] < 1 or self.players[
                                              self.active_player -
                                              1].resources[1] < 1:
                            print("You cannot afford to build a road")
                            self.road_placement_active = False

                    #___CITY PLACEMENT___
                    elif self.city_placement_active == True:
                        nearby_tiles = []
                        if self.players[
                                self.active_player -
                                1].city_cap > 0 and self.players[
                                    self.active_player -
                                    1].resources[2] >= 3 and self.players[
                                        self.active_player -
                                        1].resources[3] >= 2:
                            for i in range(len(self.all_corners)):
                                if pos[0] >= (
                                    (self.all_corners[i][0] *
                                     tile_size_mod) - 5) and pos[0] <= (
                                         (self.all_corners[i][0] *
                                          tile_size_mod) + 5) and pos[1] >= (
                                              (self.all_corners[i][1] *
                                               tile_size_mod) -
                                              5) and pos[1] <= (
                                                  (self.all_corners[i][1] *
                                                   tile_size_mod) + 5):
                                    for n in range(len(
                                            self.active_settlements)):
                                        if self.active_settlements[
                                                n].settlement_owner == self.active_player and self.active_settlements[
                                                    n].settlement_location == self.all_corners[
                                                        i] and self.all_corners[
                                                            i] in self.settlement_locations and self.all_corners[
                                                                i] not in self.city_locations:

                                            for k in range(len(self.tiles)):
                                                for j in range(6):
                                                    if self.all_corners[
                                                            i] == self.tiles[
                                                                k].tile_locations[
                                                                    j]:
                                                        nearby_tiles.append(k)

                                            self.active_cities.append(
                                                City(self.all_corners[i],
                                                     self.active_player,
                                                     nearby_tiles))
                                            self.city_locations.append(
                                                self.all_corners[i])
                                            self.players[self.active_player -
                                                         1].resources[2] -= 3
                                            self.players[self.active_player -
                                                         1].resources[3] -= 2
                                            self.players[self.active_player -
                                                         1].city_count += 1
                                            self.players[
                                                self.active_player -
                                                1].settlement_count -= 1
                                            self.city_placement_active = False

                        elif self.players[self.active_player -
                                          1].city_cap <= 0:
                            print("You cannot place anymore cities")
                            self.city_placement_active = False

                        elif self.players[self.active_player -
                                          1].resources[2] < 3 or self.players[
                                              self.active_player -
                                              1].resources[3] < 2:
                            print("You cannot afford to build a city")
                            self.city_placement_active = False

                    #___TRADE MENU___
                    elif self.trade_active == True:

                        for i in range(len(self.trade_buttons)):
                            if pos[0] >= self.trade_buttons[i].x and pos[0] <= (
                                    self.trade_buttons[i].x +
                                    self.trade_buttons[i].width
                            ) and pos[1] >= self.trade_buttons[i].y and pos[
                                    1] <= (self.trade_buttons[i].y +
                                           self.trade_buttons[i].height):
                                if i < 10:
                                    if self.trade_buttons[
                                            i].button_number % 2 == 0 and self.resource_trade1[
                                                int(i / 2)] < self.players[
                                                    self.active_player -
                                                    1].resources[int(i / 2)]:
                                        self.resource_trade1[int(i / 2)] += 1
                                        self.trade_values[int(
                                            i / 2)].current_value += 1
                                    if self.trade_buttons[
                                            i].button_number % 2 == 1 and self.resource_trade1[
                                                int((i + 1) / 2)] > 0:
                                        self.resource_trade1[int(
                                            (i + 1) / 2)] -= 1
                                        self.trade_values[int(
                                            i / 2)].current_value -= 1
                                if i >= 10:
                                    if self.trade_buttons[
                                            i].button_number % 2 == 0 and self.resource_trade2[
                                                int((i - 10) /
                                                    2)] < self.players[
                                                        self.trading_player -
                                                        1].resources[int(
                                                            (i - 10) / 2)]:
                                        self.resource_trade2[int(
                                            (i - 10) / 2)] += 1
                                        self.trade_values[int(
                                            i / 2)].current_value += 1
                                    if self.trade_buttons[
                                            i].button_number % 2 == 1 and self.resource_trade2[
                                                int((i - 9) / 2)] > 0:
                                        self.resource_trade2[int(
                                            (i - 9) / 2)] -= 1
                                        self.trade_values[int(
                                            i / 2)].current_value -= 1
                        for i in range(len(self.trade_select_buttons)):
                            if pos[0] >= self.trade_select_buttons[
                                    i].x and pos[0] <= (
                                        self.trade_select_buttons[i].x +
                                        self.trade_select_buttons[i].width
                                    ) and pos[1] >= self.trade_select_buttons[
                                        i].y and pos[1] <= (
                                            self.trade_select_buttons[i].y +
                                            self.trade_select_buttons[i].height
                                        ):
                                if i == 0 and self.trading_player > 0:
                                    self.trading_player -= 1
                                    for i in range(5):
                                        self.resource_trade1[i] = 0
                                        self.resource_trade2[i] = 0
                                    for i in range(len(self.trade_values)):
                                        self.trade_values[i].current_value = 0
                                if i == 1 and self.trading_player < self.player_count:
                                    self.trading_player += 1
                                    for i in range(5):
                                        self.resource_trade1[i] = 0
                                        self.resource_trade2[i] = 0
                                    for i in range(len(self.trade_values)):
                                        self.trade_values[i].current_value = 0

                        if pos[0] >= self.trade_accept.x and pos[0] <= (
                                self.trade_accept.x + self.trade_accept.width
                        ) and pos[1] >= self.trade_accept.y and pos[1] <= (
                                self.trade_accept.y +
                                self.trade_accept.height):
                            self.trade()

                    elif self.vic_calc_active == True:
                        if pos[0] >= self.vic_exit.x and pos[
                                0] <= self.vic_exit.x + self.vic_exit.width and pos[
                                    1] >= self.vic_exit.y and pos[
                                        1] <= self.vic_exit.y + self.vic_exit.height:
                            self.vic_calc_active = False

                        for i in range(len(self.vic_buttons)):

                            if pos[0] >= self.vic_buttons[i].x and pos[
                                    0] <= self.vic_buttons[
                                        i].x + self.vic_buttons[i].width and pos[
                                            1] >= self.vic_buttons[i].y and pos[
                                                1] <= self.vic_buttons[
                                                    i].y + self.vic_buttons[
                                                        i].height:

                                if i < self.player_count:
                                    for j in range(self.player_count):
                                        self.players[j].army = 0
                                    self.players[i].army = 1
                                elif i >= self.player_count:
                                    for j in range(self.player_count):
                                        self.players[j].road = 0
                                    self.players[i -
                                                 (self.player_count)].road = 1

    #___ROAD PLACEMENT___
    def road_placement(self, pos):
        for i in range(len(self.all_corners)):
            if pos[0] >= (
                (self.all_corners[i][0] * tile_size_mod) - 5) and pos[0] <= (
                    (self.all_corners[i][0] * tile_size_mod) +
                    5) and pos[1] >= (
                        (self.all_corners[i][1] * tile_size_mod) -
                        5) and pos[1] <= (
                            (self.all_corners[i][1] * tile_size_mod) + 5):
                if self.road_start == None:
                    if self.all_corners[
                            i] in self.settlement_locations or self.all_corners[
                                i] in self.road_locations:
                        self.road_start = self.all_corners[i]
                        print(self.road_start)
                elif self.road_end == None:
                    for n in range(len(self.nearby_points_mod)):
                        if (self.all_corners[i][0] +
                                self.nearby_points_mod[n][0],
                                self.all_corners[i][1] +
                                self.nearby_points_mod[n][1]
                            ) == self.road_start:
                            self.road_placement_active = False
                            self.road_end = self.all_corners[i]
                            self.active_roads.append(
                                Road(self.road_start, self.road_end,
                                     self.active_player))
                            self.road_locations.append(self.road_start)
                            self.road_locations.append(self.road_end)
                            print(self.road_locations)
                            print(self.road_start, self.road_end)
                            self.road_start = None
                            self.road_end = None
                            self.players[self.active_player - 1].road_cap -= 1
                            self.players[self.active_player -
                                         1].resources[0] -= 1
                            self.players[self.active_player -
                                         1].resources[1] -= 1

    #___CHECKS IF A POINT IS ON THE WATER AND DEFINES HARBOR POINTS___
    def border_check(self):
        nearby_points = 0
        border_points = []
        harbor_points = []
        nearby_tiles = []

        for i in range(len(self.all_corners)):
            for k in range(len(self.tiles)):
                for j in range(6):
                    if self.all_corners[i] == self.tiles[k].tile_locations[j]:
                        nearby_tiles.append(k)

            if len(nearby_tiles) < 3:
                border_points.append(self.all_corners[i])
                nearby_tiles = []
            if len(nearby_tiles) >= 3:
                nearby_tiles = []

        for i in range(len(border_points)):
            for n in range(len(self.nearby_points_mod)):
                if (border_points[i][0] + self.nearby_points_mod[n][0],
                        border_points[i][1] +
                        self.nearby_points_mod[n][1]) in border_points:
                    harbor_points.append(
                        (border_points[i],
                         (border_points[i][0] + self.nearby_points_mod[n][0],
                          border_points[i][1] + self.nearby_points_mod[n][1])))
        return (harbor_points)

    #___RESOURCE DISTRIBUTION AND ROBBER LOCATION SELECT___
    def turn(self):
        self.turn_counter += 1
        self.trade_active = False

        if self.turn_counter <= ((self.start_rounds + 1) / 2):
            self.active_player += 1

        if self.turn_counter > ((self.start_rounds + 1) /
                                2) and self.turn_counter <= self.start_rounds:
            self.active_player -= 1

        if self.turn_counter > self.start_rounds:

            if self.active_player < self.player_count:
                self.active_player += 1
            elif self.active_player >= self.player_count:
                self.active_player = 1

            resource_select = self.dice_roll()
            print("Rolled a " + str(resource_select))
            for i in range(len(self.tiles)):
                #___IF ROLL = 7, SELECT ROBBER LOCATION___
                if resource_select == 7:
                    self.robber_active = True
                    break

                if i == self.robber_location and self.tiles[
                        i].tile_value == resource_select:
                    print("Get robbed")

                elif self.tiles[i].tile_value == resource_select:
                    #___SETTLEMENT RESOURCE COLLECT___
                    for k in range(len(self.active_settlements)):
                        if i in self.active_settlements[k].nearby_tiles:
                            if self.tiles[i].tile_type == "hills":
                                self.players[
                                    self.active_settlements[k].settlement_owner
                                    - 1].resources[0] += 1
                            elif self.tiles[i].tile_type == "forest":
                                self.players[
                                    self.active_settlements[k].settlement_owner
                                    - 1].resources[1] += 1
                            elif self.tiles[i].tile_type == "mountain":
                                self.players[
                                    self.active_settlements[k].settlement_owner
                                    - 1].resources[2] += 1
                            elif self.tiles[i].tile_type == "fields":
                                self.players[
                                    self.active_settlements[k].settlement_owner
                                    - 1].resources[3] += 1
                            elif self.tiles[i].tile_type == "pasture":
                                self.players[
                                    self.active_settlements[k].settlement_owner
                                    - 1].resources[4] += 1
                    #___CITY RESOURCE COLLECT___
                    for k in range(len(self.active_cities)):
                        if i in self.active_cities[k].nearby_tiles:
                            if self.tiles[i].tile_type == "hills":
                                self.players[self.active_cities[k].city_owner -
                                             1].resources[0] += 1
                            elif self.tiles[i].tile_type == "forest":
                                self.players[self.active_cities[k].city_owner -
                                             1].resources[1] += 1
                            elif self.tiles[i].tile_type == "mountain":
                                self.players[self.active_cities[k].city_owner -
                                             1].resources[2] += 1
                            elif self.tiles[i].tile_type == "fields":
                                self.players[self.active_cities[k].city_owner -
                                             1].resources[3] += 1
                            elif self.tiles[i].tile_type == "pasture":
                                self.players[self.active_cities[k].city_owner -
                                             1].resources[4] += 1

    #___RESOURCE SEND FOR TRADE___
    def trade(self):
        for i in range(len(self.resource_list)):
            self.players[self.active_player -
                         1].resources[i] -= self.resource_trade1[i]
            self.players[self.trading_player -
                         1].resources[i] += self.resource_trade1[i]
            self.players[self.active_player -
                         1].resources[i] += self.resource_trade2[i]
            self.players[self.trading_player -
                         1].resources[i] -= self.resource_trade2[i]

        self.resource_trade1 = [0, 0, 0, 0, 0]
        self.resource_trade2 = [0, 0, 0, 0, 0]
        self.trade_active = False

        for i in range(len(self.trade_values)):
            self.trade_values[i].current_value = 0

    #___RESOURCE CARDS___
    def year_of_plenty(self):
        print("Resource list: " + str(self.resource_list))
        resource_select = input("What resource would you like to draw?")

        if resource_select in self.resource_list:
            if resource_select == "brick":
                self.players[self.active_player - 1].resources[0] += 1
            elif resource_select == "wood":
                self.players[self.active_player - 1].resources[1] += 1
            elif resource_select == "stone":
                self.players[self.active_player - 1].resources[2] += 1
            elif resource_select == "wheat":
                self.players[self.active_player - 1].resources[3] += 1
            elif resource_select == "wool":
                self.players[self.active_player - 1].resources[4] += 1

    def monopoly(self):
        resource_select = int(
            input(
                "What resource would you like to draw? Give a number between 0 and 4"
            ))
        starting_resource = self.players[self.active_player -
                                         1].resources[resource_select]
        resources_to_add = 0

        for i in range(len(self.players) - 1):
            resources_to_add += self.players[i].resources[resource_select]
            self.players[i].resources[resource_select] = 0
        self.players[self.active_player -
                     1].resources[resource_select] += resources_to_add

    #___RESOURCE CARD SELECTION___
    def card(self):
        print(self.players[self.active_player - 1].card_hand)
        card_choice = input("Which card would you like to play?")

        if card_choice in self.players[self.active_player - 1].card_hand:
            if card_choice == "knight":
                self.robber_active = True
            if card_choice == "monopoly":
                self.monopoly()
            if card_choice == "year of plenty":
                self.year_of_plenty()
                self.year_of_plenty()
            if card_choice == "victory point":
                self.players[self.active_player - 1].vic_card += 1
            if card_choice == "double road":
                self.double_road = True
            self.players[self.active_player - 1].card_hand.remove(card_choice)
            self.players[self.active_player -
                         1].cards_played.append(card_choice)

        else:
            print("You don't have that card")

    #___DICE ROLL___
    def dice_roll(self):
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)

        return (dice_1 + dice_2)

    def vic_points_assign(self):
        for i in range(len(self.players)):
            self.players[i].vic_point = (self.players[i].settlement_count +
                                         self.players[i].city_count +
                                         (self.players[i].army * 2) +
                                         (self.players[i].road * 2) +
                                         self.players[i].vic_card)


class Tile:
    tile_types = [
        "hills", "hills", "hills", "hills", "forest", "forest", "forest",
        "forest", "mountain", "mountain", "mountain", "mountain", "fields",
        "fields", "fields", "fields", "pasture", "pasture", "pasture",
        "pasture"
    ]
    tile_values = [10, 2, 9, 12, 6, 4, 10, 9, 11, 3, 8, 5, 4, 3, 8, 5, 6, 11]
    tile_amount = 0

    def __init__(self, starting_corner):
        self.tile_type_and_color = self.tile_type_assign()
        self.tile_type = self.tile_type_and_color[0]
        self.tile_color = self.tile_type_and_color[1]
        self.tile_value = self.tile_value_assign()
        self.tile_locations = self.tile_corners(starting_corner)

        if Tile.tile_amount != 9:
            Tile.tile_types.remove(self.tile_type)
            Tile.tile_values.remove(self.tile_value)
        Tile.tile_amount += 1

    #___TILE TYPE AND COLOR DEFINE___
    def tile_type_assign(self):
        if Tile.tile_amount != 9:
            tile_type = random.choice(Tile.tile_types)
            if tile_type == "hills":
                tile_color = brick_color
            if tile_type == "forest":
                tile_color = wood_color
            if tile_type == "mountain":
                tile_color = stone_color
            if tile_type == "fields":
                tile_color = wheat_color
            if tile_type == "pasture":
                tile_color = sheep_color
        else:
            tile_type = "desert"
            tile_color = yellow
        return (tile_type, tile_color)

    #___TILE VALUE ASSIGN___
    def tile_value_assign(self):
        if Tile.tile_amount != 9:
            tile_value = random.choice(self.tile_values)
        else:
            tile_value = 0

        return (tile_value)

    #___FIND CORNERS FOR THE TILE___
    def tile_corners(self, tl_corner):
        start_corner = tl_corner

        return (start_corner, (start_corner[0], start_corner[1] + 1),
                (start_corner[0] + 1, start_corner[1] + 2),
                (start_corner[0] + 2, start_corner[1] + 1),
                (start_corner[0] + 2, start_corner[1]), (start_corner[0] + 1,
                                                         start_corner[1] - 1))


class Settlement:
    def __init__(self, position, owner, tiles):
        self.settlement_location = position
        self.settlement_owner = owner
        self.nearby_tiles = tiles

        if self.settlement_owner == 1:
            self.settlement_color = player_one_color
        if self.settlement_owner == 2:
            self.settlement_color = player_two_color
        if self.settlement_owner == 3:
            self.settlement_color = player_three_color
        if self.settlement_owner == 4:
            self.settlement_color = player_four_color


class Road:
    def __init__(self, point1, point2, owner):
        self.road_points = (point1, point2)
        self.road_owner = owner

        if self.road_owner == 1:
            self.road_color = player_one_color
        if self.road_owner == 2:
            self.road_color = player_two_color
        if self.road_owner == 3:
            self.road_color = player_three_color
        if self.road_owner == 4:
            self.road_color = player_four_color


class City:
    def __init__(self, position, owner, tiles):
        self.city_location = position
        self.city_owner = owner
        self.nearby_tiles = tiles

        if self.city_owner == 1:
            self.city_color = player_one_color
        if self.city_owner == 2:
            self.city_color = player_two_color
        if self.city_owner == 3:
            self.city_color = player_three_color
        if self.city_owner == 4:
            self.city_color = player_four_color


class Player:

    player_count = 0

    def __init__(self):
        #brick, wood, stone, wheat, wool
        self.resources = [4, 4, 0, 2, 2]
        self.settlement_cap = 5
        self.city_cap = 4
        self.road_cap = 15
        self.card_hand = ["double road"]
        self.cards_played = []
        self.settlement_count = 0
        self.city_count = 0
        self.army = 0
        self.road = 0
        self.vic_card = 0
        self.vic_point = 0
        self.color = player_colors[Player.player_count - 1]
        Player.player_count += 1


#___TRADE BUTTONS___
class Button:
    button_count = 0

    def __init__(self):
        self.width = (scrn_width / 24)
        self.height = (scrn_height / 20)
        if Button.button_count < 10:
            self.y = (scrn_height / 10 * 4)
            self.x = (scrn_width / 16 * Button.button_count) + (scrn_width /
                                                                20 * 1)
        elif Button.button_count >= 10:
            self.y = (scrn_height / 10 * 7)
            self.x = (scrn_width / 16 *
                      (Button.button_count - 10)) + (scrn_width / 20 * 1)
        Button.button_count += 1

        self.button_number = Button.button_count


class Trade_values:
    number_count = 0

    def __init__(self):
        self.position = Trade_values.number_count
        if self.position < 5:
            self.x = (scrn_width / 8 * self.position) + (scrn_width / 20 * 2)
            self.y = scrn_width / 10 * 2
        if self.position >= 5:
            self.x = (scrn_width / 8 *
                      (self.position - 5)) + (scrn_width / 20 * 2)
            self.y = scrn_width / 11 * 5
        self.current_value = 0
        Trade_values.number_count += 1


class Harbor:
    harbor_types = [
        "brick", "wood", "stone", "wheat", "wool", "generic", "generic"
    ]

    def __init__(self, harbor_choices):
        self.harbor_type = random.choice(Harbor.harbor_types)
        self.harbor_position = random.choice(harbor_choices)
        self.harbor_color = self.harbor_color_assign()

        Harbor.harbor_types.remove(self.harbor_type)

    def harbor_color_assign(self):
        if self.harbor_type == "brick":
            harbor_color = brick_color
        if self.harbor_type == "wood":
            harbor_color = wood_color
        if self.harbor_type == "stone":
            harbor_color = stone_color
        if self.harbor_type == "wheat":
            harbor_color = wheat_color
        if self.harbor_type == "wool":
            harbor_color = sheep_color
        if self.harbor_type == "generic":
            harbor_color = white

        return (harbor_color)


class Stock_buttons:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y


class Graphics:
    def __init__(self):
        self.game = Game()

    def draw_background(self):
        pygame.draw.rect(scrn, light_blue, (0, 0, scrn_width, scrn_height))
        pygame.draw.rect(scrn, yellow,
                         (scrn_width / 3 * 2, 0, scrn_width / 3, scrn_height))

    def draw_entities(self):
        # top left, bottom left, bottom middle, bottom right, top right, top middle
        for i in range(len(self.game.tiles)):
            pygame.draw.polygon(
                scrn, self.game.tiles[i].tile_color,
                ((self.game.tiles[i].tile_locations[0][0] * tile_size_mod,
                  self.game.tiles[i].tile_locations[0][1] * tile_size_mod),
                 (self.game.tiles[i].tile_locations[1][0] * tile_size_mod,
                  self.game.tiles[i].tile_locations[1][1] * tile_size_mod),
                 (self.game.tiles[i].tile_locations[2][0] * tile_size_mod,
                  self.game.tiles[i].tile_locations[2][1] * tile_size_mod),
                 (self.game.tiles[i].tile_locations[3][0] * tile_size_mod,
                  self.game.tiles[i].tile_locations[3][1] * tile_size_mod),
                 (self.game.tiles[i].tile_locations[4][0] * tile_size_mod,
                  self.game.tiles[i].tile_locations[4][1] * tile_size_mod),
                 (self.game.tiles[i].tile_locations[5][0] * tile_size_mod,
                  self.game.tiles[i].tile_locations[5][1] * tile_size_mod)))
            stock_mess(
                str(self.game.tiles[i].tile_value), black,
                (self.game.tiles[i].tile_locations[0][0] * tile_size_mod +
                 tile_size_mod / 2),
                (self.game.tiles[i].tile_locations[0][1] * tile_size_mod), 24)
            if i == self.game.robber_location:
                pygame.draw.circle(
                    scrn, black,
                    ((self.game.tiles[i].tile_locations[0][0] * tile_size_mod +
                      tile_size_mod),
                     (self.game.tiles[i].tile_locations[0][1] * tile_size_mod +
                      tile_size_mod / 2)), int(9 * dx))

        for i in range(len(self.game.active_harbors)):
            pygame.draw.line(
                scrn, self.game.active_harbors[i].harbor_color,
                ((self.game.active_harbors[i].harbor_position[0][0] *
                  tile_size_mod),
                 (self.game.active_harbors[i].harbor_position[0][1] *
                  tile_size_mod)),
                ((self.game.active_harbors[i].harbor_position[1][0] *
                  tile_size_mod),
                 (self.game.active_harbors[i].harbor_position[1][1] *
                  tile_size_mod)), int(18 * dx))

        for i in range(len(self.game.active_settlements)):
            pygame.draw.circle(
                scrn, self.game.active_settlements[i].settlement_color,
                (self.game.active_settlements[i].settlement_location[0] *
                 tile_size_mod,
                 self.game.active_settlements[i].settlement_location[1] *
                 tile_size_mod), int(12 * dx))

        for i in range(len(self.game.active_roads)):
            pygame.draw.line(
                scrn, self.game.active_roads[i].road_color,
                (self.game.active_roads[i].road_points[0][0] * tile_size_mod,
                 self.game.active_roads[i].road_points[0][1] * tile_size_mod),
                (self.game.active_roads[i].road_points[1][0] * tile_size_mod,
                 self.game.active_roads[i].road_points[1][1] * tile_size_mod),
                int(5 * dx))

        for i in range(len(self.game.active_cities)):
            pygame.draw.polygon(
                scrn, black,
                ((self.game.active_cities[i].city_location[0] * tile_size_mod -
                  int(6 * dx),
                  self.game.active_cities[i].city_location[1] * tile_size_mod +
                  int(6 * dx)),
                 (self.game.active_cities[i].city_location[0] * tile_size_mod +
                  int(6 * dx),
                  self.game.active_cities[i].city_location[1] * tile_size_mod +
                  int(6 * dx)),
                 (self.game.active_cities[i].city_location[0] * tile_size_mod,
                  self.game.active_cities[i].city_location[1] * tile_size_mod -
                  int(6 * dx))))

        if self.game.robber_active == True:
            for tiles in range(len(self.game.robber_locations)):
                pygame.draw.circle(
                    scrn, blue,
                    ((self.game.robber_locations[tiles][0] * tile_size_mod) +
                     (tile_size_mod),
                     self.game.robber_locations[tiles][1] * tile_size_mod +
                     (tile_size_mod / 2)), 12 * dx, int(2 * dx))

        if self.game.settlement_placement_active == True:
            for l in range(len(self.game.available_settlement_locations)):
                pygame.draw.circle(
                    scrn, white,
                    (self.game.available_settlement_locations[l][0] *
                     tile_size_mod,
                     self.game.available_settlement_locations[l][1] *
                     tile_size_mod), 12 * dx, int(2 * dx))

        if self.game.road_placement_active == True:
            for l in range(len(self.game.all_corners)):
                pygame.draw.circle(
                    scrn, black, (self.game.all_corners[l][0] * tile_size_mod,
                                  self.game.all_corners[l][1] * tile_size_mod),
                    6 * dx, int(2 * dx))

    #___BUTTONS ON THE RIGHT___
    def draw_buttons(self):
        pygame.draw.rect(
            scrn, black,
            (self.game.settlement_button.x, self.game.settlement_button.y,
             self.game.settlement_button.width,
             self.game.settlement_button.height))
        dif_mess("Settlement", white, self.game.settlement_button.x,
                 self.game.settlement_button.y)
        stock_mess("1, 1, 0, 1, 1", white, self.game.settlement_button.x,
                   self.game.settlement_button.y + int(20 * dx),
                   (int(10 * dx)))
        pygame.draw.rect(
            scrn, black,
            (self.game.city_button.x, self.game.city_button.y,
             self.game.city_button.width, self.game.city_button.height))
        dif_mess("City", white, self.game.city_button.x,
                 self.game.city_button.y)
        stock_mess("0, 0, 3, 2, 0", white, self.game.city_button.x,
                   self.game.city_button.y + int(20 * dx), (int(10 * dx)))
        pygame.draw.rect(
            scrn, black,
            (self.game.road_button.x, self.game.road_button.y,
             self.game.road_button.width, self.game.road_button.height))
        dif_mess("Road", white, self.game.road_button.x,
                 self.game.road_button.y)
        stock_mess("1, 1, 0, 0, 0", white, self.game.road_button.x,
                   self.game.road_button.y + int(20 * dx), (int(10 * dx)))
        pygame.draw.rect(
            scrn, black,
            (self.game.trade_button.x, self.game.trade_button.y,
             self.game.trade_button.width, self.game.trade_button.height))
        dif_mess("Trade", white, self.game.trade_button.x,
                 self.game.trade_button.y)
        pygame.draw.rect(
            scrn, black,
            (self.game.card_button.x, self.game.card_button.y,
             self.game.card_button.width, self.game.card_button.height))
        dif_mess("Res Card", white, self.game.card_button.x,
                 self.game.card_button.y)
        stock_mess("0, 0, 1, 1, 1", white, self.game.card_button.x,
                   self.game.card_button.y + int(20 * dx), (int(10 * dx)))
        pygame.draw.rect(
            scrn, black,
            (self.game.card_play_button.x, self.game.card_play_button.y,
             self.game.card_play_button.width,
             self.game.card_play_button.height))
        dif_mess("Card Hand", white, self.game.card_play_button.x,
                 self.game.card_play_button.y)
        pygame.draw.rect(scrn, red,
                         (self.game.end_turn.x, self.game.end_turn.y,
                          self.game.end_turn.width, self.game.end_turn.height))
        dif_mess("End Turn", white, self.game.end_turn.x, self.game.end_turn.y)
        pygame.draw.rect(
            scrn, black,
            (self.game.vic_button.x, self.game.vic_button.y,
             self.game.vic_button.width, self.game.vic_button.height))
        dif_mess("Vic Button", white, self.game.vic_button.x,
                 self.game.vic_button.y)

    #___DRAWS PLAYERS AND RESOURCES___
    def draw_players(self):
        pygame.draw.rect(scrn,
                         self.game.players[self.game.active_player].color,
                         (scrn_width / 5 * 4, scrn_height / 7 *
                          (self.game.active_player), 80 * dx, 20 * dx))

        for i in range(self.game.player_count):
            stock_mess("Player " + str(i + 1), black, (scrn_width / 5 * 4),
                       scrn_height / 7 * (1 + i), 18)
            dif_mess(
                "Brick " + str(self.game.players[i].resources[0]) + "Wood " +
                str(self.game.players[i].resources[1]) + "Stone " +
                str(self.game.players[i].resources[2]) + "Wheat " +
                str(self.game.players[i].resources[3]) + "Wool " +
                str(self.game.players[i].resources[4]), black, int(570 * dx),
                int((85 * (1 + i) + 20) * dx))

    def draw_trade_menu(self):
        pygame.draw.rect(
            scrn, yellow,
            (self.game.trade_menu.x, self.game.trade_menu.y,
             self.game.trade_menu.width, self.game.trade_menu.height))
        pygame.draw.rect(
            scrn, black,
            (self.game.trade_accept.x, self.game.trade_accept.y,
             self.game.trade_accept.width, self.game.trade_accept.height))

        for i in range(len(self.game.trade_buttons)):
            pygame.draw.rect(
                scrn, red,
                (self.game.trade_buttons[i].x, self.game.trade_buttons[i].y,
                 self.game.trade_buttons[i].width,
                 self.game.trade_buttons[i].height))

        for i in range(2):
            for j in range(5):
                pygame.draw.polygon(scrn, white,
                                    ((int(96 * dx) + int(100 * j * dx),
                                      int(265 * dx) + int(180 * i * dx)),
                                     (int(116 * dx) + int(100 * j * dx),
                                      int(265 * dx) + int(180 * i * dx)),
                                     (int(106 * dx) + int(100 * j * dx),
                                      int(245 * dx) + int(180 * i * dx))))
                pygame.draw.polygon(scrn, white,
                                    ((int(46 * dx) + int(100 * j * dx),
                                      int(245 * dx) + int(180 * i * dx)),
                                     (int(66 * dx) + int(100 * j * dx),
                                      int(245 * dx) + int(180 * i * dx)),
                                     (int(56 * dx) + int(100 * j * dx),
                                      int(265 * dx) + int(180 * i * dx))))

        for i in range(len(self.game.trade_values)):
            stock_mess(str(self.game.trade_values[i].current_value), black,
                       self.game.trade_values[i].x,
                       self.game.trade_values[i].y, 24)

        for i in range(len(self.game.trade_select_buttons)):
            pygame.draw.rect(scrn, black,
                             (self.game.trade_select_buttons[i].x,
                              self.game.trade_select_buttons[i].y,
                              self.game.trade_select_buttons[i].width,
                              self.game.trade_select_buttons[i].height))

        for i in range(2):
            stock_mess("Brick", black, int(60 * dx), int((120 + i * 200) * dx),
                       20)
            stock_mess("Wood", black, int(160 * dx), int((120 + i * 200) * dx),
                       20)
            stock_mess("Stone", black, int(260 * dx), int(
                (120 + i * 200) * dx), 20)
            stock_mess("Wheat", black, int(360 * dx), int(
                (120 + i * 200) * dx), 20)
            stock_mess("Wool", black, int(460 * dx), int((120 + i * 200) * dx),
                       20)

        stock_mess("Trading Player", black,
                   self.game.trade_select_buttons[0].x,
                   self.game.trade_select_buttons[0].y - (scrn_height / 12),
                   20)

        if self.game.trading_player > 0:
            stock_mess(str(self.game.trading_player), black,
                       self.game.trade_select_buttons[0].x + (scrn_width / 18),
                       self.game.trade_select_buttons[0].y, 16)

        if self.game.trading_player == 0:
            stock_mess("Maritime", black,
                       self.game.trade_select_buttons[0].x + (scrn_width / 18),
                       self.game.trade_select_buttons[0].y, 16)

    def draw_intro_screen(self):
        scrn.fill(white)
        stock_mess("Frontiers of Catin", black, scrn_width / 4,
                   scrn_height / 6, 48)
        for i in range(len(self.game.intro_buttons)):
            pygame.draw.rect(
                scrn, black,
                (self.game.intro_buttons[i].x, self.game.intro_buttons[i].y,
                 self.game.intro_buttons[i].width,
                 self.game.intro_buttons[i].height))
        stock_mess("Start Game", white, self.game.intro_buttons[0].x,
                   self.game.intro_buttons[0].y, 22)
        stock_mess("Tutorial", white, self.game.intro_buttons[1].x,
                   self.game.intro_buttons[1].y, 22)
        stock_mess("Quit", white, self.game.intro_buttons[2].x,
                   self.game.intro_buttons[2].y, 22)
        stock_mess(str(self.game.player_count), black,
                   self.game.intro_buttons[3].x + scrn_width / 20,
                   self.game.intro_buttons[3].y, 22)
        stock_mess("Players", black, self.game.intro_buttons[3].x,
                   self.game.intro_buttons[3].y - scrn_height / 20, 22)

    def draw_vic_screen(self):
        pygame.draw.rect(
            scrn, red,
            (self.game.trade_menu.x, self.game.trade_menu.y,
             self.game.trade_menu.width, self.game.trade_menu.height))
        pygame.draw.rect(scrn, black,
                         (self.game.vic_exit.x, self.game.vic_exit.y,
                          self.game.vic_exit.width, self.game.vic_exit.height))

        for i in range(len(self.game.vic_buttons)):
            pygame.draw.rect(
                scrn, black,
                (self.game.vic_buttons[i].x, self.game.vic_buttons[i].y,
                 self.game.vic_buttons[i].width,
                 self.game.vic_buttons[i].height))

        for i in range(len(self.game.players)):
            if self.game.players[i].army == 1:
                pygame.draw.rect(
                    scrn, yellow,
                    (self.game.vic_buttons[i].x, self.game.vic_buttons[i].y,
                     int(20 * dx), int(20 * dx)))
            if self.game.players[i].road == 1:
                pygame.draw.rect(
                    scrn, yellow,
                    (self.game.vic_buttons[i + self.game.player_count].x,
                     self.game.vic_buttons[i + self.game.player_count].y,
                     int(20 * dx), int(20 * dx)))

        for i in range(len(self.game.players) - 1):
            stock_mess("Player " + str(i + 1), black,
                       int((100 * (i + 1) + 10) * dx), int(80 * dx), 20)

            stock_mess("Settlements", black, int(50 * dx), int(120 * dx), 12)
            stock_mess(str(self.game.players[i].settlement_count), black,
                       int((90 * (i + 1) + 40) * dx), int(120 * dx), 20)

            stock_mess("Cities", black, int(50 * dx), int(160 * dx), 12)
            stock_mess(str(self.game.players[i].city_count), black,
                       int((90 * (i + 1) + 40) * dx), int(160 * dx), 20)

            stock_mess("Army", black, int(50 * dx), int(200 * dx), 12)

            stock_mess("Road", black, int(50 * dx), int(240 * dx), 12)

            stock_mess("Vic Points", black, int(50 * dx), int(280 * dx), 12)
            stock_mess(str(self.game.players[i].vic_card), black,
                       int((90 * (i + 1) + 40) * dx), int(280 * dx), 20)

            stock_mess("Score", black, int(50 * dx), int(320 * dx), 12)
            stock_mess(str(self.game.players[i].vic_point), black,
                       int((90 * (i + 1) + 40) * dx), int(320 * dx), 20)

    def screen_updater(self):
        pygame.display.update()

    def main_method(self):
        if self.game.intro_screen == True:
            self.draw_intro_screen()
            self.game.intro_screen_controls()

        if self.game.game_active == True:
            self.draw_background()
            self.draw_entities()
            self.draw_buttons()
            self.draw_players()

            if self.game.trade_active == True:
                self.draw_trade_menu()

            if self.game.vic_calc_active == True:
                self.draw_vic_screen()

            if self.game.vic_calc_active == True:
                self.game.vic_points_assign()
            self.game.controls()

        if self.game.tutorial_active == True:
            self.game.controls()
            #Input tutorial here
        self.screen_updater()


graphics = Graphics()


def main():
    while True:
        graphics.main_method()


if __name__ == '__main__':
    main()
