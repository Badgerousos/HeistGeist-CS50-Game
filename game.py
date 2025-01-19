# HeistGeist


import pygame
from maze import generatemaze
from math import sin, cos, pi, atan2, ceil
from time import time
import random

# Constants
VERSION = "1.0" # hooray    
SCREEN_SIZE = (1920, 1080)
FPS = 30
FILM_FRAMES = 32
GRAIN_FRAMES = 32
COLOR_BG_MENU = (15, 15, 20)
COLOR_BG_GAME = (10, 10, 15)
COLOR_BG_HELP = (10, 10, 15)
COLOR_L = (230, 220, 240)
COLOR_G = (128, 128, 150)
COLOR_D = (30, 30, 40)
COLOR_LB = (30, 30, 30)
LEVELS = 20
STAGES = 5

# Initialize Pygame
pygame.init()
if not pygame.get_init():
    print("Pygame has failed to initialize")
    quit(1)

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.sizex, self.sizey = self.display.get_size()
        self.font_b = pygame.font.SysFont("Leelawadee", 30)
        self.font_i = pygame.font.SysFont("Space Mono Regular", 10)
        self.font_v = pygame.font.SysFont("arial", 12)
        self.font_h = pygame.font.SysFont("Century Gothic", 100, 0, 1) # Fonts startup 
        self.selected_level = 1
        self.times = [0] * LEVELS
        self.game_completed = False
        self.game_started = False
        self.rpg_unlocked = False
        self.rpg_active = False
        self.level_carry_over_reset = {
            "inventory": [None,] * 4,
            "armor_health": 0,
            "gun_ammo": 0,
            "slot": 0
        }
        self.level_carry_over = self.level_carry_over_reset.copy()
        self.stage = ceil((self.selected_level / LEVELS) * STAGES)
        self.levels = []
        for x in range(13, 1000):
            if x % 2:
                y = round((x * 9) / 16)
                if y % 2:
                    self.levels.append((x, y)) # Generate viable levels
        self.img_film = []
        for i in range(FILM_FRAMES):
            self.img_film.append(pygame.transform.scale(pygame.image.load(f"assets/gifs/film/film ({i + 1}).png"), (self.sizex, self.sizey)).convert_alpha())
        self.img_grain = []
        for i in range(GRAIN_FRAMES):
            self.img_grain.append(pygame.transform.scale(pygame.image.load(f"assets/gifs/grain/grain ({i + 1}).png"), (self.sizex, self.sizey)).convert_alpha())
        
        self.img_floor = []
        for i in range(5):
            self.img_floor.append(pygame.transform.scale(pygame.image.load(f"assets/floors/floor ({i + 1}).png"), (self.sizex, self.sizey)))
        self.img_wall = []
        for i in range(5 * 2):
            self.img_wall.append(pygame.image.load(f"assets/walls/wall ({i + 1}).png"))
        self.img_breakable = []
        self.img_broken = []
        self.img_obstacle = []
        for i in range(5):
            self.img_breakable.append(pygame.image.load(f"assets/breakables/breakable ({i + 1}).png").convert_alpha())
            self.img_broken.append(pygame.image.load(f"assets/breakables/broken ({i + 1}).png").convert_alpha())
            if i > 1:
                self.img_obstacle.append(pygame.image.load(f"assets/obstacles/obstacle ({i + 1}).png").convert_alpha())
        self.img_ghost_wall = []
        for i in range(5):
            if i == 0 or i == 1:
                temp = []
                for j in range(3):
                    temp.append(pygame.image.load(f"assets/ghost_walls/ghost_wall{j + 1} ({i + 1}).png").convert_alpha())
                self.img_ghost_wall.append(temp)
            elif i == 3:
                temp = []
                for j in range(5):
                    temp.append(pygame.image.load(f"assets/ghost_walls/ghost_wall{j + 1} ({i + 1}).png").convert_alpha())
                self.img_ghost_wall.append(temp)
            else:
                self.img_ghost_wall.append(pygame.image.load(f"assets/ghost_walls/ghost_wall ({i + 1}).png").convert_alpha())
        self.img_firewall = []
        for i in range(5):
            if i in (2, 3):
                temp = []
                for j in range(3):
                    temp.append(pygame.image.load(f"assets/firewalls/firewall{j + 1} ({i + 1}).png")) 
                self.img_firewall.append(temp) 
            else:
                self.img_firewall.append(pygame.image.load(f"assets/firewalls/firewall ({i + 1}).png")) # Initialize maze textures.
        self.img_objective = pygame.image.load("assets/misc/objective.png")
        self.img_objective_open = pygame.image.load("assets/misc/objective_open.png")
        self.img_objective_locked = pygame.image.load("assets/misc/objective_locked.png")
        self.img_objective_unlocked = pygame.image.load("assets/misc/objective_unlocked.png")
        self.img_objective_unlocked_open = pygame.image.load("assets/misc/objective_unlocked_open.png")
        self.img_prize_locked = pygame.image.load("assets/misc/prize_locked.png")
        self.img_prize_unlocked = pygame.image.load("assets/misc/prize_unlocked.png")
        self.img_prize_unlocked_open = pygame.image.load("assets/misc/prize_unlocked_open.png")
        self.img_glow = pygame.image.load("assets/misc/glow.png").convert_alpha()
        self.img_glow_flare = pygame.image.load("assets/misc/glow_flare.png").convert_alpha()
        self.img_glow_shoe = pygame.image.load("assets/misc/shoe_overlay.png").convert_alpha()
        self.img_glow_health = []
        for i in range(8):
            self.img_glow_health.append(pygame.image.load(f"assets/gifs/health_grain/health_grain ({i + 1}).png").convert_alpha())
        self.img_firewall_border = pygame.image.load("assets/misc/firewall_border.png").convert_alpha()
        self.img_powerups = []
        self.img_key = pygame.image.load("assets/items/key.png").convert_alpha()
        self.img_powerups.append(pygame.image.load("assets/items/flashlight.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/crossbow.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/bomb.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/shoe.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/flare.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/armor.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/mega_bomb.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/knife.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/krinkov.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/medkit.png").convert_alpha())
        self.img_powerups.append(pygame.image.load("assets/items/RPG.png").convert_alpha())
        self.img_crossbow = pygame.image.load("assets/items/crossbow.png").convert_alpha()
        self.img_rpg = []
        for i in range(3):
            self.img_rpg.append(pygame.image.load(f"assets/items/RPG_top_{i}.png").convert_alpha())
        self.img_krinkov = []
        for i in range(4):
            self.img_krinkov.append(pygame.image.load(f"assets/items/krinkov_top_{i}.png").convert_alpha())
        self.img_flare_gun = pygame.image.load("assets/items/flare_top.png").convert_alpha()
        self.img_armor = pygame.image.load("assets/items/worn_armor.png").convert_alpha()
        self.img_mini_bomb = pygame.image.load("assets/items/mini_bomb.png").convert_alpha()
        self.img_rocket = []
        for i in range(4):
            self.img_rocket.append(pygame.image.load(f"assets/items/rocket{i + 1}.png").convert_alpha())
        self.img_nuke = []
        for i in range(5):
            self.img_nuke.append(pygame.image.load(f"assets/items/nuke{i + 1}.png").convert_alpha())
        self.img_player = pygame.image.load("assets/misc/player.png").convert_alpha() 
        self.img_player_holding = pygame.image.load("assets/misc/player_holding.png").convert_alpha() 
        self.img_player_flare = pygame.image.load("assets/misc/player_pistol.png").convert_alpha() 
        self.img_player_gun = pygame.image.load("assets/misc/player_gun.png").convert_alpha() 
        self.img_player_crossbow = pygame.image.load("assets/misc/player_crossbow.png").convert_alpha() 
        self.img_player_rpg = pygame.image.load("assets/misc/player_rpg.png").convert_alpha() 
        self.img_gaurd = pygame.image.load("assets/misc/gaurd.png").convert_alpha() 
        self.img_gaurd_firing = pygame.image.load("assets/misc/gaurd_firing.png").convert_alpha() 
        self.img_spider = []
        for i in range(6):
            self.img_spider.append(pygame.image.load(f"assets/misc/spider ({i}).png").convert_alpha())
        self.img_spider_bite = []
        for i in range(6):
            self.img_spider_bite.append(pygame.image.load(f"assets/misc/spider_bite ({i + 1}).png").convert_alpha())
        self.img_bomb_effect = []
        for i in range(3):
            self.img_bomb_effect.append(pygame.image.load(f"assets/effects/bomb_effect ({i + 1}).png").convert_alpha())
        self.img_mega_bomb_effect = []
        for i in range(3):
            self.img_mega_bomb_effect.append(pygame.image.load(f"assets/effects/mega_bomb_effect ({i + 1}).png").convert_alpha())
        self.img_nuke_effect = []
        for i in range(3):
            self.img_nuke_effect.append(pygame.image.load(f"assets/effects/nuke_effect ({i + 1}).png").convert_alpha())
        self.img_bullet_effect = []
        for i in range(4):
            self.img_bullet_effect.append(pygame.image.load(f"assets/effects/bullet_effect ({i + 1}).png").convert_alpha())
        self.img_rocket_effect = []
        for i in range(3):
            self.img_rocket_effect.append(pygame.image.load(f"assets/effects/rocket_effect ({i + 1}).png").convert_alpha())
        self.img_sweep = []
        for i in range(8):
            self.img_sweep.append(pygame.image.load(f"assets/effects/sweep_{i}.png").convert_alpha())
        self.img_big_smoke = []
        for i in range(11):
            self.img_big_smoke.append(pygame.image.load(f"assets/effects/big_smoke_{i}.png").convert_alpha())
        self.img_flare = []
        for i in range(2):
            self.img_flare.append(pygame.image.load(f"assets/effects/flare_{i}.png").convert_alpha())
        self.img_death = []
        for i in range(8):
            self.img_death.append(pygame.image.load(f"assets/effects/generic_{i}.png").convert_alpha())
        self.img_blood = []
        for i in range(3):
            self.img_blood.append(pygame.image.load(f"assets/effects/blood ({i + 1}).png").convert_alpha())
        self.img_health_particle = pygame.image.load("assets/effects/health.png").convert_alpha()
        self.img_run_dust = []
        for i in range(7):
            self.img_run_dust.append(pygame.image.load(f"assets/effects/run_effect ({i + 1}).png").convert_alpha())
        self.img_run_shoestate = []
        for i in range(5):
            self.img_run_shoestate.append(pygame.image.load(f"assets/effects/trial_spawner_detection_ominous_{i}.png").convert_alpha())
        # initialize textures

        pygame.display.set_caption("HeistGeist")
        pygame.display.set_icon(pygame.image.load("assets/icon.ico"))
        print(f"Effective screen size: {self.sizex}x{self.sizey}")

    def run(self): # Overarching game loop
            state = "menu"
            while True:
                if state == "menu": 
                    state = self.main_menu()
                elif state == "game":
                    state = self.game_loop()

    def main_menu(self): # Main Menu
        value_offset = 0.0
        film_index = FILM_FRAMES - 1
        film_sequence = list(range(FILM_FRAMES * 3))
        gif_index = 0
        text_offset = 70
        area = [
            "Garden",
            "House",
            "Basement",
            "Cave",
            "Dungeon"   
        ]

        text_title = self.font_h.render("HeistGeist", False, COLOR_G) # Inilize texts
        text_title_rect = text_title.get_rect()
        title_surface = pygame.Surface((511, 143), pygame.SRCALPHA)

        text_time = pygame.transform.scale_by(self.font_i.render("Times / s", True, COLOR_G), 2)
        text_time_rect = text_time.get_rect(topleft=(50, self.sizey / 2 - 4 * text_offset))

        text_times = []
        for i in range(min(self.selected_level, LEVELS)):
            if i == min(self.selected_level, LEVELS) - 1:
                text_level_time = pygame.transform.scale_by(self.font_i.render(f"Total time: {sum(self.times):.1f}", True, COLOR_G), 2)
                text_level_time_rect = text_level_time.get_rect(topleft=(50, self.sizey / 2 - (3 - (i + 1) / 2) * text_offset))
            else:
                if self.times[i] != 0:
                    if not (i) % (LEVELS // STAGES):
                        text_level_time = pygame.transform.scale_by(self.font_i.render(f"{area[(i + 1) // 3]}: Level {i + 1}: {self.times[i]:.1f}", True, COLOR_G), 2)
                    else:
                        text_level_time = pygame.transform.scale_by(self.font_i.render(f"Level {i + 1}: {self.times[i]:.1f}", True, COLOR_G), 2)
                else:
                        text_level_time = pygame.transform.scale_by(self.font_i.render(f"Level {i + 1}: N/A", True, COLOR_G), 2)
                text_level_time_rect = text_level_time.get_rect(topleft=(50, self.sizey / 2 - (3 - i / 2) * text_offset / 1.5))
            text_times.append((text_level_time, text_level_time_rect))
        if sum(self.times) < 1200 and self.selected_level == LEVELS + 1 and 0 not in self.times:
            self.rpg_unlocked = True
        if self.rpg_unlocked:
            text_rpg = pygame.transform.scale_by(self.font_i.render(f"Par time beaten, RPG unlocked. Use with care! (optional)", True, COLOR_G), 2)
            text_rpg_rect = text_rpg.get_rect(center=(self.sizex / 2, self.sizey / 2 + 2 * text_offset))
            text_rpg_button = self.font_b.render(f"RPG toggle", True, COLOR_L)
            text_rpg_button_rect = text_rpg_button.get_rect(center=(self.sizex / 2, self.sizey / 2 + 3 * text_offset))
            button_rpg = pygame.Rect.inflate(text_rpg_button_rect, 20, 10)
        if self.selected_level <= LEVELS:
            text_area = pygame.transform.scale_by(self.font_i.render(f"You have reached the {area[self.stage - 1]}.", True, COLOR_G), 2)
            text_level = pygame.transform.scale_by(self.font_i.render(f"Level: {self.selected_level}/{LEVELS}", True, COLOR_G), 2)
            text_start = self.font_b.render("Start game", True, COLOR_L)
        else:
            text_area = pygame.transform.scale_by(self.font_i.render("You have beaten the maze!", True, COLOR_G), 2)
            text_level = pygame.transform.scale_by(self.font_i.render("To restart, start a new game", True, COLOR_G), 2)
            text_start = self.font_b.render("Start new game", True, COLOR_L)
        text_area_rect = text_area.get_rect(center=(self.sizex / 2, self.sizey / 2 - 1.5 * text_offset))
        text_level_rect = text_level.get_rect(center=(self.sizex / 2, self.sizey / 2 - text_offset))
        text_start_rect = text_start.get_rect(center=(self.sizex / 2, self.sizey / 2))
        button_start = pygame.Rect.inflate(text_start_rect, 20, 10)

        text_exit = self.font_b.render("Exit game", True, COLOR_L)
        text_exit_rect = text_exit.get_rect(center=(self.sizex / 2, self.sizey / 2 + text_offset))
        button_exit = pygame.Rect.inflate(text_exit_rect, 20, 10)

        text_version = self.font_v.render("Version:" + VERSION, True, "white")
        text_version_rect = text_version.get_rect()

        UPDATEFPS = pygame.USEREVENT + 1
        pygame.time.set_timer(UPDATEFPS, 1000)

        text_fps = self.font_v.render(f"FPS:{self.clock.get_fps():.0}", True, "white")
        text_fps_rect = text_fps.get_rect(topright=(self.sizex, 0))
        while True:
            value_offset += 0.03
            offset_1 = 10 * sin(value_offset)
            offset_2 = 10 * sin(2 * value_offset) # Offsets used for elemnt swaying
            text_title_rect.topleft = (20 + 2 * offset_1, 10 + offset_2)
            film_index += 1
            gif_index += 1
            if film_index == FILM_FRAMES:
                film_index = 0
                random.shuffle(film_sequence)

            self.display.fill(COLOR_BG_MENU)

            self.display.blit(self.img_grain[gif_index % GRAIN_FRAMES], (0, 0))
            pygame.draw.rect(self.display, COLOR_D, (10 + offset_1, 10 - offset_1, self.sizex - 20 - 2 * offset_1, self.sizey - 20 + 2 * offset_1), 20, 100)
            if film_sequence[film_index] < FILM_FRAMES:
                self.display.blit(self.img_film[film_sequence[film_index]], (0, 0))

            title_surface.fill((0, 0, 0, 8), None, pygame.BLEND_RGBA_SUB)
            title_surface.blit(text_title, text_title_rect)
            self.display.blit(title_surface, (self.sizex / 2 - 255, self.sizey / 2 - 300))
            if self.game_started and self.selected_level != 1:
                self.display.blit(text_area, text_area_rect)
                self.display.blit(text_level, text_level_rect)
                self.display.blit(text_time, text_time_rect)
                for i in range(min(self.selected_level, LEVELS)):
                    self.display.blit(*text_times[i])
            pygame.draw.rect(self.display, COLOR_D, button_start, 0, 10)
            self.display.blit(text_start, text_start_rect)
            pygame.draw.rect(self.display, COLOR_D, button_exit, 0, 10)
            self.display.blit(text_exit, text_exit_rect)
            
            if self.rpg_unlocked:
                self.display.blit(text_rpg, text_rpg_rect)
                if self.rpg_active:
                    pygame.draw.rect(self.display, COLOR_G, button_rpg, 0, 10)
                else:
                    pygame.draw.rect(self.display, COLOR_D, button_rpg, 0, 10)
                self.display.blit(text_rpg_button, text_rpg_button_rect)

            if button_start.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.display, COLOR_L, button_start, 3, 10)
            elif button_exit.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.display, COLOR_L, button_exit, 3, 10)
            elif self.rpg_unlocked:
                if button_rpg.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display, COLOR_L, button_rpg, 3, 10)

            pygame.draw.rect(self.display, "black", text_fps_rect)
            self.display.blit(text_fps, text_fps_rect)
            pygame.draw.rect(self.display, "black", text_version_rect)
            self.display.blit(text_version, text_version_rect)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Game quit by user in menu")
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN: # Buttons
                    if text_title_rect.collidepoint(event.pos): # easter egg
                        print("Thats not a button")
                    if button_start.collidepoint(event.pos):
                        if self.selected_level == LEVELS + 1:
                            self.times = [0] * LEVELS
                            self.selected_level = 1
                            self.game_completed = False
                        print("Game Start")
                        return "game"
                    if button_exit.collidepoint(event.pos):
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                    if self.rpg_unlocked:
                        if button_rpg.collidepoint(event.pos):
                            if self.rpg_active:
                                self.rpg_active = False
                            else:
                                self.rpg_active = True
                if event.type == UPDATEFPS:
                    text_fps = self.font_v.render(f"FPS:{self.clock.get_fps():.0f}", True, "white")
                    text_fps_rect = text_fps.get_rect(topright=(self.sizex, 0))

            self.clock.tick(FPS)


    def game_loop(self): # Main game loop
        def render_maze(objective_pos, inventory):
            powerups = []
            enemies = []
            key = [None, False, None]
            maze_surface = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
            floor_surface = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
            floor_shadow_surface = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
            firewalls = []
            # Maze rendering
            for i in range(maze_size[0]):
                for j in range(maze_size[1]):
                    floor_surface.blit(pygame.transform.scale(self.img_floor[self.stage - 1], ( MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (i * MAZE_SCALE[0], j * MAZE_SCALE[1]))
                    match maze[(i, j)]:
                        case 4:
                            img = self.img_obstacle[self.stage - 3]
                        case 3:
                            img = self.img_breakable[self.stage - 1]
                        case 2:
                            if self.stage in (3, 4):
                                img = self.img_firewall[self.stage - 1][0]
                                anim_firewalls.append([(i, j), random.randint(0, 2)])
                            else:
                                img = self.img_firewall[self.stage - 1]
                            firewalls.append([i, j])
                        case 1:
                            if self.stage in (1, 4, 5):
                                img = self.img_wall[(self.stage - 1) * 2 + int(random.randint(0, 3) / 3)]
                            else:
                                up = down = left = right = 1
                                if j == 0:
                                    up = 0
                                elif maze[i, j - 1] in (-2, 1, 2, 3):
                                    up = 0
                                if j == maze_size[1] - 1:
                                    down = 0
                                elif maze[i, j + 1] in (-2, 1, 2, 3):
                                    down = 0
                                if i == 0:
                                    left = 0
                                elif maze[i - 1, j] in (-2, 1, 2, 3):
                                    left = 0
                                if i == maze_size[0] - 1:
                                    right = 0
                                elif maze[i + 1, j] in (-2, 1, 2, 3):
                                    right = 0
                                if (left + right) and (up + down):
                                    img = self.img_wall[(self.stage - 1) * 2 + 1]
                                else:
                                    img = self.img_wall[(self.stage - 1) * 2]
                        case 0:
                            objective_pos = (i, j)
                            continue
                        case -1:
                            continue
                        case -2:
                            if self.stage in (1, 2):
                                img = self.img_ghost_wall[self.stage - 1][random.randint(0, 2)]
                            elif self.stage == 4:
                                img = self.img_ghost_wall[self.stage - 1][0]
                                anim_ghost_walls.append([(i, j), random.randint(0, 2)])
                            else:
                                img = self.img_ghost_wall[self.stage - 1]
                        case -3:
                            key = [(i, j), False, None]
                            continue
                        case -11: # KNIFE
                            if -11 not in inventory:
                                powerups.append({"type": maze[(i, j)], "pos": (i, j)})
                            else:
                                maze[(i, j)] = -1
                            continue
                        case -15: # SPIDER
                            enemies.append({"type" : SPIDER, 
                                            "pos" : [ENEMY_VALUES["MOVE_SCALE"] * i + ENEMY_VALUES["MOVE_SCALE"] // 2, ENEMY_VALUES["MOVE_SCALE"] * j + ENEMY_VALUES["MOVE_SCALE"] // 2, random.randint(0, 3), 0], 
                                            "health" : ENEMY_VALUES["HEALTH"][SPIDER], 
                                            "attack_delay" : 0, 
                                            "player_detected": 0,
                                            "player_angle": 0,
                                            "stamina" : ENEMY_VALUES["STAMINA"][SPIDER],
                                            "moving" : True})
                            maze[(i, j)] = -1
                            continue
                        case -16: # GAURD
                            enemies.append({"type" : GAURD, 
                                            "pos" : [ENEMY_VALUES["MOVE_SCALE"] * i + ENEMY_VALUES["MOVE_SCALE"] // 2, ENEMY_VALUES["MOVE_SCALE"] * j + ENEMY_VALUES["MOVE_SCALE"] // 2, random.randint(0, 3), 0], 
                                            "health" : ENEMY_VALUES["HEALTH"][GAURD], 
                                            "attack_delay" : 0, 
                                            "player_detected": 0,
                                            "player_angle": 0,
                                            "gunshot_timer": 0})
                            maze[(i, j)] = -1
                            continue
                        case _ if maze[(i, j)] <= -4 and maze[(i, j)] >= -14:
                            powerups.append({"type": maze[(i, j)], "pos": (i, j)})
                            continue
                        case _:
                            continue
                    maze_surface.blit(pygame.transform.scale(img, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (i * MAZE_SCALE[0], j * MAZE_SCALE[1]))
            for firewall in firewalls:
                floor_surface.blit(pygame.transform.scale(self.img_firewall_border, ((MAZE_SCALE[0] + 1) * 1.4, (MAZE_SCALE[1] + 1) * 1.4)), (firewall[0] * MAZE_SCALE[0] - (MAZE_SCALE[0] + 1) * 0.2, firewall[1] * MAZE_SCALE[1] - (MAZE_SCALE[1] + 1) * 0.2))
            # ///
            # Shadow rendering
            floor_shadow_surface.fill((0, 0, 0, 128))
            temp_surface = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
            if self.stage == 1:
                for i in range(int(450 / maze_size[0])):
                    temp_surface.blit(maze_surface, (i, i / 1.77))
            elif self.stage <= 3:
                for i in range(int(1350 / maze_size[0])):
                    temp_surface.blit(pygame.transform.scale(maze_surface, (self.sizex + i * 2, self.sizey + i / 1.77)), (-i, -i / 3.55))
            else:
                for i in range(-3, 5, 2):
                    for j in range(-3, 5, 2):
                        temp_surface.blit(maze_surface, (i, j))
            floor_shadow_surface.blit(temp_surface, (0, 0), None, pygame.BLEND_RGBA_MIN)
            floor_surface.blit(floor_shadow_surface, (0, 0))
            # ///
            # Objective rendering
            if self.stage == 1:        
                objective_rect = floor_surface.blit(pygame.transform.scale(self.img_objective, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
            elif self.selected_level == LEVELS:
                objective_rect = floor_surface.blit(pygame.transform.scale(self.img_prize_locked, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
            else:
                objective_rect = floor_surface.blit(pygame.transform.scale(self.img_objective_locked, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))

            return maze_surface, floor_surface, powerups, objective_rect, objective_pos, key, enemies
            # //
        # ///
        # Start of initialization
        # ///
        overlay_surface = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        self.stage = ceil((self.selected_level / LEVELS) * STAGES)
        frame_index = 0
        paused = 0
        DEFAULT_GLOW_RADIUS = 10
        glow_radius = DEFAULT_GLOW_RADIUS
        VIEWPORT_BLOCK_WIDTH = 16
        FLASHLIGHT = -4
        CROSSBOW = -5
        BOMB = -6
        SHOE = -7
        FLARE = -8
        ARMOR = -9
        MEGA_BOMB = -10
        KNIFE = -11
        GUN = -12
        MEDKIT = -13
        RPG = -14
        SPIDER = -15
        GAURD = -16
        ENEMY_VALUES = {
            "HEALTH": {
                SPIDER: 30,
                GAURD: 100,
            },
            "SPEED": {
                SPIDER: 4,
                GAURD: 1
            },
            "STAMINA": {
                SPIDER: 50,
                GAURD: 100
            },
            "MOVE_SCALE": 16
        }
        self.game_started = True
        alive = True
        is_running = False
        is_sneaking = False
        dead_timer = 0
        active_powerups = []
        objective_close = False
        touching_firewall = False
        anim_firewalls = []
        anim_ghost_walls = []
        effects = []
        maze_size = self.levels[self.selected_level - 1]
        MAZE_SCALE = [self.sizex / maze_size[0], self.sizey / maze_size[1]]
        print(f"Maze size: {maze_size}")
        random.seed(time())
        player_values = {
            "player_pos": [1.2, 1.2, 0],
            "PLAYER_SPEED": 0.1,
            "speed_mult": 2,
            "PLAYER_SCALE": 0.199,
            "player_center": (0, 0)
        }
        stamina_values = {
            "MAX_STAMINA": 100,
            "stamina": 100,
            "stamina_delay": 0
        }
        health_values = {   
            "MAX_HEALTH": 100,
            "health": 100,
            "health_speed": 10,
            "previous_health": 100,
            "damage_delay": 0,
            "MAX_DAMAGE_DELAY": 20
        }
        powerup_values = {
            "MAX_FUSE": 35,
            "MAX_SHOESTATE": 150,
            "MAX_FLASHLIGHTSTATE": 900,
            "MAX_FLARESTATE": 300,
            "MAX_KNIFE_DELAY": 20,
            "MAX_GUN_DELAY": 5,
            "MAX_GUN_AMMO": 30,
            "MAX_RPG_DELAY": 75,
            "MAX_PICKUP_DELAY": 20,
            "MAX_ARMOR_HEALTH": 200,
            "shoestate": 0,
            "flashlightstate": 0,
            "flarestate": 0,
            "knife_delay": 0,
            "gun_delay": 0,
            "gun_ammo": 0,
            "rpg_delay": 0,
            "pickup_delay": 0,
            "armor_health": 0
        }
        inventory = self.level_carry_over["inventory"].copy()
        powerup_values["armor_health"] = self.level_carry_over["armor_health"]
        powerup_values["gun_ammo"] = self.level_carry_over["gun_ammo"]
        slot = self.level_carry_over["slot"]
        if self.rpg_active:
            inventory[3] = RPG
        elif inventory[3] == RPG:
            inventory[3] = None
        maze = generatemaze(maze_size[0], maze_size[1], time(), self.stage)
        objective_pos = [(maze_size[0] - 2) * MAZE_SCALE[0], (random.randint(0, 1) * (maze_size[1] - 3) + 1) * MAZE_SCALE[1]]
        darkness_surface = pygame.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        maze_surface, floor_surface, powerups, objective_rect, objective_pos, key, enemies = render_maze(objective_pos, inventory)

        text_fps = self.font_v.render(f"FPS:{self.clock.get_fps():.0}", True, "white")
        text_fps_rect = text_fps.get_rect(topright=(self.sizex, 0))
        text_dead = self.font_h.render("Dead", True, "red")
        text_dead_rect = text_dead.get_rect(center=(self.sizex / 2, self.sizey / 3))
        text_dead_prompt = pygame.transform.scale_by(self.font_i.render("Press ESC to go back to menu", True, "red"), 4)
        text_dead_prompt_rect = text_dead_prompt.get_rect(center=(self.sizex / 2, self.sizey * 2 / 3))
        self.times[self.selected_level - 1] = 0
        text_time = pygame.transform.scale_by(self.font_i.render(f"{self.times[self.selected_level - 1]}", True, COLOR_L), 2)
        text_time_rect = text_time.get_rect(topleft=(10, 5))

        text_paused = self.font_h.render("Paused", True, COLOR_G)
        text_paused_rect = text_paused.get_rect(center=(self.sizex / 2, self.sizey / 3))
        text_resume = self.font_b.render("Resume", True, COLOR_L)
        text_resume_rect = text_resume.get_rect(center=(self.sizex / 2, self.sizey / 2))
        button_resume = pygame.Rect.inflate(text_resume_rect, 20, 10)
        text_menu = self.font_b.render("Menu", True, COLOR_L)
        text_menu_rect = text_menu.get_rect(center=(self.sizex / 2, self.sizey / 2 + 50))
        button_menu = pygame.Rect.inflate(text_menu_rect, 20, 10)
        text_restart = self.font_b.render("Restart level", True, COLOR_L)
        text_restart_rect = text_restart.get_rect(center=(self.sizex / 2 - 100, self.sizey / 2 + 100))
        button_restart = pygame.Rect.inflate(text_restart_rect, 20, 10)
        text_explode = self.font_b.render("Restart run", True, COLOR_L)
        text_explode_rect = text_explode.get_rect(center=(self.sizex / 2 + 100, self.sizey / 2 + 100))
        button_explode = pygame.Rect.inflate(text_explode_rect, 20, 10)
        text_quit = self.font_b.render("Quit", True, COLOR_L)
        text_quit_rect = text_quit.get_rect(center=(self.sizex / 2, self.sizey / 2 + 150))
        button_quit = pygame.Rect.inflate(text_quit_rect, 20, 10)
        paused_surface = pygame.surface.Surface((self.sizex, self.sizey), pygame.SRCALPHA)
        paused_surface.fill((0, 0, 0, 128))
        pygame.draw.rect(paused_surface, COLOR_BG_MENU, (self.sizex / 2 - 300, 200, 600, self.sizey - 400), 0, 20)
        pygame.draw.rect(paused_surface, COLOR_D, (self.sizex / 2 - 280, 220, 560, self.sizey - 440), 20, 20)
        paused_surface.blit(text_paused, text_paused_rect)
        # Restart, Menu, Quit, Resume

        UPDATE_FPS = pygame.USEREVENT + 1
        UPDATE_VIEW = pygame.USEREVENT + 2
        USE_POWERUP = pygame.USEREVENT + 3
        TAKE_DAMAGE = pygame.USEREVENT + 4
        ENTITY_DAMAGE_CHECK = pygame.USEREVENT + 5
        pygame.time.set_timer(UPDATE_FPS, 100)
        pygame.event.post(pygame.event.Event(UPDATE_VIEW))
        # ///
        # Start of game loop
        # ///
        while True:
            # Variable aggregation
            keys = pygame.key.get_pressed()
            frame_index += 1
            player_values["player_center"] = [player_values["player_pos"][0] * MAZE_SCALE[0], player_values["player_pos"][1] * MAZE_SCALE[1]]
            if health_values["previous_health"] > health_values["health"]:
                health_values["previous_health"] = health_values["health"]
            elif health_values["previous_health"] + 10 < health_values["health"] and alive:
                for _ in range(int(health_values["health"] - health_values["previous_health"] + 1) // 10):
                    effects.append(["health", [player_values["player_pos"][0] + random.random() - 0.5, player_values["player_pos"][1] + random.random() - 0.5], 30])
                health_values["previous_health"] = health_values["health"]
            if powerup_values["pickup_delay"]:
                powerup_values["pickup_delay"] -= 1
            if powerup_values["knife_delay"]:
                powerup_values["knife_delay"] -= 1
            if powerup_values["gun_delay"]:
                powerup_values["gun_delay"] -= 1
            if powerup_values["rpg_delay"]:
                powerup_values["rpg_delay"] -= 1

            # ///
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Game quit by user in game")
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN and alive:
                    if paused:
                        if button_resume.collidepoint(pygame.mouse.get_pos()):
                            paused = False
                        elif button_menu.collidepoint(pygame.mouse.get_pos()):
                            self.times[self.selected_level - 1] = 0
                            print("Returned to menu from pause")
                            return "menu"
                        elif button_restart.collidepoint(pygame.mouse.get_pos()):
                            self.times[self.selected_level - 1] = 0
                            print("Restarted level")
                            return "game"
                        elif button_explode.collidepoint(pygame.mouse.get_pos()):
                            alive = False
                            active_powerups.append([MEGA_BOMB, (int(player_values["player_pos"][0]), int(player_values["player_pos"][1])), 1])
                            print("Run manually restarted")
                            self.level_carry_over = self.level_carry_over_reset.copy()
                            self.selected_level = 1
                            paused = False
                        elif button_quit.collidepoint(pygame.mouse.get_pos()):
                            pygame.event.post(pygame.event.Event(pygame.QUIT))
                    else:
                        if event.button == 1:
                            pygame.event.post(pygame.event.Event(USE_POWERUP, origin="inventory"))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if alive:
                            if paused:
                                paused = 0
                            else:
                                paused = 1
                        else:
                            self.times[self.selected_level - 1] = 0
                            print("Returned to menu from death")
                            return "menu"
                    if event.key == pygame.K_g and alive and not paused:
                        if maze[(int(player_values["player_pos"][0]), int(player_values["player_pos"][1]))] == -1 and inventory[slot] and inventory[slot] != RPG:
                            if inventory[slot] != GUN:
                                maze[(int(player_values["player_pos"][0]), int(player_values["player_pos"][1]))] = inventory[slot]
                                powerups.append({"type": inventory[slot], "pos": (int(player_values["player_pos"][0]), int(player_values["player_pos"][1]))})
                            inventory[slot] = None
                            powerup_values["pickup_delay"] = powerup_values["MAX_PICKUP_DELAY"]
                    if event.key == pygame.K_SPACE and alive and not paused:
                        pygame.event.post(pygame.event.Event(USE_POWERUP, origin="inventory"))
                    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT) and not paused:
                        if is_running:
                            is_running = False
                        else:
                            is_running = True
                        is_sneaking = False
                    elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL) and not paused:
                        if is_sneaking:
                            is_sneaking = False
                        else:
                            is_sneaking = True
                        is_running = False
                    if event.key == pygame.K_1 and not paused:
                        slot = 0
                    if event.key == pygame.K_2 and not paused:
                        slot = 1
                    if event.key == pygame.K_3 and not paused:
                        slot = 2
                    if event.key == pygame.K_4 and not paused:
                        slot = 3
                if event.type == USE_POWERUP and alive:
                    if event.origin == "inventory":
                        if inventory[slot] == BOMB and maze[(int(player_values["player_pos"][0]), int(player_values["player_pos"][1]))] == -1:
                            inventory[slot] = None
                            active_powerups.append([BOMB, (int(player_values["player_pos"][0]), int(player_values["player_pos"][1])), powerup_values["MAX_FUSE"]])
                        elif inventory[slot] == SHOE:
                            inventory[slot] = None
                            powerup_values["shoestate"] = powerup_values["MAX_SHOESTATE"]
                        elif inventory[slot] == FLARE:
                            inventory[slot] = None
                            effects.append(["flare", [player_values["player_pos"][0], player_values["player_pos"][1]], powerup_values["MAX_FLARESTATE"]])
                            powerup_values["flarestate"] = powerup_values["MAX_FLARESTATE"]
                        elif inventory[slot] == CROSSBOW:
                            inventory[slot] = None
                            active_powerups.append([CROSSBOW, [player_values["player_pos"][0], player_values["player_pos"][1]], player_values["player_pos"][2], False, powerup_values["MAX_FUSE"]])
                        elif inventory[slot] == FLASHLIGHT:
                            inventory[slot] = None
                            powerup_values["flashlightstate"] = powerup_values["MAX_FLASHLIGHTSTATE"]
                        elif inventory[slot] == MEGA_BOMB and maze[(int(player_values["player_pos"][0]), int(player_values["player_pos"][1]))] == -1:
                            inventory[slot] = None
                            active_powerups.append([MEGA_BOMB, (int(player_values["player_pos"][0]), int(player_values["player_pos"][1])), powerup_values["MAX_FUSE"] * 2])
                        elif inventory[slot] == KNIFE and not powerup_values["knife_delay"]:
                            powerup_values["knife_delay"] = powerup_values["MAX_KNIFE_DELAY"]
                            effects.append(["sweep", player_values["player_pos"], 8])
                            knife_pos_list = []
                            for i in range(10):
                                knife_pos_list.append([player_values["player_pos"][0] + sin(player_values["player_pos"][2] - 1 + i % 5 / 2) * 0.8 / int(i / 5 + 1), player_values["player_pos"][1] + cos(player_values["player_pos"][2] - 1 + i % 5 / 2) * 0.8 / int(i / 5 + 1)])
                            for knife_pos in knife_pos_list:
                                if maze[(int(knife_pos[0]), int(knife_pos[1]))] == 4:
                                    maze[(int(knife_pos[0]), int(knife_pos[1]))] = -1
                                    rect_fill = (int(knife_pos[0]) * MAZE_SCALE[0], int(knife_pos[1]) * MAZE_SCALE[1], MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)
                                    maze_surface.fill((0, 0, 0, 0), rect_fill)
                                else:
                                    for i in range(len(enemies)):
                                        if pygame.rect.Rect(enemies[i]["pos"][0] // ENEMY_VALUES["MOVE_SCALE"], enemies[i]["pos"][1] // ENEMY_VALUES["MOVE_SCALE"], 1, 1).collidepoint(knife_pos):
                                            pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=5, affector=i ))
                        elif inventory[slot] == RPG and not powerup_values["rpg_delay"]:
                            powerup_values["rpg_delay"] = powerup_values["MAX_RPG_DELAY"]
                            active_powerups.append([RPG, [player_values["player_pos"][0] + sin(player_values["player_pos"][2] - pi / 5) / 5, player_values["player_pos"][1] + cos(player_values["player_pos"][2] - pi / 5) / 5], player_values["player_pos"][2], powerup_values["MAX_FUSE"] * 2])
                    elif event.origin == "pickup":
                        if event.item == ARMOR:
                            powerup_values["armor_health"] = powerup_values["MAX_ARMOR_HEALTH"]
                        elif event.item == MEDKIT:
                            health_values["health"] = health_values["MAX_HEALTH"]
                            health_values["health_speed"] = 0
                if event.type == pygame.MOUSEWHEEL and not paused:
                    slot = (slot - event.y) % 4
                if event.type == UPDATE_FPS and not paused:
                    self.times[self.selected_level - 1] += 0.1
                    text_fps = self.font_v.render(f"FPS:{self.clock.get_fps():.0f}", True, "white")
                    text_fps_rect = text_fps.get_rect(topright=(self.sizex, 0))
                    text_time = pygame.transform.scale_by(self.font_i.render(f"{self.times[self.selected_level - 1]:.1f}", True, COLOR_L), 2)
                    text_time_rect = text_time.get_rect(topleft=(10, 5))
                if event.type == UPDATE_VIEW:
                    if self.stage >= 2:
                        zoom_factor = (maze_size[0] / VIEWPORT_BLOCK_WIDTH) / min(1.5, powerup_values["flarestate"] + 1)
                    else:
                        zoom_factor = 1
                    viewport_width = self.sizex // zoom_factor
                    viewport_height = self.sizey // zoom_factor
                    if powerup_values["flarestate"]:
                        glow_radius = DEFAULT_GLOW_RADIUS * 1.5
                    else:
                        glow_radius = DEFAULT_GLOW_RADIUS
                if event.type == ENTITY_DAMAGE_CHECK:
                    if event.origin in (BOMB, MEGA_BOMB):
                        if int(player_values["player_pos"][0]) == event.pos[0] and int(player_values["player_pos"][1]) == event.pos[1]:
                            pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=event.player_damage[0], peirce=event.player_damage[1], armor_peirce=event.player_damage[2], affector="player"))
                        for i in range(len(enemies)):
                            if int(enemies[i]["pos"][0] / ENEMY_VALUES["MOVE_SCALE"]) == event.pos[0] and int(enemies[i]["pos"][1] / ENEMY_VALUES["MOVE_SCALE"]) == event.pos[1] and enemies[i]["health"] > 0:
                                pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=event.player_damage[0], affector=i))
                    elif event.origin == CROSSBOW:
                        if int(player_values["player_pos"][0]) in (event.pos[0], event.pos[2]) and int(player_values["player_pos"][1]) in (event.pos[1], event.pos[3]):
                            pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=event.player_damage[0], peirce=event.player_damage[1], armor_peirce=event.player_damage[2], affector="player"))
                        for i in range(len(enemies)):
                            if int(enemies[i]["pos"][0] / ENEMY_VALUES["MOVE_SCALE"]) in (event.pos[0], event.pos[1], event.pos[2]) and int(enemies[i]["pos"][1] / ENEMY_VALUES["MOVE_SCALE"]) in (event.pos[3], event.pos[4], event.pos[5]) and enemies[i]["health"] > 0:
                                pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=event.player_damage[0], affector=i))
                if event.type == TAKE_DAMAGE:
                    if event.affector == "player":
                        if not alive or powerup_values["shoestate"]:
                            continue
                        if powerup_values["armor_health"]:
                            if powerup_values["armor_health"] >= event.damage * event.armor_peirce:
                                armor_damage = event.damage * event.armor_peirce
                                health_damage = event.damage * event.peirce
                            else:
                                health_damage = event.damage * event.peirce + (event.damage * event.armor_peirce - powerup_values["armor_health"]) / event.armor_peirce * event.peirce
                                armor_damage = powerup_values["armor_health"]
                        else:
                            health_damage = event.damage
                            armor_damage = 0
                        health_values["health"] -= health_damage
                        powerup_values["armor_health"] -=  armor_damage
                        if health_damage:
                            health_values["health_speed"] = 0
                        for _ in range(int(health_damage / 10)):
                            effects.append(["blood", [player_values["player_pos"][0], player_values["player_pos"][1]], 20, random.random(), random.random()])
                        for _ in range(int(armor_damage / 20)):
                            effects.append(["spark", [player_values["player_pos"][0], player_values["player_pos"][1], random.random() * 2 * pi], 15, random.random() + 0.5])
                    else:
                        for _ in range(int(event.damage / 5)):
                            effects.append(["blood", [enemies[event.affector]["pos"][0] / ENEMY_VALUES["MOVE_SCALE"], enemies[event.affector]["pos"][1] / ENEMY_VALUES["MOVE_SCALE"]], 20, random.random(), random.random()])
                        enemies[event.affector]["health"] -= event.damage
                        if enemies[event.affector]["health"] <= 0:
                            effects.append(["death", [enemies[event.affector]["pos"][0] / ENEMY_VALUES["MOVE_SCALE"], enemies[event.affector]["pos"][1] / ENEMY_VALUES["MOVE_SCALE"]], 64])
                            if enemies[event.affector]["type"] == GAURD and maze[enemies[event.affector]["pos"][0] // ENEMY_VALUES["MOVE_SCALE"], enemies[event.affector]["pos"][1] // ENEMY_VALUES["MOVE_SCALE"]] == -1 and random.random() < 0.5:
                                powerups.append({"type": GUN, "pos": [enemies[event.affector]["pos"][0] // ENEMY_VALUES["MOVE_SCALE"], enemies[event.affector]["pos"][1] // ENEMY_VALUES["MOVE_SCALE"]]})
                                maze[enemies[event.affector]["pos"][0] // ENEMY_VALUES["MOVE_SCALE"], enemies[event.affector]["pos"][1] // ENEMY_VALUES["MOVE_SCALE"]] = GUN
            # ///
            # Paused handling
            if paused:
            # ///
                if not alive:
                    paused = False
                if paused == 1:
                    self.display.blit(paused_surface, (0, 0))
                    paused = 2
                self.display.blit(text_paused, text_paused_rect)
                pygame.draw.rect(self.display, COLOR_D, button_resume, 0, 10)
                self.display.blit(text_resume, text_resume_rect)
                pygame.draw.rect(self.display, COLOR_D, button_menu, 0, 10)
                self.display.blit(text_menu, text_menu_rect)
                pygame.draw.rect(self.display, COLOR_D, button_restart, 0, 10)
                self.display.blit(text_restart, text_restart_rect)
                pygame.draw.rect(self.display, COLOR_D, button_explode, 0, 10)
                self.display.blit(text_explode, text_explode_rect)
                pygame.draw.rect(self.display, COLOR_D, button_quit, 0, 10)
                self.display.blit(text_quit, text_quit_rect)
                if button_resume.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display, COLOR_L, button_resume, 3, 10)
                elif button_menu.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display, COLOR_L, button_menu, 3, 10)
                elif button_restart.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display, COLOR_L, button_restart, 3, 10)
                elif button_explode.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display, COLOR_L, button_explode, 3, 10)
                elif button_quit.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display, COLOR_L, button_quit, 3, 10)
                pygame.display.flip()
                self.clock.tick(FPS)
                continue
            # Player rotation and viewport calculation
            viewport_x = max(0, min(player_values["player_pos"][0] * MAZE_SCALE[0] - viewport_width // 2, self.sizex - viewport_width))
            viewport_y = max(0, min(player_values["player_pos"][1] * MAZE_SCALE[1] - viewport_height // 2, self.sizey - viewport_height))
            viewport_rect = pygame.Rect(viewport_x, viewport_y, viewport_width, viewport_height)
            viewport_player_center = ((player_values["player_center"][0] - viewport_x) * zoom_factor, (player_values["player_center"][1] - viewport_y) * zoom_factor)
            if self.stage == 1:
                player_values["player_pos"][2] = atan2(pygame.mouse.get_pos()[0] - player_values["player_center"][0], pygame.mouse.get_pos()[1] - player_values["player_center"][1])
            else:
                player_values["player_pos"][2] = atan2(pygame.mouse.get_pos()[0] - viewport_player_center[0], pygame.mouse.get_pos()[1] - viewport_player_center[1])
            # ///
            # HUD rendering and death handling
            if health_values["health"] <= 0 and alive:
                alive = False
                effects.append(["death", [player_values["player_pos"][0], player_values["player_pos"][1]], 64])
                print(f"Game lost at level {self.selected_level}")
                self.level_carry_over = self.level_carry_over_reset.copy()
                self.selected_level = max(1, (self.stage - 1) * LEVELS // STAGES - LEVELS // STAGES + 1)
            overlay_surface.fill((0, 0, 0, 0))
            if alive:
                if key[1]:
                    overlay_surface.blit(pygame.transform.scale(self.img_key, (80, 80)), (self.sizex - 180, self.sizey - 150))
                for i in range(4):
                    pygame.draw.rect(overlay_surface, (0, 0, 0, 64), (100 + i * 100, self.sizey - 150, 80, 80))
                    if i == slot:
                        pygame.draw.rect(overlay_surface, (128, 128, 128, 128), (100 + i * 100, self.sizey - 150, 80, 80), 10)
                    if inventory[i]:
                        if inventory[i] == KNIFE and powerup_values["knife_delay"]:
                            pygame.draw.line(overlay_surface, (255, 255, 255), (140 + i * 100, self.sizey - 70), (140 + i * 100, self.sizey - 70 - 80 * powerup_values["knife_delay"] / powerup_values["MAX_KNIFE_DELAY"]), 80)
                        elif inventory[i] == RPG and powerup_values["rpg_delay"]:
                            pygame.draw.line(overlay_surface, (255, 255, 255), (140 + i * 100, self.sizey - 70), (140 + i * 100, self.sizey - 70 - 80 * powerup_values["rpg_delay"] / powerup_values["MAX_RPG_DELAY"]), 80)
                        elif inventory[i] == GUN:
                            pygame.draw.line(overlay_surface, (max(0, min(255, 512 - 512 * powerup_values["gun_ammo"] / powerup_values["MAX_GUN_AMMO"])), min(255, 512 * powerup_values["gun_ammo"] / powerup_values["MAX_GUN_AMMO"]), 0), (90 + i * 100, self.sizey - 70), (90 + i * 100, self.sizey - 70 - 80 * powerup_values["gun_ammo"] / powerup_values["MAX_GUN_AMMO"]), 10)
                        overlay_surface.blit(pygame.transform.scale(self.img_powerups[inventory[i] * -1 - 4], (80, 80)), (100 + i * 100, self.sizey - 150))
                pygame.draw.line(overlay_surface, COLOR_LB, (100, self.sizey - 32), (self.sizex - 100, self.sizey - 32), 32)
                pygame.draw.line(overlay_surface, "red", (100, self.sizey - 36), ((self.sizex - 200) * health_values["health"] / health_values["MAX_HEALTH"] + 100, self.sizey - 36), 24)
                if stamina_values["stamina"] > 0:
                    pygame.draw.line(overlay_surface, (0, 255, 192), (100, self.sizey - 20), ((self.sizex - 200) * stamina_values["stamina"] / stamina_values["MAX_STAMINA"] + 100, self.sizey - 20), 8)
                if powerup_values["armor_health"]:
                    pygame.draw.line(overlay_surface, COLOR_LB, (100, self.sizey - 42), (self.sizex - 100, self.sizey - 42), 12)
                    pygame.draw.line(overlay_surface, "lightgrey", (100, self.sizey - 42), ((self.sizex - 200) * powerup_values["armor_health"] / powerup_values["MAX_ARMOR_HEALTH"] + 100, self.sizey - 42), 12)
                if powerup_values["flashlightstate"]:
                    pygame.draw.line(overlay_surface, COLOR_LB, (100, self.sizey - 12), (self.sizex - 100, self.sizey - 12), 8)
                    pygame.draw.line(overlay_surface, "lightyellow", (100, self.sizey - 12), ((self.sizex - 200) * powerup_values["flashlightstate"] / powerup_values["MAX_FLASHLIGHTSTATE"] + 100, self.sizey - 12), 8)
                if powerup_values["shoestate"]:
                    pygame.draw.line(overlay_surface, COLOR_LB, (100, self.sizey - 12), (self.sizex - 100, self.sizey - 12), 8)
                    pygame.draw.line(overlay_surface, "blue", (100, self.sizey - 12), ((self.sizex - 200) * powerup_values["shoestate"] / powerup_values["MAX_SHOESTATE"] + 100, self.sizey - 12), 8)
                    pygame.draw.line(overlay_surface, "cyan", (100, self.sizey - 32), (self.sizex - 100, self.sizey - 32), 32)
                    effects.append(["run_shoestate", [player_values["player_pos"][0] - player_values["PLAYER_SCALE"] + random.random() - 0.5, player_values["player_pos"][1] - player_values["PLAYER_SCALE"] + random.random() - 0.5], 20])
                    powerup_values["shoestate"] -= 1
                    is_running = True
                    is_sneaking = False
                    stamina_values["stamina"] = stamina_values["MAX_STAMINA"]
                    health_values["health"] = health_values["MAX_HEALTH"]
                if maze[(int(player_values["player_pos"][0]), int(player_values["player_pos"][1]))] > 0:
                    pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=1, peirce=1, armor_peirce=0, affector="player"))
            else:
                dead_timer += 1
                overlay_surface.blit(text_dead, text_dead_rect)
                if dead_timer > 90 and dead_timer // 30 % 2:
                    overlay_surface.blit(text_dead_prompt, text_dead_prompt_rect)
            # ///
            # Player and floor surface rendering
            self.display.blit(floor_surface, (0 ,0))
            if alive:
                if inventory[slot] == CROSSBOW:
                    temp_img = self.img_player_crossbow
                elif inventory[slot] == GUN:  
                    temp_img = self.img_player_gun
                elif inventory[slot] == RPG:  
                    temp_img = self.img_player_rpg
                elif inventory[slot] == FLARE:  
                    temp_img = self.img_player_flare
                elif inventory[slot] :  
                    temp_img = self.img_player_holding
                else:  
                    temp_img = self.img_player
                player_surface = pygame.transform.rotate(pygame.transform.scale(temp_img, (12 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 12 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), player_values["player_pos"][2] * 57.29577 + 180)
                player_rect = player_surface.get_rect(center=(viewport_player_center))
                if powerup_values["armor_health"]:
                    armor_surface = pygame.transform.rotate(pygame.transform.scale(self.img_armor, (6 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 6 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), player_values["player_pos"][2] * 57.29577 + 180)
                    armor_rect = armor_surface.get_rect(center=((player_rect[2] / 2, player_rect[3] / 2)))
                    player_surface.blit(armor_surface, armor_rect)
                if inventory[slot] == CROSSBOW or (inventory[slot] == RPG and not powerup_values["rpg_delay"]):
                    temp = 0
                    if inventory[slot] == CROSSBOW:
                        while temp < self.sizex:
                            if maze[int(player_values["player_pos"][0] + temp * sin(player_values["player_pos"][2])), int(player_values["player_pos"][1] + temp * cos(player_values["player_pos"][2]))] > 0:
                                break
                            temp += 1
                        laser = [player_values["player_pos"][0] + temp * sin(player_values["player_pos"][2]), player_values["player_pos"][1] + temp * cos(player_values["player_pos"][2])]
                        pygame.draw.line(self.display, (255, 64, 64), (player_values["player_pos"][0] * MAZE_SCALE[0], player_values["player_pos"][1] * MAZE_SCALE[1]), (laser[0] * MAZE_SCALE[0], laser[1] * MAZE_SCALE[1]), max(1, int(5 / zoom_factor)))
                    else:
                        while temp < self.sizex:
                            if maze[int(player_values["player_pos"][0] + temp * sin(player_values["player_pos"][2])), int(player_values["player_pos"][1] + temp * cos(player_values["player_pos"][2]))] > 0:
                                break
                            temp += 1
                        laser = [player_values["player_pos"][0] + temp * sin(player_values["player_pos"][2]), player_values["player_pos"][1] + temp * cos(player_values["player_pos"][2])]
                        pygame.draw.line(self.display, (255, 0, 0), (player_values["player_pos"][0] * MAZE_SCALE[0] + sin(player_values["player_pos"][2] - pi / 2) * MAZE_SCALE[0] / 10, player_values["player_pos"][1] * MAZE_SCALE[1] + cos(player_values["player_pos"][2] - pi / 2) * MAZE_SCALE[1] / 10), (laser[0] * MAZE_SCALE[0] + sin(player_values["player_pos"][2] - pi / 2) * MAZE_SCALE[0] / 10, laser[1] * MAZE_SCALE[1] + cos(player_values["player_pos"][2] - pi / 2) * MAZE_SCALE[1] / 10), max(2, int(8 / zoom_factor)))
                if inventory[slot] == KNIFE:
                    if powerup_values["knife_delay"] > powerup_values["MAX_KNIFE_DELAY"] - 8:
                        powerup_surface = pygame.transform.rotate(pygame.transform.scale(self.img_powerups[-inventory[slot] - 4], (3 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 3 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), (player_values["player_pos"][2] + 2 - (powerup_values["knife_delay"] - powerup_values["MAX_KNIFE_DELAY"] + 8) / 2) * 57.29577 + 180)
                    else:
                        powerup_surface = pygame.transform.rotate(pygame.transform.scale(self.img_powerups[-inventory[slot] - 4], (3 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 3 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), player_values["player_pos"][2] * 57.29577 + 90)
                    powerup_rect = powerup_surface.get_rect(center=((player_rect[2] / 2 + sin(player_values["player_pos"][2]) * MAZE_SCALE[0] * zoom_factor / 4, player_rect[3] / 2 + cos(player_values["player_pos"][2]) * MAZE_SCALE[1] * zoom_factor / 4)))
                    player_surface.blit(powerup_surface, powerup_rect)
                elif inventory[slot] == GUN:
                    if powerup_values["gun_delay"]:
                        temp_img = self.img_krinkov[powerup_values["gun_delay"] // 2 + 1]
                    else:
                        temp_img = self.img_krinkov[0]
                    gun_surface = pygame.transform.rotate(pygame.transform.scale(temp_img, (16 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 16 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), player_values["player_pos"][2] * 57.29577 + 180)
                    gun_rect = gun_surface.get_rect(center=((player_rect[2] / 2 + sin(player_values["player_pos"][2] - pi / 5) * MAZE_SCALE[0] * zoom_factor / 4, player_rect[3] / 2 + cos(player_values["player_pos"][2] - pi / 5) * MAZE_SCALE[1] * zoom_factor / 4)))
                    if pygame.mouse.get_pressed()[0] and not powerup_values["gun_delay"] and powerup_values["gun_ammo"]:
                        powerup_values["gun_ammo"] -= 1
                        powerup_values["gun_delay"] = powerup_values["MAX_GUN_DELAY"]
                        active_powerups.append([GUN, [player_values["player_pos"][0] + sin(player_values["player_pos"][2] - pi / 5) / 3.5, player_values["player_pos"][1] + cos(player_values["player_pos"][2] - pi / 5) / 3.5], player_values["player_pos"][2], False])
                        if not powerup_values["gun_ammo"]:
                            inventory[slot] = None
                    player_surface.blit(gun_surface, gun_rect)
                elif inventory[slot] == FLARE:
                    flare_gun_surface = pygame.transform.rotate(pygame.transform.scale(self.img_flare_gun, (2 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 2 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), player_values["player_pos"][2] * 57.29577 + 180)
                    flare_gun_rect = flare_gun_surface.get_rect(center=((player_rect[2] / 2 + sin(player_values["player_pos"][2]) * MAZE_SCALE[1] * zoom_factor / 2.5, player_rect[3] / 2 + cos(player_values["player_pos"][2]) * MAZE_SCALE[1] * zoom_factor / 2.5)))
                    player_surface.blit(flare_gun_surface, flare_gun_rect)
                elif inventory[slot] == RPG:
                    if powerup_values["rpg_delay"] > powerup_values["MAX_RPG_DELAY"] - 3:
                        temp = 2
                    elif powerup_values["rpg_delay"] > powerup_values["MAX_RPG_DELAY"] - 6:
                        temp = 1
                    else:
                        temp = 0
                    rpg_surface = pygame.transform.rotate(pygame.transform.scale(self.img_rpg[temp], (8 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 8 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), player_values["player_pos"][2] * 57.29577 + 180)
                    rpg_rect = rpg_surface.get_rect(center=((player_rect[2] / 2 + sin(player_values["player_pos"][2] - pi / 2) * MAZE_SCALE[1] * zoom_factor / 10, player_rect[3] / 2 + cos(player_values["player_pos"][2] - pi / 2) * MAZE_SCALE[1] * zoom_factor / 10)))
                    player_surface.blit(rpg_surface, rpg_rect)
                elif inventory[slot]:
                    powerup_surface = pygame.transform.rotate(pygame.transform.scale(self.img_powerups[-inventory[slot] - 4], (2 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 2 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), player_values["player_pos"][2] * 57.29577 + 180)
                    powerup_rect = powerup_surface.get_rect(center=((player_rect[2] / 2 + sin(player_values["player_pos"][2]) * MAZE_SCALE[1] * zoom_factor / 3, player_rect[3] / 2 + cos(player_values["player_pos"][2]) * MAZE_SCALE[1] * zoom_factor / 3)))
                    player_surface.blit(powerup_surface, powerup_rect)
                if powerup_values["flashlightstate"]:
                    flashlight_surface = pygame.transform.rotate(pygame.transform.scale(self.img_powerups[0], (2 * player_values["PLAYER_SCALE"] * MAZE_SCALE[0] * zoom_factor, 2 * player_values["PLAYER_SCALE"] * MAZE_SCALE[1] * zoom_factor)), player_values["player_pos"][2] * 57.29577 + 90)
                    flashlight_rect = flashlight_surface.get_rect(center=((player_rect[2] / 2, player_rect[3] / 2)))
                    player_surface.blit(flashlight_surface, flashlight_rect)
                overlay_surface.blit(player_surface, player_rect)
            # ///
            # Active powerup handling
            for powerup in active_powerups:
                if powerup[0] == BOMB:
                    self.display.blit(pygame.transform.scale(self.img_powerups[2], (powerup[2] / powerup_values["MAX_FUSE"] * MAZE_SCALE[0], powerup[2] / powerup_values["MAX_FUSE"] * MAZE_SCALE[1])), ((powerup[1][0] + 0.5 - powerup[2] / powerup_values["MAX_FUSE"] / 2) * MAZE_SCALE[0], (powerup[1][1] + 0.5 - powerup[2] / powerup_values["MAX_FUSE"] / 2) * MAZE_SCALE[1]))
                    powerup[2] -= 1
                    if not powerup[2] % 6:
                        effects.append(["spark", [powerup[1][0] + 0.5, powerup[1][1] + 0.5 - powerup[2] / powerup_values["MAX_FUSE"] / 4, random.random() * 2 * pi], 15, 1])
                    if powerup[2] == 0:
                        for i in range(powerup[1][0] -1, powerup[1][0] + 2):
                            for j in range(powerup[1][1] - 1, powerup[1][1] + 2):
                                for _ in range(5):
                                    effects.append(["big_smoke", [i + random.random() , j + random.random()], 33, CROSSBOW, 0.01 * (random.random() - 0.5)])
                                pygame.event.post(pygame.event.Event(ENTITY_DAMAGE_CHECK, pos=[i, j], player_damage=[60, 0.3, 0.5], origin=BOMB))
                                if maze[(i, j)] in (3, 4):
                                    rect_fill = (i * MAZE_SCALE[0], j * MAZE_SCALE[1], MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)
                                    maze_surface.fill((0, 0, 0, 0), rect_fill)
                                    if maze[(i, j)] == 3:
                                        floor_surface.blit(pygame.transform.scale(self.img_broken[self.stage - 1], (rect_fill[2], rect_fill[3])), (rect_fill[0], rect_fill[1]))
                                    maze[(i, j)] = -1
                                elif maze[(i, j)] in (BOMB, MEGA_BOMB):
                                    maze[(i, j)] = -1
                                    for inactive_powerup in powerups:
                                        if inactive_powerup["type"] == BOMB and inactive_powerup["pos"] == (i, j):
                                            active_powerups.append([BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"]])
                                            powerups.remove(inactive_powerup)
                                            break
                                        elif inactive_powerup["type"] == MEGA_BOMB and inactive_powerup["pos"] == (i, j):
                                            active_powerups.append([MEGA_BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"] * 2])
                                            powerups.remove(inactive_powerup)
                                            break
                        effects.append(["bomb", [int(powerup[1][0]), int(powerup[1][1])], 30])
                        active_powerups.remove(powerup)
                elif powerup[0] == MEGA_BOMB:
                    self.display.blit(pygame.transform.scale(self.img_powerups[6], (powerup[2] / powerup_values["MAX_FUSE"] / 2 * MAZE_SCALE[0], powerup[2] / powerup_values["MAX_FUSE"] / 2 * MAZE_SCALE[1])), ((powerup[1][0] + 0.5 - powerup[2] / powerup_values["MAX_FUSE"] / 4)* MAZE_SCALE[0], (powerup[1][1] + 0.5 - powerup[2] / powerup_values["MAX_FUSE"] / 4) * MAZE_SCALE[1]))
                    powerup[2] -= 1
                    if not powerup[2] % 4:
                        effects.append(["spark", [powerup[1][0] + 0.5, powerup[1][1] + 0.5 - powerup[2] / powerup_values["MAX_FUSE"] / 4, random.random() * 2 * pi], 15, 1.5])
                    if powerup[2] <= 0:
                        for i in range(16):
                            active_powerups.append([CROSSBOW, [powerup[1][0] + 0.5, powerup[1][1] + 0.5], pi * i / 8, True, powerup_values["MAX_FUSE"] * 2, random.random() + 0.5])
                        for i, x in zip(range(powerup[1][0] - 2, powerup[1][0] + 3), range(5)):
                            for j, y in zip(range(powerup[1][1] - 2, powerup[1][1] + 3), range(5)):
                                if x not in (1, 4) or y not in (1, 4):
                                    for _ in range(5):
                                        effects.append(["big_smoke", [i + random.random() , j + random.random()], 33, CROSSBOW, 0.01 * (random.random() - 0.5)])
                                if x in (1, 2, 3) and y in (1, 2, 3):
                                    pygame.event.post(pygame.event.Event(ENTITY_DAMAGE_CHECK, pos=[i, j], player_damage=[100, 1, 1], origin=BOMB))
                                else:
                                    pygame.event.post(pygame.event.Event(ENTITY_DAMAGE_CHECK, pos=[i, j], player_damage=[60, 0.3, 0.5], origin=BOMB))
                                if i >= 0 and i < maze_size[0] and j >= 0 and j < maze_size[1]:
                                    if maze[(i, j)] in (3, 4) or ((maze[(i, j)] > 0 or maze[(i, j)] == -2) and x in (1, 2, 3) and y in (1, 2, 3) and (i > 0 and i < maze_size[0] - 1 and j > 0 and j < maze_size[1] - 1)):
                                        rect_fill = (i * MAZE_SCALE[0], j * MAZE_SCALE[1], MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)
                                        maze_surface.fill((0, 0, 0, 0), rect_fill)
                                        if maze[(i, j)] == 3 and (x in (0, 4) or y in (0, 4)):
                                            floor_surface.blit(pygame.transform.scale(self.img_broken[self.stage - 1], (rect_fill[2], rect_fill[3])), (rect_fill[0], rect_fill[1]))
                                        maze[(i, j)] = -1
                                    elif maze[(i, j)] in (BOMB, MEGA_BOMB):
                                        maze[(i, j)] = -1
                                        for inactive_powerup in powerups:
                                            if inactive_powerup["type"] == BOMB and inactive_powerup["pos"] == (i, j):
                                                active_powerups.append([BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"]])
                                                powerups.remove(inactive_powerup)
                                                break
                                            elif inactive_powerup["type"] == MEGA_BOMB and inactive_powerup["pos"] == (i, j):
                                                active_powerups.append([MEGA_BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"] * 2])
                                                powerups.remove(inactive_powerup)
                                                break
                        if random.random() < 0.10:
                            active_powerups.append([BOMB, powerup[1], powerup_values["MAX_FUSE"]])
                        effects.append(["mega_bomb", [int(powerup[1][0]), int(powerup[1][1])], 45])
                        active_powerups.remove(powerup)
                elif powerup[0] == RPG:
                    rpg = pygame.transform.rotate(pygame.transform.scale(self.img_nuke[frame_index // 2 % 5], MAZE_SCALE), powerup[2] * 57.29577 + 180)
                    effects.append(["big_smoke", [powerup[1][0], powerup[1][1]], 33, CROSSBOW, random.random() * 0.05 - 0.025])
                    powerup[1][0] += sin(powerup[2]) * 0.1
                    powerup[1][1] += cos(powerup[2]) * 0.1
                    rpg_rect = rpg.get_rect(center=(powerup[1][0] * MAZE_SCALE[0], powerup[1][1] * MAZE_SCALE[1]))
                    self.display.blit(rpg, rpg_rect)
                    powerup[3] -= 1
                    for i in range(len(enemies)):
                        if rpg_rect.collidepoint(enemies[i]["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[0], enemies[i]["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[1]) and enemies[i]["health"] > 0:
                            powerup[3] = 0
                            break
                    if maze[int(powerup[1][0] + sin(powerup[2]) * 0.1), int(powerup[1][1] + cos(powerup[2]) * 0.1)] > 0 or not powerup[3] or maze[(int(powerup[1][0]), int(powerup[1][1]))] in (BOMB, MEGA_BOMB):
                        for i, x in zip(range(int(powerup[1][0]) - 3, int(powerup[1][0]) + 4), range(7)):
                            for j, y in zip(range(int(powerup[1][1]) - 3, int(powerup[1][1]) + 4), range(7)):
                                if x not in (0, 6) or y not in (0, 6):
                                    for _ in range(5):
                                        effects.append(["big_smoke", [i + random.random() , j + random.random()], 33, CROSSBOW, 0.01 * (random.random() - 0.5)])
                                if x in (1, 2, 3, 4, 5) and y in (1, 2, 3, 4, 5):
                                    pygame.event.post(pygame.event.Event(ENTITY_DAMAGE_CHECK, pos=[i, j], player_damage=[100, 1, 1], origin=BOMB))
                                else:
                                    pygame.event.post(pygame.event.Event(ENTITY_DAMAGE_CHECK, pos=[i, j], player_damage=[60, 0.3, 0.5], origin=BOMB))
                                if i >= 0 and i < maze_size[0] and j >= 0 and j < maze_size[1]:
                                    if maze[(i, j)] in (3, 4) or ((maze[(i, j)] > 0 or maze[(i, j)] == -2) and x in (1, 2, 3, 4, 5) and y in (1, 2, 3, 4, 5) and (i > 0 and i < maze_size[0] - 1 and j > 0 and j < maze_size[1] - 1)):
                                        rect_fill = (i * MAZE_SCALE[0], j * MAZE_SCALE[1], MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)
                                        maze_surface.fill((0, 0, 0, 0), rect_fill)
                                        if maze[(i, j)] == 3 and (x in (0, 6) or y in (0, 6)):
                                            floor_surface.blit(pygame.transform.scale(self.img_broken[self.stage - 1], (rect_fill[2], rect_fill[3])), (rect_fill[0], rect_fill[1]))
                                        maze[(i, j)] = -1
                                    elif maze[(i, j)] in (BOMB, MEGA_BOMB):
                                        maze[(i, j)] = -1
                                        for inactive_powerup in powerups:
                                            if inactive_powerup["type"] == BOMB and inactive_powerup["pos"] == (i, j):
                                                active_powerups.append([BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"]])
                                                powerups.remove(inactive_powerup)
                                                break
                                            elif inactive_powerup["type"] == MEGA_BOMB and inactive_powerup["pos"] == (i, j):
                                                active_powerups.append([MEGA_BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"] * 2])
                                                powerups.remove(inactive_powerup)
                                                break
                        effects.append(["nuke", [int(powerup[1][0]), int(powerup[1][1])], 45])
                        active_powerups.remove(powerup)
                    elif powerup[1][0] < 0 or powerup[1][0] >= maze_size[0] or powerup[1][1] < 0 or powerup[1][1] >= maze_size[1]:
                        active_powerups.remove(powerup)
                elif powerup[0] == CROSSBOW:
                    if powerup[3]:
                        rocket = pygame.transform.rotate(pygame.transform.scale(self.img_mini_bomb, (MAZE_SCALE[0] / 3, MAZE_SCALE[1] / 3)), frame_index * powerup[5] * 20 + powerup[2] * 57.29577 + 180)
                        powerup[1][0] += sin(powerup[2]) * 0.2
                        powerup[1][1] += cos(powerup[2]) * 0.2
                    else:
                        rocket = pygame.transform.rotate(pygame.transform.scale(self.img_rocket[frame_index // 2 % 4], MAZE_SCALE), powerup[2] * 57.29577 + 180)
                        effects.append(["big_smoke", [powerup[1][0], powerup[1][1]], 33, CROSSBOW, random.random() * 0.05 - 0.025])
                        powerup[1][0] += sin(powerup[2]) * 0.3
                        powerup[1][1] += cos(powerup[2]) * 0.3
                    rocket_rect = rocket.get_rect(center=(powerup[1][0] * MAZE_SCALE[0], powerup[1][1] * MAZE_SCALE[1]))
                    self.display.blit(rocket, rocket_rect)
                    powerup[4] -= 1
                    for i in range(len(enemies)):
                        if rocket_rect.collidepoint(enemies[i]["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[0], enemies[i]["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[1]) and enemies[i]["health"] > 0:
                            powerup[4] = 0
                            break
                    if rocket_rect.collidepoint(player_values["player_center"]) and powerup[3]:
                        powerup[4] = 0
                    if maze[int(powerup[1][0]), int(powerup[1][1])] > 0 or not powerup[4]:
                        if maze[int(powerup[1][0]), int(powerup[1][1])] in (3, 4):
                            rect_fill = (int(powerup[1][0]) * MAZE_SCALE[0], int(powerup[1][1]) * MAZE_SCALE[1], MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)
                            maze_surface.fill((0, 0, 0, 0), rect_fill)
                            if maze[(int(powerup[1][0]), int(powerup[1][1]))] == 3:
                                floor_surface.blit(pygame.transform.scale(self.img_broken[self.stage - 1], (rect_fill[2], rect_fill[3])), (rect_fill[0], rect_fill[1]))
                            maze[int(powerup[1][0]), int(powerup[1][1])] = -1
                        pygame.event.post(pygame.event.Event(ENTITY_DAMAGE_CHECK, pos=[int(powerup[1][0] - sin(powerup[2]) * 0.45), int(powerup[1][0]), int(powerup[1][0] + sin(powerup[2]) * 0.45), int(powerup[1][1] - cos(powerup[2]) * 0.45), int(powerup[1][1]), int(powerup[1][1] + cos(powerup[2]) * 0.45)], player_damage=[60, 0.3, 0.5], origin=CROSSBOW))
                        effects.append(["rocket", [int(powerup[1][0]), int(powerup[1][1])], 30])
                        active_powerups.remove(powerup)
                    elif maze[(int(powerup[1][0]), int(powerup[1][1]))] in (BOMB, MEGA_BOMB):
                        for inactive_powerup in powerups:
                            if inactive_powerup["type"] == BOMB and inactive_powerup["pos"] == (int(powerup[1][0]), int(powerup[1][1])):
                                active_powerups.append([BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"]])
                                powerups.remove(inactive_powerup)
                                break
                            elif inactive_powerup["type"] == MEGA_BOMB and inactive_powerup["pos"] == (int(powerup[1][0]), int(powerup[1][1])):
                                active_powerups.append([MEGA_BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"] * 2])
                                powerups.remove(inactive_powerup)
                                break
                        effects.append(["rocket", [int(powerup[1][0]), int(powerup[1][1])], 30])
                        active_powerups.remove(powerup)
                    elif powerup[1][0] < 0 or powerup[1][0] >= maze_size[0] or powerup[1][1] < 0 or powerup[1][1] >= maze_size[1]:
                        active_powerups.remove(powerup)
                elif powerup[0] == GUN:
                    hitbox_rect = pygame.rect.Rect((powerup[1][0] - 0.5) * MAZE_SCALE[0], (powerup[1][1] - 0.5) * MAZE_SCALE[1], MAZE_SCALE[0], MAZE_SCALE[1])
                    pygame.draw.line(self.display, (255, 255, 162), (powerup[1][0] * MAZE_SCALE[0], powerup[1][1] * MAZE_SCALE[1]), ((powerup[1][0] + sin(powerup[2]) * 0.6) * MAZE_SCALE[0], (powerup[1][1] + cos(powerup[2]) * 0.6) * MAZE_SCALE[1]), max(1, int(MAZE_SCALE[0] / 20)))
                    pygame.draw.line(self.display, "yellow", ((powerup[1][0] + sin(powerup[2]) * 0.2) * MAZE_SCALE[0], (powerup[1][1] + cos(powerup[2]) * 0.2) * MAZE_SCALE[1]), ((powerup[1][0] + sin(powerup[2]) * 0.6) * MAZE_SCALE[0], (powerup[1][1] + cos(powerup[2]) * 0.6) * MAZE_SCALE[1]), max(1, int(MAZE_SCALE[0] / 20)))
                    pygame.draw.circle(self.display, "orange", ((powerup[1][0] + sin(powerup[2]) * 0.6) * MAZE_SCALE[0], (powerup[1][1] + cos(powerup[2]) * 0.6) * MAZE_SCALE[1]), max(1, MAZE_SCALE[0] // 20))
                    for _ in range(3):
                        powerup[1][0] += sin(powerup[2]) * 0.2
                        powerup[1][1] += cos(powerup[2]) * 0.2
                        if hitbox_rect.collidepoint(player_values["player_center"]) and powerup[3] and alive:
                            pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=20, peirce=0.5, armor_peirce=1, affector="player"))
                            powerup[1][0] = -1
                        for i in range(len(enemies)):
                            if hitbox_rect.collidepoint(enemies[i]["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[0], enemies[i]["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[1]) and enemies[i]["health"] > 0 and (enemies[i]["type"] != GAURD or not powerup[3]):
                                pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=20, affector=i))
                                powerup[1][0] = -1
                        if powerup[1][0] < 0 or powerup[1][0] >= maze_size[0] or powerup[1][1] < 0 or powerup[1][1] >= maze_size[1]:
                            active_powerups.remove(powerup)
                            break
                        elif maze[int(powerup[1][0]), int(powerup[1][1])] > 0:
                            if maze[int(powerup[1][0]), int(powerup[1][1])] == 4:
                                maze[int(powerup[1][0]), int(powerup[1][1])] = -1
                                rect_fill = (int(powerup[1][0]) * MAZE_SCALE[0], int(powerup[1][1]) * MAZE_SCALE[1], MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)
                                maze_surface.fill((0, 0, 0, 0), rect_fill)
                            effects.append(["spark", [powerup[1][0], powerup[1][1], powerup[2]], 15, random.random() + 0.5])
                            active_powerups.remove(powerup)
                            break
                        elif maze[(int(powerup[1][0]), int(powerup[1][1]))] in (BOMB, MEGA_BOMB):
                            for inactive_powerup in powerups:
                                if inactive_powerup["type"] == BOMB and inactive_powerup["pos"] == (int(powerup[1][0]), int(powerup[1][1])):
                                    active_powerups.append([BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"]])
                                    powerups.remove(inactive_powerup)
                                    break
                                elif inactive_powerup["type"] == MEGA_BOMB and inactive_powerup["pos"] == (int(powerup[1][0]), int(powerup[1][1])):
                                    active_powerups.append([MEGA_BOMB, inactive_powerup["pos"], powerup_values["MAX_FUSE"] * 2])
                                    powerups.remove(inactive_powerup)
                                    break
                            active_powerups.remove(powerup)
                            break
            # ///
            # Enemy handling
            player_hitbox_rect = pygame.rect.Rect(player_values["player_center"][0] - player_values["PLAYER_SCALE"] * MAZE_SCALE[0], player_values["player_center"][1] - player_values["PLAYER_SCALE"] * MAZE_SCALE[1], MAZE_SCALE[0] * player_values["PLAYER_SCALE"] * 2, MAZE_SCALE[1] * player_values["PLAYER_SCALE"] * 2)
            for enemy in enemies:
                enemy["pos"][3] = (4 - enemy["pos"][2]) % 4 * 90
                enemy["player_angle"] = atan2(player_values["player_pos"][0] - enemy["pos"][0] / ENEMY_VALUES["MOVE_SCALE"],  player_values["player_pos"][1] - enemy["pos"][1] / ENEMY_VALUES["MOVE_SCALE"])
                if enemy["player_detected"]:
                    enemy["player_detected"] -= 1
                if not frame_index * 5 % FPS and 10 > player_values["player_pos"][0] - enemy["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] > -10 and 10 > player_values["player_pos"][1] - enemy["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] > -10 and alive:
                    for i in range(30):
                        point_of_sight = [(enemy["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] + sin(enemy["player_angle"]) * i / 3) * MAZE_SCALE[0],(enemy["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] + cos(enemy["player_angle"]) * i / 3) * MAZE_SCALE[1]]
                        if maze[(int(point_of_sight[0] / MAZE_SCALE[0]), int(point_of_sight[1] / MAZE_SCALE[1]))] in (1, 2, 3, -2):
                            break
                        elif player_hitbox_rect.collidepoint(point_of_sight):
                            enemy["player_detected"] = 10
                            player_distance = round(i / 3)
                if enemy["type"] == GAURD and enemy["health"] > 0:
                    if enemy["player_detected"] > 1:
                        enemy["pos"][3] = enemy["player_angle"] * 57.29577 + 180
                        gaurd = pygame.transform.rotate(pygame.transform.scale(self.img_gaurd_firing, (3 * MAZE_SCALE[0], 3 * MAZE_SCALE[1])), enemy["pos"][3])
                        if enemy["attack_delay"] == 0:
                            enemy["attack_delay"] = max(3, (6 - player_distance // 2)) * -powerup_values["MAX_GUN_DELAY"]
                        if not enemy["attack_delay"] % powerup_values["MAX_GUN_DELAY"] and enemy["attack_delay"] < 0:
                            active_powerups.append([GUN, [enemy["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] + sin((enemy["pos"][3] + 170) / 57.29577) / 2, enemy["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] + cos((enemy["pos"][3] + 170) / 57.29577) / 2], enemy["player_angle"] + random.randint(-10, 10) / 70, True])
                            enemy["gunshot_timer"] = frame_index
                        if enemy["attack_delay"] < 0:
                            enemy["attack_delay"] += 1
                            if enemy["attack_delay"] == 0:
                                enemy["attack_delay"] = 30
                        else:
                            enemy["attack_delay"] -= 1
                    else:
                        gaurd = pygame.transform.rotate(pygame.transform.scale(self.img_gaurd, (3 * MAZE_SCALE[0], 3 * MAZE_SCALE[1])), enemy["pos"][3])
                        if enemy["attack_delay"] > 10:
                            enemy["attack_delay"] -= 1
                        elif enemy["attack_delay"] < 10:
                            enemy["attack_delay"] += 1
                        move_locations = ((enemy["pos"][0], enemy["pos"][1] - ENEMY_VALUES["MOVE_SCALE"]), (enemy["pos"][0] + ENEMY_VALUES["MOVE_SCALE"], enemy["pos"][1]), (enemy["pos"][0], enemy["pos"][1] + ENEMY_VALUES["MOVE_SCALE"]), (enemy["pos"][0] - ENEMY_VALUES["MOVE_SCALE"], enemy["pos"][1]))
                        if enemy["pos"][0] % ENEMY_VALUES["MOVE_SCALE"] != ENEMY_VALUES["MOVE_SCALE"] // 2:
                            enemy["pos"][0] += (2 - enemy["pos"][2]) * ENEMY_VALUES["SPEED"][enemy["type"]]
                        elif enemy["pos"][1] % ENEMY_VALUES["MOVE_SCALE"] != ENEMY_VALUES["MOVE_SCALE"] // 2:
                            enemy["pos"][1] += (enemy["pos"][2] % 4 - 1) * ENEMY_VALUES["SPEED"][enemy["type"]]
                        else:
                            directions = []
                            for x, i in zip(move_locations, range(4)):
                                if i != (enemy["pos"][2] - 2) % 4 and maze[int(x[0] / ENEMY_VALUES["MOVE_SCALE"]), int(x[1] / ENEMY_VALUES["MOVE_SCALE"])] < 1 and x[0] / ENEMY_VALUES["MOVE_SCALE"] > maze_size[0] / 3:
                                    directions.append(i)
                            if directions:
                                if enemy["player_detected"] and int((3 - enemy["player_angle"] + pi / 4) / pi * 2) % 4 in directions + [(enemy["pos"][2] - 2) % 4]:
                                    enemy["pos"][2] = int((3 - enemy["player_angle"] + pi / 4) / pi * 2) % 4
                                else:
                                    enemy["pos"][2] = random.choice(directions) % 4
                                enemy["pos"][0] += enemy["pos"][2] % 2 * (1 - 2 * int(enemy["pos"][2] / 2)) * ENEMY_VALUES["SPEED"][enemy["type"]]
                                enemy["pos"][1] += (enemy["pos"][2] + 1) % 2 * (-1 + 2 * int(enemy["pos"][2] / 2)) * ENEMY_VALUES["SPEED"][enemy["type"]]
                            else:
                                enemy["pos"][2] = (enemy["pos"][2] + 2) % 4
                    gaurd_rect = gaurd.get_rect(center=(enemy["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[0], enemy["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[1]))
                    if enemy["player_detected"]:
                        gun_surface = pygame.transform.rotate(pygame.transform.scale(self.img_krinkov[max(0, enemy["gunshot_timer"] + 3 - frame_index)], [MAZE_SCALE[0] * 3, MAZE_SCALE[1] * 3]), enemy["pos"][3])
                        gun_rect = gun_surface.get_rect(center=(gaurd_rect[2] / 2 + sin((enemy["pos"][3] + 170) / 57.29577) * MAZE_SCALE[0] / 1.5, gaurd_rect[3] / 2 + cos((enemy["pos"][3] + 170) / 57.29577) * MAZE_SCALE[1] / 1.5))
                    else:
                        gun_surface = pygame.transform.rotate(pygame.transform.scale(self.img_krinkov[0], [MAZE_SCALE[0] * 3, MAZE_SCALE[1] * 3]), enemy["pos"][3] + 90)
                        gun_rect = gun_surface.get_rect(center=(gaurd_rect[2] / 2 + sin((enemy["pos"][3] + 180) / 57.29577) * MAZE_SCALE[0] / 3, gaurd_rect[3] / 2 + cos((enemy["pos"][3] + 180) / 57.29577) * MAZE_SCALE[1] / 3))
                    gaurd.blit(gun_surface, gun_rect)
                    self.display.blit(gaurd, gaurd_rect)
                elif enemy["type"] == SPIDER and enemy["health"] > 0:
                    if enemy["player_detected"]:
                        enemy["stamina"] = ENEMY_VALUES["STAMINA"][SPIDER]
                    if enemy["moving"]:
                        img_spider_index = int((frame_index // 2) % 5) + 1
                    else:
                        img_spider_index = 0
                    spider = pygame.transform.rotate(pygame.transform.scale(self.img_spider[img_spider_index], MAZE_SCALE), enemy["pos"][3])
                    spider_rect = spider.get_rect(center=(enemy["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[0], enemy["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] * MAZE_SCALE[1]))
                    spider_bite = pygame.transform.rotate(pygame.transform.scale(self.img_spider_bite[min(5, 16 - enemy["attack_delay"])], (MAZE_SCALE[0] / 2, MAZE_SCALE[1] / 2)), enemy["pos"][3])
                    spider_bite_rect = spider_bite.get_rect(center=((enemy["pos"][0] / ENEMY_VALUES["MOVE_SCALE"] - sin((4 - enemy["pos"][2]) % 4 * pi / 2) / 3) * MAZE_SCALE[0], (enemy["pos"][1] / ENEMY_VALUES["MOVE_SCALE"] - cos((4 - enemy["pos"][2]) % 4 * pi / 2) / 3) * MAZE_SCALE[1]))
                    if spider_bite_rect.colliderect(player_hitbox_rect) and not enemy["attack_delay"] and alive:
                        enemy["attack_delay"] = 20
                    if enemy["attack_delay"]:
                        enemy["moving"] = 0
                        spider = pygame.transform.rotate(pygame.transform.scale(self.img_spider[0], MAZE_SCALE), enemy["pos"][3])
                        enemy["attack_delay"] -= 1
                        if enemy["attack_delay"] == 16 and spider_bite_rect.colliderect(player_hitbox_rect):
                            pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=30, peirce=0.1, armor_peirce=0.5, affector="player"))
                        self.display.blit(spider_bite, spider_bite_rect)
                        if not enemy["attack_delay"] and not spider_bite_rect.colliderect(player_hitbox_rect):
                            enemy["moving"] = 1
                            enemy["stamina"] = ENEMY_VALUES["STAMINA"][SPIDER]
                    if enemy["stamina"] and enemy["moving"]:
                        enemy["stamina"] -= 1
                        if not enemy["stamina"]:
                            enemy["moving"] = 0
                        if enemy["pos"][0] % ENEMY_VALUES["MOVE_SCALE"] != ENEMY_VALUES["MOVE_SCALE"] / 2:
                            enemy["pos"][0] += (2 - enemy["pos"][2]) * ENEMY_VALUES["SPEED"][enemy["type"]]
                        elif enemy["pos"][1] % ENEMY_VALUES["MOVE_SCALE"] != ENEMY_VALUES["MOVE_SCALE"] / 2:
                            enemy["pos"][1] += (enemy["pos"][2] % 4 - 1) * ENEMY_VALUES["SPEED"][enemy["type"]]
                        else:
                            move_locations = ((enemy["pos"][0], enemy["pos"][1] - ENEMY_VALUES["MOVE_SCALE"]), (enemy["pos"][0] + ENEMY_VALUES["MOVE_SCALE"], enemy["pos"][1]), (enemy["pos"][0], enemy["pos"][1] + ENEMY_VALUES["MOVE_SCALE"]), (enemy["pos"][0] - ENEMY_VALUES["MOVE_SCALE"], enemy["pos"][1]))
                            directions = []
                            for x, i in zip(move_locations, range(4)):
                                if i != (enemy["pos"][2] - 2) % 4 and maze[int(x[0] / ENEMY_VALUES["MOVE_SCALE"]), int(x[1] / ENEMY_VALUES["MOVE_SCALE"])] < 1:
                                    directions.append(i)
                            if directions:
                                if enemy["player_detected"] and int((3 - enemy["player_angle"] + pi / 4) / pi * 2) % 4 in directions + [(enemy["pos"][2] - 2) % 4]:
                                    enemy["pos"][2] = int((3 - enemy["player_angle"] + pi / 4) / pi * 2) % 4
                                else:
                                    enemy["pos"][2] = random.choice(directions) % 4
                                enemy["pos"][0] += enemy["pos"][2] % 2 * (1 - 2 * int(enemy["pos"][2] / 2)) * ENEMY_VALUES["SPEED"][enemy["type"]]
                                enemy["pos"][1] += (enemy["pos"][2] + 1) % 2 * (-1 + 2 * int(enemy["pos"][2] / 2)) * ENEMY_VALUES["SPEED"][enemy["type"]]
                            else:
                                enemy["pos"][2] = (enemy["pos"][2] + 2) % 4
                    elif not spider_bite_rect.colliderect(player_hitbox_rect):
                        enemy["stamina"] += 1
                        enemy["moving"] = int(random.random() + (enemy["stamina"] - 10) / ENEMY_VALUES["STAMINA"][SPIDER])
                    self.display.blit(spider, spider_rect)
            # ///
            # Animated textures and maze surface blitting
            for ghost_wall in anim_ghost_walls:
                maze_surface.blit(pygame.transform.scale(self.img_ghost_wall[self.stage - 1][int(frame_index / 20 + ghost_wall[1]) % 5], (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (ghost_wall[0][0] * MAZE_SCALE[0], ghost_wall[0][1] * MAZE_SCALE[1]))
            for firewall in anim_firewalls:
                maze_surface.blit(pygame.transform.scale(self.img_firewall[self.stage - 1][int(frame_index / 20 + firewall[1]) % 3], (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (firewall[0][0] * MAZE_SCALE[0], firewall[0][1] * MAZE_SCALE[1]))
            self.display.blit(maze_surface, (0 ,0))
            # ///
            # Effect blitting
            for effect in effects:
                if effect[0] == "spark":
                    self.display.blit(pygame.transform.scale(self.img_bullet_effect[3 - effect[2] // 5], (MAZE_SCALE[0] / 10 + 1, MAZE_SCALE[1] / 10 + 1)), ((effect[1][0] - 0.05) * MAZE_SCALE[0], (effect[1][1] - 0.05) * MAZE_SCALE[1]))
                    effect[2] -= 1
                    effect[1][0] += sin(effect[1][2]) * 0.01
                    effect[1][1] -= 0.02 * effect[3]
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "run_shoestate":
                    self.display.blit(pygame.transform.scale(self.img_run_shoestate[5 - int(effect[2] / 4 + 0.8)], (MAZE_SCALE[0], MAZE_SCALE[1] / 2)), ((effect[1][0] - 0.05) * MAZE_SCALE[0], (effect[1][1] - 0.05) * MAZE_SCALE[1]))
                    effect[2] -= 1
                    effect[1][1] - 0.1
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "run_dust":
                    self.display.blit(pygame.transform.flip(pygame.transform.scale(self.img_run_dust[7 - int(effect[2] / 2 + 0.5)], (MAZE_SCALE[0] / 2 + 1, MAZE_SCALE[1] / 2 + 1)), 1 - int(effect[1][2] / 2), 0), ((effect[1][0] - 0.05) * MAZE_SCALE[0], (effect[1][1] - 0.05) * MAZE_SCALE[1]))
                    effect[2] -= 1
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "big_smoke":
                    if effect[3] == FLARE:
                        big_smoke_img = pygame.transform.scale(self.img_big_smoke[ceil(effect[2] / powerup_values["MAX_FLARESTATE"] * 22) - 1], MAZE_SCALE)
                    elif effect[3] == CROSSBOW:
                        big_smoke_img = pygame.transform.scale(self.img_big_smoke[11 - ceil(effect[2] / 3)], (MAZE_SCALE[0] / 2, MAZE_SCALE[1] / 2))
                    big_smoke_rect = big_smoke_img.get_rect(center=(effect[1][0] * MAZE_SCALE[0], effect[1][1] * MAZE_SCALE[1]))
                    self.display.blit(big_smoke_img, big_smoke_rect)
                    effect[2] -= 1
                    effect[1][0] += effect[4]
                    effect[1][1] -= 0.01
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "flare":
                    effect[2] -=1
                    if effect[2] / powerup_values["MAX_FLARESTATE"] > 0.85:
                        effect[1][1] -= 0.1
                    else:
                        effect[1][1] += 0.01
                    flare_img = pygame.transform.scale(self.img_flare[effect[2] // 6 % 2], (MAZE_SCALE[0] * 2 * effect[2] / powerup_values["MAX_FLARESTATE"], MAZE_SCALE[1] * 2 * effect[2] / powerup_values["MAX_FLARESTATE"]))
                    flare_rect = flare_img.get_rect(center=(effect[1][0] * MAZE_SCALE[0], effect[1][1] * MAZE_SCALE[1]))
                    self.display.blit(flare_img, flare_rect)
                    if not effect[2] % 15:
                        effects.append(["big_smoke", [effect[1][0], effect[1][1]], powerup_values["MAX_FLARESTATE"] / 2, FLARE, random.random() * 0.02 - 0.01])
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "rocket":
                    self.display.blit(pygame.transform.scale(self.img_rocket_effect[2 - effect[2] // 10], (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (effect[1][0] * MAZE_SCALE[0], effect[1][1] * MAZE_SCALE[1]))
                    effect[2] -= 1
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "bomb":
                    self.display.blit(pygame.transform.scale(self.img_bomb_effect[2 - effect[2] // 10], (MAZE_SCALE[0] * 3 + 1, MAZE_SCALE[1] * 3 + 1)), ((effect[1][0] - 1) * MAZE_SCALE[0], (effect[1][1] - 1) * MAZE_SCALE[1]))
                    effect[2] -= 1
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "mega_bomb":
                    self.display.blit(pygame.transform.scale(self.img_mega_bomb_effect[2 - effect[2] // 15], (MAZE_SCALE[0]  * 5 + 1, MAZE_SCALE[1] * 5 + 1)), ((effect[1][0] - 2)* MAZE_SCALE[0], (effect[1][1] - 2) * MAZE_SCALE[1]))
                    effect[2] -= 1
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "nuke":
                    self.display.blit(pygame.transform.scale(self.img_nuke_effect[2 - effect[2] // 15], (MAZE_SCALE[0] * 9 + 1, MAZE_SCALE[1] * 9 + 1)), ((effect[1][0] - 4)* MAZE_SCALE[0], (effect[1][1] - 4) * MAZE_SCALE[1]))
                    effect[2] -= 1
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "sweep":
                    sweep_img = pygame.transform.rotate(pygame.transform.scale(self.img_sweep[8 - effect[2]], (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), effect[1][2] * 57.29577 + 180)
                    sweep_rect = sweep_img.get_rect(center=((effect[1][0] + 0.5 * sin(effect[1][2])) * MAZE_SCALE[0], (effect[1][1] + 0.5 * cos(effect[1][2])) * MAZE_SCALE[1]))
                    self.display.blit(sweep_img, sweep_rect)
                    effect[2] -= 1
                    if effect[2] == 0:
                        effects.remove(effect) 
                elif effect[0] == "blood":
                    blood_img = pygame.transform.scale(self.img_blood[int(effect[4] * 3)], (MAZE_SCALE[0] / 2, MAZE_SCALE[1] / 2))
                    blood_rect = blood_img.get_rect(center=(effect[1][0] * MAZE_SCALE[0], effect[1][1] * MAZE_SCALE[1]))
                    self.display.blit(blood_img, blood_rect)
                    effect[2] -= 1
                    effect[1][0] += effect[3] / 10 - 0.05
                    effect[1][1] -= effect[4] * (effect[2] - 15) / 100
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "health":
                    health_img = pygame.transform.scale(self.img_health_particle, (MAZE_SCALE[0] / 3, MAZE_SCALE[1] / 3))
                    health_rect = health_img.get_rect(center=(effect[1][0] * MAZE_SCALE[0], effect[1][1] * MAZE_SCALE[1]))
                    self.display.blit(health_img, health_rect)
                    effect[2] -= 1
                    effect[1][1] -= 0.01
                    if effect[2] == 0:
                        effects.remove(effect)
                elif effect[0] == "death":
                    effect[2] -= 1
                    death_img = pygame.transform.scale(self.img_death[int(effect[2] / 8)], (MAZE_SCALE[0] / 2, MAZE_SCALE[1] / 2))
                    death_rect = death_img.get_rect(center=(effect[1][0] * MAZE_SCALE[0], effect[1][1] * MAZE_SCALE[1]))
                    self.display.blit(death_img, death_rect)
                    effect[1][1] -= 0.01
                    if effect[2] == 0:
                        effects.remove(effect)
            # ///
            # Powerup handling
            i = 0
            while i < len(powerups):
                temp_rect = self.display.blit(pygame.transform.scale(self.img_powerups[powerups[i]["type"] * -1 - 4], (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (powerups[i]["pos"][0] * MAZE_SCALE[0] + sin(frame_index / 20 + powerups[i]["pos"][0]) * 2, powerups[i]["pos"][1] * MAZE_SCALE[1] + cos(frame_index / 20 + powerups[i]["pos"][0]) * 2))
                if temp_rect.collidepoint((player_values["player_pos"][0] * MAZE_SCALE[0], player_values["player_pos"][1] * MAZE_SCALE[1])):
                    if (powerups[i]["type"] == MEDKIT and health_values["health"] < health_values["MAX_HEALTH"]) or (powerups[i]["type"] == ARMOR and powerup_values["armor_health"] < powerup_values["MAX_ARMOR_HEALTH"]):
                        pygame.event.post(pygame.event.Event(USE_POWERUP, origin="pickup", item=powerups[i]["type"]))
                        temp = True
                    elif powerups[i]["type"] == GUN and GUN in inventory:
                        powerup_values["gun_ammo"] = powerup_values["MAX_GUN_AMMO"]
                        temp = True
                    elif not inventory[slot] and not powerup_values["pickup_delay"] and powerups[i]["type"] not in [MEDKIT, ARMOR] and inventory.count(powerups[i]["type"]) < 2:
                        inventory[slot] = powerups[i]["type"]
                        if powerups[i]["type"] == GUN:
                            powerup_values["gun_ammo"] = powerup_values["MAX_GUN_AMMO"]
                        temp = True
                    else:
                        temp = False
                    if temp:
                        maze[(powerups[i]["pos"][0], powerups[i]["pos"][1])] = -1
                        powerups.pop(i)
                        i -= 1
                i += 1
            # ///
            # Key handling
            if key[0]:
                key[2] = self.display.blit(pygame.transform.scale(self.img_key, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (key[0][0] * MAZE_SCALE[0], key[0][1] * MAZE_SCALE[1]))
                if key[2].collidepoint((player_values["player_pos"][0] * MAZE_SCALE[0], player_values["player_pos"][1] * MAZE_SCALE[1])):
                    key[1] = True
                    key[0] = None
                    if self.selected_level == LEVELS:
                        objective_rect = floor_surface.blit(pygame.transform.scale(self.img_prize_unlocked, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
                    else:
                        objective_rect = floor_surface.blit(pygame.transform.scale(self.img_objective_unlocked, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
            # ///
            # Darkness overlay blitting
            if self.stage > 1:
                if powerup_values["flarestate"]:
                    glow = self.img_glow_flare
                    darkness_surface.fill((127 * (powerup_values["flarestate"] / powerup_values["MAX_FLARESTATE"]), 0, 0, self.stage // 2 * 64 + 127 - 127 * (powerup_values["flarestate"] / powerup_values["MAX_FLARESTATE"])))
                    if powerup_values["flarestate"] == powerup_values["MAX_FLARESTATE"]:
                        pygame.event.post(pygame.event.Event(UPDATE_VIEW))
                    powerup_values["flarestate"] -= 1
                    if powerup_values["flarestate"] == 0:
                        pygame.event.post(pygame.event.Event(UPDATE_VIEW))
                else:
                    glow = self.img_glow
                    darkness_surface.fill((0, 0, 0, self.stage // 2 * 64 + 127))
                if powerup_values["flashlightstate"]:
                    pos1 = [player_values["player_pos"][0] + maze_size[0] * viewport_width * sin(player_values["player_pos"][2] + 0.5), player_values["player_pos"][1] + maze_size[0] * viewport_height * cos(player_values["player_pos"][2] + 0.5)]
                    pos2 = [player_values["player_pos"][0] + maze_size[0] * viewport_width * sin(player_values["player_pos"][2] - 0.5), player_values["player_pos"][1] + maze_size[0] * viewport_height * cos(player_values["player_pos"][2] - 0.5)]
                    if powerup_values["flashlightstate"] < powerup_values["MAX_FLASHLIGHTSTATE"] * 0.2:
                        pygame.draw.polygon(darkness_surface, (0, 0, 0, random.randint(64, 127)), (player_values["player_center"], pos1, pos2))
                    else:
                        pygame.draw.polygon(darkness_surface, (0, 0, 0, 0), (player_values["player_center"], pos1, pos2))
                    powerup_values["flashlightstate"] -= 1
                darkness_surface.blit(pygame.transform.scale(glow, (glow_radius * MAZE_SCALE[0], glow_radius * MAZE_SCALE[0])), (player_values["player_pos"][0] * MAZE_SCALE[0] - (glow_radius * MAZE_SCALE[0]) / 2, player_values["player_pos"][1] * MAZE_SCALE[1] - (glow_radius * MAZE_SCALE[0]) / 2), None, pygame.BLEND_RGBA_MIN)
                self.display.blit(darkness_surface, (0, 0))
            # ///
            # Objective rendering
            if key[1] or self.stage == 1:
                collision_rect_x = ((player_values["player_pos"][0] - 2) * MAZE_SCALE[0], player_values["player_pos"][1] * MAZE_SCALE[1], 4 * MAZE_SCALE[0], 1)
                collision_rect_y = (player_values["player_pos"][0] * MAZE_SCALE[0], (player_values["player_pos"][1] - 2) * MAZE_SCALE[1], 1, 4 * MAZE_SCALE[1])
                if (objective_rect.colliderect(collision_rect_x) or objective_rect.colliderect(collision_rect_y)) and (not objective_close and maze[int((player_values["player_pos"][0] + objective_pos[0]) / 2), int((player_values["player_pos"][1] + objective_pos[1]) / 2)] < 0):
                    objective_close = True
                    if self.stage == 1:
                        objective_rect = floor_surface.blit(pygame.transform.scale(self.img_objective_open, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
                    elif self.selected_level == LEVELS:
                        objective_rect = floor_surface.blit(pygame.transform.scale(self.img_prize_unlocked_open, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
                    else:
                        objective_rect = floor_surface.blit(pygame.transform.scale(self.img_objective_unlocked_open, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
                elif not (objective_rect.colliderect(collision_rect_x) or objective_rect.colliderect(collision_rect_y)) and objective_close:
                    objective_close = False
                    if self.stage == 1:
                        objective_rect = floor_surface.blit(pygame.transform.scale(self.img_objective, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
                    elif self.selected_level == LEVELS:
                        objective_rect = floor_surface.blit(pygame.transform.scale(self.img_prize_unlocked, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
                    else:
                        objective_rect = floor_surface.blit(pygame.transform.scale(self.img_objective_unlocked, (MAZE_SCALE[0] + 1, MAZE_SCALE[1] + 1)), (objective_pos[0] * MAZE_SCALE[0], objective_pos[1] * MAZE_SCALE[1]))
            # ///
            # FPS and grain rendering
            if self.stage > 1:
                overlay_surface.blit(self.img_grain[frame_index % GRAIN_FRAMES], (0, 0))
            if powerup_values["shoestate"] and alive:
                overlay_surface.blit(pygame.transform.scale(self.img_glow_shoe, (self.sizex, self.sizey)), (0, 0))
            elif health_values["health"] < health_values["MAX_HEALTH"] / 5 and alive:
                overlay_surface.blit(pygame.transform.scale(self.img_glow_health[frame_index % 8], (self.sizex, self.sizey)), (0, 0))
            pygame.draw.rect(overlay_surface, "black", text_fps_rect)
            overlay_surface.blit(text_fps, text_fps_rect)
            overlay_surface.blit(text_time, text_time_rect)
            # ///
            # Level completion handling
            if objective_rect.collidepoint((player_values["player_pos"][0] * MAZE_SCALE[0], player_values["player_pos"][1] * MAZE_SCALE[1])) and (key[1] or self.stage == 1):
                if self.selected_level < LEVELS:
                    print(f"Level {self.selected_level} beaten")
                    self.selected_level += 1
                    self.level_carry_over["inventory"] = inventory
                    self.level_carry_over["armor_health"] = powerup_values["armor_health"]
                    self.level_carry_over["gun_ammo"] = powerup_values["gun_ammo"]
                    self.level_carry_over["slot"] = slot
                    return "game"
                else:
                    print(f"Final level {self.selected_level} beaten! Congratulations!")
                    self.level_carry_over = self.level_carry_over_reset.copy()
                    self.selected_level += 1
                    self.game_completed = True
                    return "menu"                
            # ///
            # Viewport scaling and blitting
            zoomed_surface = self.display.subsurface(viewport_rect)
            self.display.blit(pygame.transform.scale(zoomed_surface, (self.sizex, self.sizey)), (0, 0))
            self.display.blit(overlay_surface, (0, 0))
            pygame.display.flip()
            # ///
            # Movement handling
            directions = [
                ((keys[pygame.K_UP] or keys[pygame.K_w]), (0, -1)),
                ((keys[pygame.K_LEFT] or keys[pygame.K_a]), (-1, 0)),
                ((keys[pygame.K_DOWN] or keys[pygame.K_s]), (0, 1)),
                ((keys[pygame.K_RIGHT] or keys[pygame.K_d]), (1, 0))
            ]
            moved_x = 0
            moved_y = 0
            for _ in range(player_values["speed_mult"]):
                for move, (dx, dy) in directions:
                    if move and alive:
                        new_x = player_values["player_pos"][0] + dx * player_values["PLAYER_SPEED"]
                        new_y = player_values["player_pos"][1] + dy * player_values["PLAYER_SPEED"]
    
                        # Check for collisions in the x direction
                        if 0 <= new_x - player_values["PLAYER_SCALE"] < maze_size[0] and 0 <= new_x + player_values["PLAYER_SCALE"] < maze_size[0]:
                            if maze[int(new_x + dx * player_values["PLAYER_SCALE"]), int(player_values["player_pos"][1] + player_values["PLAYER_SCALE"])] < 1 and maze[int(new_x + dx * player_values["PLAYER_SCALE"]), int(player_values["player_pos"][1] - player_values["PLAYER_SCALE"])] < 1:
                                player_values["player_pos"][0] = new_x
                                moved_x = 2 - dx
    
                        # Check for collisions in the y direction
                        if 0 <= new_y - player_values["PLAYER_SCALE"] < maze_size[1] and 0 <= new_y + player_values["PLAYER_SCALE"] < maze_size[1]:
                            if maze[int(player_values["player_pos"][0] + player_values["PLAYER_SCALE"]), int(new_y + dy * player_values["PLAYER_SCALE"])] < 1 and maze[int(player_values["player_pos"][0] - player_values["PLAYER_SCALE"]), int(new_y + dy * player_values["PLAYER_SCALE"])] < 1:
                                player_values["player_pos"][1] = new_y
                                moved_y = 1
            if (moved_x or moved_y) and is_running and not frame_index % 3:
                effects.append(["run_dust", [player_values["player_pos"][0] - player_values["PLAYER_SCALE"], player_values["player_pos"][1] - player_values["PLAYER_SCALE"], moved_x], 14])
            # ///
            # Health and stamina handling
            for corner, i in zip([(0, -1), (-1, 0), (0, 1), (1, 0)], range(4)):
                if maze[int(player_values["player_pos"][0] + corner[0] * (player_values["PLAYER_SPEED"] + player_values["PLAYER_SCALE"])), int(player_values["player_pos"][1] + corner[1] * (player_values["PLAYER_SPEED"] + player_values["PLAYER_SCALE"]))] == 2:
                    touching_firewall = True 
                    break
            if touching_firewall:
                if not health_values["damage_delay"]:
                    pygame.event.post(pygame.event.Event(TAKE_DAMAGE, damage=20, peirce=0, armor_peirce=0.1, affector="player"))
                    health_values["damage_delay"] = health_values["MAX_DAMAGE_DELAY"]
                else:
                    health_values["damage_delay"] -= 1
            else:
                if health_values["damage_delay"]:
                    health_values["damage_delay"] -= 1
            touching_firewall = False
            if is_running and health_values["health"] >= health_values["MAX_HEALTH"] / 5 and alive:
                if stamina_values["stamina"] > 0 and (inventory[slot] not in (BOMB, MEGA_BOMB, ARMOR, RPG) or powerup_values["shoestate"]):
                    player_values["speed_mult"] = 3 + min(powerup_values["shoestate"], 2)
                    if moved_x or moved_y:
                        stamina_values["stamina"] -= 1
                        stamina_values["stamina_delay"] = 20
                    else:
                        stamina_values["stamina_delay"] -= 1
                        if stamina_values["stamina_delay"] <= 0:
                            is_running = False
                else:
                    player_values["speed_mult"] = 2
                    is_running = False
                    stamina_values["stamina_delay"] = 20
            else:
                if is_sneaking and alive:
                    player_values["speed_mult"] = 1
                else:
                    player_values["speed_mult"] = 2
                if stamina_values["stamina_delay"] > 0:
                    stamina_values["stamina_delay"] -= 1
                elif stamina_values["stamina"] < stamina_values["MAX_STAMINA"]:
                    if inventory[slot] in (BOMB, MEGA_BOMB, ARMOR, RPG):
                        stamina_values["stamina"] += 0.25
                    else:
                        stamina_values["stamina"] += 0.5
            if health_values["health"] < health_values["MAX_HEALTH"]:
                health_values["health_speed"] += 1
                health_values["health"] += health_values["health_speed"] / 1000
            # ///
            self.clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()