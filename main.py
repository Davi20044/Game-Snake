import pygame
import random

# Inicializando o Pygame
pygame.init()

# Definindo cores
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (128, 128, 128)

# Obtendo informações da tela
screen_info = pygame.display.Info()
dis_width = screen_info.current_w
dis_height = screen_info.current_h

# Calculando o tamanho do bloco da cobra e da comida
snake_block = int(min(dis_width, dis_height) / 10)
food_block = snake_block

# Calculando o tamanho da área de jogo
game_area_width = snake_block * 10
game_area_height = snake_block * 10

# Calculando a posição inicial da área de jogo
game_area_x = (dis_width - game_area_width) // 2
game_area_y = (dis_height - game_area_height) // 2

# Criando a tela em tela cheia
dis = pygame.display.set_mode((dis_width, dis_height), pygame.FULLSCREEN)
pygame.display.set_caption('Jogo da Cobrinha')

clock = pygame.time.Clock()

snake_speed = 5

# Definindo fontes
font_size = int(dis_width / 20)
font_style = pygame.font.SysFont("bahnschrift", font_size)
score_font = pygame.font.SysFont("comicsansms", font_size)


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color, y_displacement=0):
    mesg = font_style.render(msg, True, color)
    text_width = mesg.get_width()
    text_height = mesg.get_height()
    dis.blit(mesg, [(dis_width - text_width) // 2, (dis_height - text_height) // 2 + y_displacement])


def show_score(score):
    score_text = score_font.render("Pontuação: " + str(score), True, black)
    dis.blit(score_text, [game_area_x, game_area_y - 40])


def generate_food(snake_list):
    while True:
        foodx = round(random.randrange(0, game_area_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, game_area_height - snake_block) / snake_block) * snake_block
        if [foodx, foody] not in snake_list:
            return foodx, foody


def gameLoop():
    game_over = False
    game_close = False

    # Posição inicial da cobra
    x1 = game_area_width / 2
    y1 = game_area_height / 2

    # Mudança de coordenadas da cobra
    x1_change = 0
    y1_change = 0

    # Lista de corpo da cobra e comprimento inicial
    snake_List = []
    Length_of_snake = 1

    # Posição aleatória da comida
    foodx, foody = generate_food(snake_List)

    # Direção inicial da cobra (parado)
    direction = "STOP"

    # Pontuação
    score = 0

    # Recorde
    high_score = 0

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("Você Perdeu! Pressione C-Play Novamente ou Q-Sair", red)
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if direction != "RIGHT":
                        x1_change = -snake_block
                        y1_change = 0
                        direction = "LEFT"
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if direction != "LEFT":
                        x1_change = snake_block
                        y1_change = 0
                        direction = "RIGHT"
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    if direction != "DOWN":
                        y1_change = -snake_block
                        x1_change = 0
                        direction = "UP"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if direction != "UP":
                        y1_change = snake_block
                        x1_change = 0
                        direction = "DOWN"

        if x1 >= game_area_width or x1 < 0 or y1 >= game_area_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, gray, [0, 0, dis_width, dis_height])
        pygame.draw.rect(dis, green, [game_area_x, game_area_y, game_area_width, game_area_height])

        # Verificar se a comida está dentro da cobra
        while [foodx, foody] in snake_List:
            foodx, foody = generate_food(snake_List)

        pygame.draw.rect(dis, red, [game_area_x + foodx, game_area_y + foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(game_area_x + x1)
        snake_Head.append(game_area_y + y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)
            Length_of_snake += 1
            score += 1
            if score > high_score:
                high_score = score

        clock.tick(snake_speed)

    return high_score


def gameMenu():
    menu_exit = False
    high_score = 0

    while not menu_exit:
        dis.fill(blue)
        message("Bem-vindo ao Jogo da Cobrinha", green, y_displacement=-50)
        message("Pressione P-Jogar ou Q-Sair", black, y_displacement=50)
        message(f"Recorde anterior: {high_score}", black, y_displacement=100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:
                    high_score = gameLoop()


gameMenu()
