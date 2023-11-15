import pygame
import copy

board = []

row_count = 30
column_count = 30

for i in range(row_count):
  board_row = [0] * column_count
  board.append(board_row)

#pygame init and variables
#==========
pygame.init()
pygame.display.set_caption("Game of Life")
WHITE = (200,200,200)
BLACK = (0, 0, 0)
GREY = (50,50,50)
square_buffer = 2
info_object = pygame.display.Info()
screen_width = round(info_object.current_h/1.3)
screen_height = round(info_object.current_h/1.3)
screen = pygame.display.set_mode((screen_width+square_buffer, screen_height+square_buffer))
squaresize = screen_width / column_count
drawing = True
playing = False
#==========

def iterate(board, dist = 1):
  board_next = copy.deepcopy(board)
  for row_index, row in enumerate(board):
    for element_index, element in enumerate(row):
      local_squares = [r[max(0, element_index-1):element_index+dist+1] for r in board[max(0, row_index-1):row_index+dist+1]]
      checking_square = board[row_index][element_index]
      live_neighbours = sum(sublist.count(1) for sublist in local_squares)
      if checking_square == 1:
        live_neighbours -= 1
      if checking_square == 1 and live_neighbours < 2:
        board_next[row_index][element_index] = 0
      if checking_square == 1 and live_neighbours > 3:
        board_next[row_index][element_index] = 0
      if checking_square == 0 and live_neighbours == 3:
        board_next[row_index][element_index] = 1
  return(copy.deepcopy(board_next))

def draw_vis_board(grid):
  pygame.draw.rect(screen, GREY, ((0, 0, screen_width+square_buffer, screen_height+square_buffer)))
  for c in range(column_count):
    for r in range(row_count):
      pygame.draw.rect(screen, BLACK, ((c*squaresize+square_buffer, r*squaresize+square_buffer, squaresize-square_buffer, squaresize-square_buffer)))
      if grid[r][c] == 1:
        pygame.draw.rect(screen, WHITE, ((c*squaresize+square_buffer, r*squaresize+square_buffer, squaresize-square_buffer, squaresize-square_buffer)))

  pygame.display.flip()

while drawing == True:
  for event in pygame.event.get():

    if event.type == pygame.QUIT:
      drawing = False

    if pygame.mouse.get_pressed(num_buttons=3)[0] == True:
      cell_x = round((pygame.mouse.get_pos()[0]+squaresize/2) / squaresize - 1)
      cell_y = round((pygame.mouse.get_pos()[1]+squaresize/2) / squaresize - 1)
      try:
        board[cell_y][cell_x] = 1
      except:
        pass

    if pygame.mouse.get_pressed(num_buttons=3)[2] == True:
      cell_x = round((pygame.mouse.get_pos()[0]+squaresize/2) / squaresize - 1)
      cell_y = round((pygame.mouse.get_pos()[1]+squaresize/2) / squaresize - 1)
      try:
        board[cell_y][cell_x] = 0
      except:
        pass

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
          playing = True
          drawing = False

  draw_vis_board(board)

while playing == True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      playing = False
  board = iterate(board)
  draw_vis_board(board)
  pygame.time.delay(100)

pygame.quit()