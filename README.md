# Three-Body Problem Simulation

## Bug

There is a bug with the raycasting in the raycasting file:
The z-axis rotates unexpectedly when only the x-axis and y-axis is supposed to rotate.
This occurs during the rendering of 3D axes in the _3d_axis class and in raycast_transform
So when, in the simulation, you turn head right or left, it's like you're in a plane, it uses roll instead of yaw but only if pitch is not equal to k * pi (k belonging to the integers)

Look at the comments of the file at the bottom, where `if __name__=="__main__":` is written
I made some tests, you can run the code

## Overview

This project aims to simulate the three-body problem in classical mechanics, which involves predicting the motion of three celestial bodies interacting with each other through gravitational forces. This simulation visualizes the complex dynamics that arise from the gravitational interactions between the bodies.

## Features

- **Real-time Visualization**: Render the positions and trajectories of the three bodies in a 3D space.
- **Adjustable Parameters**: Customize the initial positions, velocities, and masses of the bodies.
- **Dynamic Interactions**: Observe how the gravitational pull affects the motion of each body over time.

## Getting Started

### Prerequisites

To run this simulation, you will need:

- Python 3.x
- Required libraries:
  - `numpy`
  - `matplotlib`
  - `pygame`

### Installation

1. Clone the repository:
   
   `git clone <your-github-repo-link>`
   
   `cd <your-repo-name>`
   
2. Install the required libraries:
   
   `pip install numpy matplotlib pygame`
   
3. Running the Simulation
   To run the simulation, execute the following command:
   
   `python main.py`
   
Adjust the parameters in the code as needed to explore different scenarios of the three-body problem.

Code Structure
main.py: The entry point for the simulation.
raycasting.py: Contains the Camera class, and render every point on your screen
Contributing
Contributions are welcome! Please feel free to submit a pull request or report issues you encounter.

License
This project is licensed under the GNU General Public License v3.0 License. See the LICENSE file for details.

Acknowledgements
The simulation is based on the classical mechanics concepts and numerical methods.
vbnet
Copier le code

### Instructions to Customize
1. Replace `<your-github-repo-link>` with your actual GitHub repository link.
2. Fill in `<your-repo-name>` with the name of your repository.
3. Adjust the **Code Structure** section according to your actual file structure.
4. Add any additional information about the project that you think would be helpful to users or contributors.

Let me know if you need any more adjustments!
