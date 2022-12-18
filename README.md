# solarsystem-simulator
In the main branch, ***solar_system.py*** is a file with texture mapping, and ***solar_system_fast.py*** is a file excluding texture mapping. ***solar_system_fast.py*** is not texture mapped, but there is almost no delay so the user can see the natural movement of the planets.

## User interface
### Direction Keys
  - Top: Global zoom in
  - Bottom: Global zoom out
  - Left: Global left movement
  - Right: Global right movement
### Mouse Movement
  - Move from left to right after left-clicking the button: Rotates counterclockwise based on the y-axis of the sun. In the initial state, the positive direction of the y-axis is the top of the screen.
  - Move from bottom to top after left-clicking the button: Rotates counterclockwise based on the z-axis of the sun. In the initial state, the positive direction of the z-axis is toward entering the screen.
### Press the keyboard
  - a: If you press 'a', **'INPUT CENTER(x, y, z):'** appears on the terminal. Write down the arrival x,y,z coordinates of the planet to be created. The user can distinguish the x, y, and z coordinates by using the space bar. At this time, the coordinates of the center of the sun are (0, 0, 0).
  - d: Rotation conversion using the mouse is initialized.
  - w: The speed of the generated planet is instantly increased.
  - s: Shooting stars are randomly generated.
