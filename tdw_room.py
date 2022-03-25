from tdw.controller import Controller
from tdw.add_ons.third_person_camera import ThirdPersonCamera


"""
GOAL: Position the camera so that you can see the box.
"""

# Initialize the controller.
c = Controller()
# Get a unique object ID.
object_id = Controller.get_unique_id()

# This is a bad position for the camera! Change this position.
position = {"x": 0, "y": 0, "z": 0}
camera = ThirdPersonCamera(position=position, look_at=object_id)

# Append the camera add-on.
c.add_ons.append(camera)

# Create a scene. Add an object.
# This will also initialize the camera add-on.
c.communicate([Controller.get_add_scene(scene_name="tdw_room"),
               Controller.get_add_object(model_name="iron_box",
                                         object_id=object_id)])
