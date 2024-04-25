import pygame
import requests
import time

class Alert:
    def __init__(self):
        self.sensitivity_levels = {
            'High': 1.2,
            'Medium': 0.9,
            'Low': 0.6
        }
        self.sensitivity = "Low"
        self.last_get_sensitivity = time.time()
    
    def updateSensivitivty(self):
        current_time = time.time()
        if (current_time - self.last_get_sensitivity > 2):
        #make a get request to the server to get the sensitivity
            response = requests.get("http://localhost:3001/sensitivity")
            self.sensitivity = response.json()["sensitivity"]
            self.last_get_sensitivity = current_time

    
    def play_alert(self, mp3_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file_path)
        pygame.mixer.music.play()

    def pre_collision_warning(self, velocity_mph, distance_in):
        
        self.updateSensivitivty()
        if self.sensitivity != "Low" and self.sensitivity != "Medium" and self.sensitivity != "High":
            self.sensitivity = "High"
        # Convert mph to m/s

        print("Sensitivity", self.sensitivity)
        velocity_mps = velocity_mph * 0.44704
        # Convert mph/s to m/s^2
        
        distance_m = distance_in * 0.025
        print("Vel:", velocity_mps)
        print("Distance:", distance_m)
        
        if distance_m < 1.5:
            return False


        stopping_time = distance_m / velocity_mps

        print("Stopping:", stopping_time)

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
