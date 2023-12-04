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
                pygame.draw.circle(SCREEN, WHITE, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 
                                    3*PADDING), 2)
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
                if player == 'X':
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

        p2img = font.render(f'Player 2 : {p2_score}', True, BLUE)
        p2rect = p2img.get_rect()
        p2rect.right, p2rect.y = width-2*PADDING, 15

        SCREEN.blit(p1img, p1rect)
        SCREEN.blit(p2img, p2rect)
        if player == 'X':
            pygame.draw.line(SCREEN, BLUE, (p1rect.x, p1rect.bottom+2), 
                                (p1rect.right, p1rect.bottom+2), 1)
        else:
            pygame.draw.line(SCREEN, BLUE, (p2rect.x, p2rect.bottom+2), 
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
