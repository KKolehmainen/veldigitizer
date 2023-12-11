# Veldigitizer
Veldigitizer is a purpose-built GUI application for digitizing seismic wide-angle refraction and reflection (WARR) 2D velocity models. The tool is used to digitize velocity values from model images and save them to text files. The axes of the velocity figure are scaled by choosing scaling points before velocity values can be picked. The program automatically calculates the geographic coordinates of digitized values using the start and end point coordinates of the given model provided by the user.

The tool was used to gather additional data for my master's thesis (https://helda.helsinki.fi/items/c2d5b8cc-26eb-4574-a982-94b1c45e8f66).

Additionally, the tool can also be used as a simple plot digitizer.

## Installation
The app can be easily installed and run using the Poetry dependency tool. Without Poetry, the app can be run as a regular Python program with dependencies installed. The program has been tested to work with Python 3.10 and pillow 9.5.0.

### Using poetry
1. Install dependencies with Bash command:
```bash
poetry install
```
2. Run program with Bash command:
```bash
poetry run python3 src/veldigitizer.py
```

### Without poetry
Run with Python having the dependencies installed using the command:
```bash
python3 src/veldigitizer.py
```
## Manual

1. Open the velocity model or plot image file.
2. Scale the image by clicking on positions where the plot coordinates are known and give the coordinates when prompted. Choose the leftmost position along profile first, the rightmost the second, the zero depth third and the deepest the last. The scaling points are indicated by blue colored circles. Typically the points are chosen along the axes of the model/plot.
3. Digitize the velocity values by giving a velocity value in the text box and then clicking on the position of the value in the image. The data points are indicated by red colored circles. The undo button can be used to remove the latest given point.
4. Save the digitized data using the "Save as" button. The "Convert negative depths to zero" toggle is used to convert possible accidentally negative depth values to zero when saving. This is beneficial for picking velocity values on the ground surface as velocity models should not contain information with negative depths (i.e. above ground seismic velocities).

### Notes
- The save format is a space delimited text file.
- The velocity model can be rescaled by using the scale mode button. This will delete all the scaling values and digitized data.
