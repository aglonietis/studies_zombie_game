import pygame
import constants as c
import player
import zombieHorde as zh

# Set Game Running
running = True

# Initialize the game
pygame.init()

# Set title
pygame.display.set_caption(c.TITLE)

# Set Icon
icon = pygame.image.load('resources/default/zombieIcon.png')
pygame.display.set_icon(icon)

# Init Text drawing
pygame.font.init()


# Create the screen
screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT),pygame.FULLSCREEN)

game_active = False
active = True
start_font = pygame.font.SysFont('Times New Roman', 50)
startGameText = start_font.render("START GAME!", False, c.TEXT_COLOR)
clock = pygame.time.Clock()

last_game = False
last_result = 0


while active:

    screen.fill(c.SCREEN_COLOR)
    screen.blit(startGameText, ((c.WIDTH - startGameText.get_width()) / 2, (c.HEIGHT - startGameText.get_height()) / 2))

    if last_game:
        lastResultText = start_font.render("Points gained in last game: %d" % (last_result,), False, c.TEXT_COLOR)
        screen.blit(lastResultText, (
            (c.WIDTH - lastResultText.get_width()) / 2,
            ((c.HEIGHT + lastResultText.get_height() / 2 + startGameText.get_height()) / 2)
        ))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                active = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_active = True

    if game_active:
        last_game = True
        my_font = pygame.font.SysFont('Times New Roman', 30)
        playerObject = player.Player()
        zombies = zh.ZombieHorde()
        running = True
        while running:
            screen.fill(c.SCREEN_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key in playerObject.keys:
                        playerObject.act(event)
                if event.type == pygame.KEYUP:
                    if event.key in playerObject.keys:
                        playerObject.act(event)
            playerObject.run(screen)
            playerObject.injure(zombies.check(playerObject))
            zombies.run(screen, playerObject)
            zombies.remove_killed(playerObject.calculate_killed(zombies))

            if playerObject.health <= c.MIN_HEALTH:
                running = False

            playerObject.draw_info(screen, my_font)
            pygame.display.update()
            clock.tick(c.FRAMES_PER_SECOND)
        last_result = playerObject.points
        game_active = False
    pygame.display.update()
    clock.tick(c.FRAMES_PER_SECOND)


