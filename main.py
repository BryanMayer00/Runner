import pygame
from sys import exit
from random import randint, choice

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.25)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()

        if obstacle_type == 'snail':
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        else:
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation()
        if score < 250:
            self.rect.x -= 6
        elif score < 500:
            self.rect.x -= 8
        elif score < 750:
            self.rect.x -= 10
        else:
            self.rect.x -= 12
        self.destroy()


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 100)
    score_surface = score_font.render(f'Score:  {current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def add_obstacles(level):
    obstacle_group.add(Obstacle(choice(level)))


screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.25)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Backgrounds
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

game_name = score_font.render('Pixel  Runner', False, (111, 196, 169))
game_name_rectangle = game_name.get_rect(center=(400, 80))

game_message = score_font.render('Press  space  to  run', False, (111, 196, 169))
game_message_rectangle = game_message.get_rect(center=(400, 340))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

# Level
level_1 = ['snail', 'snail', 'snail', 'snail']
level_2 = ['fly', 'snail', 'snail', 'snail']
level_3 = ['fly', 'snail', 'snail']
level_4 = ['fly', 'snail']

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

        if event.type == obstacle_timer:
            if score < 250:
                add_obstacles(level_1)
            elif score < 500:
                add_obstacles(level_2)
            elif score < 750:
                add_obstacles(level_3)
            else:
                add_obstacles(level_4)

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player Code
        player.draw(screen)
        player.update()

        # Obstacle Code
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()

        if score == 250:
            pygame.time.set_timer(obstacle_timer, 1600)
        elif score == 500:
            pygame.time.set_timer(obstacle_timer, 1300)
        elif score == 750:
            pygame.time.set_timer(obstacle_timer, 1000)
        elif score == 1000:
            pygame.time.set_timer(obstacle_timer, 700)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rectangle)
        player.y = 300
        player.gravity = 0

        score_message = score_font.render(f'Your  score:  {score}', False, (111, 196, 169))
        score_message_rectangle = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rectangle)

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)

    pygame.display.update()
    clock.tick(60)
