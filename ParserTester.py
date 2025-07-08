import os
import sys


for filename in os.listdir("Tests/"):
    print("Running test on file: " + filename)
    os.system("py MainRunner.py Tests/" + filename)


for filename in os.listdir("Tests/NewTests/"):
    print("Running test on file: " + filename)
    os.system("py MainRunner.py Tests/NewTests/" + filename)


for filename in os.listdir("Tests/NewTests3/"):
    print("Running test on file: " + filename)
    os.system("py MainRunner.py Tests/NewTests3/" + filename)
