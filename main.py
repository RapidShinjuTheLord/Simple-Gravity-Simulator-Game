import pygame
import sys
import math
from colorsys import hsv_to_rgb
import random


#Window is scaleable, but you can change these variables to adjust initial size if desired.
initial_screen_width = 800
initial_screen_height = 800


class Game:

    class Planet:
        def __init__(self, xpos, ypos, mass, xvel=0, yvel=0):
            self.mass = mass
            self.pos = [xpos,ypos]
            self.velocity = [xvel,yvel]
            self.acceleration = [0,0]
            self.color = []
            self.rgb = self.mass_to_rgb()
            self.alive = True
            self.id = random.randint(0,9999999)

            
        def update_pos(self):
            self.pos[0] += self.velocity[0]
            self.pos[1] += self.velocity[1]
            self.velocity[0] += self.acceleration[0]
            self.velocity[1] += self.acceleration[1] 
        
        def mass_to_rgb(self):
            return hsv_to_rgb(math.tanh(self.mass/2), 1, 1)
        
        def gravitate(self, objects, gravitic_constant):
            
            self.acceleration = [0,0]

            planets = objects.copy()
            planets.remove(self)
            collided = []
            for planet in planets:
                if planet.alive:
                    x_d = planet.pos[0] - self.pos[0]
                    y_d = planet.pos[1] - self.pos[1]
                    x_dis = x_d + random.random() * 0.0001
                    y_dis = y_d + random.random() * 0.0001
                    if x_dis >= 0:
                        angle = math.atan(y_dis/x_dis)
                    else:
                        angle = math.pi + math.atan(y_dis/x_dis)
                    force = gravitic_constant * self.mass * planet.mass / ((x_dis*6) ** 2 + (y_dis*6) ** 2)
                    self.acceleration[0] += (force/self.mass) * math.cos(angle)
                    self.acceleration[1] += (force/self.mass) * math.sin(angle)

                    dis = (x_d ** 2 + y_d ** 2) ** 0.5
                    if dis <= 50 * (self.mass**0.5) + 50 * (planet.mass**0.5):
                        collided.append(planet.id)
            
            return collided


    def __init__(self, screen_width = 800, screen_height = 800, fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width,screen_height), pygame.RESIZABLE)
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.display.set_caption("Gravity")
        self.load_media()
        while True:
            self.simulation(fps)
        
    def simulation(self, fps):
        #pygame.mixer.Sound.set_volume((0.5))
        pygame.mixer.music.play(-1)

        self.title = True
        self.clock = pygame.time.Clock()
        self.planets = list()
        self.title_scale = ( int(348 * min(self.screen_width/800, self.screen_height/800)), int(369 * min(self.screen_width/800, self.screen_height/800)) )
        self.title_img = pygame.transform.scale(self.titlegraphics[0], self.title_scale)
        self.title_rect = self.title_img.get_rect()
        while self.title:
            self.screen_width, self.screen_height = pygame.display.get_window_size()
            self.title_scale = ( int(348 * min(self.screen_width/800, self.screen_height/800)), int(369 * min(self.screen_width/800, self.screen_height/800)) )
            self.title_img = pygame.transform.scale(self.titlegraphics[0], self.title_scale)
            self.title_rect = self.title_img.get_rect()
            #print((self.screen_width, self.screen_height))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                    self.title = False
        
            self.screen.fill((255,255,255))
            
            #self.screen.blit(pygame.transform.scale(self.titlegraphics[0], self.title_scale))
            self.title_rect.center = (self.screen_width/2, self.screen_height/2)
            self.screen.blit(self.title_img, self.title_rect)

            self.clock.tick(fps)
            pygame.display.update()

        self.instructions = True
        self.instr_scale = ( int(572 * min(self.screen_width/800, self.screen_height/800)), int(526 * min(self.screen_width/800, self.screen_height/800)) )
        self.instr_img = pygame.transform.scale(self.titlegraphics[2], self.instr_scale)
        self.instr_rect = self.instr_img.get_rect()

        pygame.mixer.Sound.play(self.pop)
        while self.instructions:
            self.screen_width, self.screen_height = pygame.display.get_window_size()
            self.instr_scale = ( int(800 * min(self.screen_width/800, self.screen_height/800)), int(770 * min(self.screen_width/800, self.screen_height/800)) )
            self.instr_img = pygame.transform.scale(self.titlegraphics[2], self.instr_scale)
            self.instr_rect = self.instr_img.get_rect()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                    self.instructions = False
            
            self.screen.fill((255,255,255))
            self.instr_rect.center = (self.screen_width/2, self.screen_height/2)
            self.screen.blit(self.instr_img, self.instr_rect)

            self.clock.tick(fps)
            pygame.display.update()

        self.running = True
        self.gravitic_constant = 50000
        self.spawnmass = 0.1625
        mousepos = [0,0]
        self.mousedown = False
        spawn_x = 0
        spawn_y = 0
        self.x_offset = 0
        self.y_offset = 0
        increasing_mass = False
        decreasing_mass = False
        increasing_offset_x = False
        decreasing_offset_x = False
        increasing_offset_y = False
        decreasing_offset_y = False
        pygame.mixer.Sound.play(self.pop)
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mousedown == False:
                        spawn_x = mousepos[0] + self.x_offset
                        spawn_y = mousepos[1] + self.y_offset
                        #print("planet")
                        self.mousedown = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        decreasing_mass = True
                    elif event.key == pygame.K_UP:
                        increasing_mass = True

                    if event.key == pygame.K_w:
                        decreasing_offset_y = True
                    elif event.key == pygame.K_s:
                        increasing_offset_y = True
                    elif event.key == pygame.K_a:
                        decreasing_offset_x = True
                    elif event.key == pygame.K_d:
                        increasing_offset_x = True


                    if event.key == pygame.K_SPACE:
                        pygame.mixer.Sound.play(self.pop)
                        self.planets = list()

                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.mousedown == True:
                        d_x = - ((mousepos[0] + self.x_offset) - spawn_x) / 60
                        d_y = - ((mousepos[1] + self.y_offset) - spawn_y) / 60
                        self.planets.append(self.Planet(spawn_x, spawn_y, self.spawnmass, d_x, d_y))

                    self.mousedown = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        decreasing_mass = False
                    elif event.key == pygame.K_UP:
                        increasing_mass = False

                    if event.key == pygame.K_w:
                        decreasing_offset_y = False
                    elif event.key == pygame.K_s:
                        increasing_offset_y = False
                    elif event.key == pygame.K_a:
                        decreasing_offset_x = False
                    elif event.key == pygame.K_d:
                        increasing_offset_x = False


            mousepos = pygame.mouse.get_pos()
            
            if decreasing_mass:
                self.spawnmass /= 1.03
            if increasing_mass:
                self.spawnmass *= 1.03
            if increasing_offset_x:
                self.x_offset += 6
            if decreasing_offset_x:
                self.x_offset -= 6
            if increasing_offset_y:
                self.y_offset += 6
            if decreasing_offset_y:
                self.y_offset -= 6



            self.screen.fill((255,255,255))
            incplan = []
            incmass = []
            incpos = []
            incvel = []
            for planet in self.planets:
                

                pygame.draw.circle(self.screen, 
                                   (planet.rgb[0]*255, 
                                    planet.rgb[1]*255, 
                                    planet.rgb[2]*255), 
                                    (planet.pos[0] - self.x_offset,planet.pos[1] - self.y_offset), 
                                    50*(planet.mass**0.5))
                
                
                planet.update_pos()

            for planet in self.planets:
                crash = planet.gravitate(self.planets, self.gravitic_constant)
                if planet.id in incplan:
                    
                    planet.pos[0] = (planet.pos[0] * planet.mass + incpos[incplan.index(planet.id)][0] * incmass[incplan.index(planet.id)]) / (planet.mass + incmass[incplan.index(planet.id)])
                    planet.pos[1] = (planet.pos[1] * planet.mass + incpos[incplan.index(planet.id)][1] * incmass[incplan.index(planet.id)]) / (planet.mass + incmass[incplan.index(planet.id)])
                    planet.velocity[0] = (planet.velocity[0] * planet.mass + incvel[incplan.index(planet.id)][0] * incmass[incplan.index(planet.id)]) / (planet.mass + incmass[incplan.index(planet.id)])
                    planet.velocity[1] = (planet.velocity[1] * planet.mass + incvel[incplan.index(planet.id)][1] * incmass[incplan.index(planet.id)]) / (planet.mass + incmass[incplan.index(planet.id)])

                    planet.mass += incmass[incplan.index(planet.id)]
                    planet.rgb = planet.mass_to_rgb()

                    pygame.mixer.Sound.play(self.pop)

                else:

                    if len(crash) != 0:
                        planet.alive = False
                        if crash[0] not in incplan:
                            incplan.append(crash[0])
                            incmass.append(planet.mass)
                            
                        else:
                            incmass[incplan.index(crash[0])] += planet.mass
                        incpos.append(planet.pos)
                        incvel.append(planet.velocity)
                

            for planet in self.planets:
                if planet.alive == False:
                    self.planets.remove(planet)

            
            if self.mousedown:
                pygame.draw.circle(self.screen, (200,200,200,100), (spawn_x - self.x_offset , spawn_y - self.y_offset), 50*(self.spawnmass**0.5))
            pygame.draw.circle(self.screen, (180,180,180,100), (mousepos[0], mousepos[1]), 50*(self.spawnmass**0.5))
            
            
            self.clock.tick(fps)
            pygame.display.update()

        
    
    def load_media(self):
        self.titlegraphics = [pygame.image.load("media/graphics/title1.png"), 
                              pygame.image.load("media/graphics/title2.png"),
                              pygame.image.load("media/graphics/instructions.png")]
        self.pop = pygame.mixer.Sound("media/sfx/pop.mp3")
        self.bgmusic = pygame.mixer.music.load("media/bgmusic/gravity.mp3")


simulation = Game(initial_screen_width,initial_screen_height)