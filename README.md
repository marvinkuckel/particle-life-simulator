Dear User,

To install the needed python libraries you can run `pip install -r requirements.txt` while beeing in the root directory.

To run the simulation, you can simply execute "src/main.py" with python. In this file you can also set the starting parameters in the simulation_parameters dictionary.

After that, a Pygame window will open, with the graphics depending on the screen size, so you might have a different resolution.

In the opened Pygame window, you have many options to control the simulation, both through the buttons and the interactive panel. The buttons allow you to start, stop, reset, and exit the simulation.

With the panel, you can configure the simulation speed, force scaling, friction, randomness in movement, general repulsion, and the minimum and maximum radius in real-time. The radius defines the surrounding area of the particles where forces can act. The closer these two values are to each other, the greater the force will be.

Additionally, you can decide how the particles should interact. By hovering over a matrix field, you can either increase attraction with the left mouse button/scroll up or increase repulsion with the right mouse button/scroll down. The axes will indicate which interactions you are currently controlling. The colors on the top, indicating the types, are acting a force on the color on the left.

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

In the figure below, you can see the flowchart and the relationships between the files and methods.

The most important loop of the code structure is shown. If run is executed, the four methods on the left-hand side are always executed one after the other (while True).
With each run, the attraction, positions, etc. of the particles and the status of the control_panel are updated.


![Flowchart](https://github.com/marvinkuckel/particle-life-simulator/blob/Documentations/Flowchart.png?raw=true)


## Simulation Results  
The code functions as expected, with particles displaying emergent behavior. The forces can be dynamically adjusted.  

## Requirements  
The following software versions were used:  
- Python **3.12.7**  
- Pygame **2.5.2**  

Required libraries:  
`pygame, numba, numpy`  

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

#### 1. `interaction.py` Tests:  
- **Test 1:** Verify the interaction matrix is 3x3.  
- **Test 2:** Ensure forces between two particles return correct values.  

#### 2. `interaction_matrix.py` Tests:  
- **Test 1:** Verify `calculate_force` returns zero when no interaction exists.  
- **Test 2:** Ensure `calculate_force` produces nonzero force for interacting particles.  

#### 3. `interactions_interface.py` Tests:  
- **Test 1:** Verify if a mouse click updates the interaction matrix.  
- **Test 2:** Check if the matrix values reflect expected interactions after changes.  

#### 4. `particle.py` Tests:  
- **Test 1:** Verify correct initialization of particle attributes.  
- **Test 2:** Ensure `apply_force` modifies velocity correctly.  
- **Test 3:** Confirm `update_position` changes position and applies friction.  
- **Test 4:** Check random movement affects position.  
- **Test 5:** Ensure `draw` function executes without errors.  

#### 5. `simulation.py` Tests:  
- **Test 1:** Ensure the number of particles and simulation grid size are correct.  
- **Test 2:** Verify particles stay within valid boundaries.  
- **Test 3:** Confirm particle positions change with each timestep.  

## License  
The repository is private; no license has been determined yet.  

## Troubleshooting  
Performance may decrease if the number of particles exceeds 10,000.
To improve performance, try reducing the number of particles. Additionally, you can optimize the particle update logic by simplifying calculations or using more efficient data structures. Make sure your system has enough resources, such as CPU, GPU, and RAM, to handle a large number of particles.
