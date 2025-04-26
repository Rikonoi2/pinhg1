from pygame import *  # Импортируем всю библиотеку PyGame, чтобы иметь доступ ко всем её модулям и функциям.

'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):  # Создаем класс GameSprite, наследуя его от встроенного класса Sprite из PyGame.
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):  # Конструктор класса принимает имя файла изображения, начальную позицию (x,y), скорость и размеры изображения.
        super().__init__()  # Вызываем конструктор родительского класса Sprite.
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (width, height))  # Загружаем изображение и масштабируем его до заданных размеров.
        self.speed = player_speed  # Сохраняем скорость передвижения спрайта.
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()  # Получаем объект Rect (прямоугольник), соответствующий размеру изображения.
        self.rect.x = player_x  # Устанавливаем положение спрайта по оси x.
        self.rect.y = player_y  # Устанавливаем положение спрайта по оси y.

    def reset(self):  # Метод для вывода спрайта на экран.
        window.blit(self.image, (self.rect.x, self.rect.y))  # Рисуем изображение спрайта на окне игры в указанном месте.

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):  # Новый класс Player, наследующий свойства и методы класса GameSprite.
    def update_r(self):  # Обработка движений правой ракетки (правого игрока).
        keys = key.get_pressed()  # Проверка нажатых клавиш.
        if keys[K_UP] and self.rect.y > 5:  # Если нажата клавиша вверх и позиция ракеты больше верхнего края окна.
            self.rect.y -= self.speed  # Ракетка двигается вверх.
        if keys[K_DOWN] and self.rect.y < win_height - 80:  # Если нажата клавиша вниз и ракета ниже нижнего края окна.
            self.rect.y += self.speed  # Ракетка двигается вниз.
            
    def update_l(self):  # Аналогично предыдущему методу, но для левого игрока.
        keys = key.get_pressed()  # Проверка нажатых клавиш.
        if keys[K_w] and self.rect.y > 5:  # Движение вверх по клавише 'W'.
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:  # Движение вниз по клавише 'S'.
            self.rect.y += self.speed

#Игровая сцена:
back = (200, 255, 255)  # Цвет фона игры RGB (светло-голубой оттенок).
win_width = 600  # Ширина окна игры.
win_height = 500  # Высота окна игры.
window = display.set_mode((win_width, win_height))  # Создание окна игры заданного размера.
window.fill(back)  # Заполнение окна цветом фона.

#флаги отвечающие за состояние игры
game = True  # Флаг продолжения игры.
finish = False  # Флаг завершения игры.
clock = time.Clock()  # Объект часов для синхронизации кадров.
FPS = 60  # Количество кадров в секунду.
#Звуки
mixer.init()
mixer.music.load('de144d31b1f3b3f.mp3')
mixer.music.play()
fire = mixer.Sound('otskok-myacha.mp3')
#создания мяча и ракетки   
racket1 = Player('racket.png', 30, 200, 4, 50, 150)  # Левая ракетка (игрок 1).
racket2 = Player('racket.png', 520, 200, 4, 50, 150)  # Правая ракетка (игрок 2).
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)  # Мяч.

font.init()  # Инициализируем модуль шрифтов PyGame.
font = font.Font(None, 35)  # Создаем шрифт размером 35 пикселей.
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))  # Текст о поражении игрока 1.
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))  # Текст о поражении игрока 2.

speed_x = 3  # Начальная горизонтальная скорость мяча.
speed_y = 3  # Начальная вертикальная скорость мяча.

while game:  # Основной игровой цикл.
    for e in event.get():  # Обрабатываем события (например, закрытие окна).
        if e.type == QUIT:  # Если событие закрытия окна.
            game = False  # Завершаем игру.
    
    if finish != True:  # Пока игра продолжается...
        window.fill(back)  # Очищаем окно, заполняя фоновым цветом.
        racket1.update_l()  # Обновляем положение левой ракетки.
        racket2.update_r()  # Обновляем положение правой ракетки.
        ball.rect.x += speed_x  # Перемещаем мяч по горизонтали.
        ball.rect.y += speed_y  # Перемещаем мяч по вертикали.

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):  # Если мяч столкнулся с одной из ракеток.
            speed_x *= -1  # Меняем направление движения мяча по горизонтали.
            speed_y *= 1   # Оставляем прежнее вертикальное направление.
            fire.play()
        
        # если мяч достиг верхней или нижней границы экрана, отражаем его обратно
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1  # Изменение направления движения мяча по вертикали.
            fire.play()

        # проверка вылета мяча за пределы поля
        if ball.rect.x < 0:  # Если мяч ушел за левый край поля.
            finish = True  # Заканчиваем игру.
            window.blit(lose1, (200, 200))  # Показываем надпись поражения игрока 1.
            game_over = True  # Опциональный флаг окончания игры (не влияет на дальнейшую работу).

        if ball.rect.x > win_width:  # Если мяч ушел за правый край поля.
            finish = True  # Заканчиваем игру.
            window.blit(lose2, (200, 200))  # Показываем надпись поражения игрока 2.
            game_over = True  # Опциональный флаг окончания игры (не влияет на дальнейшую работу).

        racket1.reset()  # Перерисовываем первую ракетку.
        racket2.reset()  # Перерисовываем вторую ракетку.
        ball.reset()     # Перерисовываем мяч.

    display.update()  # Обновляем экран (перерисовка всего содержимого окна).
    clock.tick(FPS)  # Регулируем частоту обновления кадра (60 FPS).
