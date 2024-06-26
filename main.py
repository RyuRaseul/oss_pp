import pygame
import random

#기본 상수 정의
fps = 60                #게임의 fps
field_width = 9        #게임판 너비
field_height = 9       #게임판 높이
mines = 10              #지뢰 갯수
tile_size = 40          #타일 크기
screen_width = tile_size * field_width     #창 너비
screen_height = tile_size * field_height    #창 높이
game_over = False
game_win = False
#기본 상수 정의

#################################
#############PHASE2##############
#################################
pygame.init()

flag_mark = '|>'

game_state = 1
# 0 == 게임 진행 중, 1 == 난이도 정하기, 2 == 설정창

screen_set = 0
# screen size 변경을 위한 변수
# 0 = 변경 가능, 1 = 변경 불가

level_font = pygame.font.Font(None, 30)
easy_text = level_font.render("Easy", True, 30)
easy_rect = easy_text.get_rect(center = (180 ,90))
normal_text = level_font.render("Normal", True, 30)
normal_rect = normal_text.get_rect(center = (180 ,170))
hard_text = level_font.render("Hard", True, 30)
hard_rect = hard_text.get_rect(center = (180 ,250))
level = ""

block_x_size = 0
block_y_size = 0


#################################
#############PHASE2##############
#################################



#색상 정의
black = (0, 0, 0)           #8
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0, 0)           #7
redgreen = (255, 170, 0)    #6
greenred = (170, 255, 0)    #5
green = (0, 255, 0)         #4
greenblue = (0, 255, 170)   #3
bluegreen = (0, 170, 255)   #2
blue = (0, 0, 255)          #1
#색상 정의

#게임판
field = []          #숫자와 지뢰의 위치정보, 0~8은 주변칸의 지뢰 갯수, 9는 지뢰
field_cover = []    #가림막 정보, 0은 공개된 위치, 1은 가려진 위치
#게임판

#해당 칸의 지뢰 여부 판별
def isMine(x, y):
    return (field[x][y] == 9)
#해당 칸의 지뢰 여부 판별

#주변의 지뢰 갯수 세기
def countMine(x, y):
    count = 0
    if(x != 0):
        if(isMine(x - 1, y)):
            count += 1

        if(y != 0):
            if(isMine(x - 1, y - 1)):
                count += 1
        
        if(y != field_height - 1):
            if(isMine(x - 1, y + 1)):
                count += 1

    if(x != field_width - 1):
        if(isMine(x + 1, y)):
            count += 1

        if(y != 0):
            if(isMine(x + 1, y - 1)):
                count += 1

        if(y != field_height - 1):
            if(isMine(x + 1, y + 1)):
                count += 1

    if(y != 0):
        if(isMine(x, y - 1)):
            count += 1

    if(y != field_height - 1):
        if(isMine(x, y + 1)):
            count += 1

    return count
#주변의 지뢰 갯수 세기

#게임판 만들기
def gameSetup():
    #################################
    #############PHASE2##############
    #################################
    global field, field_cover, game_state, mines, field_width, field_height, screen_height, screen_width
    game_state = 0
    if level == 'e':
        field_width = 9
        field_height = 9
        screen_height = tile_size * field_height
        screen_width = tile_size * field_width
        mines = 10
    elif level == 'n':
        field_width = 15
        field_height = 15
        screen_height = tile_size * field_height
        screen_width = tile_size * field_width
        mines = 25
    else:
        field_width = 21
        field_height = 21
        screen_height = tile_size * field_height
        screen_width = tile_size * field_width
        mines = 45
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill(white)
    
    field = []
    field_cover = []
    #################################
    #############PHASE2##############
    #################################
    #게임판 0, 가림막 1로 초기화
    for x in range(0, field_width):
        field.append([])
        field_cover.append([])
        for y in range(0, field_height):
            field[x].append(0)
            field_cover[x].append(1)
    #게임판 0, 가림막 1로 초기화

    #지뢰 위치 설정
    i = 0
    while(i < mines):
        rand = random.randrange(0, field_width * field_height)
        x = rand // field_height
        y = rand % field_height
        if(field[x][y] == 9):
            continue
        i += 1
        field[x][y] = 9
    #지뢰 위치 설정

    #지뢰가 없는 칸에 주변 지뢰 갯수 입력
    for x in range(0, field_width):
        for y in range(0, field_height):
            if(field[x][y] != 9):
                field[x][y] = countMine(x, y)
    #지뢰가 없는 칸에 주변 지뢰 갯수 입력
