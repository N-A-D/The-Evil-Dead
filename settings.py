'''
@author: Ned Austin Datiles
'''
import pygame as pg
from core_functions import get_image_names

vec = pg.math.Vector2

# Define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SANDYBROWN = (244, 164, 96)
DEEPSKYBLUE = (0, 191, 255)
DODGERBLUE = (30, 144, 255)
LIMEGREEN = (50, 205, 50)
GOLD = (255, 215, 0)
# Game settings
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 640  # 16 * 48 or 32 * 24 or 64 * 12

FPS = 60
TITLE = "My game"
BGCOLOR = DARKGREY

TILESIZE = 64
GRIDWIDTH = 32
GRIDHEIGHT = 24

# HUD settings
BAR_LENGTH = 300
BAR_HEIGHT = 20

# HUD element images
CROSSHAIR = 'crosshair.png'
CROSSHAIRS = ['simple_ch_1.png',
              'simple_ch_2.png',
              'simple_ch_2.png',
              'simple_ch_4.png',
              'simple_ch_5.png',
              'simple_ch_6.png',
              'simple_ch_7.png',
              'simple_ch_8.png',
              'simple_ch_9.png',
              'simple_ch_10.png',
              'simple_ch_11.png'
              ]
CLIP_IMG = 'UI/clip_0001.png'

# Bullet images
RIFLE_BULLET_IMG = 'Bullets/rifle_bullet.png'
SHOTGUN_BULLET_IMG = 'Bullets/shotgun_bullet.png'
HANDGUN_BULLET_IMG = 'Bullets/handgun_bullet.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Effects
MUZZLE_FLASHES = ['smokeparticleassets/PNG/Flash/flash00.png',
                  'smokeparticleassets/PNG/Flash/flash01.png',
                  'smokeparticleassets/PNG/Flash/flash02.png',
                  'smokeparticleassets/PNG/Flash/flash03.png',
                  'smokeparticleassets/PNG/Flash/flash04.png',
                  'smokeparticleassets/PNG/Flash/flash05.png',
                  'smokeparticleassets/PNG/Flash/flash06.png',
                  'smokeparticleassets/PNG/Flash/flash07.png',
                  'smokeparticleassets/PNG/Flash/flash08.png',
                  ]
FLASH_DURATION = 60
DAMAGE_ALPHA = [x for x in range(0, 255, 50)]
LASER_SIGHT_COLORS = [(124, 252, 0), (50, 205, 50), (173, 255, 47), (152, 251, 152), (34, 139, 34)]
# Item settings
BOB_RANGE = 20
BOB_SPEED = .5

# Player settings
DEFAULT_WEAPON = 'knife'
PLAYER_SPEED = 110
PLAYER_HIT_RECT = pg.Rect(0, 0, 50, 50)
PLAYER_MELEE_RECT = pg.Rect(0, 0, 64, 64)
PLAYER_HEALTH = 100
PLAYER_STAMINA = 100
PLAYER_MELEE_STUMBLE = 100

# Enemy settings
ENEMY_DAMAGE = [10]
ENEMY_KNOCKBACK = 10
ENEMY_LINE_OF_SIGHT = TILESIZE / 2
ENEMY_HIT_RECT = pg.Rect(0, 0, 50, 50)
ENEMY_SPEEDS = [speed for speed in range(40, 100, 10)]
ENEMY_HEALTH = [400]
DETECT_RADIUS = 400
APPROACH_RADIUS = 150
AVOID_RADIUS = 10
SEEK_FORCE = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
WANDER_RING_DISTANCE = 100
WANDER_RING_RADIUS = [40, 50, 60]

# Enemy Animations
ENEMY_IMGS = [
    'img/Enemies/citizenzombie1.png',
    'img/Enemies/citizenzombie2.png',
    'img/Enemies/citizenzombie3.png',
    'img/Enemies/citizenzombie4.png',
    'img/Enemies/citizenzombie5.png',
    'img/Enemies/citizenzombie6.png',
    'img/Enemies/citizenzombie7.png',
    'img/Enemies/citizenzombie8.png',
    'img/Enemies/citizenzombie9.png',
    'img/Enemies/citizenzombie10.png',
]

# Weapon settings
WEAPONS = {}

WEAPONS['animation times'] = {'handgun': {'idle': 100, 'melee': 35, 'move': 100, 'reload': 70, 'shoot': 125},
                              'knife': {'idle': 100, 'melee': 35, 'move': 75, 'reload': 0, 'shoot': 0},
                              'rifle': {'idle': 100, 'melee': 35, 'move': 125, 'reload': 70, 'shoot': 55},
                              'shotgun': {'idle': 100, 'melee': 35, 'move': 125, 'reload': 70, 'shoot': 175}}

