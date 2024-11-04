import math
import numpy as np

screen = (800, 600)

'''
BUG:
The z-axis rotates unexpectedly when only the x-axis and y-axis is supposed to rotate.
This occurs during the rendering of 3D axes in the _3d_axis class
and in raycast_transform
So when, in the simulation, you turn head right or left, it's like you're in a plane
it uses roll instead of yaw but only if pitch is not equal to k * pi (k belonging to the integers)

==> Look at the comments at the bottom, where if __name__=="__main__": is written
I made some test, you can run the code
'''

class Camera:
    def __init__(self, position:tuple, rotation:tuple) -> None:
        '''
        ˗ˋˏ ♡ ˎˊ˗

        Initialize the camera with a given position and rotation.

        :param position: A tuple (x, y, z) representing the camera's position in 3D space.
        :param rotation: A tuple (yaw, pitch) representing the camera's orientation.
        yaw : rotation around the vertical axis (left-right)
        pitch : rotation around the horizontal axis (up-down)
        '''
        self.x, self.y, self.z = position
        self.yaw, self.pitch = rotation

    def move(self, position2=None, rotation2=None):
        '''
        Move the camera by a specified position and/or rotation.
        
        :param position2: A tuple (dx, dy, dz) to change the current position.
        :param rotation2: A tuple (dyaw, dpitch) to change the current rotation.
        '''
        if position2:
            self.x += position2[0]
            self.y += position2[1]
            self.z += position2[2]
        if rotation2:
            self.yaw += rotation2[0]
            self.pitch += rotation2[1]

    def moveTo(self, position2):
        '''
        Move the camera to an exact position.
        
        :param position2: A tuple (x, y, z) to set the camera's position.
        '''
        self.x = position2[0]
        self.y = position2[1]
        self.z = position2[2]

    def __str__(self) -> str:
        return f"Camera(\tposition : ({self.x}, {self.y}, {self.z}) | yaw : {self.yaw} | pitch : {self.pitch} )"


