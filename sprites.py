import pygame as pg
from tilemap import collide_hit_rect
from settings import *
vec=pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.image =pg.image.load("player_top.png")
        self.image = pg.transform.scale(self.image,(TILESIZE, TILESIZE))
        self.player_img=self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vel=vec(0,0)
        self.pos=vec(x,y)* TILESIZE
        self.rot=0

    def get_keys(self):
        self.rot_speed=0
        self.vel=vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel =vec(PLAYER_SPEED,0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(PLAYER_SPEED/2).rotate(-self.rot)

    def update(self):
        self.get_keys()
        self.rot=(self.rot+self.rot_speed*self.game.dt)%360
        self.image=pg.transform.rotate(self.player_img,self.rot)
        self.rect=self.image.get_rect()
        self.rect.center=self.pos
        self.pos+=self.vel*self.game.dt
        self.rect.centerx=self.pos.x


        collide_with_walls(self,self.game.walls,'x')
        self.rect.y = self.y
        self.rect.centery = self.pos.y
        collide_with_walls(self,self.game.walls,'y')
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.mob_img = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center =  self.rect.center
        self.pos=vec(x,y)* TILESIZE
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.rect.center=self.pos
        self.rot=0

    def update(self):
        self.rot=(self.game.player.pos -self.pos). angle_to(vec(1,0))
        self.image=pg.transform.rotate(self.mob_img, self.rot)
        self.rect=self.image.get_rect()
        self.rect.center=self.pos
        self.acc=vec(MOB_SPEED,0).rotate(-self.rot)
        self.acc+= self.vel*-1
        self.vel+=self.acc*self.game.dt
        self.pos+=self.vel*self.game.dt+.5*self.acc*self.game.dt**2
        self.rect.centerx=self.pos.x
        collide_with_walls(self,self.game.walls,'x')
        self.rect.centery = self.pos.y
        collide_with_walls(self,self.game.walls,'y')
        self.rect.center = self.hit_rect.center


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.walls=[]
        self.load_images()

        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        if self.type == 1:
            self.image = self.walls[1]
        if self.type == 2:
            self.image = self.walls[2]
        if self.type == 3:
            self.image = self.walls[3]
        if self.type == 4:
            self.image = self.walls[4]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def load_images(self):
        for i in range(1,25):
            filename = 'images/peice_{}.png'.format(i)
            self.image = pg.image.load(filename)
            self.image.set_colorkey(BLACK)
            self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
            self.walls.append(self.image)

