# tf-2_d2
Utility to almost automatically convert destiny 2 textures to something that is "ok" in titanfall 2

## Setup


Download the latest release zip and unzip somewhere on your PC (only tested on windows)

Make sure you have Python 3.10+ installed and the imagemagick module installed [Instructions](https://pillow.readthedocs.io/en/stable/installation.html)

Also make sure to have PILLOW installed via pip: [install](https://pillow.readthedocs.io/en/stable/installation.html#)


## Usage
in the directory of the script make a folder with the same name as the folder in the weapons_r2 directory that you want your materials to be in,

for each material you are making make another folder and put its XXXX_diffuse, XXXX_normal and XXXX_gstack png files in, 
# MAKE SURE YOUR DIFFUSE IS BAKED, IF NOT YOU WILL NOT HAVE THE WEAPON COLORED, MAKE SURE THE DIFFUSE IS A BAKED ONE WITH THE PROPER COLORING

Example file structure:
```
.
└── D2Tex_2_TF2/
    ├── base_pak.json
    ├── d2_texture_to_tf2.py
    ├── material_include.json
    ├── texconv.exe
    └── battle_rifle/
        ├── body/
        │   ├── XXXX_normal.png
        │   ├── XXXX_diffuse.png
        │   └── XXXX_gstack.png
        └── stock/
            ├── XXXX_normal.png
            ├── XXXX_diffuse.png
            └── XXXX_gstack.png
 ```
In the example we will be creating 2 materials, "body" and "stock" in the "texture/models/weapons_r2/battle_rifle/" directory

open a command line in the directory your script is in, execute the script on your folder, in the example `py d2_texture_to_tf2.py battle_rifle` (note that "py" may not work for you, depends on how your installation of python is setup)

The script will output your dds files to the newly created "output" folder, and your repak map to the maps folder, you can now copy the images to your repak folder the script tells you in the cmd.
run repak and your done.


## License

[GPL3](https://github.com/EM4Volts/tf-2_substance_maker/blob/main/LICENSE)

Textconv.exe from Microsofts DirectXTex tools [DIREXTXTEX](https://github.com/microsoft/DirectXTex)
