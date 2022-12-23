'''python3 get-pip.py
python3 -m pip install pygame --user'''
import pygame

pygame.init()
wind = pygame.display.set_mode((500, 500))   #окно

pygame.display.set_caption("Survival Game")   #заголовок окна


walkRight = [pygame.image.load('images/right_1.png').convert_alpha(),
pygame.image.load('images/right_2.png').convert_alpha(), pygame.image.load('images/right_3.png').convert_alpha(),
pygame.image.load('images/right_4.png').convert_alpha(), pygame.image.load('images/right_5.png').convert_alpha(),
pygame.image.load('images/right_6.png').convert_alpha()]
walkLeft = [pygame.image.load('images/left_1.png').convert_alpha(),
pygame.image.load('images/left_2.png').convert_alpha(), pygame.image.load('images/left_3.png').convert_alpha(),
pygame.image.load ('images/left_4.png').convert_alpha(), pygame.image.load('images/left_5.png').convert_alpha(),
pygame.image.load('images/left_6.png').convert_alpha()]

label = pygame.font.Font('fonts/Roboto-Black.ttf', 40)
lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
restart_label = label.render('Играть заново.', False, (200, 50, 50))
restart_label_rect = restart_label.get_rect(topleft=(100, 250))

gameplay = True
bg = pygame.image.load('images/bg.png').convert_alpha()
playerStand = pygame.image.load('images/idle.png').convert_alpha()

ghost_list = []
ghost = pygame.image.load('images/ghost.png').convert_alpha()
clock = pygame.time.Clock()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

x = 50
y = 405
widht = 72
height = 97
speed = 5
isJump = False
jumpCount = 10
run = True
left = False
right = False
animCount = 0
bullets = []
lastMove = "right"
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets_left = 5



def drawWindow():      #вывод изображения на экран
    """Функция заливает экран игры фоном и выводит на него анимацию передвижения персонажа.Анимация
     происходит при помощи покадрового перемещения и переключения картинок. Выставлена частота обновлений
      равная 30 кадрам в секунду."""
    global animCount
    wind.blit(bg, (0, 0))

    if animCount + 1 >= 30:
        animCount = 0
    if left:
        wind.blit(walkLeft[animCount // 5], (x, y))
        animCount += 1
    elif right:
        wind.blit(walkRight[animCount // 5], (x, y))
        animCount += 1
    else:
        wind.blit(playerStand, (x, y))

    pygame.display.update()


def ghostprinter():
    """Функция отвечает за вывод приведений на экран.Функция достает приведение из  списка и передвигает
    его по экрану по координате х, при этом ,когда приведение выходит за экран- оно удаляется.
    Так же функция отслеживает соприкосновение невидимой рамки вокруг персонажа с невидимой рамкой
    вокруг приведения. И когда происходит соприкосновение, игра завершается и выводится экран проигрыша."""
    global gameplay
    global ghost_list
    if ghost_list:
        for (i, el) in enumerate(ghost_list):
            wind.blit(ghost, el)
            el.x -= 6.5

            if el.x < -10:
                ghost_list.pop(i)

            if player_rect.colliderect(el):
                gameplay = False
    pygame.display.update()

def bulletsprinter():
    """Функция, которая достает из списка bullets патроны и вырисовывает их на экране игры wind меняя
     ее координату по оси x, дабы пуля летела горизонтально.А также функция отслеживает соприкосновение
     невидимой рамки вокруг пули и вокруг приведения.И при наличии соприкосновения удаляет пулю и
     приведение по их индексам.Так же функця вводит ограничения для максимального количества патрогнов
     на экране."""
    global bullets_left
    if bullets:
        for (i, el) in enumerate(bullets):
            wind.blit(bullet, (el.x, el.y))
            el.x += 10

            if el.x > 500:
                bullets.pop(i)
                bullets_left += 1

            if ghost_list:
                for (index, ghost_el) in enumerate(ghost_list):
                    if el.colliderect(ghost_el):
                        ghost_list.pop(index)
                        bullets.pop(i)
                        bullets_left += 1
    pygame.display.update()




if __name__ == '__main__':
    while run:  # цикл для работы/остановки игры
        clock.tick(30)

        if gameplay:
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and x > 5:  # передвижение с ограничением в окно
                x -= speed
                left = True
                right = False
                lastMove = "left"
            elif keys[pygame.K_RIGHT] and x < 500 - widht - 5:
                x += speed
                left = False
                right = True
                lastMove = "right"
            else:
                left = False
                right = False
                animCount = 0
            if not (isJump):
                if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                    isJump = True
            else:
                if jumpCount >= -10:  # реализация прыжка
                    if jumpCount < 0:
                        y += (jumpCount ** 2) / 2
                    else:
                        y -= (jumpCount ** 2) / 2
                    jumpCount -= 1
                else:
                    isJump = False
                    jumpCount = 10

            drawWindow()
            ghostprinter()
            bulletsprinter()
        else:
            wind.fill((87, 88, 89))
            wind.blit(lose_label, (100, 100))
            wind.blit(restart_label, restart_label_rect)

            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                ghost_list.clear()
                x = 0
                bullets.clear()
                bullets_left = 5

        pygame.display.update()
        player_rect = walkLeft[0].get_rect(topleft=(x, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == ghost_timer:
                ghost_list.append(ghost.get_rect(topleft=(500, 425)))

            if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_f and bullets_left > 0:
                bullets.append(bullet.get_rect(topleft=(x + 20, y + 20)))
                bullets_left -= 1
    pygame.quit()
