import math
import time
import pygame
from pygame.locals import *
import raycasting as rc

'''
     ♡ ☆  .♡‧₊˚  ☆ .♡ ‧₊ ♡‧₊ ☆ .♡˚ 
     ╭◜◝ ͡ ◜◝╮        ╭◜◝ ͡ ◜◝╮. 
    (     3    )  ♡   (  Problem )☆ ♡
     ╰◟◞ ͜ ◟◞╭◜◝ ͡ ◜◝╮ ͜ ◟   ◞╯♡ 
     . ☆     (    Body  )☆ ♡
     ♡        ╰◟◞ ͜ ◟◞╯
'''

'''
Description:
	The code is an interactive simulation of (here)
	a two-body system (like the Earth and the Moon) in 3D,
	using Pygame for graphical display.
	It allows users to visualize the effects of gravity and orbital motion.
	Users can manipulate the camera to explore the simulation
	and observe how celestial bodies interact based on their mass, position, and velocity.
'''


''' TODO:
For future versions:
---> Adding a third body !!!! otherwise it's not a 3-body problem ╮( ˘ ､ ˘ )╭
---> Sizes of bodies adapted to their distance from the player's camera
---> Trajectories of bodies
---> Short predictions by AI
'''

# Initialization
pygame.init()
pygame.font.init()
font1 = pygame.font.SysFont('Comic Sans MS', 30)
pygame.mouse.set_visible(False)

