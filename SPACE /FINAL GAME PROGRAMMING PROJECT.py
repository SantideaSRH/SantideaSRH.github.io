import pygame
import os

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
VEL = 5
PROJECTILE_SPEED = 8
FIRE_COOLDOWN = 400

# Load sounds
hit_sound = pygame.mixer.Sound(os.path.join('hit.mp3'))
shoot_sound = pygame.mixer.Sound(os.path.join('shoot.mp3'))

# Load background
background_image = pygame.image.load(os.path.join('BG.png'))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Font and game name
pygame.display.set_caption("Spaceship Shooting Game Project")
font = pygame.font.SysFont(None, 36)

# Load Bullets
bullet_img = pygame.image.load(os.path.join('fire.png'))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))


class Bullet:
    # Initialize new objects atomaticlly
    def __init__(self, x, y, width=10, height=20, color=RED, direction='up'):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.direction = direction
        self.image = bullet_img 

    def move(self):
        if self.direction == 'up':
            self.rect.y -= PROJECTILE_SPEED
        elif self.direction == 'down':
            self.rect.y += PROJECTILE_SPEED

    def draw(self, surface):
        # Draw the image at the bullet's rect position
        surface.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.y + self.rect.height < 0 or self.rect.y > SCREEN_HEIGHT
    
