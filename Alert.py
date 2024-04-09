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

    def pre_collision_warning(self, velocity_mph, acceleration_mphps, distance_in, sensitivity='high'):
        # Convert mph to m/s
        velocity_mps = velocity_mph * 0.44704
        # Convert mph/s to m/s^2
        acceleration_mps2 = acceleration_mphps * 0.44704
        # Convert inches to meters
        distance_m = distance_in * 0.0254

        # Check if acceleration is zero
        if acceleration_mps2 != 0:
            # Calculate stopping distance and time (assuming constant deceleration)
            stopping_distance = (velocity_mps**2) / (2 * acceleration_mps2)
            stopping_time = velocity_mps / acceleration_mps2
        else:
            # Calculate stopping distance and time (assuming constant velocity)
            stopping_distance = distance_m
            stopping_time = distance_m / velocity_mps


        # Adjust stopping distance based on sensitivity level
        stopping_distance *= self.sensitivity_levels[sensitivity]

        # If the car is too close, issue a warning
        if distance_m <= stopping_distance:
            print("Warning: Obstacle detected. Please slow down or stop.")
            print(f"Estimated stopping time: {stopping_time} seconds")
            # Play a sound
            self.play_alert("Sounds/forward_collision_warning.mp3")
        else:
            print("No obstacles detected within stopping distance.")
