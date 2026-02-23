import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon Jeu de Plateforme")
clock = pygame.time.Clock()
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 128, 255))      
        self.rect = self.image.get_rect()
        self.rect.center = (100, 300)

        self.vel_y = 0          
        self.on_ground = False 
        self.speed = 5
        self.jump_force = -15

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
          
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_force

        self.vel_y += 0.8
        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
