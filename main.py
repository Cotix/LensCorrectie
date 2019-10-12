
import math
import pygame
from raytracing import RayTracing
from models.lens import ConvexLens

WIDTH = 200
HEIGHT = 200

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lens Correction")

bitmap_surf = pygame.transform.scale(pygame.image.load("image2.png"), (200,200))
pygame.image.save(bitmap_surf, "scaled_input.png")



lens_size = 0.1

tracer = RayTracing(ConvexLens(-2, 2, math.sqrt(4+(2*lens_size)**2), math.sqrt(4+(2*lens_size)**2)), lens_size, lens_size, 40, 1, bitmap_surf, screen)

# print(tracer.search_source_dist(40))
# tracer = RayTracing(ConvexLens(-2, 2, 2.23606797749979, 2.23606797749979), 50, 50, 40, 2)
tracer.trace_bitmap()
pygame.display.flip()

pygame.image.save(screen, "output.png")



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()