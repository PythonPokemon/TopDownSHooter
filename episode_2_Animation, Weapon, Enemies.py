import pygame #---importiert pygame bibliothek
import sys#---?
import math #---importiert aus der Python Bibliothek berechnungsgrundlagen
import random #---mportiert aus der Python Bibliothek zufallsgenerator

pygame.init()#---initialisiert das spiel

display = pygame.display.set_mode((800, 600))#------------------Display größe-------------------
clock = pygame.time.Clock()#---fps?

player_walk_images = [pygame.image.load("player_walk_0.png"), pygame.image.load("player_walk_1.png"),
pygame.image.load("player_walk_2.png"), pygame.image.load("player_walk_3.png")]

class Player:#----objekt Player Parameter
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0 #--- zählt das animationsframe 0.png - 3.png also maximale anzhal
        self.moving_right = False
        self.moving_left = False
    def main(self, display): #---Player auf dem bilschirm zeichnen mit entsprechenden Parametern
        if self.animation_count + 1 >= 16:
            self.animation_count = 0 #---wenn 0.png >= 16 erreicht ist, wird es zurückgesetzt auf 0
            
        self.animation_count += 1#--animationszähler

        if self.moving_right:
            display.blit(pygame.transform.scale(player_walk_images[self.animation_count//4], (32, 42)), (self.x, self.y))
        elif self.moving_left:
             display.blit(pygame.transform.scale(pygame.transform.flip(player_walk_images[self.animation_count//4], True, False), (32, 42)), (self.x, self.y))
        else:
            display.blit(pygame.transform.scale(player_walk_images[0], (32, 42)), (self.x, self.y))
        #pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))#----farbe
        self.moving_right = False
        self.moving_left = False

class PlayerBullet: #----objekt Kugeln Parameter
    def __init__(self, x, y, mouse_x, mouse_y,):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0,0,0), (self.x, self.y), 5)

class SlimeEnemy: #----Objekt Slime Parameter
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_images = [pygame.image.load("slime_animation_0.png"), pygame.image.load("slime_animation_1.png"), pygame.image.load("slime_animation_2.png"), pygame.image.load("slime_animation_3.png")]
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange (-150, 150)
        self.offset_y = random.randrange (-150, 150)
    def main(self, display):
        if self.animation_count + 1 == 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange (-150, 150)
            self.offset_y = random.randrange (-150, 150)
            self.reset_offset = random.randrange (120, 150)
        else:
            self.reset_offset -= 1

        if player.x + self.offset_x > self.x-display_scroll[0]:
            self.x += 1
        elif player.x + self.offset_x < self.x-display_scroll[0]:
            self.x -= 1

        if player.y + self.offset_y > self.y-display_scroll[1]:
            self.y += 1
        elif player.y + self.offset_y < self.y-display_scroll[1]:
            self.y -= 1


        display.blit(pygame.transform.scale(self.animation_images[self.animation_count//4], (32, 30)), (self.x-display_scroll[0], self.y-display_scroll[1]))



enemies = [SlimeEnemy(400, 300)]
player = Player(400, 300, 32, 32)#-------positionierung auf dem displya x, y, -achse , höhe, breite

display_scroll =[0,0]

player_bullets = []

while True:#----schleife
    display.fill((24,164,86,))#---display hintergrund farbe

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

    keys = pygame.key.get_pressed() #---tastenzuweisung & funktion

    pygame.draw.rect(display, (255,255,255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))

    if keys[pygame.K_a]: #---taste a scrollt -5 speed, links
        display_scroll[0] -= 5

        player.moving_left = True

        for bullet in player_bullets:
            bullet.x += 5
    if keys[pygame.K_d]: #---taste d scrollt -5 speed, rechts
        display_scroll[0] += 5

        player.moving_right = True

        for bullet in player_bullets:
            bullet.x -= 5

    if keys[pygame.K_w]: #---taste w scrollt -5 speed, hoch
        display_scroll[1] -= 5
        for bullet in player_bullets:
            bullet.x += 5

    if keys[pygame.K_s]: #---taste a scrollt -5 speed, runter
        display_scroll[1] += 5
        for bullet in player_bullets:
            bullet.x -= 5


    player.main(display)

    for bullet in player_bullets:
        bullet.main(display)

    for enemy in enemies:
        enemy.main(display)

    clock.tick(60)
    pygame.display.update()#---schleifen update