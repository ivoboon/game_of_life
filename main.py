import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import qrcode

def main():
	qr_text = ("Hi, mom!")
	qr = qrcode.make(qr_text).modules
	
	scale_factor = 50
	
	original_height = len(qr)
	original_width = len(qr[0])

	new_height = original_height * scale_factor
	new_width = original_height * scale_factor

	scaled_matrix = []
	for _ in range(new_height):
		row = [False] * new_width
		scaled_matrix.append(row)
	
	for y in range(original_height):
		for x in range(original_width):
			if qr[y][x]:
				start_y = y * scale_factor
				start_x = x * scale_factor
				for dy in range(scale_factor):
					for dx in range(scale_factor):
						scaled_matrix[start_y + dy][start_x + dx] = True
	
	pygame.init()
	screen = pygame.display.set_mode((new_width, new_height))
	pygame.display.set_caption("QR Code Game of Life")
	surface = pygame.Surface((new_width, new_height))
	surface.fill((255, 255, 255))

	for y in range(new_height):
		for x in range(new_width):
			if scaled_matrix[y][x]:
				surface.set_at((x, y), (0, 0, 0))
	
	screen.blit(surface, (0, 0))
	pygame.display.flip()

	running = True
	
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

if __name__ == "__main__":
	main()