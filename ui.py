import pygame
from database import setup_database, add_user, check_user
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 102, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
YELLOW = (255, 153, 51)
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Music Quiz")
icon_image = pygame.image.load("icon.png")
pygame.display.set_icon(icon_image)
def draw_text(text, x, y, color=BLACK, font=font_medium):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def draw_button(x, y, width, height, text, color=GRAY, text_color=BLACK):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    draw_text(text, x + 10, y + 10, text_color, font_small)
def login_register_screen():
    username_input = ""
    password_input = ""
    input_active = None
    message = ""

    while True:
        screen.fill(LIGHT_BLUE)
        draw_text("Login or Register", 250, 100, DARK_RED, font_large)

        # Username and Password Fields
        draw_text("Username: ", 100, 200, YELLOW, font_medium)
        draw_text("Password: ", 100, 300, YELLOW, font_medium)

        # Input boxes for username and password
        username_box = pygame.Rect(300, 200, 300, 50)
        password_box = pygame.Rect(300, 300, 300, 50)
        pygame.draw.rect(screen, LIGHT_GRAY, username_box, 2)
        pygame.draw.rect(screen, LIGHT_GRAY, password_box, 2)
        draw_text(username_input, 350, 205, BLACK, font_small)
        draw_text('*' * len(password_input), 350, 315, BLACK, font_small)

        draw_text(message, 250, 400, RED, font_medium)
        draw_button(200, 450, 150, 50, "Login", BLUE, WHITE)
        draw_button(450, 450, 150, 50, "Register", GREEN, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if user clicked on the login or register buttons
                login_button_rect = pygame.Rect(200, 450, 150, 50)
                register_button_rect = pygame.Rect(450, 450, 150, 50)

                if login_button_rect.collidepoint(mouse_x, mouse_y):
                    if check_user(username_input, password_input):
                        return username_input 
                    else:
                        message = "Invalid login. Try again."

                if register_button_rect.collidepoint(mouse_x, mouse_y):
                    # Register new user
                    if username_input and password_input:
                        add_user(username_input, password_input)
                        message = "Registration successful! You can now log in."
                    else:
                        message = "Please enter both username and password."

            if event.type == pygame.KEYDOWN:
                if input_active == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username_input = username_input[:-1]
                    else:
                        username_input += event.unicode
                elif input_active == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password_input = password_input[:-1]
                    else:
                        password_input += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if username_box.collidepoint(mouse_x, mouse_y):
                    input_active = "username"
                elif password_box.collidepoint(mouse_x, mouse_y):
                    input_active = "password"
                else:
                    input_active = None

def display_summary(correct_guesses, incorrect_guesses, skipped_questions, game_history):
    while True:
        screen.fill(LIGHT_BLUE)
        draw_text("Game Over!", 280, 50, DARK_RED, font_large)
        draw_text("Here's your result:", 250, 150, YELLOW, font_medium)
        draw_text(f"Correct Guesses: {correct_guesses}", 200, 250, GREEN, font_small)
        draw_text(f"Incorrect Guesses: {incorrect_guesses}", 200, 300, RED, font_small)
        draw_text(f"Skipped Questions: {skipped_questions}", 200, 350, DARK_RED, font_small)

        # Display history
        y_offset = 400
        for i, (result, title) in enumerate(game_history):
            draw_text(f"{i + 1}. {result}: {title}", 50, y_offset + i * 30, BLACK, font_small)

        # Quit and Play Again buttons
        draw_button(250, 600, 200, 50, "Play Again", GREEN, WHITE)
        draw_button(550, 600, 200, 50, "Quit", DARK_RED, WHITE)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                play_again_button_rect = pygame.Rect(250, 600, 200, 50)
                quit_button_rect = pygame.Rect(550, 600, 200, 50)

                if play_again_button_rect.collidepoint(mouse_x, mouse_y):
                    return "restart"  # Signal to restart the game
                if quit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    exit()


def genre_selection_screen():
    genres = ["K-pop", "Japanese", "Chinese", "International"]
    while True:
        screen.fill(LIGHT_BLUE)
        draw_text("Select Genre", 350, 100, DARK_RED, font_large)

        # Display genre options
        y_offset = 200
        genre_height = 50
        genre_width = 600
        for i, genre in enumerate(genres):
            genre_rect = pygame.Rect(200, y_offset + i * (genre_height + 10), genre_width, genre_height)
            pygame.draw.rect(screen, LIGHT_GRAY, genre_rect, 2, border_radius=10)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if genre_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, (173, 216, 230), genre_rect)  # Highlight on hover
            draw_text(genre, 220, y_offset + i * (genre_height + 10), BLACK, font_small)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, genre in enumerate(genres):
                    genre_rect = pygame.Rect(200, y_offset + i * (genre_height + 10), genre_width, genre_height)
                    if genre_rect.collidepoint(mouse_x, mouse_y):
                        return genre  # Return selected genre
