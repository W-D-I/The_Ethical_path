import pygame
import cv2

pygame.init()
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

font = pygame.font.SysFont('Comic Sans MS', 30)

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
        all_videos.append(self.video)  # auto track for cleanup

    def update(self):
        if not self.done:
            playing = play_video(screen, self.video)
            if not playing:
                self.done = True

    def finished(self):
        return self.done

    def next(self):
        return self.next_scene_obj

    def release(self):
        self.video.release()

class MenuScene(Scene):
    def __init__(self, options):
        self.options = options  # list of (label, callback)
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        start_y = 200
        width = 400
        height = 60
        gap = 20
        for i, (label, _) in enumerate(self.options):
            rect = pygame.Rect((SCREEN_WIDTH - width)//2, start_y + i * (height + gap), width, height)
            self.buttons.append((rect, label))

    def update(self):
        screen.fill((50, 50, 50))
        for rect, label in self.buttons:
            pygame.draw.rect(screen, (200, 0, 0), rect)
            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        score_text = font.render(f"Career: {career}  Ethics: {ethics}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (rect, _) in enumerate(self.buttons):
                if rect.collidepoint(event.pos):
                    self.options[i][1]()  # call the callback

# ---------------- MAIN MENU ---------------
def main_menu(current_scene, start_callback):
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
            return "../assets/end1.mp4"
        elif ethics >= MAXETHICS or career < ethics:
            return "../assets/end2.mp4"
        else:
            return "../assets/end3.mp4"

    # ------------------ CHAPTER MENUS ------------------
    def chapter1_menu():
        set_scene(MenuScene([
            ("Do the project as the manager instructs", lambda: choose_option("../assets/office.mp4", chapter2, 2, 0)),
            ("Totally refuse to work on this project", lambda: choose_option("../assets/extra1.mp4", chapter2, 0, 2)),
            ("Express your concerns but do what the manager says", lambda: choose_option("../assets/office_1.mp4", chapter2, 1, 1)),
        ]))

    def chapter2_menu():
        set_scene(MenuScene([
            ("Continue your work it is not your responsibility", lambda: choose_option("../assets/office.mp4", chapter3, 2, 0)),
            ("Ask for new data but the project needs more time to complete", lambda: choose_option("../assets/extra1.mp4", chapter3, 0, 2)),
            ("Try to fix bias manually", lambda: choose_option("../assets/office_1.mp4", chapter3, 1, 1)),
        ]))

    def chapter3_menu():
        set_scene(MenuScene([
            ("Optimize the algorithm for engagement", lambda: choose_option("../assets/office.mp4", chapter4, 2, 0)),
            ("Leak the information anonymously", lambda: choose_option("../assets/extra1.mp4", chapter4, 0, 2)),
            ("Try to make it more “neutral”", lambda: choose_option("../assets/office_1.mp4", chapter4, 1, 1)),
        ]))

    def chapter4_menu():
        set_scene(MenuScene([
            ("No, I’ll save up and buy it. Maybe I can take on extra work.", lambda: choose_option("../assets/office.mp4", end_scene, 2, 0)),
            ("Pirating is wrong. I’ll wait for a sale or just skip it.", lambda: choose_option("../assets/extra1.mp4", end_scene, 0, 2)),
            ("I mean… everyone pirates sometimes. I probably won’t get caught.", lambda: choose_option("../assets/office_1.mp4", end_scene, 1, 1)),
        ]))

    # ------------------ VIDEO SCENES ------------------
    intro = VideoScene("../assets/intro.mp4", chapter1_menu)
    chapter1 = VideoScene("../assets/chapter1.mp4", chapter1_menu)
    chapter2 = VideoScene("../assets/2okef.mp4", chapter2_menu)
    chapter3 = VideoScene("../assets/3oKef.mp4", chapter3_menu)
    chapter4 = VideoScene("../assets/chapter4.mp4", chapter4_menu)

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

