import time
import pygame
import sys
import random


class Pong:
    def __init__(self):
        pygame.init()
        self.window_height = 680
        self.window_width = 1200

        self.height_players = 50
        self.width_players = 20

        self.height_boll = 15
        self.width_boll = 15

        self.velocity_players = 5

        self.velocity_boll_x_initial = 2
        self.velocity_boll_y_initial = 1

        self.velocity_boll_x = self.velocity_boll_x_initial
        self.velocity_boll_y = self.velocity_boll_y_initial

        self.time = 60

        self.distance_border_players = 10
        self.distance_border_player1 = self.distance_border_players
        self.distance_border_player2 = (
            self.window_width-self.width_players-self.distance_border_players
            )

        self.position_boll_initial_x = (
            (self.window_width/2)-(self.width_boll/2)
            )
        self.position_boll_initial_y = (
            (self.window_height/2)-(self.height_boll/2)
            )
        self.position_players_initial_y = (
            (self.window_height/2)-(self.height_players/2)
            )

        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_BLUE = (0, 0, 255)
        self.COLOR_GREEN = (0, 255, 0)
        self.COLOR_WHITE = (255, 255, 255)

        self.game_name = "PONG IA"

        self.initial_time = time.time()

        self.font_size = 36
        self.points_player1 = 0
        self.points_player2 = 0
        self.points_text = f"{self.points_player1}:{self.points_player2}"

        self.initial_move_boll = 0
        self.running = True

    def create_window(self):
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
            )
        pygame.display.set_caption(self.game_name)
        self.clock = pygame.time.Clock()

    def create_elements(self):
        self.player1 = pygame.Rect(
            self.distance_border_player1, self.position_players_initial_y,
            self.width_players, self.height_players
            )
        self.player2 = pygame.Rect(
            self.distance_border_player2, self.position_players_initial_y,
            self.width_players, self.height_players
            )
        self.boll = pygame.Rect(
            self.position_boll_initial_x, self.position_boll_initial_y,
            self.width_boll, self.height_boll
            )
        self.font = pygame.font.Font(
            None, self.font_size
            )
        self.surface_points = self.font.render(
            self.points_text, True, self.COLOR_WHITE
            )
        self.position_text = (
            (self.window_width - self.surface_points.get_width()) / 2,
            (10 + self.surface_points.get_height())
            )
    
    def draw_elements(self):
        pygame.draw.rect(self.screen, self.COLOR_BLUE, self.player1)
        pygame.draw.rect(self.screen, self.COLOR_BLUE, self.player2)
        pygame.draw.rect(self.screen, self.COLOR_GREEN, self.boll)
        self.screen.blit(self.surface_points, self.position_text)

    def verify_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()

    def update_points_text(self):
        self.points_text = f"{self.points_player1}:{self.points_player2}"
        self.surface_points = self.font.render(
            self.points_text, True, self.COLOR_WHITE
            )
        self.position_text = (
            (self.window_width - self.surface_points.get_width()) / 2,
            (10 + self.surface_points.get_height())
            )

    def verify_points(self):
        if self.boll.x <= 0:
            self.points_player2 += 1

        if self.boll.x >= self.window_width:
            self.points_player1 += 1

        self.update_points_text()

    def verify_exit_boll_screen(self):
        if self.boll.x <= 0 or self.boll.x >= self.window_width:
            self.boll.x = self.position_boll_initial_x
            self.boll.y = self.position_boll_initial_y
            self.velocity_boll_x = self.velocity_boll_x_initial
            self.velocity_boll_y = self.velocity_boll_y_initial
            time.sleep(1)
            self.initial_move_boll = 0

    def speed_boll(self):
        self.end_time = time.time()
        self.delta_time = self.end_time - self.initial_time
        if self.delta_time >= 30 and self.velocity_boll_x == 6 and self.velocity_boll_y == 6:
            self.initial_time = self.end_time
            self.velocity_boll_x += 1
            self.velocity_boll_y += 1

    def direction_boll_random_initial(self):
        if self.initial_move_boll == 0:
            self.initial_move_boll = 1

            self.x_boll = random.randint(0,1)
            self.y_boll = random.randint(0,1)

            if self.x_boll == 0 and self.y_boll == 0:
                self.direction_boll = 1
            if self.x_boll == 1 and self.y_boll == 1:
                self.direction_boll = 2
            if self.x_boll == 1 and self.y_boll == 0:
                self.direction_boll = 3
            if self.x_boll == 0 and self.y_boll == 1:
                self.direction_boll = 4

        return self.direction_boll
        
    def move_boll(self):
        match self.direction_boll:
            case 1:
                self.boll.x += self.velocity_boll_x
                self.boll.y += self.velocity_boll_y
                if self.boll.y >= self.window_height:
                    self.direction_boll = 2
            case 2:
                self.boll.x += self.velocity_boll_x
                self.boll.y -= self.velocity_boll_y
                if self.boll.y <= 0:
                    self.direction_boll = 1
            case 3:
                self.boll.x -= self.velocity_boll_x
                self.boll.y += self.velocity_boll_y
                if self.boll.y >= self.window_height:
                    self.direction_boll = 4
            case 4:
                self.boll.x -= self.velocity_boll_x
                self.boll.y -= self.velocity_boll_y
                if self.boll.y <= 0:
                    self.direction_boll = 3

    def blocked_players_in_screen(self):
        self.player1.y = max(
            self.distance_border_players,
            min(
                self.player1.y,
                self.window_height - self.distance_border_players - self.height_players
                )
            )
        self.player2.y = max(
            self.distance_border_players,
            min(
                self.player2.y,
                self.window_height - self.distance_border_players - self.height_players
                )
            )
        
    def boll_collide_players(self):
        self.boll_collide_player1 = self.boll.colliderect(self.player1)
        self.boll_collide_player2 = self.boll.colliderect(self.player2)
        if self.boll_collide_player1 is True and self.direction_boll == 3:
            self.direction_boll = 1
        
        if self.boll_collide_player1 is True and self.direction_boll == 4:
            self.direction_boll = 2

        if self.boll_collide_player2 is True and self.direction_boll == 1:
            self.direction_boll = 3

        if self.boll_collide_player2 is True and self.direction_boll == 2:
            self.direction_boll = 4

    def verify_move_players(self):
        if pygame.key.get_pressed()[pygame.K_a]:
            self.player1.y = self.player1.y - self.velocity_players
        
        if pygame.key.get_pressed()[pygame.K_d]:
            self.player1.y = self.player1.y + self.velocity_players

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.player2.y = self.player2.y - self.velocity_players

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.player2.y = self.player2.y + self.velocity_players

    def run_game(self):
        self.create_window()
        self.create_elements()

        while self.running:
            self.screen.fill(self.COLOR_BLACK)

            self.draw_elements()

            self.speed_boll()

            self.verify_quit()
            self.verify_points()
            self.verify_exit_boll_screen()
            self.direction_boll_random_initial()
            self.boll_collide_players()
            self.move_boll()
            self.blocked_players_in_screen()
            self.verify_move_players()

            pygame.display.update()

            self.clock.tick(self.time)

        pygame.quit()




if __name__ == '__main__':
    pong = Pong()
    pong.run_game()