### setting mouse in the middle of the screen !!!
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.mouse.set_pos(screen_width // 2, screen_height // 2)
###

screen_dims = (800, 600) # PAY ATTENTION : if you want to change it then do it in the two files

screen = pygame.display.set_mode(screen_dims)

axes = rc._3d_axis() # BUG (ᗒᗣᗕ)՞

# Unities : second, meters, meters by seconds (づ￣ ³￣)づ
simulation_speed = 50
scale = 1/1_000_000 # to represent real distances of bodies to scale
G = 6.67430e-11


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


# Initializing the stopwatch
stopwatch = Stopwatch()


class Vector:
	def __init__(self, ijk:tuple) -> None:
		'''
		˗ˋˏ ♡ ˎˊ˗
		- As it says, this class is made to create a vector object,
			which will speed up the calculations, because numpy is slower... (´∩｀。)
		
		:param ijk: the components of the vector

		(づ￣ ³￣)づ	i
		(づ￣ ³￣)づ	j
		(づ￣ ³￣)づ	k
		'''
		self.i = ijk[0]
		self.j = ijk[1]
		self.k = ijk[2]

	def __add__(self, other): # other, is another vector
		return Vector((self.i+other.i, self.j+other.j, self.k+other.k))
	
	def __mul__(self, scalar):
		return Vector((self.i * scalar, self.j * scalar, self.k * scalar))
		
	def __str__(self) -> str: # ===> called when print is used on the object
		return f"Vector({self.i}, {self.j}, {self.k})"

class Body:
	def __init__(self, mass:float, R:float, position:tuple, velocity_vector = Vector((0, 0, 0))) -> None:
		'''
		˗ˋˏ ♡ ˎˊ˗

		:param mass: the mass of the body
		:param R: the body radius
		:param position: the original position of the body
		:param velocity_vector: the original speed vector of the body

		(๑˃̵ᴗ˂̵)و it will flyyyyyyy
		'''
		self.mass = mass
		self.R = R
		self.x = position[0]
		self.y = position[1]
		self.z = position[2]
		self.velocity_vector = velocity_vector

	def move(self) -> None:
		'''
		˗ˋˏ ♡ ˎˊ˗
		- Add velocity_vector of the object to his own position
		'''
		self.x += self.velocity_vector.i
		self.y += self.velocity_vector.j
		self.z += self.velocity_vector.k

	def gravitational_force(self, other) -> Vector:
		'''
		˗ˋˏ ♡ ˎˊ˗
		- Computes the gravitational force between 2 objects
		- This part was very complicated (눈_눈)
		
		Drop a thought and it will faaall DOOOOOoOooooown...
		'''
		distance_ = distance(self, other)
		if distance_ == 0:
			return Vector((0, 0, 0)) # Avoid division by zero
		
		# Calculating the magnitude (intensity) of the gravitational force between each object
		force_magnitude = G * self.mass * other.mass / (distance_ ** 2) # Newton's law of universal gravitation
		
		# Calculate the relative position of "self" with respect to "other"
		relative_position = (self.x - other.x, self.y - other.y, self.z - other.z)
		
		# Calculate the Euclidean distance to normalize the relative position vector
		magnitude = -(relative_position[0]**2 + relative_position[1]**2 + relative_position[2]**2) ** 0.5
		
		# Calculate the components of the force in each direction using the normalized vector
		force_x = (relative_position[0] / magnitude) * force_magnitude
		force_y = (relative_position[1] / magnitude) * force_magnitude
		force_z = (relative_position[2] / magnitude) * force_magnitude

		# Return a vector representing the gravitational force in three dimensions
		return Vector((force_x, force_y, force_z))
	
	
	def update_velocity(self, force: Vector):
		'''
		˗ˋˏ ♡ ˎˊ˗
		- Use gravitational force to get the acceleration of the object and then update the velocity
		- Formula is F = m * a
		'''
		acceleration = force * (1/self.mass)  # a = F/m
		self.velocity_vector = self.velocity_vector + acceleration


	def __str__(self) -> str:
		return (
			f"Body(\n"
			f"  mass = {self.mass},\n"
			f"  R = {self.R},\n"
			f"  position = ({self.x}, {self.y}, {self.z}),\n"
			f"  velocity_vector = {self.velocity_vector}\n"
			f")"
		)


'''
     /|、♡
    (` - 7
     |、⁻〵
     じしˍ,)/
'''

def distance(body_a:Body, body_b:Body) -> float:
	'''
    ˗ˋˏ ♡ ˎˊ˗
	- Return the distance between two 3d points
	:param body_a: the first body
	:param body_b: the second one
	'''
	# (눈_눈) Bruh : This formula computes the "Euclidean distance" between two points in 3D space. (눈_눈)
	return ((body_a.x-body_b.x)**2 + (body_a.y-body_b.y)**2 + (body_a.z-body_b.z)**2)**0.5

''' εїз
		A bug is flying in my room
		Looping again in the rain of my toughts		εїз
		You 'd better catch your own sun
		In the heat of it all
		When your gun 'll cast a shadow

										- Me
'''

# Initializing two body : Earth and Moon; The data for the bodies are taken from the Internet
Earth = Body(5.972e24, 6_371_000, (0, 0, 0), Vector((0, 0, 0)))
Moon = Body(7.342e22, 1_737_000, (0, 384_400_000, 0), Vector((1023, 0, 0)))

# Initializing player's camera
player = rc.Camera((17.7, -87, 76), (0, 2.3))

# # Dictionary to store the state of keys for player control
keys = {"z":False, # move forward
		"s":False, # move backward
		"q":False, # move left
		"d":False, # move right
		" ":False, # move upward
		"sh ":False} # move downward

# trajectory = [] # TODO

time_ = 0
running = 1
while running:
	stopwatch.start()
	time_+=1
	for evenement in pygame.event.get():
		if evenement.type == QUIT or (evenement.type == KEYDOWN and (evenement.key == K_ESCAPE)):
			running = False
		if evenement.type == KEYDOWN: 
			if evenement.key == pygame.K_z:
				keys["z"] = True
			if evenement.key == pygame.K_s:
				keys["s"] = True
			if evenement.key == pygame.K_q:
				keys["q"] = True
			if evenement.key == pygame.K_d:
				keys["d"] = True
			if evenement.key == pygame.K_SPACE:
				keys[" "] = True
			if evenement.key == pygame.K_LSHIFT:
				keys["sh "] = True
		if evenement.type == KEYUP:
			if evenement.key == pygame.K_z:
				keys["z"] = False
			if evenement.key == pygame.K_s:
				keys["s"] = False
			if evenement.key == pygame.K_q:
				keys["q"] = False
			if evenement.key == pygame.K_d:
				keys["d"] = False
			if evenement.key == pygame.K_SPACE:
				keys[" "] = False
			if evenement.key == pygame.K_LSHIFT:
				keys["sh "] = False

	if keys["z"]: # move forward
		player.move((0, 0.1, 0))
	elif keys["s"]: # move backward
		player.move((0, -0.1, 0))
	elif keys["q"]: # move left
		player.move((-0.1, 0, 0))
	elif keys["d"]: # move right
		player.move((0.1, 0, 0))
	elif keys[" "] and not keys["sh "]: # move upward
		player.move((0, 0, 0.1))
	elif keys[" "] and keys["sh "]: # move downward
		player.move((0, 0, -0.1))

	# Get the current position of the mouse cursor (⌐■_■)
	mouse_pos = pygame.mouse.get_pos()

	# Calculate the pointer's position relative to the center of the screen
	pointer_pos = (mouse_pos[0]-screen_dims[0]/2, mouse_pos[1]-screen_dims[1]/2)

	# Check if the pointer is not centered (i.e., if it's moved from the center)
	if pointer_pos[0] or pointer_pos[1]:
		# Set the mouse position back to the center of the screen
		pygame.mouse.set_pos(screen_dims[0] // 2 - pointer_pos[0]/2, screen_dims[1] // 2 - pointer_pos[1]/2)
		# Move the player based on the pointer's position, adjusting the rotation
		sensibility = 0.001 # sensitivity of the movement
		player.move(rotation2=(-pointer_pos[0]*sensibility, -pointer_pos[1]*sensibility))
	

	screen.fill((255,255,255))

	
	# Calculate the position of the Earth in the player's view using raycasting
	body1_pos = rc.raycast_transform(player, (Earth.x*scale, Earth.y*scale, Earth.z*scale)) # BUG: bad raycasting, see the raycasting file
	if body1_pos:
		# If the position is visible by the player, draw the Earth as a circle on the screen
		pygame.draw.circle(screen, (0,0,0), body1_pos, Earth.R*scale)
	
	# Calculate the position of the Moon in the player's view using raycasting
	body2_pos = rc.raycast_transform(player, (Moon.x*scale, Moon.y*scale, Moon.z*scale)) # BUG: bad raycasting, see the raycasting file (눈_눈)
	if body2_pos:
		# TODO: ( -_･) ︻デ═一 ▸ Calculate the adjusted radius for the Moon based on its distance from the player
		# radius = scale*rc.adjusted_radius(Moon.R, (Moon.x*scale, Moon.y*scale, Moon.z*scale), player)
		# print(radius, rc.adjusted_radius(Moon.R, (Moon.x*scale, Moon.y*scale, Moon.z*scale), player))
		
		# If the position is visible by the player, draw the Moon as a circle on the screen
		pygame.draw.circle(screen, (0,0,0), body2_pos, Moon.R*scale)

	# Render 3D axes based on the player's orientation (pitch (radian) and yaw (radian))
	axes_x_y_z = axes.render(player.pitch, 0, player.yaw) # BUG: bad raycasting, see the raycasting file (눈_눈)
	pygame.draw.line(screen, (255, 0, 0), (screen_dims[0]/2, screen_dims[1]/2), axes_x_y_z[0]) # Draw the X-axis in red
	pygame.draw.line(screen, (0, 255, 0), (screen_dims[0]/2, screen_dims[1]/2), axes_x_y_z[1]) # Draw the Y-axis in green
	pygame.draw.line(screen, (0, 0, 255), (screen_dims[0]/2, screen_dims[1]/2), axes_x_y_z[2]) # Draw the Z-axis in blue
	

	# Calculate the positions of endpoints of another 3d-axis using raycasting
	x_axis_a = rc.raycast_transform(player, (-100,.1,.1))
	x_axis_b = rc.raycast_transform(player, (100,.1,.1))
	if x_axis_a and x_axis_b:
		pygame.draw.line(screen, (255, 100,100), x_axis_a, x_axis_b)

	y_axis_a = rc.raycast_transform(player, (.1,-100,.1))
	y_axis_b = rc.raycast_transform(player, (.1,100,.1))
	if y_axis_a and y_axis_b:
		pygame.draw.line(screen, (100, 255,100), y_axis_a, y_axis_b)

	z_axis_a = rc.raycast_transform(player, (.1,.1,-50))
	z_axis_b = rc.raycast_transform(player, (.1,.1,50))
	if z_axis_a and z_axis_b:
		pygame.draw.line(screen, (100, 100,255), z_axis_a, z_axis_b)
	

	'''
	TODO: ( -_･) ︻デ═一 ▸ trajectory
	for i in trajectory:
		pos = rc.raycast_transform(player, (i[0]+player.x, i[1]+player.y, i[2]+player.z))
		if pos:
			pygame.draw.circle(screen, (0,255,0), pos, 1)'''

	# Run the simulation for a number of iterations based on the simulation speed (つ▀¯▀)つ
	for _ in range(simulation_speed):
		# Calculate the gravitational force exerted on the Moon by the Earth
		force_on_moon = Moon.gravitational_force(Earth)

		# Calculate the gravitational force exerted on the Earth by the Moon
		force_on_earth = Earth.gravitational_force(Moon)
		
		# Update the Moon's velocity based on the calculated gravitational force
		Moon.update_velocity(force_on_moon)

		# Update the Earth's velocity based on the calculated gravitational force
		Earth.update_velocity(force_on_earth)

		# Move the Moon to its new position based on the updated velocity
		Moon.move()

		# Move the Earth to its new position based on the updated velocity
		Earth.move()

	# Every 70 time steps, render text to display the player's yaw and pitch
	if time_%70==0:
		# Create a text surface displaying the player's yaw, rounded to 2 decimal places
		text=font1.render(f"yaw: {round(player.yaw, 2)}", True, (0,0,0))
		rect = text.get_rect()
		rect.center=(screen_dims[0]-100, 25)
		screen.blit(text, rect)

		# Create a text surface displaying the player's pitch, rounded to 2 decimal places
		text2=font1.render(f"pitch: {round(player.pitch, 2)}", True, (0,0,0))
		rect2 = text2.get_rect()
		rect2.center=(screen_dims[0]-100, 50)
		screen.blit(text2, rect2)

		# Update the display
		pygame.display.flip()

	'''
	TODO: ( -_･) ︻デ═一 ▸ trajectory
	if time_%1000==0:
		if body2_pos:
			trajectory.append((Moon.x, Moon.y, Moon.z))
		if len(trajectory)>20:
			trajectory.pop(0)'''
	
	stopwatch.stop()
pygame.quit()
