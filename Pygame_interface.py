import pygame
import sys
import matplotlib.pyplot as plt
import numpy as np
import threading

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
DARK_BLUE = (25, 25, 112)
BUTTON_BLUE = (70, 130, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50
BOX_WIDTH, BOX_HEIGHT = 200, 50
FONT_SIZE = 24

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PlinkoStat Interface")

# Create a font object
font = pygame.font.Font(None, FONT_SIZE)

# PlinkoStat parameters
num_slots = 0 # Default value removed
depth_level = 0  # Default value removed
sample_size = 100
is_paused = False
is_running = False

# PlinkoStat results
results = []

def plinko_simulation():
    global results, num_slots, depth_level, sample_size
    results = []  # Reset results
    for _ in range(sample_size):
        position = np.random.randint(num_slots)
        for _ in range(depth_level):
            if np.random.choice([True, False]):  # Random left or right movement
                position = max(0, position - 1)
            else:
                position = min(num_slots - 1, position + 1)
        results.append(position)

# Function to update the depth level
def update_depth_level(new_depth_level):
    global depth_level
    depth_level = int(new_depth_level)

# Function to update the number of slots
def update_num_slots(new_num_slots):
    global num_slots
    num_slots = int(new_num_slots)

# Function to start the simulation
def start_simulation():
    global is_running
    is_running = True
    threading.Thread(target=plinko_simulation).start()

# Function to stop the simulation
def stop_simulation():
    global is_running
    is_running = False

# Function to toggle pause
def toggle_pause():
    global is_paused
    is_paused = not is_paused

# Function to plot results
def plot_results():
    plt.hist(results, bins=np.arange(-0.5, num_slots + 0.5, 1), density=True)
    plt.title('PlinkoStat Simulation Results')
    plt.xlabel('Slot')
    plt.ylabel('Frequency')
    plt.show()

# Function to draw a button
def draw_button(x, y, width, height, color, text, action=None):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

    # Check for button click and perform action
    if action is not None:
        button_rect = pygame.Rect(x, y, width, height)
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                action["function"]()

# Function to draw an input box
def draw_input_box(x, y, width, height, color, text, input_value, action=None):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(topleft=(x + 10, y + height // 2 - 10))
    screen.blit(text_surface, text_rect)
    pygame.draw.rect(screen, BLACK, (x + 10 + text_rect.width + 10, y + 10, 100, 30))  # Input box

    input_surface = font.render(str(input_value), True, WHITE)
    input_rect = input_surface.get_rect(center=(x + 10 + text_rect.width + 10 + 50, y + height // 2))
    screen.blit(input_surface, input_rect)

    # Check for input box click and perform action
    if action is not None:
        input_box_rect = pygame.Rect(x + 10 + text_rect.width + 10, y + 10, 100, 30)
        if input_box_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                action["function"]()

# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_button(50, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BLUE, "Start", action={"function": start_simulation})
            draw_button(220, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BLUE, "Stop", action={"function": stop_simulation})
            draw_button(390, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BLUE, "Pause/Resume", action={"function": toggle_pause})
            draw_button(560, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BLUE, "Plot Results", action={"function": plot_results})

            draw_input_box(50, 200, BOX_WIDTH, BOX_HEIGHT, BUTTON_BLUE, "Depth/Level:", depth_level, action={"function": update_depth_level})
            draw_input_box(50, 300, BOX_WIDTH, BOX_HEIGHT, BUTTON_BLUE, "Number of Slots:", num_slots, action={"function": update_num_slots})

    # Clear the screen
    screen.fill(DARK_BLUE)

    # Display the message with changing text color
    color_change = int(pygame.time.get_ticks() / 10) % 255
    message_surface = font.render("WANNA MAKE SOME MONEY?, THEN LET'S PLAY SOME PLINKOSTAT!", True, (color_change, 255 - color_change, 100))
    message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 25))
    screen.blit(message_surface, message_rect)

    # Draw UI elements
    draw_button(50, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BLUE, "Start", action={"function": start_simulation})
    draw_button(220, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BLUE, "Stop", action={"function": stop_simulation})
    draw_button(390, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BLUE, "Pause/Resume", action={"function": toggle_pause})
    draw_button(560, 100, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BLUE, "Plot Results", action={"function": plot_results})

    # Draw Depth/Level input box
    draw_input_box(50, 200, BOX_WIDTH, BOX_HEIGHT, BUTTON_BLUE, "Depth/Level:", depth_level, action={"function": update_depth_level})

    # Draw Number of Slots input box
    draw_input_box(50, 300, BOX_WIDTH, BOX_HEIGHT, BUTTON_BLUE, "Number of Slots:", num_slots, action={"function": update_num_slots})

    # Draw Total Money Won box with money emoji
    pygame.draw.rect(screen, BUTTON_BLUE, (50, 400, BOX_WIDTH, BOX_HEIGHT))
    money_emoji = font.render("💰", True, WHITE)
    money_rect = money_emoji.get_rect(topleft=(50 + 10, 400 + BOX_HEIGHT // 2 - 10))
    screen.blit(money_emoji, money_rect)
    text_surface = font.render("Total Money Won: {:.2f}".format(np.mean(results) if results else 0), True, WHITE)
    text_rect = text_surface.get_rect(center=(50 + BOX_WIDTH // 2, 400 + BOX_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
