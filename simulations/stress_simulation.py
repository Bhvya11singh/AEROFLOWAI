import random


class StressSimulator:

    def __init__(self):

        self.component_factors = {
            "cockpit": 0.3,
            "fuselage_center": 0.5,
            "left_wing": 1.2,
            "right_wing": 1.2,
            "tail": 1.5,
            "vertical_fin": 2.0
        }

    def compute_stress(
        self,
        component,
        wind_speed,
        turbulence
    ):

        base_factor = self.component_factors[component]

        vibration_noise = random.uniform(0.8, 1.2)

        stress = (
            base_factor *
            wind_speed *
            turbulence *
            vibration_noise
        )

        normalized_stress = round(stress / 100, 2)

        return normalized_stress