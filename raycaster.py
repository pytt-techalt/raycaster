import pygame
import math

# Initialize Pygame
pygame.init()

# Set screen size
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycaster")

# Define player variables
player_x = 400
player_y = 300
player_angle = 0
player_speed = 5

# Define raycasting variables
FOV = math.pi / 3
num_rays = 120
ray_angle_increment = FOV / num_rays

# Define wall data
walls = [
    ((100, 100), (100, 500)),  # Wall 1
    ((100, 500), (700, 500)),  # Wall 2
    ((700, 500), (700, 100)),  # Wall 3
    ((700, 100), (100, 100))   # Wall 4
    ]

# Draw walls on the screen
for wall in walls:
    pygame.draw.line(screen, (255, 255, 255), wall[0], wall[1], 3)
    

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= 0.1
    if keys[pygame.K_RIGHT]:
        player_angle += 0.1
    if keys[pygame.K_UP]:
        player_x += player_speed * math.cos(player_angle)
        player_y += player_speed * math.sin(player_angle)
    if keys[pygame.K_DOWN]:
        player_x -= player_speed * math.cos(player_angle)
        player_y -= player_speed * math.sin(player_angle)
    
    screen.fill((0, 0, 0))
    
    for ray in range(num_rays):
        ray_angle = player_angle - (FOV / 2) + ray * ray_angle_increment
        
        ray_dx = math.cos(ray_angle)
        ray_dy = math.sin(ray_angle)
        
        intersection = None
        min_distance = float('inf')
        
        for wall in walls:
            x1, y1 = wall[0]
            x2, y2 = wall[1]
            
            den = (x1 - x2)*(player_y - (player_y + ray_dy)) - (y1 - y2)*(player_x - (player_x + ray_dx))
            
            if den == 0:
                continue
            
            t = ((x1 - player_x)*(player_y - (player_y + ray_dy)) - (y1 - player_y)*(player_x - (player_x + ray_dx))) / den
            u = -((x1 - x2)*(y1 - player_y) - (y1 - y2)*(x1 - player_x)) / den
            
            if t > 0 and t < 1 and u > 0:
                px = x1 + t*(x2 - x1)
                py = y1 + t*(y2 - y1)
                
                distance = math.sqrt((player_x - px)**2 + (player_y - py)**2)
                
                if distance < min_distance:
                    min_distance = distance
                    intersection = (px, py)
        
        if intersection:
            pygame.draw.circle(screen, (255, 0, 0), (int(intersection[0]), int(intersection[1])), 2)
    
    pygame.draw.circle(screen, (0, 255, 0), (int(player_x), int(player_y)), 5)
    
 
    pygame.display.flip()

pygame.quit()