def raycast_transform(camera:Camera, point_pos:tuple, screen=screen) ->  tuple:
    '''
    ˗ˋˏ ♡ ˎˊ˗

    Transforms a 3D point's position to 2D screen coordinates based on the camera's perspective.

    :param camera: An instance of the Camera class that contains the camera's position and rotation.
    :param point_pos: A tuple (x, y, z) representing the 3D coordinates of the point to be projected.
    :param screen: A tuple (width, height) representing the dimensions of the screen for projection.
    :return: A tuple (screen_x, screen_y) representing the 2D coordinates on the screen, or None if the point is behind the camera.
    '''
    cam_x, cam_y, cam_z = (camera.x, camera.y, camera.z)
    point_x, point_y, point_z = point_pos
    
    dx = point_x - cam_x
    dy = point_y - cam_y
    dz = point_z - cam_z

    yaw = camera.yaw
    pitch = camera.pitch

    # Rotate the point around the Z-axis (yaw) to account for camera's left-right view # BUG
    rotated_x = dx * math.cos(yaw) - dz * math.sin(yaw)
    rotated_z = dx * math.sin(yaw) + dz * math.cos(yaw)

    # Rotate the point around the X-axis (pitch) to account for camera's up-down view
    rotated_y = dy * math.cos(pitch) - rotated_z * math.sin(pitch)
    rotated_z = dy * math.sin(pitch) + rotated_z * math.cos(pitch)
    
    # Project the 3D point onto 2D (perspective projection)
    if rotated_z <= 0:  # If the point is behind the camera, do not render it
        return None
    
    focal_length = 1.0  # Adjustable focal length for the perspective projection
    projected_x = (rotated_x / rotated_z) * focal_length # Projected x coordinate
    projected_y = (rotated_y / rotated_z) * focal_length # Projected y coordinate
    
    # Convert projected coordinates to 2d screen coordinates
    screen_x = int(projected_x * (screen[0] // 2)) + screen[0]/2
    screen_y = int(projected_y * (screen[1] // 2)) + screen[1]/2
    
    return (screen_x, screen_y)

def adjusted_radius(radius, planet_position, player, base_distance=300):
    '''
    ˗ˋˏ ♡ ˎˊ˗

    This function returns an adjusted radius based on the distance between the planet and the player.
    # TODO : ( -_･) ︻デ═一 ▸
    
    :param radius: The scaled radius of the planet.
    :param planet_position: A tuple (x, y, z) representing the scaled position of the planet.
    :param player: The player object containing position attributes (x, y, z).
    :param base_distance: The distance at which the radius starts to decrease (default is 300).
    :return: The adjusted radius based on the distance from the planet to the player.
    '''

    # Calculate the distance between the planet and the player using the Euclidean distance formula
    distance_player_planet = math.sqrt(
        (planet_position[0] - player.x)**2 +
        (planet_position[1] - player.y)**2 +
        (planet_position[2] - player.z)**2
    )

    # Calculate the scaling factor based on the distance to the planet
    if distance_player_planet > base_distance:
        scale_factor = base_distance / distance_player_planet
    else:
        scale_factor = 1  # # No reduction if the player is close enough to the planet
    
    # Return the adjusted radius
    return radius * scale_factor

class _3d_axis():
    def __init__(self, screen=screen):
        '''
        ˗ˋˏ ♡ ˎˊ˗

        Initializes the 3D axis with a given screen resolution and sets up the camera.
        
        :param screen: The dimensions of the screen
        '''
        self.screen = screen
        self.camera = Camera((0,0,-2), (0,0))

    def render(self, psy, theta, phi):
        '''
        Renders the 3D axis based on the provided Euler angles (psy, theta, phi).
        # BUG
        
        :param psy: Rotation around the x-axis (pitch). (눈_눈)
        :param theta: Rotation around the y-axis (roll). (눈_눈)
        :param phi: Rotation around the z-axis (yaw). (눈_눈)
        :return: A tuple containing the 2D screen coordinates of the three axes.
        '''

        # Define the initial unit vectors along the x, y, and z axes
        self.vecteur_x = np.array([1, 0, 0])
        self.vecteur_y = np.array([0, 1, 0])
        self.vecteur_z = np.array([0, 0, 1])

        # Create rotation matrices for x, y, and z axes
        rotation_x = np.array([
            [1, 0, 0],
            [0, np.cos(psy), -np.sin(psy)],
            [0, np.sin(psy), np.cos(psy)]
            ])
        rotation_y = np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
            ])
        rotation_z = np.array([
            [np.cos(phi), -np.sin(phi), 0],
            [np.sin(phi), np.cos(phi), 0],
            [0, 0, 1]
            ])
        
        # Apply the rotations to the initial vectors
        # Rotate x,y,z-axis by pitch
        self.vecteur_x = np.dot(rotation_x, self.vecteur_x)
        self.vecteur_y = np.dot(rotation_x, self.vecteur_y)
        self.vecteur_z = np.dot(rotation_x, self.vecteur_z)

        # Rotate x,y,z-axis by roll
        self.vecteur_x = np.dot(rotation_y, self.vecteur_x)
        self.vecteur_y = np.dot(rotation_y, self.vecteur_y)
        self.vecteur_z = np.dot(rotation_y, self.vecteur_z)

        # Rotate x,y,z-axis by yaw
        self.vecteur_x = np.dot(rotation_z, self.vecteur_x)
        self.vecteur_y = np.dot(rotation_z, self.vecteur_y)
        self.vecteur_z = np.dot(rotation_z, self.vecteur_z)

        # RENDERING: Transform the 3D vectors to 2D screen coordinates using raycasting
        return (raycast_transform(self.camera, self.vecteur_x, self.screen),
                raycast_transform(self.camera, self.vecteur_y, self.screen),
                raycast_transform(self.camera, self.vecteur_z, self.screen)
        )
    

import time
class Stopwatch:
	def __init__(self) -> None:
		'''
		˗ˋˏ ♡ ˎˊ˗
		- Stopwatch is used to measure time between one moment and another
		- To use it, call "start" before the first moment then call stop after the second moment
		- The unity "yearno" is 1/(2*10E6) second(s), it is used to measure fast computation time
		- To desactive the print display, just give the "stop()" function a Boolean value "False"

		 ∧,,,∧   ~ ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
		( ̳• · • ̳)  ~ ♡  You're purrfect   ♡
		/       づ ~┗━━━━━━━━━━━━━━━━━━━━━━━━┛
		'''
	def start(self) -> None:
		self.time_at_start = time.perf_counter()

	def stop(self, debbug = True) -> None:
		num = time.perf_counter()-self.time_at_start
		scale_time = -int(math.floor(math.log10(abs(num)))) + 1
		yearno = num/2E-06
		if debbug:
			print("Time passed:", round(num, scale_time), "second(s), or", round(yearno, 3), "yearno")


stopwatch = Stopwatch()

my_ax = _3d_axis()

def test(a,b,c):
    '''
    This function visualizes three 3D vectors representing the axes in a 3D coordinate system.
    
    Parameters:
    - a: Rotation angle around the x-axis (pitch).
    - b: Rotation angle around the y-axis (yaw).
    - c: Rotation angle around the z-axis (roll).
    '''
    import matplotlib.pyplot as plt
    import numpy as np

    # Render the 3D axis with the given rotation angles
    my_ax.render(a,b,c)
    vector1 = my_ax.vecteur_x
    vector2 = my_ax.vecteur_y
    vector3 = my_ax.vecteur_z

    # Create a 3D figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set the origin point for the vectors
    origin = np.array([1, 1, 1])

    # Plot the vectors starting from the origin
    ax.quiver(origin[0], origin[1], origin[2], vector1[0], vector1[1], vector1[2], color='r', label="Vecteur 1")
    ax.quiver(origin[0], origin[1], origin[2], vector2[0], vector2[1], vector2[2], color='g', label="Vecteur 2")
    ax.quiver(origin[0], origin[1], origin[2], vector3[0], vector3[1], vector3[2], color='b', label="Vecteur 3")

    # Set limits for the axes
    ax.set_xlim([0, 2])
    ax.set_ylim([0, 2])
    ax.set_zlim([0, 2])

    # Labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Legend
    ax.legend()

    # Display
    plt.show()

if __name__=="__main__":
     # Run the test function with different rotation angles
     # TEST 1 : everything is okay
     test(0,0,0) # No rotation
     test(0,0,np.pi/4)
     test(0,0,np.pi/2)

     time.sleep(1)

     # BUG:  TEST 2: not okay : the z-axis rotate, while he should not ! (ᗒᗣᗕ)՞
     # Normaly, x-axis and y-axis should rotate
     test(np.pi/2,0,0) # X-rotation, Y-rotation, Z-rotation
     test(np.pi/2,0,np.pi/4) #pitch, 0, yaw
     test(np.pi/2,0,np.pi/2)