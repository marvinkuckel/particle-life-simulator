Dear User,

To run the simulation, you can simply execute "src/main.py" with python. In this file you can also adjust the number of particles with n_particles and the number of types with n_types.

After that, a Pygame window will open, with the graphics depending on the screen size, so you might have a different resolution.

In the opened Pygame window, you have many options to control the simulation, both through the buttons and the interactive panel. The buttons allow you to start, stop, reset, and exit the simulation.

With the panel, you can configure the simulation speed, force, friction, randomness in movement, general attraction, and the minimum and maximum radius in real-time. The radius defines the surrounding area of the particles where forces can act.

Additionally, you can decide how the particles should interact. By hovering over a matrix field, you can either increase attraction with the left mouse button/scroll up or increase repulsion with the right mouse button/scroll down. The axes will indicate which interactions you are currently controlling.

We – Lilith, Beliz, Marc, Marvin, Nevriye – wish you an enjoyable time with the simulation!

___________________________________________________________________________________________________________________________________________________


## Objectives  
The *Particle Life Simulator* simulates independent particles of specific types, following the principle of emergence, where significant structures form through interactions between small particles.  

## Technology Stack  
Written in Python, the program utilizes several external libraries and follows object-oriented programming principles, treating code elements as interacting objects.  

The code is divided into six files:  
- `particle.py`  
- `interactions.py`  
- `interactions_interface.py`  
- `simulation.py`  
- `gui.py`  
- `main.py`  

The `__init__.py` file connects the individual modules.

At the bottom, you will find a diagram that visualises the relationships between the classes.

## Simulation Results  
The code functions as expected, with particles displaying emergent behavior. The forces can be dynamically adjusted.  

## Requirements  
The following software versions were used:  
- Python **3.12.7**  
- Pygame **2.5.2**  

Required libraries:  
`random, pygame, typing, time, math, numba, numpy, sys, cProfile, pstats`  

To install locally via Git Bash:  
`git clone https://github.com/marvinkuckel/particle-life-simulator`  

## Configuration  
Adjustable parameters:  
- In `particle.py`:  
  - Number of types  
  - Size  
  - Speed  
  - Friction  

- In `main.py`:  
  - Number of particles  
  - Number of types  

- In `simulation.py`:  
  - Number of particles  
  - Speed  
  - Size of simulation grid  

## Execution  
The main loop is located in `main.py`.  

## Code Organization  
- The core simulation logic is in `simulation.py`:  
  - Generates particles  
  - Creates the grid  
  - Updates particles  
  - Calculates forces based on interactions  
  - Starts, stops, or resets the simulation  

- `simulation.py` interacts with `particle.py` and `interactions.py` to perform calculations.  
- `interactions.py` defines interaction rules.  
- `interactions_interface.py` provides the graphical representation of the interaction matrix.  

- `gui.py` contains two classes:  
  - **Button** → Manages button design, position, and interaction  
  - **GUI** → Handles colors, user instructions, and projection of particles onto the screen  

Positions of graphical elements in `gui.py` can be adjusted for different screen resolutions.  

## Testing  

#### 1. `interactions_interface.py` Tests:
- **Test 1:** Verify if a mouse click updates the interaction matrix.
- **Test 2:** Check if the matrix values reflect expected interactions after changes.

#### 2. `simulation.py` Tests:
- **Test 1:** Ensure the number of particles and simulation grid size are correct.
- **Test 2:** Verify particles stay within valid boundaries.
- **Test 3:** Confirm particle positions change with each timestep.

#### 3. `interactions.py` Tests:
- **Test 1:** Verify the interaction matrix is 3x3.
- **Test 2:** Ensure forces between two particles return correct values.

## License  
The repository is private; no license has been determined yet.  

## Troubleshooting  
Performance may decrease if the number of particles exceeds 10,000.
