import pygame


class Alert:
    def __init__(self):
        self.sensitivity_levels = {
            'High': 1.2,
            'Medium': 0.9,
            'Low': 0.6
        }
        self.sensitivity = "Low"
    
    def updateSensivitivty(self):
        with open("/Users/jasonsze/Desktop/CSCE 483/repo/YOLOv4-distance-tracking/sensitivity.txt", "r") as file:
            content = str(file.read())
            self.sensitivity = content
    
    def play_alert(self, mp3_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file_path)
        pygame.mixer.music.play()

    def pre_collision_warning(self, velocity_mph, distance_in):
        
        self.updateSensivitivty()
        if self.sensitivity != "Low" or self.sensitivity != "Medium" or self.sensitivity != "High":
            self.sensitivity = "High"
        # Convert mph to m/s
        velocity_mps = velocity_mph * 0.44704
        # Convert mph/s to m/s^2
        
        distance_m = distance_in * 0.0254

        stopping_time = distance_m / velocity_mps


        # If the car is too close, issue a warning
        if stopping_time < self.sensitivity_levels[self.sensitivity]:
            print("Warning: Obstacle detected. Please slow down or stop.")
            print(f"Estimated stopping time: {stopping_time} seconds")
            # Play a sound
            self.play_alert("Sounds/forward_collision_warning.mp3")
            return True
        else:
            print("No obstacles detected within stopping distance.")
            return False
