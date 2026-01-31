import pygame
import cv2
import os 

cwd = os.getcwd() 
print(cwd)
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# --------- SCORE COUNTERS -----------
career = 0
ethics = 0
MAXCAREER = 6
MAXETHICS = 6

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Visual Novel Example")

font = pygame.font.SysFont('DejaVu Sans', 30)
title_font = pygame.font.SysFont('DejaVu Sans', 72, bold=True)
button_font = pygame.font.SysFont("DejaVu Sans", 22, bold=True)

# Menu BG
MENU_BG = pygame.image.load("./Ethic_game/assets/bg.jpg").convert()
MENU_BG = pygame.transform.scale(MENU_BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

music_volume = 0.4
music_muted = False

# Text-wrap helper
def render_multiline_text(text, font, color, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    if current_line:
        lines.append(current_line)

    rendered_lines = [font.render(line.strip(), True, color) for line in lines]
    return rendered_lines

# Keep track of all videos for cleanup
all_videos = []

# ------------------ VIDEO PLAY FUNCTION ------------------
def play_video(surface, video_capture):
    ret, frame = video_capture.read()
    if not ret:
        return False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, surface.get_size())
    surf = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    surface.blit(surf, (0, 0))
    return True

# ------------------- MUSIC MANAGER -----------------------
def play_music(path, loop=-1):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0 if music_muted else music_volume)
    pygame.mixer.music.play(loop)

def apply_music_volume():
    pygame.mixer.music.set_volume(0 if music_muted else music_volume)

def stop_music(fade_ms=1000):
    pygame.mixer.music.fadeout(fade_ms)

# SLIDER UI
def draw_slider(surface, x, y, width, value):
    # Track
    pygame.draw.rect(surface, (120, 120, 120), (x, y, width, 6), border_radius=3)

    # Knob
    knob_x = x + int(width * value)
    pygame.draw.circle(surface, (255, 255, 255), (knob_x, y + 3), 8)

    return pygame.Rect(x, y - 10, width, 20)



# ------------------ SCENE CLASSES ------------------
class Scene:
    def update(self):
        pass
    def handle_event(self, event):
        pass
    def finished(self):
        return False
    def next(self):
        return None

class VideoScene(Scene):
    def __init__(self, path, next_scene=None):
        self.video = cv2.VideoCapture(path)
        if not self.video.isOpened():
            print(f"Failed to load video: {path}")

        self.next_scene_obj = next_scene
        self.done = False

        # UI
        self.skip_rect = pygame.Rect(SCREEN_WIDTH - 160, 20, 140, 50)

        # Fast-forward settings
        self.normal_speed = 1
        self.fast_speed = 6

        all_videos.append(self.video)

    def update(self):
        if self.done:
            return

        # Check fast-forward
        keys = pygame.key.get_pressed()
        speed = self.fast_speed if keys[pygame.K_f] else self.normal_speed
        # speed = self.fast_speed if keys[pygame.K_f] or keys[pygame.K_RIGHT] else self.normal_speed

        # Play multiple frames per update if fast-forwarding
        for _ in range(speed):
            playing = play_video(screen, self.video)
            if not playing:
                self.done = True
                break

        # Draw skip button
        pygame.draw.rect(screen, (0, 0, 0), self.skip_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.skip_rect, 2)
        text = font.render("Skip ▶▶", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=self.skip_rect.center))

        # Fast-forward indicator
        if speed > 1:
            ff_text = font.render("⏩ FAST FORWARD", True, (255, 255, 0))
            screen.blit(ff_text, (20, SCREEN_HEIGHT - 50))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.skip_rect.collidepoint(event.pos):
                self.done = True

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                self.done = True

    def finished(self):
        return self.done

    def next(self):
        return self.next_scene_obj

