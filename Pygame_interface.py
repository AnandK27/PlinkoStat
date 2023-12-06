import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Interface")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 36)

# Set up button
button_rect = pygame.Rect(150, 150, 100, 50)
button_color = (0, 128, 255)

# Set up label
label_text = "Hello, Pygame!"
label = font.render(label_text, True, black)
label_rect = label.get_rect(center=(width // 2, 100))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                label_text = "Button Clicked!"
                label = font.render(label_text, True, black)

    # Clear the screen
    screen.fill(white)

    # Draw button
    pygame.draw.rect(screen, button_color, button_rect)

    # Draw label
    screen.blit(label, label_rect)

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    pygame.time.Clock().tick(30)
