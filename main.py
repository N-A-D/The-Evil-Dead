'''
@author: Ned Austin Datiles
'''
import pygame as pg
from os import path
from settings import *
from random import random, choice
from player import Player
from mobs import Mob
from tilemap import Map, Camera
from sprites import Obstacle
from core_functions import collide_hit_rect


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.pre_init(44100, -16, 1, 1024)
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        # Resource folders
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.snd_folder = path.join(self.game_folder, 'snd')

        self.load_data()
        self.running = True

        # Debugging flags
        self.debug = False

    def load_data(self):
        """
        Loads the necessary assets for the game. 
        :return: 
        """
        # Game map
        self.map = Map(path.join(self.game_folder, 'map.txt'))

        # HUD Elements
        self.mag_img = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, CLIP_IMG)),
                                                (32, 32)).convert_alpha()

        # Crosshair
        self.crosshair = pg.image.load(path.join(self.img_folder, 'crosshair.png')).convert_alpha()

        # Fonts
        self.hud_font = path.join(self.img_folder, 'Impacted2.0.ttf')

        # Sound loading
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                noise = pg.mixer.Sound(path.join(self.snd_folder, snd))
                if weapon == 'rifle':
                    noise.set_volume(1.5)
                self.weapon_sounds[weapon].append(noise)

        # Bullets
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(self.img_folder, RIFLE_BULLET_IMG)).convert_alpha()
        self.bullet_images['med'] = pg.image.load(path.join(self.img_folder, HANDGUN_BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.smoothscale(pg.image.load(
            path.join(self.img_folder, SHOTGUN_BULLET_IMG)).convert_alpha(), (7, 7))

        # Effects
        self.gun_flashes = [pg.image.load(path.join(self.img_folder, flash)).convert_alpha() for flash in
                            MUZZLE_FLASHES]

        # Load enemy animations
        self.enemy_imgs = [pg.transform.smoothscale(pg.image.load(path.join(self.game_folder, name)),
                                                    (96, 96)).convert_alpha() for name in
                           ENEMY_IMGS]
        # Load player animations
        self.default_player_weapon = 'knife'
        self.default_player_action = 'idle'
        self.player_animations = {'handgun': {}, 'knife': {}, 'rifle': {}, 'shotgun': {}}

        # Create all hand gun animations
        self.player_animations['handgun']['idle'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in HANDGUN_ANIMATIONS['idle']]
        self.player_animations['handgun']['melee'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                      for name in HANDGUN_ANIMATIONS['melee']]
        self.player_animations['handgun']['move'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in HANDGUN_ANIMATIONS['move']]
        self.player_animations['handgun']['reload'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                       for name in HANDGUN_ANIMATIONS['reload']]
        self.player_animations['handgun']['shoot'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                      for name in HANDGUN_ANIMATIONS['shoot']]

        # Create all knife animations
        self.player_animations['knife']['idle'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                   name in KNIFE_ANIMATIONS['idle']]
        self.player_animations['knife']['melee'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                    name in KNIFE_ANIMATIONS['melee']]
        self.player_animations['knife']['move'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                   name in KNIFE_ANIMATIONS['move']]

        # Create all rifle animations
        self.player_animations['rifle']['idle'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                   name in RIFLE_ANIMATIONS['idle']]
        self.player_animations['rifle']['melee'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                    name in RIFLE_ANIMATIONS['melee']]
        self.player_animations['rifle']['move'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                   name in RIFLE_ANIMATIONS['move']]
        self.player_animations['rifle']['reload'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in RIFLE_ANIMATIONS['reload']]
        self.player_animations['rifle']['shoot'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha() for
                                                    name in RIFLE_ANIMATIONS['shoot']]

        # Create all shotgun animations
        self.player_animations['shotgun']['idle'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in SHOTGUN_ANIMATIONS['idle']]
        self.player_animations['shotgun']['melee'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                      for name in SHOTGUN_ANIMATIONS['melee']]
        self.player_animations['shotgun']['move'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                     for name in SHOTGUN_ANIMATIONS['move']]
        self.player_animations['shotgun']['reload'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                       for name in SHOTGUN_ANIMATIONS['reload']]
        self.player_animations['shotgun']['shoot'] = [pg.image.load(path.join(self.game_folder, name)).convert_alpha()
                                                      for name in SHOTGUN_ANIMATIONS['shoot']]

    def new(self):
        """
        Creates a new game
        :return: 
        """
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.melee_box = pg.sprite.GroupSingle()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Obstacle(self, col, row, TILESIZE, TILESIZE)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'E':
                    Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        g.run()

    def run(self):
        """
        Runs the game
        :return: 
        """
        self.playing = True
        while self.playing:
            pg.display.set_caption("{:.0f}".format(self.clock.get_fps()))
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        """
        Updates game state
        :return: 
        """
        self.all_sprites.update()
        self.camera.update(self.player)
        # self.melee_box.update()

        # Enemy hits player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            # if random() < 0.7:
            #     choice(self.player_hit_sounds).play()
            # Barrel stuffing cancels out any attack by an enemy

            hit_melee_box = pg.sprite.spritecollide(hit, self.melee_box, True)
            if hit_melee_box:
                hit.vel = vec(2 * PLAYER_MELEE_STUMBLE, 0).rotate(-self.player.rot)
                hit.health -= WEAPONS[self.player.weapon]['damage']
            else:
                # self.player.health -= ENEMY_DAMAGE
                hit.vel = vec(0, 0)
                if self.player.health <= 0:
                    self.playing = False

        if hits:
            self.player.pos += vec(ENEMY_KNOCKBACK, 0).rotate(-hits[0].rot)

        # Bullet collisions
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True, collide_hit_rect)
        for mob in hits:
            mob.hit()
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def events(self):
        """
        Game loop event handling
        :return: 
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_COMMA:
                    self.player.pick_up_ammo()
                if event.key == pg.K_b:
                    self.debug = not self.debug

    def draw_grid(self):
        """
        Used for debugging
        :return: 
        """
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        """
        Draws the updated game state onto the screen
        :return: 
        """
        self.screen.fill(DARKGREY)
        x, y = pg.mouse.get_pos()
        self.screen.blit(self.crosshair, (x - self.crosshair.get_rect().width // 2,
                                          y - self.crosshair.get_rect().height // 2))
        if self.debug:
            self.draw_grid()

        # Draw all sprites to the screen
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.debug:
                pg.draw.rect(self.screen, (0, 255, 255), self.camera.apply_rect(sprite.hit_rect), 1)

        # draw hud information
        self.update_hud()
        pg.display.flip()

    def update_hud(self):
        """
        Updates the HUD information for the player to see
        :return: 
        """
        self.draw_player_stats()
        self.draw_text(str(len(self.mobs)) + " zombies remain", self.hud_font, 30, WHITE, WIDTH // 2, 10)
        if self.player.weapon != 'knife':
            self.draw_current_clip(self.screen, 10, 70, self.player.fire_arms[self.player.weapon]['clip'], 3, 15)

    def draw_player_stats(self):
        """
        Gives the player visual indication of their health & stamina
        :return: 
        """
        self.draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text(str(self.player.health) + "%", self.hud_font, 15, (119, 136, 153),
                       BAR_LENGTH // 2 - 5, 10)
        self.draw_player_stamina(self.screen, 10, 40, self.player.stamina / PLAYER_STAMINA)
        self.draw_text("{0:.0f}".format(self.player.stamina) + "%", self.hud_font, 15, (119, 136, 153),
                       BAR_LENGTH // 2 - 5, 40)

    def draw_current_clip(self, surface, x, y, bullets, bullet_length, bullet_height):
        """
        Used to give the player visual indication of how much ammunition they have at 
        the moment in their weapon
        :param surface: The location in which to draw this information
        :param x: The x location to draw
        :param y: The y location to draw
        :param bullets: How many bullets to draw
        :param bullet_length: How wide the bullet figure will be
        :param bullet_height: How tall the bullet figure will be
        :return: 
        """
        if self.player.weapon != 'knife':
            temp = x
            # Draws a grey set of bullets onto the screen
            # As the player fires their weapon, these grey bullet figures will be revealed
            # to give the player a sense of the emptiness of their weapon's clip
            for j in range(0, WEAPONS[self.player.weapon]['clip size']):
                bullet_outline = pg.Rect(temp, y, bullet_length, bullet_height)
                pg.draw.rect(surface, LIGHTGREY, bullet_outline)
                temp += 2 * bullet_length

            self.screen.blit(self.mag_img, (temp + 16, y - 5))
            self.draw_text('x' + str(self.player.fire_arms[self.player.weapon]['reloads']), self.hud_font, 20, WHITE,
                           temp + 48, y - 5)
            temp = x

            # Draws the bullets the actually remain in the clip as gold figures.
            # These bullets will cover up the grey bullets drawn just above and
            # are removed as the player shoots these bullets
            for i in range(0, bullets):
                bullet = pg.Rect(temp, y, bullet_length, bullet_height)
                pg.draw.rect(surface, GOLD, bullet)
                temp += 2 * bullet_length

    def draw_player_health(self, surface, x, y, pct):
        """
        Draws the player's health bar
        :param surface: 
        :param x: 
        :param y: 
        :param pct: 
        :return: 
        """
        if pct < 0:
            pct = 0

        fill = pct * BAR_LENGTH
        static = BAR_LENGTH

        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        filled_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        static_rect = pg.Rect(x, y, static, BAR_HEIGHT)

        pg.draw.rect(surface, LIMEGREEN, static_rect)
        pg.draw.rect(surface, GREEN, filled_rect)
        pg.draw.rect(surface, WHITE, outline_rect, 2)

    def draw_player_stamina(self, surface, x, y, pct):
        """
        Draws the player's stamina bar
        :param surface: 
        :param x: 
        :param y: 
        :param pct: 
        :return: 
        """
        if pct < 0:
            pct = 0

        fill = pct * BAR_LENGTH
        static = BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        filled_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        static_rect = pg.Rect(x, y, static, BAR_HEIGHT)

        pg.draw.rect(surface, DODGERBLUE, static_rect)
        pg.draw.rect(surface, DEEPSKYBLUE, filled_rect)
        pg.draw.rect(surface, WHITE, outline_rect, 2)

    def draw_text(self, text, font_name, size, color, x, y, align='nw'):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)

        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        """
        Displays the start screen for the game
        :return: 
        """
        pass

    def show_gameover_screen(self):
        """
        Displays the gameover screen for the game
        :return: 
        """
        pass

    def show_pause_screen(self):
        """
        Displays the pause screen for the game
        :return: 
        """
        pass


if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_gameover_screen()

    pg.quit()