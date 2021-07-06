import pygame, sys, random

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos,speed):
        super().__init__()
        self.uncharged = pygame.image.load(path)
        self.charged = pygame.image.load('spaceship_charged.png')

        self.image = self.uncharged
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.shield_surface = pygame.image.load('shield.png')
        self.health = 5  # lifes times

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()
        self.display_health()

    def screen_constrain(self):
       if self.rect.right >= 1280:
           self.rect.right = 1280
       if self.rect.left <= 0:
           self.rect.left = 0

    def display_health(self):
        for index,shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface,(10 + index * 40 ,10))
            #screen.blit(self.score_surface,(680,10))

    def get_damage(self,damage_amount):
        self.health -= damage_amount

    def charge(self):
        self.image = self.charged

    def discharge(self):
        self.image = self.uncharged

class Meteor(pygame.sprite.Sprite):
    def __init__(self,path,x_pos,y_pos,x_speed,y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 800:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self,path,pos,speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed
        if self.rect.centery <= -100:
            self.kill()

def main_game():
    global laser_active
    laser_group.draw(screen)
    spaceship_group.draw(screen)
    meteor_group.draw(screen)
    #main_score.draw(screen)

    laser_group.update()
    spaceship_group.update()
    meteor_group.update()
    #main_score.update()

    # Collision
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        spaceship_group.sprite.get_damage(1)  # Reduce 1 life
        explosion_sound.play()
    # Laser shoot
    for laser in laser_group:
        pygame.sprite.spritecollide(laser, meteor_group, True)
    # Laser timer
    if pygame.time.get_ticks() - laser_timer >= 200:
        laser_active = True
        spaceship_group.sprite.charge()


    return 1

def end_game():
    text_surface = game_font.render('Game Over !',True,(255,255,255))
    text_rect = text_surface.get_rect(center = (640,340))
    screen.blit(text_surface,text_rect)

    score_surface = game_font.render(f'Score: {score}',True,(255,255,255))
    score_rect = score_surface.get_rect(center = (640,380))
    screen.blit(score_surface, score_rect)
    end_sound.play()

pygame.init()  # initiate pygame
pygame.mixer.init()
screen = pygame.display.set_mode((1280,720)) # Create display surface
clock = pygame.time.Clock()  # Create clock object
game_font = pygame.font.Font('LazenbyCompSmooth.ttf',40)
score = 0
laser_timer = 0
laser_active = False

# Sounds
#music_fond = pygame.music.load('')
#self.music_fond.play(3)
laser_sound = pygame.mixer.Sound('LASRLIT2.wav')
#laser_sound.play()
explosion_sound = pygame.mixer.Sound('xxxplode.wav') # delobj01.wav
#explosion_sound.play()
#explosion_meteor = pygame.mixer.Sound('delobj01.wav')
#lost_sound = pygame.mixer.Sound('')
end_sound = pygame.mixer.Sound('smrpg_geno_stargun.wav')

spaceship = SpaceShip('spaceship.png',640,500,10)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

meteor_group = pygame.sprite.Group()
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT,250)  # cantidad de meteoritos

laser_group = pygame.sprite.Group()


while True:  # Game loop
    for event in pygame.event.get(): # Check for events / Player input
        if event.type == pygame.QUIT: # Close the game
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and laser_active:
            new_laser = Laser('Laser.png', event.pos, 15)
            laser_group.add(new_laser)
            laser_sound.play()
            laser_active = False
            laser_timer = pygame.time.get_ticks()
            spaceship_group.sprite.discharge()

        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health <= 0:
            spaceship_group.sprite.health = 5
            meteor_group.empty()
            score = 0

        if event.type == METEOR_EVENT:
            meteor_path = random.choice(('Meteor1.png','Meteor2.png','Meteor3.png'))
            random_x_pos = random.randrange(0,1280)
            random_y_pos = random.randrange(-500,-50)
            random_x_speed = random.randrange(-1,1)
            random_y_speed = random.randrange(4,10)
            meteor = Meteor(meteor_path,random_x_pos,random_y_pos,random_x_speed,random_y_speed)
            meteor_group.add(meteor)

    screen.fill((42,45,51))
    if spaceship_group.sprite.health > 0:
        score += main_game()

    else:
        end_game()

    pygame.display.update()
    clock.tick(120)




