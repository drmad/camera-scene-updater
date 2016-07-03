# Camera Scene Tracker
Blender 2.7x addon for changing scene parameters, like render resolution, using data stored in the camera name.

Many times I've found myself manually changing some parameters for certain cameras in my Blender projects: Some 'test' cameras should render in low quality, other cameras have a different start-end frame range, a still camera requires high resolution, etc.

This script behaves like the `Ctrl + NUMPAD_0` key combination for active a object as default camera, but analizes the camera name for changing some scene parameters.

## Installation
Once downloaded, follow the standard installation and activation procedure found in https://www.blender.org/manual/advanced/scripting/python/addons.html

## Usage
The commands and its arguments must be written in the camera name inside square brackets. Several commands are separater by a colon character. If the script doesn't found the square brakets, it just behaves the same as `Ctrl + NUMPAD_0`.

    camera_name[<command><args>:<command><args>:...]

`<command>` is a single character, and can be:

* **r**: Changes the scene resolution. `<args>` must be in the format `WIDTHxLENGTH`
* **p**: Changes the resolution percentage scale. `<args>` must be an integer in the range 0-100
* **f**: Changes the start-end frames. `<args>` must be in the format `START:END`, and one of the params can be ommited (i.e. for changing the end frame to 120, write `f:120`)
* **s**: Changes the Cycles render samples. `<args>` must be an integer.
* **o**: Changes the Output path. If no arguments are provided, it removes the last directory segment from the actual output path, and replaces it with the camera name (minus the square brackets segment). Otherwise uses the `<args>` as target path.
* **c**: Executes an arbitrary function. For this, you must create a TextBlock and change its name to something with the `.py` extension. Inside this TextBlock, create your function with one argument, which will receive the camera object, for convenience. Then, write the `<args>` as `TEXTBLOCKNAME.FUNCTIONAME`. E.g. If your TextBlock is called `utils.py`, and you create a function `show_name()`, `<args>` should be `utils.show_name`.
