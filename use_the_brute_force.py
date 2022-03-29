from typing import Dict
import numpy as np
from tdw.controller import Controller
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.collision_manager import CollisionManager
from tdw.add_ons.object_manager import ObjectManager


class UseTheBruteForce(Controller):
    """
    GOAL: Use an automated brute-force method to find a solution to the `UseTheForce` demo.
    """

    def trial(self, camera_position: Dict[str, float], ball_position: Dict[str, float],
              ball_bounciness: float, ball_mass: float, ball_force: float):
        # Clear the list of add-ons.
        self.add_ons.clear()
        # Add a camera.
        camera = ThirdPersonCamera(position=camera_position,
                                   look_at={"x": 0, "y": 0.5, "z": 0})
        # Add a collision manager.
        collision_manager = CollisionManager(enter=True, stay=True, exit=True)
        # Add an object manager.
        object_manager = ObjectManager(transforms=False, rigidbodies=True, bounds=False)
        self.add_ons.extend([camera, collision_manager, object_manager])
        # Add the scene.
        commands = [Controller.get_add_scene(scene_name="tdw_room")]
        # Add a table with objects on it.
        commands.extend(Controller.get_add_physics_object(model_name="small_table_green_marble",
                                                          object_id=Controller.get_unique_id()))
        commands.extend(Controller.get_add_physics_object(model_name="rh10",
                                                          position={"x": 0.7, "y": 0, "z": 0.4},
                                                          rotation={"x": 0, "y": 30, "z": 0},
                                                          object_id=Controller.get_unique_id()))
        commands.extend(Controller.get_add_physics_object(model_name="jug01",
                                                          position={"x": -0.3, "y": 0.9, "z": 0.2},
                                                          object_id=Controller.get_unique_id()))
        commands.extend(Controller.get_add_physics_object(model_name="jug05",
                                                          position={"x": 0.3, "y": 0.9, "z": -0.2},
                                                          object_id=Controller.get_unique_id()))
        # Add a ball.
        ball_id = Controller.get_unique_id()
        commands.extend(Controller.get_add_physics_object(model_name="sphere",
                                                          position=ball_position,
                                                          object_id=ball_id,
                                                          scale_factor={"x": 0.2, "y": 0.2, "z": 0.2},
                                                          default_physics_values=False,
                                                          dynamic_friction=0.9,
                                                          static_friction=0.9,
                                                          bounciness=ball_bounciness,
                                                          mass=ball_mass,
                                                          scale_mass=False,
                                                          library="models_flex.json"))
        # Rotate the ball.
        commands.append({"$type": "object_look_at_position",
                         "position": {"x": 0, "y": 0.5, "z": 0},
                         "id": ball_id})
        # Apply a force to the ball.
        commands.append({"$type": "apply_force_magnitude_to_object",
                         "magnitude": ball_force,
                         "id": ball_id})
        # Send the commands.
        self.communicate(commands)

        # Use the `ObjectManager` to wait until objects stop moving (when they are "sleeping").
        done = False
        num = 0
        while not done and num < 500:
            done = True
            for object_id in object_manager.objects_static:
                # At least one object is still moving.
                if not object_manager.rigidbodies[object_id].sleeping:
                    done = False
                    break
            # Advance one frame.
            self.communicate([])
            num += 1
        # Check if all objects are on the floor.
        all_objects_are_on_floor = len(collision_manager.env_collisions) == len(object_manager.objects_static)
        return all_objects_are_on_floor

    def run(self):
        """
        Run a series of trials.
        """

        camera_position = {"x": 2, "y": 2.5, "z": 1.5}
        for ball_bounciness in np.arange(0.1, 1.1, step=0.1, dtype=float):
            for ball_mass in np.arange(5, 15, dtype=int):
                for ball_force in np.arange(10, 40, step=5, dtype=int):
                    for ball_x in np.arange(1, 3, step=0.2, dtype=float):
                        for ball_y in np.arange(1.5, 3, step=0.2, dtype=float):
                            # Run a trial.
                            success = self.trial(camera_position=camera_position,
                                                 ball_bounciness=float(ball_bounciness),
                                                 ball_mass=float(ball_mass),
                                                 ball_force=float(ball_force),
                                                 ball_position={"x": float(ball_x), "y": float(ball_y), "z": 0})
                            if success:
                                return {"ball_bounciness": ball_bounciness,
                                        "ball_mass": ball_mass,
                                        "ball_force": ball_force,
                                        "ball_position": {"x": ball_x, "y": ball_y, "z": 0}}
        raise Exception("No solution found.")


if __name__ == "__main__":
    c = UseTheBruteForce()
    solution = c.run()
    print(solution)
    c.communicate({"$type": "terminate"})
