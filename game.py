import pygame
import random
import os
from database import setup_database
from user_database import setup_user_database, save_user_results
from ui import screen, draw_text,display_summary, draw_button,genre_selection_screen, login_register_screen, LIGHT_BLUE, DARK_RED, YELLOW, GRAY, LIGHT_GRAY, GREEN, WHITE, RED, BLACK, BLUE
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)
def load_songs(genre=None):
    song_path = "Genre_Song"  # Folder containing genre subdirectories
    if not os.path.exists(song_path):
        print(f"Error: The directory '{song_path}' does not exist.")
        return []

    song_files = []

    # If a genre is provided, only load songs from that genre folder
    if genre:
        genre_folder = os.path.join(song_path, genre)
        if os.path.exists(genre_folder):
            for song in os.listdir(genre_folder):
                if song.endswith('.mp3'): 
                    song_files.append((os.path.join(genre_folder, song), os.path.splitext(song)[0]))
        else:
            print(f"Error: The genre folder '{genre}' does not exist.")
    else:
        for genre in os.listdir(song_path):
            genre_folder = os.path.join(song_path, genre)
            if os.path.isdir(genre_folder): 
                for song in os.listdir(genre_folder):
                    if song.endswith('.mp3'): 
                        song_files.append((os.path.join(genre_folder, song), os.path.splitext(song)[0]))

    return song_files

def start_game():
    while True:
        screen.fill(LIGHT_BLUE)
        draw_text("Welcome to Music Quiz!", 160, 100, DARK_RED, font_large)
        draw_text("Test your music knowledge!", 180, 180, YELLOW, font_medium)
        draw_button(300, 350, 200, 50, "Start Game", BLUE, WHITE)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                start_button_rect = pygame.Rect(300, 350, 200, 50)
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    return  
def main_game():
    running = True
    clock = pygame.time.Clock()
    setup_database()
    setup_user_database()
    username = login_register_screen()
    genre = genre_selection_screen()
    # Print selected genre for debugging
    print(f"Selected genre: {genre}")
    songs = load_songs(genre)  
    if not songs:
        print(f"No songs found in the selected genre: {genre}.")
        return
    while running:
        # Start the game only when "Start Game" is clicked
        screen.fill(LIGHT_BLUE)
        draw_text("Welcome to Music Quiz!", 160, 100, DARK_RED, font_large)
        draw_text("Test your music knowledge!", 180, 180, YELLOW, font_medium)
        draw_button(300, 350, 200, 50, "Start Game", BLUE, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                start_button_rect = pygame.Rect(300, 350, 200, 50)
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    # Once the start button is clicked, begin the game loop
                    rounds_played = 0
                    max_rounds = 6
                    correct_guesses = 0
                    incorrect_guesses = 0
                    skipped_questions = 0
                    game_history = []  # Keep track of the game history

                    while rounds_played < max_rounds:
                        correct_song = random.choice(songs)
                        correct_title = correct_song[1]
                        incorrect_titles = random.sample(
                            [song[1] for song in songs if song[1] != correct_title],
                            k=min(3, len(songs) - 1)
                        )
                        options = [correct_title] + incorrect_titles
                        random.shuffle(options)
                        try:
                            pygame.mixer.music.load(correct_song[0])
                            pygame.mixer.music.play()
                            start_ticks = pygame.time.get_ticks()  # Timer for music
                            selected_option = None
                            skipped = False
                            timer_duration = 15
                            while selected_option is None:
                                screen.fill(LIGHT_BLUE)
                                remaining_time = timer_duration - (pygame.time.get_ticks() - start_ticks) // 1000
                                if remaining_time < 0:
                                    remaining_time = 0
                                draw_text(f"Time: {remaining_time}s", 800, 20, BLACK, font_small)
                                draw_text("Guess the Song Title!", 220, 150, YELLOW, font_medium)
                                option_y = 220
                                option_height = 50
                                option_width = 600
                                for i, option in enumerate(options):
                                    option_rect = pygame.Rect(200, option_y + i * (option_height + 10), option_width, option_height)
                                    pygame.draw.rect(screen, LIGHT_GRAY, option_rect, 2, border_radius=10) 
                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                    if option_rect.collidepoint(mouse_x, mouse_y):
                                        pygame.draw.rect(screen, (173, 216, 230), option_rect)  
                                    draw_text(option, 220, option_y + i * (option_height + 10), BLACK, font_small)
                                skip_button_rect = pygame.Rect(400, 500, 200, 50)
                                draw_button(skip_button_rect.x, skip_button_rect.y, skip_button_rect.width, skip_button_rect.height, "Skip", DARK_RED, WHITE)
                                pygame.display.flip()
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_x, mouse_y = event.pos
                                        if skip_button_rect.collidepoint(mouse_x, mouse_y):
                                            skipped = True
                                            pygame.mixer.music.stop()
                                            selected_option = -1  # Indicate skip
                                            break
                                        for i, option in enumerate(options):
                                            option_rect = pygame.Rect(200, option_y + i * (option_height + 10), option_width, option_height)
                                            if option_rect.collidepoint(mouse_x, mouse_y):
                                                selected_option = i
                                                pygame.mixer.music.stop()
                                                break
                                if remaining_time == 0:
                                    skipped = True
                                    break
                                clock.tick(30)
                            if skipped or selected_option == -1:  # Skip button clicked or time ran out
                                game_history.append(("Skipped", correct_title))
                                skipped_questions += 1
                            else:
                                if options[selected_option] == correct_title:
                                    correct_guesses += 1
                                    game_history.append(("Correct", correct_title))
                                else:
                                    incorrect_guesses += 1
                                    game_history.append(("Incorrect", correct_title))

                        except pygame.error as e:
                            print(f"Error playing song: {e}")
                        rounds_played += 1
                    save_user_results(username, correct_guesses, incorrect_guesses, skipped_questions)
                    result = display_summary(correct_guesses, incorrect_guesses, skipped_questions, game_history)
                    if result == "restart":
                        continue  # Restart from Start Game screen
                    else:
                        break
