from PIL import Image, ImageSequence
import sys

"""
This is a script for converting a gif into a frame list for better compatibilty with python arcade.
Run using "python gif_to_frame.py gifFilname fileLabel"

gifFilename: file name of gif
fileLabel: what you would like each frame to be named (frame number will be added as well) ex. blinky -> blinky_frame1.png

NOTE: make sure the gif is in the images folder
"""
fileName = sys.argv[1]
fileLabel = sys.argv[2]
folder = sys.argv[3]

gif = Image.open("images/" + fileName)

frames = []
frameNum = 0
for frame in ImageSequence.Iterator(gif):
    frame.save(f"images/{folder}/{fileLabel}_frame{frameNum}.png", "PNG")
    frameNum += 1