#게임판 만들기

#게임종료
def gameover(win):
    global game_over, game_win
    game_over = True
    game_win = win
    for x in range(0, field_width):
        for y in range(0, field_height):
            if(isMine(x, y)):
                field_cover[x][y] = 0
#게임종료

#칸 열기
def uncover(x, y):
    #################################
    #############PHASE2##############
    #################################
    if(field_cover[x][y] == 2):
         return
    # Flag Tile은 클릭 방지
    #################################
    #############PHASE2##############
    ################################# 
    #무한재귀 방지
    if(field_cover[x][y] == 0):
        return
    #무한재귀 방지

    field_cover[x][y] = 0

    #해당칸이 0이면 주변칸도 열어야 함
    if(field[x][y] == 0):
        if(x != 0):
            uncover(x - 1, y)

            if(y != 0):
                uncover(x - 1, y - 1)
        
            if(y != field_height - 1):
                uncover(x - 1, y + 1)

        if(x != field_width - 1):
            uncover(x + 1, y)

            if(y != 0):
                uncover(x + 1, y - 1)

            if(y != field_height - 1):
                uncover(x + 1, y + 1)

        if(y != 0):
            uncover(x, y - 1)

        if(y != field_height - 1):
            uncover(x, y + 1)
    #해당칸이 0이면 주변칸도 열어야 함
    
    #해당칸이 지뢰면 게임오버
    elif(isMine(x, y)):
        gameover(False)
    #해당칸이 지뢰면 게임오버

#칸 열기

#승리 확인
def gameWin():
    for x in range(0, field_width):
        for y in range(0, field_height):
            if(field[x][y] != 9 and field_cover[x][y] == 1):
                return False
    return True
#승리 확인

#################################
#############PHASE2##############
#################################
def open_option():
    global block_x_size, block_y_size
    screen.fill(white)
    if level == 'e':
        option_font = pygame.font.Font(None, 32)
        block_x_size = 200 
        block_y_size = 70
    elif level == 'n':
        option_font = pygame.font.Font(None, 48)
        block_x_size = 280
        block_y_size = 120
    else:
        option_font = pygame.font.Font(None, 64)
        block_x_size = 360
        block_y_size = 200
    
    block_y_padding = (screen_height - 3*block_y_size)/4
    restart_op_text = option_font.render("RESTART", True, black)
    restart_op_rect = restart_op_text.get_rect(center = (screen_width/2, block_y_padding + block_y_size/2))
    level_op_text = option_font.render("SELECT LEVEL", True, black)
    level_op_rect = level_op_text.get_rect(center = (screen_width/2, screen_height/2))
    resume_op_text = option_font.render("RESUME", True, black)
    resume_op_rect = resume_op_text.get_rect(center = (screen_width/2, screen_height - block_y_padding - block_y_size/2))
    pygame.draw.rect(screen, black, (screen_width/2 - block_x_size/2, block_y_padding, block_x_size, block_y_size), 4) 
    pygame.draw.rect(screen, black, (screen_width/2 - block_x_size/2, screen_height/2 - block_y_size/2, block_x_size, block_y_size), 4) 
    pygame.draw.rect(screen, black, (screen_width/2 - block_x_size/2, screen_height - block_y_padding - block_y_size, block_x_size, block_y_size), 4) 
    screen.blit(restart_op_text, restart_op_rect)
    screen.blit(level_op_text, level_op_rect)
    screen.blit(resume_op_text, resume_op_rect)
