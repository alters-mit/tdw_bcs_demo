from typing import Dict
from tdw.controller import Controller
from tdw.add_ons.third_person_camera import ThirdPersonCamera
from tdw.add_ons.collision_manager import CollisionManager
from tdw.add_ons.object_manager import ObjectManager


class UseTheForce(Controller):
    """
    GOAL: Apply a force to a ball in order to knock objects off the table.
    """

    def __init__(self, port: int = 1071, check_version: bool = True, launch_build: bool = True):
        super().__init__(port=port, check_version=check_version, launch_build=launch_build)

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
        while not done:
            done = True
            for object_id in object_manager.objects_static:
                # At least one object is still moving.
                if not object_manager.rigidbodies[object_id].sleeping:
                    done = False
                    break
            # Advance one frame.
            self.communicate([])
        # Check if all objects are on the floor.
        all_objects_are_on_floor = len(collision_manager.env_collisions) == len(object_manager.objects_static)
        return all_objects_are_on_floor


if __name__ == "__main__":
    c = UseTheForce()
    success = c.trial(camera_position={"x": 2, "y": 2.5, "z": 0.5},
                      ball_bounciness=0.8,
                      ball_mass=10,
                      ball_force=8,
                      ball_position={"x": 2, "y": 2.5, "z": 0})
    print(success)
    c.communicate({"$type": "terminate"})
