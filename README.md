# ShaderToyVid
This is a tool built with python that can easily display and render any effect-shader from [**Shadertoy.com**](https://www.shadertoy.com/)

[<img src="https://img.shields.io/badge/DOWNLOAD-ShaderToyVid-informational?&color=orange&logo=Python&logoColor=yellow&style=for-the-badge"  width="300">](https://github.com/Akascape/ShaderToyVid/archive/refs/heads/main.zip)

## Features
- Ability to input any **video** as an i-channel
- Render to video or image-sequence
- Quick conversions
- Apply effects like CRT filters, VHS filters, glitch and retro effects, and much more (**Read Details**)

## How it works?

https://user-images.githubusercontent.com/89206401/194752036-e2c7df0e-4646-4ed9-a152-1e08004ac594.mp4

## Dependencies (python)
- **Arcade**
- **Customtkinter**
- **OpenCV**
- **Numpy**

## Details

This is an *experimental* project based on this [shadertoy feature](https://github.com/pythonarcade/arcade/blob/development/arcade/experimental/shadertoy.py) of [Arcade](https://github.com/pythonarcade/arcade). 

There is always some chances of shader errors with this tool so I recommend you to copy the shaders properly from shadertoy.

Not all shaders from shadertoy are supported in ShaderToyVid, those shaders which have **more than one i-channel or having any buffers are not supported.**

I have collected some **effect-shaders** from shadertoy.com which you can **download** from here. *(Sources are given within the files)*

[<img src="https://img.shields.io/badge/DOWNLOAD-SHADERS-informational?&color=green&style=for-the-badge" width="200">](https://github.com/Akascape/ShaderToyVid/files/9746351/Shaders.zip)

*Paste the `My Shaders` folder with ShaderToyVid.*

Sometimes you may have to **force quit** the program if the shader window freezes after any shader-error, so keep that in mind.

## Future Development
- Live Preview is unstable and is not implemented yet. (The demo video was just to show the effects)
- I don't know if buffer support is available in arcade shadertoy, maybe I will try to research more about it in future.
- Any advice or pull requests are welcomed. 

Please Note: This project is released under MIT license **without any warranty**!

**Current version: 0.3**

[<img src="https://img.shields.io/badge/LICENSE-MIT-informational?&color=yellow&style=for-the-badge" width="100">](https://github.com/Akascape/ShaderToyVid/blob/main/LICENSE)
