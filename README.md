# ShaderToyVid
This is a tool build with python that can easily display or render any effect shader from [Shadertoy.com](https://www.shadertoy.com/)

### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/ShaderToyVid?color=orange&label=Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="200">](https://github.com/Akascape/ShaderToyVid/archive/refs/heads/main.zip)

## Features
- Ability to input any video as an i-channel
- Easily export the shader filter/effect with the video
- Apply effects like CRT filter, VHS, glitch effects, retro effects and much more (All from Shadertoy.com)

## How it works?

## Dependencies (python)
- Arcade
- Customtkinter
- OpenCV

## More Info
This is an experimental project based on this [shadertoy feature](https://github.com/pythonarcade/arcade/blob/development/arcade/experimental/shadertoy.py) of [Arcade](https://github.com/pythonarcade/arcade). 

There is always some chances of shader errors with this tool so I recommend you to built/copy shader from [Shadertoy.com](https://www.shadertoy.com/) and use them with ShaderToyVid to apply them in your videos.

Not all shaders from shadertoy are supported in ShaderToyVid, those shaders which have more than one i-channel or having any buffers are not supported. 

I have taken some shaders from shadertoy.com which are available in the `My Shaders` folder. (Credits are given within the files)

Please Note: This project is given without any warranty

[<img src="https://img.shields.io/badge/LICENSE-MIT-informational?&color=yellow&style=for-the-badge" width="100">](https://github.com/Akascape/ShaderToyVid/blob/main/LICENSE)

## Future Development (Notes)
- Direct video capture is not available in Arcade, though it is in [development](https://github.com/pythonarcade/arcade/issues/1349)
- Live Preview is unstable and is not implemented yet.
- I don't know if buffer support is available in arcade shadertoy, maybe I will try to research more about it in future.
- Any advice or pull requests are welcomed. 
