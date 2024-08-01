import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import qrcode
import time

def main():
	qr_text = ("Hi mom!")
	qr = qrcode.make(qr_text).modules
	
	scale_factor = 15
	
	original_height = len(qr)
	original_width = len(qr[0])

	new_height = original_height * scale_factor
	new_width = original_height * scale_factor

	matrix = []
	for _ in range(new_height):
		row = [False] * new_width
		matrix.append(row)
	
	for y in range(original_height):
		for x in range(original_width):
			if qr[y][x]:
				start_y = y * scale_factor
				start_x = x * scale_factor
				for dy in range(scale_factor):
					for dx in range(scale_factor):
						matrix[start_y + dy][start_x + dx] = True
	
	pygame.init()
	screen = pygame.display.set_mode((new_width, new_height))
	pygame.display.set_caption("QR Code Game of Life")
	surface = pygame.Surface((new_width, new_height))
	surface.fill((255, 255, 255))

	for y in range(new_height):
		for x in range(new_width):
			if matrix[y][x]:
				surface.set_at((x, y), (0, 0, 0))

	screen.blit(surface, (0, 0))
	pygame.display.flip()

	print(qr_text)
	time.sleep(2)

	running = True
	
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		new_matrix = []
		for y in range(new_height):
			new_row = []
			for x in range(new_width):
				num_neighbours = 0
				if y == 0 and x == 0:
					num_neighbours = matrix[y][x+1] + matrix[y+1][x] + matrix[y+1][x+1]
				elif y == 0 and x == new_width - 1:
					num_neighbours = matrix[y][x-1] + matrix[y+1][x-1] + matrix[y+1][x]
				elif y == new_height - 1 and x == 0:
					num_neighbours = matrix[y-1][x] + matrix[y-1][x+1] + matrix[y][x+1]
				elif y == new_height - 1 and x == new_width - 1:
					num_neighbours = matrix[y-1][x-1] + matrix[y-1][x] + matrix[y][x-1]
				elif y == 0:
					num_neighbours = matrix[y][x-1] + matrix[y][x+1] + matrix[y+1][x-1] + matrix[y+1][x] + matrix[y+1][x+1]
				elif x == 0:
					num_neighbours = matrix[y-1][x] + matrix[y-1][x+1] + matrix[y][x+1] + matrix[y+1][x] + matrix[y+1][x+1]
				elif x == new_width - 1:
					num_neighbours = matrix[y-1][x-1] + matrix[y-1][x] + matrix[y][x-1] + matrix[y+1][x-1] + matrix[y+1][x]
				elif y == new_height - 1:
					num_neighbours = matrix[y-1][x-1] + matrix[y-1][x] + matrix[y-1][x+1] + matrix[y][x-1] + matrix[y][x+1]
				else:
					num_neighbours = matrix[y-1][x-1] + matrix[y-1][x] + matrix[y-1][x+1] + matrix[y][x-1] + matrix[y][x+1] + matrix[y+1][x-1] + matrix[y+1][x] + matrix[y+1][x+1]
				if matrix[y][x]:
					if num_neighbours == 2 or num_neighbours == 3:
						new_row.append(True)
					else:
						new_row.append(False)
				else:
					if num_neighbours == 3:
						new_row.append(True)
					else:
						new_row.append(False)
			new_matrix.append(new_row)
		
		matrix = new_matrix

		surface.fill((255, 255, 255))

		for y in range(new_height):
			for x in range(new_width):
				if matrix[y][x]:
					surface.set_at((x, y), (0, 0, 0))
		
		screen.blit(surface, (0, 0))
		pygame.display.flip()

if __name__ == "__main__":
	main()