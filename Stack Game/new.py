from button import Button
import os , sys
import pygame
from pygame import mixer


pygame.init()
mixer.init()
mixer.music.set_volume(0.2)

width=500
height=500

def Get_Path(DB_DOCS_NAME):
    dir = os.path.dirname(__file__)
    abs_path = os.path.join(dir, DB_DOCS_NAME)
    return abs_path 
    
BG = pygame.image.load(Get_Path("assets/Background.png"))

SCREEN = pygame.display.set_mode((width, height))

ico = pygame.image.load("assets/icon.ico")

pygame.display.set_icon(ico)

CELLSIZE = 80
PADDING = 40
ROWS = COLS = (width - 4 * PADDING) // CELLSIZE

WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (78, 193, 246)
GREEN = (0, 255, 0)
BLACK = (12, 12, 12)

font = pygame.font.SysFont('cursive', 20)

def get_font(size): 
    return pygame.font.Font(Get_Path("assets/font.ttf"), size)

pygame.display.set_caption("Dots and Boxes")

class Cell:
	def __init__(self, r, c):
		self.r = r
		self.c = c
		self.index = self.r * ROWS + self.c

		self.rect = pygame.Rect((self.c*CELLSIZE + 2*PADDING, self.r*CELLSIZE + 
								3*PADDING, CELLSIZE, CELLSIZE))
		self.left = self.rect.left
		self.top = self.rect.top
		self.right = self.rect.right
		self.bottom = self.rect.bottom
		self.edges = [
					  [(self.left, self.top), (self.right, self.top)],
					  [(self.right, self.top), (self.right, self.bottom)],
					  [(self.right, self.bottom), (self.left, self.bottom)],
					  [(self.left, self.bottom), (self.left, self.top)]
					 ]
		self.sides = [False, False, False, False]
		self.winner = None

	def checkwin(self, winner):
		if not self.winner:
			if self.sides == [True]*4:
				self.winner = winner
				if winner == '1':
					self.color = GREEN
				else:
					self.color = RED
				self.text = font.render(self.winner, True, WHITE)

				return 1
		return 0

	def update(self, win):
		if self.winner:
			pygame.draw.rect(win, self.color, self.rect)
			win.blit(self.text, (self.rect.centerx-5, self.rect.centery-7))

		for index, side in enumerate(self.sides):
			if side:
				pygame.draw.line(win, RED, (self.edges[index][0]),
										(self.edges[index][1]), 5)

def create_cells():
	cells = []
	for r in range(ROWS):
		for c in range(COLS):
			cell = Cell(r, c)
			cells.append(cell)
	return cells

def reset_cells():
	pos = None
	ccell = None
	up = False
	right = False
	bottom = False
	left = False
	return pos, ccell, up, right, bottom, left

def reset_score():
	fillcount = 0
	p1_score = 0
	p2_score = 0
	return fillcount, p1_score, p2_score

def reset_player():
	turn = 0
	players = ['1', '2']
	player = players[turn]
	next_turn = False
	return turn, players, player, next_turn




