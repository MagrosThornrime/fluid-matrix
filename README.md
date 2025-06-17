# Fluid matrix

https://github.com/user-attachments/assets/20d5b9e4-9f5a-4546-a573-89fc0c046caa

## Introduction
This is a fluid dynamics simulation shown on RGB 64x32 matrix with Raspberry Pi Pico and a MPU6050 gyroscope. You can rotate the board, affecting the particles' gravitation. Currently, the simulation supports following particle types:
- stone - it can't fall and doesn't interact with anything - no particle can pass through it
- water - it can fall, it can randomly move left and right if it's on a surface, tries to lay flat on screen
- sand - it can fall, it creates mounds when falls on a surface, and it can go through the water

## Schematic
![schematic](https://github.com/user-attachments/assets/83c18071-c21d-42b3-a61e-95df86c95192)

## How to run
Move all files to your Raspberry Pi Pico board and run main.py file. After moving all files, the board should always run main.py after booting.
