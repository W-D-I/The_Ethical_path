import pygame
import cv2

pygame.init()
clock = pygame.time.Clock()

#________SCORE COUNTERS_______________
career=0
ethics=0
MAXCAREER=10
MAXETHICS=10


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Visual Novel Example")

font = pygame.font.SysFont('Comic Sans MS', 30)

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

class VideoScene(Scene):
    def __init__(self, path, next_scene=None):
        self.video = cv2.VideoCapture(path)
        self.next_scene = next_scene
        self.done = False

    def update(self):
        if not self.done:
            playing = play_video(screen, self.video)
            if not playing:
                self.done = True

    def finished(self):
        return self.done

    def next(self):
        return self.next_scene

    def release(self):
        self.video.release()

class MenuScene(Scene):
    def __init__(self, options):
        self.options = options  # list of (label, callback)
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        start_y = 200
        width = 200
        height = 60
        gap = 20
        for i, (label, _) in enumerate(self.options):
            rect = pygame.Rect(540, start_y + i * (height + gap), width, height)
            self.buttons.append((rect, label))

    def update(self):
        screen.fill((50, 50, 50))
        for rect, label in self.buttons:
            pygame.draw.rect(screen, (200, 0, 0), rect)
            text = font.render(label, True, (255, 255, 255))
            screen.blit(text, (rect.x + 10, rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, (rect, _) in enumerate(self.buttons):
                if rect.collidepoint(event.pos):
                    # call the callback
                    self.options[i][1]()

# ------------------ GAME ------------------
def main():
    # We will use a mutable object to allow callbacks to change the current scene
    current_scene = {"scene": None}

    # ---------------- Define Scenes ----------------
    # Later options can change this dict to update scene

    # Ending scenes
    end_scene = MenuScene([
        ("The End", lambda: None)
    ])
    #____________________-ENDING __________________
    if career==MAXCAREER or career>ethics:
        end_video="./assets/end1.mp4"
    elif ethics==MAXETHICS or career<ethics:
        end_video="./assets/end2.mp4"
    else:
        end_video="./assets/end3.mp4"
    end = VideoScene(end_video, None)

    #_______________ CHAPTER 4______________________
    def chapter4_menu():
        current_scene["scene"] = MenuScene([
            ("Continue your work it is not your responsibility", lambda: set_scene(vc21)),
            ("Ask for new data but the project needs more time to complete", lambda: set_scene(vc22)),
            ("Try to fix bias manually", lambda: set_scene(vc23)),
        ])

    chapter4 = VideoScene("./assets/chapter4.mp4", next_scene=chapter4_menu)
    
    vc41 = VideoScene("./assets/office.mp4", next_scene=end)

    # Path B video
    vc42= VideoScene("./assets/extra1.mp4", next_scene=end)

    vc43 = VideoScene("./assets/office_1.mp4", next_scene=end)
    # ___________________ CHAPTER 3______________________
    def chapter3_menu():
        current_scene["scene"] = MenuScene([
            ("Continue your work it is not your responsibility", lambda: choose_option(vc31,2,0)),
            ("Ask for new data but the project needs more time to complete", lambda: choose_option(vc32,0,2)),
            ("Try to fix bias manually", lambda: choose_option(vc33,1,1)),
        ])

    chapter3 = VideoScene("./assets/3okef.mp4", next_scene=chapter3_menu)
    
    vc31 = VideoScene("./assets/office.mp4", next_scene=chapter3)

    # Path B video
    vc32= VideoScene("./assets/extra1.mp4", next_scene=chapter3)

    vc33 = VideoScene("./assets/office_1.mp4", next_scene=chapter3)
    # _____ CHAPTER 2 _____________
    def chapter2_menu():
        current_scene["scene"] = MenuScene([
            ("Continue your work it is not your responsibility", lambda: choose_option(vc21,2,0)),
            ("Ask for new data but the project needs more time to complete", lambda: choose_option(vc22,0,2)),
            ("Try to fix bias manually", lambda: choose_option(vc23,1,1)),
        ])

    chapter2 = VideoScene("./assets/2okef.mp4", next_scene=chapter2_menu)
    
    vc21 = VideoScene("./assets/office.mp4", next_scene=chapter3)

    # Path B video
    vc22= VideoScene("./assets/extra1.mp4", next_scene=chapter3)

    vc23 = VideoScene("./assets/office_1.mp4", next_scene=chapter3)

    # Menu after chapter1
    def chapter1_menu():
        current_scene["scene"] = MenuScene([
            ("Do the project as the manager instructs", lambda: choose_option(vc11,2,0)),
            ("Totally refuse to work on this project", lambda: choose_option(vc12,0,2)),
            ("Express your concerns but do what the manager says", lambda: choose_option(vc13,1,1)),
        ])

    chapter1 = VideoScene("./assets/chapter1.mp4", next_scene=chapter1_menu)

    # Path A video
    vc11 = VideoScene("./assets/office.mp4", next_scene=chapter2)

    # Path B video
    vc12= VideoScene("./assets/extra1.mp4", next_scene=chapter2)

    vc13 = VideoScene("./assets/office_1.mp4", next_scene=chapter2)

     
    # Intro video
    intro = VideoScene("./assets/intro.mp4", next_scene=chapter1)

    # ---------------- Helper to switch scene ----------------
    def set_scene(scene_obj):
        current_scene["scene"] = scene_obj

    def choose_option(next_scene, career_incr=0, ethics_incr=0):
        global career, ethics
        career += career_incr
        ethics += ethics_incr
        set_scene(next_scene)
    # Start game
    current_scene["scene"] = intro

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if current_scene["scene"]:
                current_scene["scene"].handle_event(event)

        screen.fill((0, 0, 0))
        if current_scene["scene"]:
            current_scene["scene"].update()
            finished = current_scene["scene"].finished()
            if finished:
                next_scene = current_scene["scene"].next()
                if callable(next_scene):
                    next_scene()  # dynamic menu creation
                elif next_scene:
                    set_scene(next_scene)

        pygame.display.update()
        clock.tick(30)

    # Release videos
    intro.release()
    chapter1.release()
    video_path_a.release()
    video_path_b.release()
    pygame.quit()

if __name__ == "__main__":
    main()
