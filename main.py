import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import qrcode
import time
import numpy as np
import copy

def main():
	# Generate a qr code based on the text
	qr_text = ("Hi, mom!")
	qr = qrcode.make(qr_text).modules
	
	# Scale up the QR code based on a scaling factor
	scale_factor = 20
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

	# Pad matrix with False on border
	matrix = np.pad(matrix, pad_width=1, mode='constant', constant_values=False)
	
	# Set up PyGame
	pygame.init()
	screen = pygame.display.set_mode((new_width, new_height))
	pygame.display.set_caption("QR Code Game of Life")
	surface = pygame.Surface((new_width, new_height))
	surface.fill((255, 255, 255))

	# Draw initial QR code and display it for a few seconds
	for y in range(1, new_height + 1):
		for x in range(1, new_width + 1):
			if matrix[y][x]:
				surface.set_at((x-1, y-1), (0, 0, 0))

	screen.blit(surface, (0, 0))
	pygame.display.flip()

	print(qr_text)
	time.sleep(2)

	running = True
	
	while running:
		# Exit PyGame
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		surface.fill((255, 255, 255))

		# Build new matrix
		new_matrix = [matrix[0]]
		for y in range(1, new_height + 1):
			new_row = [False]
			for x in range(1, new_width + 1):
				num_neighbours = sum(matrix[y-1][x-1:x+2]) + sum(matrix[y][x-1:x+2]) + sum(matrix[y+1][x-1:x+2]) - matrix[y][x]
				if matrix[y][x]:
					if num_neighbours == 2 or num_neighbours == 3:
						new_row.append(True)
						surface.set_at((x-1, y-1), (0, 0, 0))
					else:
						new_row.append(False)
				else:
					if num_neighbours == 3:
						new_row.append(True)
						surface.set_at((x-1, y-1), (0, 0, 0))
					else:
						new_row.append(False)
			new_row.append(False)
			new_matrix.append(new_row)
		
		new_matrix.append(matrix[-1])

		matrix = copy.copy(new_matrix)
		
		# Show new matrix
		screen.blit(surface, (0, 0))
		pygame.display.flip()

if __name__ == "__main__":
	main()