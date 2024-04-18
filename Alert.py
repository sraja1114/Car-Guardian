import pygame


class Alert:
    def __init__(self):
        self.sensitivity_levels = {
            'high': 1.5,
            'medium': 1.25,
            'low': 1.15
        }

    def play_alert(self, mp3_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file_path)
        pygame.mixer.music.play()

    def pre_collision_warning(self, velocity_mph, distance_in):
        # Convert mph to m/s
        velocity_mps = velocity_mph * 0.44704
        # Convert mph/s to m/s^2
        
        distance_m = distance_in * 0.0254

        stopping_time = distance_m / velocity_mps


        # If the car is too close, issue a warning
        if stopping_time < 0.9:
            print("Warning: Obstacle detected. Please slow down or stop.")
            print(f"Estimated stopping time: {stopping_time} seconds")
            # Play a sound
            self.play_alert("Sounds/forward_collision_warning.mp3")
        else:
            print("No obstacles detected within stopping distance.")