def gameloop(running = True):
    gameover = False
    cells = create_cells()
    pos, ccell, up, right, bottom, left = reset_cells()
    fillcount, p1_score, p2_score = reset_score()
    turn, players, player, next_turn = reset_player()
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                pos = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r:
                    gameover = False
                    cells = create_cells()
                    pos, ccell, up, right, bottom, left = reset_cells()
                    fillcount, p1_score, p2_score = reset_score()
                    turn, players, player, next_turn = reset_player()

                if not gameover:
                    if event.key == pygame.K_UP:
                        up = True
                    if event.key == pygame.K_RIGHT:
                        right = True
                    if event.key == pygame.K_DOWN:
                        bottom = True
                    if event.key == pygame.K_LEFT:
                        left = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_DOWN:
                    bottom = False
                if event.key == pygame.K_LEFT:
                    left = False

        for r in range(ROWS+1):
            for c in range(COLS+1):
                pygame.draw.circle(SCREEN, GREEN, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 
                                    3*PADDING), 5)
        for cell in cells:
            cell.update(SCREEN)
            if pos and cell.rect.collidepoint(pos):
                ccell = cell

        if ccell:
            index = ccell.index
            if not ccell.winner:
                pygame.draw.circle(SCREEN, RED, (ccell.rect.centerx, ccell.rect.centery), 2)

            if up and not ccell.sides[0]:
                ccell.sides[0] = True
                if index - ROWS >= 0:			
                    cells[index-ROWS].sides[2] = True
                    next_turn = True
            if right and not ccell.sides[1]:
                ccell.sides[1] = True
                if (index + 1) % COLS > 0:
                    cells[index+1].sides[3] = True
                    next_turn = True
            if bottom and not ccell.sides[2]:
                ccell.sides[2] = True
                if index + ROWS < len(cells):			
                    cells[index+ROWS].sides[0] = True
                    next_turn = True
            if left and not ccell.sides[3]:
                ccell.sides[3] = True
                if (index % COLS) > 0:
                    cells[index-1].sides[1] = True
                    next_turn = True
            
            res = ccell.checkwin(player)
            if res:
                fillcount += res
                if player == '1':
                    p1_score += 1
                else:
                    p2_score += 1
                if fillcount == ROWS * COLS:
                    print(p1_score, p2_score)
                    gameover = True

            if next_turn:
                turn = (turn + 1) % len(players)
                player = players[turn]
                next_turn = False

        p1img = font.render(f'Player 1 : {p1_score}', True, BLUE)
        p1rect = p1img.get_rect()
        p1rect.x, p1rect.y = 2*PADDING, 15

        p2img = font.render(f'Player 2 : {p2_score}', True, RED)
        p2rect = p2img.get_rect()
        p2rect.right, p2rect.y = width-2*PADDING, 15

        SCREEN.blit(p1img, p1rect)
        SCREEN.blit(p2img, p2rect)
        if player == '1':
            pygame.draw.line(SCREEN, BLUE, (p1rect.x, p1rect.bottom+2), 
                                (p1rect.right, p1rect.bottom+2), 1)
        else:
            pygame.draw.line(SCREEN, RED, (p2rect.x, p2rect.bottom+2), 
                                (p2rect.right, p2rect.bottom+2), 1)

        if gameover:
            rect = pygame.Rect((50, 100, width-100, height-200))
            pygame.draw.rect(SCREEN, BLACK, rect)
            pygame.draw.rect(SCREEN, RED, rect, 2)

            over = font.render('Game Over', True, WHITE)
            SCREEN.blit(over, (rect.centerx-over.get_width()/2, rect.y + 10))
            
            winner = '1' if p1_score > p2_score else '2'
            winner_img = font.render(f'Player {winner} Won', True, GREEN)
            SCREEN.blit(winner_img, (rect.centerx-winner_img.get_width()/2, rect.centery- 10))

            msg = 'Press r:restart, q:quit'
            msgimg = font.render(msg, True, RED)
            SCREEN.blit(msgimg, (rect.centerx-msgimg.get_width()/2, rect.centery + 20))

        pygame.draw.rect(SCREEN, WHITE, (0,0,width,height),2, border_radius=10)
        pygame.display.update()

def main_menu():
    try:
        mixer.music.load(Get_Path('assets/main.mp3'))
        mixer.music.play()
    except:
        print("Music error")
    while True:
       
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        GAME_TITLE = get_font(33).render("Dots and Boxes", True, "#DF6589FF")
        GAME_RECT = GAME_TITLE.get_rect(center=(width/2, height/2 - 100))

        MENU_TEXT = get_font(25).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(width/2, height/2 - 50))

        PLAY_BUTTON = Button(image=None, pos=(width/2, height/2 ), 
                            text_input="PLAY", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        
        QUIT_BUTTON = Button(image=None, pos=(width/2, height/2 + 50), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(GAME_TITLE, GAME_RECT)
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    try:
                        gameloop()
                    except:
                        print("error in gameplay")
                    try:
                        mixer.music.stop()
                        mixer.music.load(Get_Path('assets/play.mp3'))
                        mixer.music.play()
                    except:
                        print("Music Error")

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
