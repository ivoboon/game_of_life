import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import qrcode
import time
import sys

def generate_qr_matrix(qr_text, version):
	"""
	Creates a QR code, converts it to a matrix, and returns it
	Border of 1 is used for padding, which makes the code for alive/dead checks a bit more neat
	"""
	qr = qrcode.QRCode(
		version=version,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		border=1
	)
	qr.add_data(qr_text)
	qr = qr.get_matrix()
	return qr


def resize_matrix(matrix, scaling_factor):
	"""
	Resizes a matrix based on a scaling factor
	"""
	resized_matrix = []

	for y in range(len(matrix)):
		for _ in range(scaling_factor):
			row = []
			for x in range(len(matrix[0])):
				row.extend([matrix[y][x]] * scaling_factor)
			resized_matrix.append(row)

	return resized_matrix


def display_matrix(surface, matrix, scaling_factor):
	"""
	Draws the resized QR code on the surface
	Some translating has to be done because of the padding
	"""
	display_matrix = resize_matrix(matrix, scaling_factor)
	for y in range(scaling_factor, len(display_matrix) - scaling_factor):
		for x in range(scaling_factor, len(display_matrix[0]) - scaling_factor):
			if display_matrix[y][x]:
					surface.set_at((x - scaling_factor, y - scaling_factor), (0, 0, 0))

def game_of_life(matrix):
	"""
	Applies the Game of Life rules
	Generates a matrix for the next time step
	It copies the False padded first and last rows
	Prepends and appends a False column in the new rows
	"""
	height = len(matrix) - 2
	width = len(matrix[0]) - 2

	new_matrix = [matrix[0]]
	for y in range(1, height + 1):
		new_row = [False]
		for x in range(1, width + 1):
			num_neighbours = sum(matrix[y-1][x-1:x+2]) + sum(matrix[y][x-1:x+2]) + sum(matrix[y+1][x-1:x+2]) - matrix[y][x]
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
		new_row.append(False)
		new_matrix.append(new_row)
	new_matrix.append(matrix[-1])

	return new_matrix

def main():
	"""
	Main function
	"""
	# Input variables
	qr_text = ("Hi, mom!")	# The text used to generate the QR code
	version = 40			# The QR code version from 1-40, newer version = larger QR code
	scaling_factor = 2		# Scales each pixel by a factor
	display_delay = 2		# Number of seconds the initial QR gets displayed before the Game of Life starts

	# Make QR code
	qr_code = generate_qr_matrix(qr_text, version)

	# Set up PyGame
	pygame.init()
	display_height = len(qr_code) * scaling_factor - 2 * scaling_factor
	display_width = len(qr_code[0]) * scaling_factor - 2 * scaling_factor
	screen = pygame.display.set_mode((display_width, display_height))
	pygame.display.set_caption("QR Code Game of Life")
	surface = pygame.Surface((display_width, display_height))
	surface.fill((255, 255, 255))

	# Draw initial QR code and display it for a few seconds
	display_matrix(surface, qr_code, scaling_factor)
	screen.blit(surface, (0, 0))
	pygame.display.flip()
	print(qr_text)
	time.sleep(display_delay)

	# PyGame loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		surface.fill((255, 255, 255))		
		qr_code = game_of_life(qr_code)
		display_matrix(surface, qr_code, scaling_factor)
		screen.blit(surface, (0, 0))
		pygame.display.flip()

if __name__ == "__main__":
	main()