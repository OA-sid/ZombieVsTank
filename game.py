import pgzrun
import random

TITLE = "Zombies vs Tanks"
WIDTH = 600
HEIGHT = 440

UP = 180
DOWN = 0
LEFT = 270
RIGHT = 90
BULLET_SPEED = 10

blue_tank = Actor("tank_blue.png")
blue_tank.x = WIDTH / 2
blue_tank.y = HEIGHT / 2

bullet = Actor("bulletblue")
bullet_fired = False

zombie_list = []
ZOMBIE_SPEED = 1.0

score = 0
game_over = False
zombie_count = 2  

game_state = "start"  

def draw():
    if game_state == "start":
        screen.fill((10, 30, 50))
        screen.draw.text("ZOMBIES VS TANKS", (70, 100), fontsize=60, color="lime")
        screen.draw.text("Press ENTER to Start", (150, 250), fontsize=40, color="white")
        screen.draw.text("Use arrow keys to move", (160, 300), fontsize=30, color="yellow")
        screen.draw.text("Press SPACE to shoot", (170, 350), fontsize=30, color="yellow")
    elif game_state == "playing":
        screen.blit("bg.jpg", (0, 0))
        blue_tank.draw()
        if bullet_fired:
            bullet.draw()
        for zomb in zombie_list:
            zomb.draw()
        screen.draw.text(f"Score: {score}", (350, 150), fontsize=30, color="white")
    elif game_state == "game_over":
        screen.fill("blue")
        screen.draw.text(f"GAME OVER, Your Score: {score}", (150, 200), fontsize=40, color="white")
        screen.draw.text("Returning to Start Screen...", (130, 250), fontsize=20, color="white")

def update():
    global bullet_fired, game_state, game_over, score, zombie_list, bullet

    if game_state == "start":
        if keyboard.RETURN:
            game_state = "playing"
            score = 0
            game_over = False
            zombie_list.clear()
            clock.schedule(create_zombies, 2)
            clock.schedule(increase_zombie_count, 10)

    elif game_state == "playing":
        if keyboard.left: 
            blue_tank.x -= 5 
            blue_tank.angle = LEFT 
        if keyboard.right:
            blue_tank.x += 5
            blue_tank.angle = RIGHT
        if keyboard.up:
            blue_tank.y -= 5
            blue_tank.angle = UP
        if keyboard.down:
            blue_tank.y += 5
            blue_tank.angle = DOWN
        if keyboard.space:
            if not bullet_fired:
                bullet_fired = True
                sounds.laserretro_004.play()
                if blue_tank.angle == LEFT:
                    bullet.x = blue_tank.x - 30
                    bullet.y = blue_tank.y
                elif blue_tank.angle == RIGHT:
                    bullet.x = blue_tank.x + 30
                    bullet.y = blue_tank.y
                elif blue_tank.angle == DOWN:
                    bullet.x = blue_tank.x
                    bullet.y = blue_tank.y + 30
                elif blue_tank.angle == UP:
                    bullet.x = blue_tank.x
                    bullet.y = blue_tank.y - 30

        if game_over:
            game_state = "game_over"
            clock.schedule_unique(return_to_start, 3)  # Return to start screen after 3 seconds

    elif game_state == "game_over":
        pass  # Do nothing while waiting to return to the start screen

def shoot_bullet():
    global bullet_fired
    if bullet_fired:
        if blue_tank.angle == LEFT:
            bullet.x -= BULLET_SPEED
        elif blue_tank.angle == RIGHT:
            bullet.x += BULLET_SPEED
        elif blue_tank.angle == DOWN:
            bullet.y += BULLET_SPEED
        elif blue_tank.angle == UP:
            bullet.y -= BULLET_SPEED

        # Check if the bullet is off the screen
        if bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:
            bullet_fired = False  # Reset the bullet

def create_zombies():
    global zombie_count
    if game_state == "playing":  # Only create zombies if the game is playing
        for _ in range(zombie_count):
            loc_rand = random.randint(0, 3)
            z = Actor("zombie.png")
            if loc_rand == 0:
                z.x = 0
                z.y = random.randint(40, HEIGHT - 40)
            elif loc_rand == 1:
                z.x = WIDTH
                z.y = random.randint(40, HEIGHT - 40)
            elif loc_rand == 2:
                z.y = 0
                z.x = random.randint(40, WIDTH - 40)
            elif loc_rand == 3:
                z.y = HEIGHT
                z.x = random.randint(40, WIDTH - 40)
            zombie_list.append(z)

        clock.schedule_unique(create_zombies, 5)  # Schedule next wave of zombies in 5 seconds

def increase_zombie_count():
    global zombie_count
    if game_state == "playing":  # Only increase zombie count if the game is playing
        zombie_count += 2  # Increase the number of zombies by 2
        clock.schedule(increase_zombie_count, 10)  # Schedule to increase again in 10 seconds

def move_zombies():
    global score, game_over, bullet_fired
    if game_state == "playing":  # Only move zombies if the game is playing
        for zomb in zombie_list[:]:  # Use a slice to avoid issues when removing items
            # Move zombie towards the tank
            if zomb.x < blue_tank.x:
                zomb.x += ZOMBIE_SPEED
            elif zomb.x > blue_tank.x:
                zomb.x -= ZOMBIE_SPEED
            if zomb.y < blue_tank.y:
                zomb.y += ZOMBIE_SPEED
            elif zomb.y > blue_tank.y:
                zomb.y -= ZOMBIE_SPEED

            # Check collision with bullet
            if bullet_fired and zomb.colliderect(bullet):
                zombie_list.remove(zomb)
                bullet_fired = False  # Reset bullet after hitting a zombie
                score += 1

            # Check collision with the tank
            if zomb.colliderect(blue_tank):
                game_over = True

def return_to_start():
    global game_state, blue_tank, bullet_fired, zombie_list, score, game_over, zombie_count

    # Reset the game variables
    blue_tank.x = WIDTH / 2
    blue_tank.y = HEIGHT / 2
    blue_tank.angle = UP  # Default angle
    bullet_fired = False
    bullet.x = blue_tank.x  # Reset bullet position
    bullet.y = blue_tank.y
    zombie_list.clear()  # Clear the zombies
    score = 0  # Reset the score
    zombie_count = 2  # Reset the zombie count to the initial value
    game_over = False

    game_state = "start"

clock.schedule_interval(shoot_bullet, 0.001)  # Check bullet movement every 0.1 second
clock.schedule_interval(move_zombies, 0.1)  # Move zombies every 0.1 second
pgzrun.go()
