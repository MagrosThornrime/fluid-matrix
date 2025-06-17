# Fluid matrix

## Introduction
This is a fluid dynamics simulation shown on RGB 64x32 matrix with Raspberry Pi Pico and a MPU6050 gyroscope. You can rotate the board, affecting the particles' gravitation. Currently, the simulation supports following particle types:
- stone - it can't fall and doesn't interact with anything - no particle can pass through it
- water - it can fall, it can randomly move left and right if it's on a surface, tries to lay flat on screen
- sand - it can fall, it creates mounds when falls on a surface, and it can go through the water

The schematic and a video is work-in-progress.