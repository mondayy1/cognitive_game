# main.py
import pygame
import sys
from pri_game import PRIGame
from wmi_game import WMIGame
from psi_game import PSIGame
from vci_game import VCIGame
from gptapi import get_diagnosis_gpt

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cognitive Skills Test Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Button dimensions and positions
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
START_BTN_POS = (300, 250)
HOW_TO_PLAY_BTN_POS = (300, 350)


def draw_button(text, position, color=BLUE):
    """Draw a button with text at the given position."""
    pygame.draw.rect(screen, color, (*position, BUTTON_WIDTH, BUTTON_HEIGHT))
    btn_text = font.render(text, True, WHITE)
    text_rect = btn_text.get_rect(center=(position[0] + BUTTON_WIDTH // 2, position[1] + BUTTON_HEIGHT // 2))
    screen.blit(btn_text, text_rect)


def show_instructions():
    """Display game instructions."""
    instructions = [
        "Instructions:",
        "1. PRI Game: Complete the missing pattern in a matrix.",
        "2. WMI Game: Memorize and recall a sequence of numbers.",
        "3. PSI Game: Identify symbols quickly within a time limit.",
        "4. VCI Game: Verbal comprehension game (if included).",
        "Press any key to return."
    ]
    screen.fill(WHITE)
    for i, line in enumerate(instructions):
        text = small_font.render(line, True, BLACK)
        screen.blit(text, (50, 100 + i * 40))
    pygame.display.flip()

    # Wait for user to press any key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False


def display_diagnosis(diagnosis, scores):
    screen.fill(WHITE)
    # Prepare lines for scores and average reaction time
    results = [
        f"Scores:",
        f"  - PRI: {scores[0]}",
        f"  - WMI: 70",
        f"  - PSI: {scores[1]}",
        f"  - VCI: 90",
        f"Average Reaction Time: {4.2:.2f} seconds",
        "",
        "GPT Diagnosis:",
    ]
    
    # Split GPT diagnosis into multiple lines for readability
    wrapped_text = []
    words = diagnosis.split()
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= 50:  # Assuming 50 characters per line
            line += word + " "
        else:
            wrapped_text.append(line.strip())
            line = word + " "
    if line:
        wrapped_text.append(line.strip())

    results.extend(wrapped_text)

    # Render each line
    y_offset = 50
    for line in results:
        text = small_font.render(line, True, BLACK)
        screen.blit(text, (50, y_offset))
        y_offset += 40

    # Display prompt to exit
    exit_text = small_font.render("Press any key to exit.", True, BLACK)
    screen.blit(exit_text, (50, y_offset + 40))
    pygame.display.flip()

    # Wait for user to press any key to exit
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False


def start_game_sequence():
    """Run the sequence of games and display the total score."""
    total_score = 0
    scores = []
    games = [PRIGame(screen), PSIGame(screen)]  # Add VCIGame if implemented

    for game in games:
        game.run()
        scores.append(game.score)

        # Display final score
        screen.fill(BLACK)
        score_text = font.render(f"Total Score: {game.score}", True, GREEN)
        screen.blit(score_text, (300, 250))
        pygame.display.flip()
        pygame.time.wait(1000)

    # Fetch and display diagnosis
    diagnosis = get_diagnosis_gpt(pri=scores[0], psi=scores[1])
    display_diagnosis(diagnosis, scores)


def main():
    """Main game loop for the start screen."""
    while True:
        screen.fill(WHITE)
        draw_button("Game Start", START_BTN_POS)
        draw_button("How to Play", HOW_TO_PLAY_BTN_POS)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if Game Start button is clicked
                if (START_BTN_POS[0] <= mouse_pos[0] <= START_BTN_POS[0] + BUTTON_WIDTH and
                        START_BTN_POS[1] <= mouse_pos[1] <= START_BTN_POS[1] + BUTTON_HEIGHT):
                    start_game_sequence()
                    pygame.quit()
                    sys.exit()
                # Check if How to Play button is clicked
                elif (HOW_TO_PLAY_BTN_POS[0] <= mouse_pos[0] <= HOW_TO_PLAY_BTN_POS[0] + BUTTON_WIDTH and
                      HOW_TO_PLAY_BTN_POS[1] <= mouse_pos[1] <= HOW_TO_PLAY_BTN_POS[1] + BUTTON_HEIGHT):
                    show_instructions()


if __name__ == "__main__":
    main()
    pygame.quit()