WEAPONS['sound'] = {'handgun': {'attack': 'pistol.wav', 'pickup': 'gun_pickup.wav'},
                    'shotgun': {'attack': 'shotgun.wav', 'pickup': 'gun_pickup.wav'},
                    'rifle': {'attack': 'Futuristic SMG Single Shot.wav', 'pickup': 'gun_pickup.wav'},
                    'knife': {'draw': 'knifedraw.wav'}
                    }

WEAPONS['handgun'] = {'bullet_speed': 4000,
                      'bullet_lifetime': 20000,
                      'rate': 200,
                      'kickback': 125,
                      'spread': 1,
                      'damage': 100,
                      'bullet_size': 'med',
                      'clip size': 12,
                      'weight': 3,
                      'wobble': {'sprint': 10, 'walk': 4, 'idle': 1},
                      'muzzle flash range': [25, 35],
                      'barrel offset': vec(50, 20),
                      'default ammo': 5,

                      'bullet_count': 1}

WEAPONS['rifle'] = {'bullet_speed': 4000,
                    'bullet_lifetime': 20000,
                    'rate': 150,
                    'kickback': 200,
                    'spread': 2,
                    'damage': 125,
                    'bullet_size': 'lg',
                    'clip size': 45,
                    'weight': 6,
                    'wobble': {'sprint': 14, 'walk': 7, 'idle': 2},
                    'muzzle flash range': [35, 60],
                    'barrel offset': vec(72, 20),
                    'default ammo': 20,
                    'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 4000,
                      'bullet_lifetime': 20000,
                      'rate': 600,
                      'kickback': 300,
                      'spread': 12,
                      'damage': 135,
                      'bullet_size': 'sm',
                      'clip size': 8,
                      'weight': 7,
                      'wobble': {'sprint': 15, 'walk': 8, 'idle': 2},
                      'muzzle flash range': [50, 70],
                      'barrel offset': vec(75, 20),
                      'default ammo': 3,
                      'bullet_count': 11}
WEAPONS['knife'] = {
    'damage': 50,
    'weight': 1,
    'knockback': 20,
    'wobble': {'sprint': 0, 'walk': 0, 'idle': 0}
}

# Item images
ITEM_IMAGES = {'rifle': 'rifle.png',
               'handgun': 'glock.png',
               'shotgun': 'shotgun.png',
               'ammo': 'Ammo.png',
               'health': 'health.png'
               }

# Blood colors
BLOOD_SHADES = [(value, 0, 0) for value in range(255, 16, -8)]
# Player Animations
HANDGUN_ANIMATIONS = {}
KNIFE_ANIMATIONS = {}
RIFLE_ANIMATIONS = {}
SHOTGUN_ANIMATIONS = {}

HANDGUN_ANIMATIONS['idle'] = get_image_names('img/Player animations/handgun/idle/')
HANDGUN_ANIMATIONS['melee'] = get_image_names('img/Player animations/handgun/meleeattack/')
HANDGUN_ANIMATIONS['move'] = get_image_names('img/Player animations/handgun/move/')
HANDGUN_ANIMATIONS['reload'] = get_image_names('img/Player animations/handgun/reload/')
HANDGUN_ANIMATIONS['shoot'] = get_image_names('img/Player animations/handgun/shoot/')

KNIFE_ANIMATIONS['idle'] = get_image_names("img/Player animations/knife/idle/")
KNIFE_ANIMATIONS['melee'] = get_image_names("img/Player animations/knife/meleeattack/")
KNIFE_ANIMATIONS['move'] = get_image_names('img/Player animations/knife/move/')

RIFLE_ANIMATIONS['idle'] = get_image_names("img/Player animations/rifle/idle/")
RIFLE_ANIMATIONS['melee'] = get_image_names("img/Player animations/rifle/meleeattack/")
RIFLE_ANIMATIONS['move'] = get_image_names("img/Player animations/rifle/move/")
RIFLE_ANIMATIONS['reload'] = get_image_names('img/Player animations/rifle/reload/')
RIFLE_ANIMATIONS['shoot'] = get_image_names('img/Player animations/rifle/shoot/')

SHOTGUN_ANIMATIONS['idle'] = get_image_names("img/Player animations/shotgun/idle/")
SHOTGUN_ANIMATIONS['melee'] = get_image_names("img/Player animations/shotgun/meleeattack/")
SHOTGUN_ANIMATIONS['move'] = get_image_names("img/Player animations/shotgun/move/")
SHOTGUN_ANIMATIONS['reload'] = get_image_names('img/Player animations/shotgun/reload/')
SHOTGUN_ANIMATIONS['shoot'] = get_image_names('img/Player animations/shotgun/shoot/')