def level_select():
    pygame.draw.rect(screen, black, (100, 60, 160, 60), 4)
    pygame.draw.rect(screen, black, (100, 140, 160, 60), 4)
    pygame.draw.rect(screen, black, (100, 220, 160, 60), 4)
    screen.blit(easy_text, easy_rect)
    screen.blit(normal_text, normal_rect)
    screen.blit(hard_text, hard_rect)

def game_end():
    for x in range(field_width):
        for y in range(field_height):
            if isMine(x, y) and field_cover[x][y] != 2:
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, white, rect)
                mine = 'X'
                color = red
                text = pygame.font.Font(None, 24).render((mine), True, color)
                screen.blit(text, (x * tile_size + 12, y * tile_size + 8))
    end_message_font = pygame.font.Font(None, 50)
    if(game_win):
        end_message_text = end_message_font.render("You WIN!", True, black)
    else:
        end_message_text = end_message_font.render("You LOSE!", True, black)
    end_message_rect = end_message_text.get_rect(center = (screen_width/2, screen_height/2 - 20))
    restart_font = pygame.font.Font(None, 40)
    restart_text = restart_font.render("Restart : Enter", True, black)
    restart_rect = restart_text.get_rect(center = (screen_width/2 , screen_height/2 + 50 - 20))
    quit_font = pygame.font.Font(None, 40)
    quit_text = quit_font.render("Quit : Q", True, black)
    quit_rect = quit_text.get_rect(center = (screen_width/2, screen_height/2 + 80 - 20))
    screen.blit(end_message_text, end_message_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)

def check_flag():
    for x in range(field_width):
        for y in range(field_height):
            if field_cover[x][y] == 0 and 0 < field[x][y] < 9:
                if around_flag_num(x, y) == field[x][y]:
                    if x != 0:
                        uncover(x-1, y)
                        if y != 0:
                            uncover(x-1, y-1)
                        if y != field_height-1:
                            uncover(x-1, y+1)
                    if x != field_width-1:
                        uncover(x+1, y)
                        if y != 0:
                            uncover(x+1, y-1)
                        if y != field_height-1:
                            uncover(x+1, y+1)
                    if y != 0:
                        uncover(x, y-1)
                    if y != field_height - 1:
                        uncover(x, y+1)

def around_flag_num(x, y):
    flag_num = 0
    if x != 0:
        if field_cover[x-1][y] == 2:
        	flag_num += 1
        if y != 0:
            if field_cover[x-1][y-1] == 2:
                flag_num += 1
        if y != field_height-1:
            if field_cover[x-1][y+1] == 2:
                flag_num += 1 
    if x != field_width-1:
        if field_cover[x+1][y] == 2:
            flag_num += 1
        if y != 0:
            if field_cover[x+1][y-1] == 2:
                flag_num += 1
        if y != field_height-1:
            if field_cover[x+1][y+1] == 2:
                flag_num += 1
    if y != 0:
        if field_cover[x][y-1] == 2:
            flag_num += 1
    if y != field_height - 1:
        if field_cover[x][y+1] == 2:
            flag_num += 1
    return flag_num
    
#################################
#############PHASE2##############
#################################
   
#게임 시작
#pygame.init()                           #pygame 라이브러리 초기화
pygame.display.set_caption("minesweeper")  #창 제목 설정
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

