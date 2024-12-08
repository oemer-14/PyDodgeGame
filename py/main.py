import pygame  # import pygame
import time
import random
pygame.font.init()

# creating the window
WIDTH, HEIGHT = 1400, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # set window size
pygame.display.set_caption("Space Dodge") # set caption on top of the window

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT)) # image for background
# scale the image for full window size if image is to small 

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5 # player velocity 
STAR_VEL = 3  # star velocity 

STAR_WIDTH = 10
STAR_HEIGHT = 20

FONT = pygame.font.SysFont("comicsans", 30) # font art for timer

def draw(player, elapsed_time, stars): # function to draw in the window to show game actions
    WIN.blit(BG, (0,0)) # background image

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white") # timer left-side on top
    WIN.blit(time_text, (10, 10)) # show the time in the window

    pygame.draw.rect(WIN, "white", player) # show player

    for star in stars:
        pygame.draw.rect(WIN, "red", star) # show the "enemies"

    pygame.display.update()

def main(): # main function
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) # for moving the character

    clock = pygame.time.Clock() # for speed of character

    start_time = time.time() # start time for timer - starts with 0
    elapsed_time = 0

    star_add_increment = 2000  # enemies
    star_count = 0

    stars = []  # list
    hit = False

    while run:  # game loop
        star_count += clock.tick(80) 
        elapsed_time = time.time() - start_time # seconds that elapsed since the game started 

        if star_count > star_add_increment: # for adding more enemies
            for _ in range(6):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)    
            star_count = 0

        for event in pygame.event.get(): # event type
            if event.type == pygame.QUIT:  # if X button is pressed for closing the window
                run = False # run will be set to False
                break
        
        keys = pygame.key.get_pressed() # move character
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0: # left side, make sure that there is a limit on the left
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH: # right side, make sure that there is a limit on the right
            player.x += PLAYER_VEL

        for star in stars[:]: # copy of the list
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit: # check if player was hit by enemie
            lost_text = FONT.render("You Lost!", 1, "white") # text that game ended 
            # record_text = FONT.render("Record: %d", last_score, "white")

            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
             # WIN.blit(record_text, (WIDTH/4 - record_text.get_width()/4, HEIGHT/4 - record_text.get_height()/4))
            pygame.display.update() # update window
            pygame.time.delay(4000) # delay to see that the game is over
            break

        draw(player, elapsed_time, stars) # call function draw

    pygame.quit() # game closed 

if __name__ == "__main__":  # call the main function 
    events = pygame.event.get()
    if events:
        main()