class Player:

    # Initialize new objects atomaticlly
    def __init__(self):
        self.width, self.height = 75, 45
        self.pos = [200, 600]
        self.rect = pygame.Rect(*self.pos, self.width, self.height) 
        self.image = pygame.image.load(os.path.join('player.png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, 90)
        self.health = 150
        self.max_health = 150
        self.alive = True
        self.last_shot_time = 0

    def move(self, keys_pressed):
        if keys_pressed[pygame.K_a] and self.rect.left - VEL > 0:
            self.rect.x -= VEL
        if keys_pressed[pygame.K_d] and self.rect.right + VEL < SCREEN_WIDTH:
            self.rect.x += VEL
        if keys_pressed[pygame.K_w] and self.rect.top - VEL > 0:
            self.rect.y -= VEL
        if keys_pressed[pygame.K_s] and self.rect.bottom + VEL < SCREEN_HEIGHT:
            self.rect.y += VEL

    def shoot(self, current_time):
        if current_time - self.last_shot_time > FIRE_COOLDOWN:
            bullet_x = self.rect.centerx - 5
            bullet_y = self.rect.top - 20
            self.last_shot_time = current_time
            shoot_sound.play()
            return Bullet(bullet_x, bullet_y, direction='up')

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
            self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 5
        ratio = self.health / self.max_health
        current_width = int(bar_width * ratio)
        x = self.rect.x
        y = self.rect.y - bar_height - 2
        # Red background bar
        pygame.draw.rect(surface, (RED), (x, y, bar_width, bar_height))
        # Green current health bar
        pygame.draw.rect(surface, (GREEN), (x, y, current_width, bar_height))

class Enemy:

    # Initialize new objects atomaticlly
    def __init__(self, x=150, y=200, width=50, height=50, image_path='enemy_1.png', max_health=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path)), (width, height))
        self.health = max_health
        self.max_health = max_health
        self.VEL = 3
        self.alive = True
        self.fire_cooldown = 1000
        self.last_shot_time = 0

    def move(self, screen_width):
        self.rect.x += self.VEL
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.VEL *= -1

    def shoot(self, current_time):
        if current_time - self.last_shot_time > self.fire_cooldown:
            bullet_width, bullet_height = 10, 20
            bullet_x = self.rect.centerx - (bullet_width // 2)
            bullet_y = self.rect.bottom
            self.last_shot_time = current_time
            shoot_sound.play()
            return Bullet(bullet_x, bullet_y, width=bullet_width, height=bullet_height, direction='down')

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
            self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 5
        health_ratio = self.health / self.max_health
        current_width = int(bar_width * health_ratio)
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 2
        pygame.draw.rect(surface, (RED), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (GREEN), (bar_x, bar_y, current_width, bar_height))

class Enemy_2:

    # Initialize new objects atomaticlly
    def __init__(self, x=150, y=200, width=50, height=50, image_path='enemy_1.png', max_health=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path)), (width, height))
        self.health = max_health
        self.max_health = max_health
        self.VEL = -3
        self.alive = True
        self.fire_cooldown = 1000
        self.last_shot_time = 0

    def move(self, screen_width):
        self.rect.x += self.VEL
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.VEL *= -1

    def shoot(self, current_time):
        if current_time - self.last_shot_time > self.fire_cooldown:
            bullet_width, bullet_height = 10, 20
            bullet_x = self.rect.centerx - (bullet_width // 2)
            bullet_y = self.rect.bottom
            self.last_shot_time = current_time
            shoot_sound.play()
            return Bullet(bullet_x, bullet_y, width=bullet_width, height=bullet_height, direction='down')
        

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
            self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 5
        health_ratio = self.health / self.max_health
        current_width = int(bar_width * health_ratio)
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 2
        pygame.draw.rect(surface, (RED), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (GREEN), (bar_x, bar_y, current_width, bar_height))

class Enemy_boss:

    # Initialize new objects atomaticlly
    def __init__(self, x=45, y=100, width=100, height=100, image_path='boss.png', max_health=200):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path)), (width, height))
        self.health = max_health
        self.max_health = max_health
        self.VEL = -5
        self.alive = True
        self.fire_cooldown = 1000
        self.last_shot_time = 0

    def move(self, screen_width):
        self.rect.x += self.VEL
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.VEL *= -1

    def shoot(self, current_time):
        if current_time - self.last_shot_time > self.fire_cooldown:
            bullet_width, bullet_height = 40, 80
            bullet_x = self.rect.centerx - (bullet_width // 2)
            bullet_y = self.rect.bottom
            self.last_shot_time = current_time
            shoot_sound.play()
            return Bullet(bullet_x, bullet_y, width=bullet_width, height=bullet_height, direction='down')
        
    
    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
            self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 5
        health_ratio = self.health / self.max_health
        current_width = int(bar_width * health_ratio)
        bar_x = self.rect.x
        bar_y = self.rect.y - bar_height - 2
        pygame.draw.rect(surface, (RED), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (GREEN), (bar_x, bar_y, current_width, bar_height))

def draw_window(player, enemy, enemy_2, enemy_boss, enemy_boss_bullets, player_bullets, enemy_bullets, enemy_2_bullets, game_over, game_won):
    
    # Draw background
    screen.blit(background_image, (0, 0))
    
    # Draw player
    if player.alive:
        player.draw(screen)
        player.draw_health_bar(screen)
    
    # Draw enemy
    if enemy.alive:
        enemy.draw(screen)
        enemy.draw_health_bar(screen)
    
    # Draw enemy_2
    if enemy_2.alive:
        enemy_2.draw(screen)
        enemy_2.draw_health_bar(screen)
    
    # Draw boss
    if enemy_boss.alive:
        enemy_boss.draw(screen)
        enemy_boss.draw_health_bar(screen)

    # Draw player bullets
    for bullet in player_bullets:
        bullet.draw(screen)
    
    # Draw enemy bullets
    for bullet in enemy_bullets:
        bullet.draw(screen)
    
    # Draw enemy_2 bullets
    for bullet in enemy_2_bullets:
        bullet.draw(screen)
    
    # Draw boss bullets
    for bullet in enemy_boss_bullets:
        bullet.draw(screen)
    
    # Render "Game Over" text
    if game_over:
        over_text = font.render("Game Over", True, (RED))
        over_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(over_text, over_rect)
        pygame.display.update()
        return
    
     # Render "Game won" text
    if game_won:
        congrats_text = font.render("Congratulations! You Win!", True, (GREEN))
        congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(congrats_text, congrats_rect)
        pygame.display.update()
        return
    pygame.display.update()

def main():

    # Calling the classes
    player = Player()
    enemy = Enemy()
    enemy_2 = Enemy_2()
    boss = Enemy_boss()

    # Bullet lists
    player_bullets = []
    enemy_bullets = []
    enemy_2_bullets = []
    boss_bullets = []


    game_won = False  # Flag to track win condition
    game_over = False # Flag to track loss conditions
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        current_time = pygame.time.get_ticks()
        keys_pressed = pygame.key.get_pressed()

        # Player movement and shooting
        if player.alive:
            player.move(keys_pressed)
        if keys_pressed[pygame.K_SPACE]:
            new_bullet = player.shoot(current_time)
            if new_bullet:
                player_bullets.append(new_bullet)

        # Move player's bullets
        for b in player_bullets[:]:
            b.move()
            if b.off_screen():
                player_bullets.remove(b)


        # Enemy movement and shooting
        if enemy.alive:
            enemy.move(SCREEN_WIDTH)
            bullet = enemy.shoot(current_time)
            if bullet:
                enemy_bullets.append(bullet)

        # Move enemy bullets
        for b in enemy_bullets[:]:
            b.move()
            if b.off_screen():
                enemy_bullets.remove(b)

        # Enemy_2 movement and shooting
        if enemy_2.alive:
            enemy_2.move(SCREEN_WIDTH)
            bullet = enemy_2.shoot(current_time)
            if bullet:
                enemy_2_bullets.append(bullet)

        # Move enemy_2 bullets
        for b in enemy_2_bullets[:]:
            b.move()
            if b.off_screen():
                enemy_2_bullets.remove(b)

        # Boss movement and shooting
        if boss.alive:
            boss.move(SCREEN_WIDTH)
            boss_bullet = boss.shoot(current_time)
            if boss_bullet:
                boss_bullets.append(boss_bullet)

        # Move boss bullets
        for b in boss_bullets[:]:
            b.move()
            if b.off_screen():
                boss_bullets.remove(b)

        # Collisions: Player bullets with enemy
        for b in player_bullets[:]:
            if enemy.alive and b.rect.colliderect(enemy.rect): # Bullet rectangle overlap with the enemy
                enemy.health -= 5
                hit_sound.play()
                player_bullets.remove(b)
                if enemy.health <= 0:
                    enemy.alive = False

        # Collisions: Player bullets with boss
        for b in player_bullets[:]:
            if boss.alive and b.rect.colliderect(boss.rect): # Bullet rectangle overlap with the boss
                boss.health -= 5
                hit_sound.play()
                player_bullets.remove(b)
                if boss.health <= 0:
                    boss.alive = False

        # Collisions: Player bullets with enemy_2
        for b in player_bullets[:]:
            if enemy_2.alive and b.rect.colliderect(enemy_2.rect): # Bullet rectangle overlap with the enemy_2
                enemy_2.health -= 5
                hit_sound.play()
                player_bullets.remove(b)
                if enemy_2.health <= 0:
                    enemy_2.alive = False

        # Collisions: Enemy bullets with player
        for b in enemy_bullets[:]:
            if b.rect.colliderect(player.rect): # Bullet rectangle overlap with the player
                player.health -= 10
                hit_sound.play()
                enemy_bullets.remove(b)
                if player.health <= 0:
                    game_over = True
                    player.alive = False
        
        # Collisions: Enemy_2 bullets with player
        for b in enemy_2_bullets[:]:
            if b.rect.colliderect(player.rect): # Bullet rectangle overlap with the player
                player.health -= 10
                hit_sound.play()
                enemy_2_bullets.remove(b)
                if player.health <= 0:
                    game_over = True


        # Collisions: Boss bullets with player
        for b in boss_bullets[:]:
            if b.rect.colliderect(player.rect): # Bullet rectangle overlap with the player
                player.health -= 10
                hit_sound.play()
                boss_bullets.remove(b)
                if player.health <= 0:
                    game_over = True


        # Victory condition: both enemies and boss defeated
        if not enemy.alive and not enemy_2.alive and not boss.alive:
                game_won = True


        # Draw window
        draw_window(player, enemy, enemy_2, boss, boss_bullets, player_bullets, enemy_bullets, enemy_2_bullets, game_over, game_won)
    pygame.quit()

if __name__ == "__main__":
    main()
