# Fluid matrix

## Introduction
This is a fluid dynamics simulation shown on RGB 64x32 matrix with Raspberry Pi Pico and a MPU6050 gyroscope. You can rotate the board, affecting the particles' gravitation. Currently, the simulation supports following particle types:
- stone - it can't fall and doesn't interact with anything - no particle can pass through it
- water - it can fall, it can randomly move left and right if it's on a surface, tries to lay flat on screen
- sand - it can fall, it creates mounds when falls on a surface, and it can go through the water

## Schematic
![schematic](https://github.com/user-attachments/assets/83c18071-c21d-42b3-a61e-95df86c95192)

## How to run
Move all files to your Raspberry Pi Pico board and run the main.py file.

## Work in progress
Stuff we want to add to README:
- video with a presentation