class MenuScene(Scene):
    def __init__(self, options):
        self.options = options  # list of (label, callback)
        self.buttons = []
        self.pressed_index = None
        self.selected_index = 0  # currently selected button
        self.create_buttons()

        self.options = options
        self.buttons = []

        self.pressed_index = None
        self.selected_index = 0

        # Slider positioning
        self.slider_width = 400
        self.slider_x = (SCREEN_WIDTH - self.slider_width) // 2
        self.slider_y = SCREEN_HEIGHT - 40

        self.slider_hitbox = pygame.Rect(
            self.slider_x,
            self.slider_y - 10,
            self.slider_width,
            20
        )

        self.mute_rect = pygame.Rect(
            self.slider_x + self.slider_width + 30,
            self.slider_y - 20,
            120,
            40
        )

        # 🔴 THIS WAS MISSING
        self.dragging_slider = False

        self.create_buttons()


    def create_buttons(self):
        start_y = 260
        width = 500
        height = 70
        gap = 20

        for i, (label, _) in enumerate(self.options):
            rect = pygame.Rect(
                (SCREEN_WIDTH - width) // 2,
                start_y + i * (height + gap),
                width,
                height
            )
            self.buttons.append((rect, label))

    def update(self):
        # Background
        screen.blit(MENU_BG, (0, 0))

        # ----- TITLE -----
        title_text = title_font.render("Ethic Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))

        shadow = title_font.render("Ethic Game", True, (0, 0, 0))
        screen.blit(shadow, title_rect.move(4, 4))
        screen.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        # ----- BUTTONS -----
        for i, (rect, label) in enumerate(self.buttons):
            hovered = rect.collidepoint(mouse_pos) or (i == self.selected_index)
            if i == self.selected_index:
                arrow = font.render("▶", True, (255, 255, 0))
                screen.blit(arrow, (rect.left - 30, rect.centery - arrow.get_height() // 2))

            pressed = self.pressed_index == i

            # Colors
            base_color = (170, 0, 0)
            hover_color = (220, 40, 40)
            color = hover_color if hovered else base_color

            # Press animation
            y_offset = 4 if pressed else 0
            draw_rect = rect.move(0, y_offset)

            # Shadow
            shadow_rect = draw_rect.move(0, 6)
            pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=14)

            # Button
            pygame.draw.rect(screen, color, draw_rect, border_radius=14)

            # Text
            padding = 20
            text_surfaces = render_multiline_text(
                label,
                button_font,
                (255, 255, 255),
                draw_rect.width - padding * 2
            )

            total_height = sum(t.get_height() for t in text_surfaces)
            start_y = draw_rect.centery - total_height // 2

            for line in text_surfaces:
                line_rect = line.get_rect(centerx=draw_rect.centerx, y=start_y)
                screen.blit(line, line_rect)
                start_y += line.get_height()

        # ---- MUSIC UI ----
        vol_text = font.render("Music", True, (255, 255, 255))
        screen.blit(
            vol_text,
            (self.slider_x - vol_text.get_width() - 20, self.slider_y - 12)
        )

        draw_slider(
            screen,
            self.slider_x,
            self.slider_y,
            self.slider_width,
            music_volume
        )

        # Mute button
        mute_label = "Unmute" if music_muted else "Mute"
        pygame.draw.rect(screen, (60, 60, 60), self.mute_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), self.mute_rect, 2, border_radius=8)

        mute_text = font.render(mute_label, True, (255, 255, 255))
        screen.blit(mute_text, mute_text.get_rect(center=self.mute_rect.center))


        # Score (optional)
        '''score_text = font.render(f"Career: {career}  Ethics: {ethics}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))'''

    def handle_event(self, event):
        global music_volume, music_muted

        # ---------------- MOUSE DOWN ----------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Buttons
            for i, (rect, _) in enumerate(self.buttons):
                if rect.collidepoint(event.pos):
                    self.pressed_index = i

            # Slider click
            if self.slider_hitbox.collidepoint(event.pos):
                self.dragging_slider = True

            # Mute button
            if self.mute_rect.collidepoint(event.pos):
                music_muted = not music_muted
                apply_music_volume()

        # ---------------- MOUSE UP ----------------
        if event.type == pygame.MOUSEBUTTONUP:
            for i, (rect, _) in enumerate(self.buttons):
                if rect.collidepoint(event.pos) and self.pressed_index == i:
                    self.options[i][1]()

            self.pressed_index = None
            self.dragging_slider = False

        # ---------------- MOUSE DRAG (SLIDER) ----------------
        if event.type == pygame.MOUSEMOTION and self.dragging_slider:
            x = max(self.slider_x, min(event.pos[0], self.slider_x + self.slider_width))
            music_volume = (x - self.slider_x) / self.slider_width
            apply_music_volume()

        # ---------------- KEYBOARD NAVIGATION ----------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)

            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)

            elif event.key == pygame.K_RETURN:
                self.options[self.selected_index][1]()

            # ---- MUSIC KEYS ----
            elif event.key == pygame.K_m:
                music_muted = not music_muted
                apply_music_volume()

            elif event.key == pygame.K_LEFT:
                music_volume = max(0.0, music_volume - 0.05)
                apply_music_volume()

            elif event.key == pygame.K_RIGHT:
                music_volume = min(1.0, music_volume + 0.05)
                apply_music_volume()


