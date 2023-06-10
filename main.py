import os
import time
import random
import math
import threading
import pygame
from pygame.locals import *


# TODO: Add a way to change the window size
# TODO: Add audio
# TODO: Add settings page
# TODO: Add each animatronic's AI, each animatronic should have a class
# TODO: Add night system, time system, power system, etc

class Animation:
    def __init__(self, frames, speed):
        self.frames = frames
        self.speed = speed
        self.current_frame = 0
        self.last_update = 0

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        return self.get_current_frame()

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def get_frame(self, frame):
        return self.frames[frame]

    def get_frame_count(self):
        return len(self.frames)

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed = speed

    def get_frames(self):
        return self.frames

    def set_frames(self, frames):
        self.frames = frames

    def get_current_frame_index(self):
        return self.current_frame

    def set_current_frame_index(self, index):
        self.current_frame = index

    def get_last_update(self):
        return self.last_update

    def set_last_update(self, last_update):
        self.last_update = last_update

    def get_last_frame(self):
        return self.frames[-1]

    def get_first_frame(self):
        return self.frames[0]

    def get_frame_by_index(self, index):
        return self.frames[index]


class Game:
    def __init__(self, window_size: tuple[int, int] = (1280, 720), fps: int = 60):
        self.window_size = window_size
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.window_size)
        self.running = True
        self.on_menu = True

        pygame.init()
        self.font = pygame.font.Font(r'assets/fonts/font.ttf', 24)
        pygame.display.set_caption("Five Nights at Freddy's 1 - RECREATION")

        self.loading_screen(None)
        self.load()

    def loading_screen(self, custom = None):
        self.screen.fill((0, 0, 0))  # Fill the screen with black color

        if custom is None:
            loading_text = self.font.render("Loading...", True, (255, 255, 255))
        else:
            loading_text = self.font.render(custom, True, (255, 255, 255))
        loading_rect = loading_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(loading_text, loading_rect)

        pygame.display.flip()

    def update_loading_screen(self, type_of_progress, progress):
        self.screen.fill((0, 0, 0))  # Fill the screen with black color

        loading_text = self.font.render(f"Loading {type_of_progress}...   {int(progress * 100)}%", True, (255, 255, 255))
        loading_rect = loading_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(loading_text, loading_rect)

        pygame.display.flip()

    def load(self):
        print("Attempting to load rest of sprites in mass... Wish for the best")
        start = time.perf_counter()

        sprites_directory = 'assets/sprites'
        self.sprites = []
        self.animations = {
            'freddy': {},
            'bonnie': {},
            'chica': {},
            'foxy': {},
            'title': {}
        }
        total_files = 0
        loaded_files = 0

        for root, dirs, files in os.walk(sprites_directory):
            total_files += len(files)

        for root, dirs, files in os.walk(sprites_directory):
            for file in files:
                if file.endswith('.png'):
                    path = os.path.join(root, file)
                    image = pygame.image.load(path)

                    # Extract parent folder and file name
                    parent_folder = os.path.basename(root)
                    file_name = os.path.splitext(file)[0]

                    # Create the description using parent folder and file name
                    description = f"{parent_folder}/{file_name}"

                    # Create a dictionary with the image details
                    image_details = {
                        'description': description,
                        'surface': image
                    }

                    self.sprites.append(image_details)

                    loaded_files += 1
                    progress = loaded_files / total_files
                    self.update_loading_screen('sprites', progress)

        print(f"Loaded {len(self.sprites)} sprites in {time.perf_counter() - start} seconds")
        self.loading_screen('Creating animations...')

        start = time.perf_counter()
        print(f"Creating animations...")
        # Create animations with the sprites
        self.create_animation('freddy', 'freddy', 0.1)
        self.create_animation('freddy', 'no_power', 0.1)
        print("Made freddy animations")

        self.create_animation('bonnie', 'bonnie', 0.1)
        print("Made bonnie animations")

        self.create_animation('chica', 'chica', 0.1)
        print("Made chica animations")

        self.create_animation('foxy', 'foxy', 0.1)
        self.create_animation('foxy', 'foxy_run', 0.1)
        print("Made foxy animations")

        self.create_animation('title', None, 700)
        print("Made title animation")

        print(f"Created animations in {time.perf_counter() - start} seconds")

    def create_animation(self, name: str, subtype: None, speed: int | float):
        # Hardcoded animations, quicker and easier to do
        animations = {
            'animatronics': {
                'freddy': {
                    'types': ['freddy', 'freddy_no_power'],
                    'frames': {
                        'freddy': ['power/1', 'power/2', 'power/3', 'power/4', 'power/5', 'power/6', 'power/7',
                                   'power/8', 'power/9', 'power/10', 'power/11', 'power/12', 'power/13', 'power/14',
                                   'power/15', 'power/16', 'power/17', 'power/18', 'power/19', 'power/20', 'power/21',
                                   'power/22', 'power/23', 'power/24', 'power/25', 'power/26', 'power/27', 'power/28'],
                        'freddy_no_power': ['no_power/1', 'no_power/2', 'no_power/3', 'no_power/4', 'no_power/5',
                                            'no_power/6', 'no_power/7', 'no_power/8', 'no_power/9', 'no_power/10',
                                            'no_power/11', 'no_power/12', 'no_power/13', 'no_power/14', 'no_power/15',
                                            'no_power/16', 'no_power/17', 'no_power/18', 'no_power/19']
                    }
                },
                'bonnie': {
                    'types': ['bonnie'],
                    'frames': {
                        'bonnie': ['bonne/1', 'bonne/2', 'bonne/3', 'bonne/4', 'bonne/5', 'bonne/6', 'bonne/7',
                                   'bonne/8', 'bonne/9', 'bonne/10', 'bonne/11']
                    }
                },
                'chica': {
                    'types': ['chica'],
                    'frames': {
                        'chica': ['chica/1', 'chica/2', 'chica/3', 'chica/4', 'chica/5', 'chica/6', 'chica/7',
                                  'chica/8', 'chica/9', 'chica/10', 'chica/11', 'chica/12', 'chica/13', 'chica/14',
                                  'chica/15', 'chica/16']
                    }
                },
                'foxy': {
                    'types': ['foxy', 'foxy_run'],
                    'frames': {
                        'foxy': ['foxy/1', 'foxy/2', 'foxy/3', 'foxy/4', 'foxy/5', 'foxy/6', 'foxy/7', 'foxy/8',
                                 'foxy/9', 'foxy/10', 'foxy/11', 'foxy/12', 'foxy/13', 'foxy/14', 'foxy/15', 'foxy/16',
                                 'foxy/17', 'foxy/18', 'foxy/19', 'foxy/20', 'foxy/21'],
                        'foxy_run': ['foxy_run/1', 'foxy_run/2', 'foxy_run/3', 'foxy_run/4', 'foxy_run/5', 'foxy_run/6',
                                     'foxy_run/7', 'foxy_run/8', 'foxy_run/9', 'foxy_run/10', 'foxy_run/11',
                                     'foxy_run/12', 'foxy_run/13', 'foxy_run/14', 'foxy_run/15', 'foxy_run/16',
                                     'foxy_run/17', 'foxy_run/18', 'foxy_run/19', 'foxy_run/20', 'foxy_run/21',
                                     'foxy_run/22', 'foxy_run/23', 'foxy_run/24', 'foxy_run/25', 'foxy_run/26',
                                     'foxy_run/27', 'foxy_run/28', 'foxy_run/29']
                    }
                }
            }
        }

        if name in ['freddy', 'bonnie', 'chica', 'foxy']:
            animation = animations['animatronics'][name]
            if name == 'freddy' and subtype == 'freddy_no_power':
                type_of_animation = animation['types'][1]
            else:
                type_of_animation = animation['types'][0]

            if name == 'foxy' and subtype == 'foxy_run':
                type_of_animation = animation['types'][1]
            else:
                type_of_animation = animation['types'][0]

            if name == 'chica':
                type_of_animation = animation['types'][0]

            if name == 'bonnie':
                type_of_animation = animation['types'][0]

            frames = animation['frames'][type_of_animation]
            self.animations[name][subtype] = Animation(frames, speed)
        elif name == 'title':
            # The title requires you to combine frames, so we'll do that here
            freddy_frames = []
            static_frames = []

            for entry in self.sprites:
                parent_folder, file_name = entry['description'].split('/')
                print("Parent folder:", parent_folder)
                print("Entry description:", entry['description'])

                if entry['description'] in ['secrets/f1', 'secrets/f2', 'secrets/f3', 'secrets/f4']:
                    freddy_frames.append(entry['surface'])
                elif 'static' in entry['description']:
                    static_frames.append(entry['surface'])

            # Combine the Freddy frames and static frames
            combined_frames = []
            for freddy_frame, static_frame in zip(freddy_frames, static_frames):
                # Create a surface with the same size as the Freddy frame
                combined_frame = pygame.Surface(freddy_frame.get_size())

                # Blit the Freddy frame onto the combined surface
                combined_frame.blit(freddy_frame, (0, 0))

                # Blit the static frame onto the combined surface with the overlay effect
                combined_frame.blit(static_frame, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

                # Append the combined frame to the list of combined frames
                combined_frames.append(combined_frame)
            # Create the animation
            self.animations['title']['anim'] = Animation(combined_frames, speed)

    def title(self):
        # Background Animation
        self.screen.blit(self.animations['title']['anim'].update(), (0, 0))

        # Title Banner
        title_lines = ["Five", "Nights", "at", "Freddy's", "REMAKE"]
        font_sizes = [30, 30, 30, 30, 30]
        line_positions = [(176, 50), (176, 90), (176, 130), (170, 170), (176, 220)]
        for line, size, position in zip(title_lines, font_sizes, line_positions):
            font = pygame.font.Font("assets/fonts/font.ttf", size)
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(topleft=position)
            self.screen.blit(text, text_rect)

        # Display text for buttons
        play_text = self.font.render('New Game', True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=(236, 475))

        continue_text = self.font.render('Continue', True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=(236, 534))

        # Check if mouse is hovering over button
        if play_text_rect.collidepoint(pygame.mouse.get_pos()):
            # Add >> to the text
            play_text = self.font.render('>> New Game', True, (255, 255, 255))

        if continue_text_rect.collidepoint(pygame.mouse.get_pos()):
            # Add >> to the text
            continue_text = self.font.render('>> Continue', True, (255, 255, 255))

        # Create a transparent surface for text rendering
        text_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)

        # Draw text on the transparent surface
        text_surface.blit(play_text, play_text_rect)
        text_surface.blit(continue_text, continue_text_rect)

        # Blit the transparent surface onto the screen
        self.screen.blit(text_surface, (0, 0))

        # Check if button is clicked
        if play_text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.running = False

        if continue_text_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.running = False

    def count_files(self, descriptions):
        count = 0
        for description in descriptions:
            files = description.get("files", [])
            count += len(files)
        return count

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black color
        # FPS Banner
        fps = self.font.render(f'FPS: {round(self.clock.get_fps())}', True, (255, 255, 255))
        self.screen.blit(fps, (0, 0))

        if self.on_menu:
            self.title()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()