running = True
while running:
    #################################
    #############PHASE2##############
    #################################
    if game_state == 1:
        if screen_set == 0:
            field_width = 9
            field_height = 9
            screen_width = field_width * tile_size
            screen_height = field_height * tile_size
            screen = pygame.display.set_mode((screen_width, screen_height))
            screen.fill(white)
            screen_set = 1
            level_select()
    elif game_over == True:
        game_end()
    #################################
    #############PHASE2##############
    #################################
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
        #################################
        #############PHASE2##############
        #################################
        elif event.type == pygame.KEYDOWN:
            if game_over == True:
                if event.key == pygame.K_RETURN:
                    screen_set = 0
                    game_state = 1
                    game_over = False
                    break
                elif event.unicode.upper() == 'Q':
                    running = False
            elif game_over == False:
                if event.key == pygame.K_ESCAPE:
                    if game_state == 0:
                        game_state = 2
                        open_option()
                    elif game_state == 2:
                        game_state = 0
        #################################
        #############PHASE2##############
        #################################
        elif(event.type == pygame.MOUSEBUTTONDOWN and not game_over):
            #################################
            #############PHASE2##############
            #################################
            x, y = event.pos[0], event.pos[1]
            
            if game_state == 2:
                block_y_padding = (screen_height - 3*block_y_size)/4
                if screen_width/2 - block_x_size/2 <= x <= screen_width/2 + block_x_size/2:
                    if block_y_padding <= y <= block_y_padding + block_y_size:
                        game_state = 0
                        gameSetup()
                    elif screen_height/2 - block_y_size/2 <= y <= screen_height/2 + block_y_size/2:
                        game_state = 1;
                        screen_set = 0
                    elif screen_height - block_y_padding - block_y_size <= y <= screen_height - block_y_padding:
                        game_state = 0;
            elif game_state == 1:
                if 100 <= x < 260:
                    if 60 <= y <=120:
                        level = 'e'
                        gameSetup()
                    elif 140 <= y <= 200:
                        level = 'n'
                        gameSetup()
                    elif 220 <= y <= 280:
                        level = 'h'
                        gameSetup()
                continue
            elif game_state == 0:
                x, y = x // tile_size, y // tile_size
                if(0 <= x < field_width and 0 <= y < field_height):
                    if event.button == 1:
                        uncover(x, y)
                    elif event.button == 2:
                        check_flag()
                    elif event.button == 3:
                        if field_cover[x][y] == 1:
                            field_cover[x][y] = 2
                        elif field_cover[x][y] == 2:
                            field_cover[x][y] = 1
            #################################
            #############PHASE2##############
            #################################

    if game_state == 0 and game_over == False:
        for x in range(field_width):
            for y in range(field_height):
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if(field_cover[x][y]):
                    pygame.draw.rect(screen, white, rect)
                    #################################
                    #############PHASE2##############
                    #################################
                    if field_cover[x][y] == 2:
                        pygame.draw.rect(screen, black, rect, 2)
                        text = pygame.font.Font(None, 24).render((flag_mark), True, red)
                        screen.blit(text, (x * tile_size + 12, y * tile_size + 8))
                    #################################
                    #############PHASE2##############
                    #################################
                else:
                    color = gray
                    pygame.draw.rect(screen, color, rect)
                    number = field[x][y]
                    if(isMine(x, y)):
                        if(game_win):
                            mine = 'O'
                            color = white
                        else:
                            mine = 'X'
                            color = red
                        text = pygame.font.Font(None, 24).render((mine), True, color)
                    if(number > 0 and not isMine(x, y)):
                        if(number == 1):
                            text_color = blue
                        elif(number == 2):
                            text_color = bluegreen
                        elif(number == 3):
                            text_color = greenblue
                        elif(number == 4):
                            text_color = green
                        elif(number == 5):
                            text_color = greenred
                        elif(number == 6):
                            text_color = redgreen
                        elif(number == 7):
                            text_color = red
                        elif(number == 8):
                            text_color = black
                        text = pygame.font.Font(None, 24).render(str(number), True, text_color)
                    if(number != 0):
                        screen.blit(text, (x * tile_size + 12, y * tile_size + 8))

        if(gameWin()):
            gameover(True)

    pygame.display.flip()
    clock.tick(fps)


#for x in range(0, field_width):
#    print(field[x])
    
#게임 종료
pygame.quit()
