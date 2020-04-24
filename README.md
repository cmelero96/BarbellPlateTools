# BarbellPlateTools
A simple set of Python tools to find weight combinations available given a (configurable) set of plates.


TO-DO:
 - Truncate list of possible combinations for a given weight (e.g. prevent the app to display 300 different possibilities to end up with 200kg on the bar)
	- Possibly create a config variable to show only the X "best" options, where best will likely be simply the first elements in an ordered (descending) array. That means that it will display the combinations that use always the higher-weight discs.
 - Implement the operation #3: Introduce the weight you're aiming for, and the program will tell you if the combination is possible (and different ways to achieve this weight; similar to previous point, but maybe a different config variable?)
	- Also shown, if not possible to end up with the target weight, the closest options both up and down, and weight combinations.