# ---------------- MAIN MENU ---------------
def main_menu(current_scene, start_callback):
    play_music("./Ethic_game/assets/dejavu.mp3")
    menu = MenuScene([
        ("Start Game", start_callback),
        ("Quit", exit_game)
    ])
    current_scene["scene"] = menu

def exit_game():
    global running
    running = False
    for video in all_videos:
        video.release()

# ------------------ GAME ------------------
def main():
    global career, ethics

    current_scene = {"scene": None}

    def set_scene(scene_obj):
        current_scene["scene"] = scene_obj

    def choose_option(video_path, next_scene, career_incr=0, ethics_incr=0):
        global career, ethics
        career += career_incr
        ethics += ethics_incr
        # create a fresh VideoScene
        set_scene(VideoScene(video_path, next_scene))

    def back_to_main_menu():
        global career, ethics
        career = 0
        ethics = 0
        main_menu(current_scene, start_game)

    # ------------------ ENDING ------------------
    def choose_ending():
        if career >= MAXCAREER or career > ethics:
            return "./Ethic_game/assets/evilcore.mp4"
        elif ethics >= MAXETHICS or career < ethics:
            return "./Ethic_game/assets/ethical_ending.mp4"
        else:
            return "./Ethic_game/assets/end3.mp4"

    # ------------------ CHAPTER MENUS ------------------
    def chapter1_menu():
        set_scene(MenuScene([
            ("Do the project as the manager instructs", lambda: choose_option("./Ethic_game/assets/office.mp4", chapter2, 2, 0)),
            ("Totally refuse to work on this project", lambda: choose_option("./Ethic_game/assets/extra1.mp4", chapter2, 0, 2)),
            ("Express your concerns but do what the manager says", lambda: choose_option("./Ethic_game/assets/office_1.mp4", chapter2, 1, 1)),
        ]))

    def chapter2_menu():
        set_scene(MenuScene([
            ("Continue your work it is not your responsibility", lambda: choose_option("./Ethic_game/assets/tv.mp4", chapter3, 2, 0)),
            ("Ask for new data but the project needs more time to complete", lambda: choose_option("./Ethic_game/assets/extra1.mp4", chapter3, 0, 2)),
            ("Try to fix bias manually", lambda: choose_option("./Ethic_game/assets/office_1.mp4", chapter3, 1, 1)),
        ]))

    def chapter3_menu():
        set_scene(MenuScene([
            ("Optimize the algorithm for engagement", lambda: choose_option("./Ethic_game/assets/office.mp4", chapter4, 2, 0)),
            ("Leak the information anonymously", lambda: choose_option("./Ethic_game/assets/extra1.mp4", chapter4, 0, 2)),
            ("Try to make it more “neutral”", lambda: choose_option("./Ethic_game/assets/office_1.mp4", chapter4, 1, 1)),
        ]))

    def chapter4_menu():
        set_scene(MenuScene([
            ("No, I’ll save up and buy it. Maybe I can take on extra work.", lambda: choose_option("./Ethic_game/assets/office.mp4", end_scene, 2, 0)),
            ("Pirating is wrong. I’ll wait for a sale or just skip it.", lambda: choose_option("./Ethic_game/assets/extra1.mp4", end_scene, 0, 2)),
            ("I mean… everyone pirates sometimes. I probably won’t get caught.", lambda: choose_option("./Ethic_game/assets/office_1.mp4", end_scene, 1, 1)),
        ]))

    # ------------------ VIDEO SCENES ------------------
    intro = VideoScene("./Ethic_game/assets/intro.mp4",lambda: set_scene(chapter1))
    chapter1 = VideoScene("./Ethic_game/assets/chapter1.mp4", chapter1_menu)
    chapter2 = VideoScene("./Ethic_game/assets/2okef.mp4", chapter2_menu)
    chapter3 = VideoScene("./Ethic_game/assets/3oKef.mp4", chapter3_menu)
    chapter4 = VideoScene("./Ethic_game/assets/chapter4.mp4", chapter4_menu)

    # End scene menu
    def end_scene():
        set_scene(VideoScene(choose_ending(), back_to_main_menu))

    def start_game():
        global career, ethics
        career = 0
        ethics = 0
        set_scene(intro)

    # Start at main menu
    main_menu(current_scene, start_game)

    # ------------------ MAIN LOOP ------------------
    global running
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if current_scene["scene"]:
                current_scene["scene"].handle_event(event)

        screen.fill((0,0,0))
        if current_scene["scene"]:
            current_scene["scene"].update()
            finished = current_scene["scene"].finished()
            if finished:
                next_scene = current_scene["scene"].next()
                if callable(next_scene):
                    next_scene()
                elif next_scene:
                    set_scene(next_scene)

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()

