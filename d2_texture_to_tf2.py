from PIL import Image
import sys,os
from PIL import Image, ImageEnhance
from PIL import ImageOps


material_sets = []

def isolate_channels(image_path, material_name):
    # Open the input image
    with Image.open(image_path) as image:
        # Convert the image to RGBA if it is a palettized image
        image = image.convert("RGBA")



    # Split the image into individual channels
    red, green, blue, alpha = image.split()
    #invert the green channel to get the roughness
    green = Image.eval(green, lambda a: 255 - a)

    
    # Save each channel as a separate image in the same directory as the original image
    #red ao green gls blue emissive alpha metallic
    red.save(image_path + "_ao.png")
    green.save(image_path + "_gls.png")  
    blue.save(image_path + "_emissive.png")  
    alpha.save(image_path + "_Metallic.png")
    print("Channels saved successfully!")

def isolate_cavity(image_path, material_name):
    #open the image then isolate its blue channel and save it in the same directory as the original image with the name of the material + _cav.png
    with Image.open(image_path) as image:
        red, green, blue, alpha = image.split()
        blue.save(material_name + "_cav.png")

def rename_textures(textures_in, material_name):
    for filename in os.scandir(textures_in):
        split_filename = filename.name.split("_")
        if split_filename[-1] == "ao.png":
            os.rename(textures_in + "/" + filename.name, textures_in + "/" + material_name + "_ao.png")
        if filename.name.lower().endswith("normal.png"):
            os.rename(textures_in + "/" + filename.name, textures_in + "/" + material_name + "_nml.png")
        if filename.name.lower().endswith("diffuse.png"):
            os.rename(textures_in + "/" + filename.name, textures_in + "/" + material_name + "_col.png")
        if split_filename[-1] == "Metallic.png":
            os.rename(textures_in + "/" + filename.name, textures_in + "/" + material_name + "_mtl.png")
        if split_filename[-1] == "gls.png":
            os.rename(textures_in + "/" + filename.name, textures_in + "/" + material_name + "_gls.png")
        if split_filename[-1] == "emissive.png":
            os.rename(textures_in + "/" + filename.name, textures_in + "/" + material_name + "_ilm.png")

def make_materials(base_path):
    #save base_path as a variable called "weapon_dir"
    weapon_dir = base_path
    for folder in os.listdir(weapon_dir):
        #save the folder name as a variable called "material_name"
        material_name = folder
        material_sets.append(material_name)
        #for each file in the folder that ends with "gstack.png" do isolate_channels
        for file in os.listdir(os.path.join(weapon_dir, folder)):
            if file.lower().endswith("gstack.png"):
                print(f"Creating channels for {folder}")
                #use isolate_channels on the file with its absolute path and the material_name
                isolate_channels(os.path.join(weapon_dir, folder, file), material_name)
                print(os.path.join(weapon_dir, folder, file))
            else:
                pass
        #for each folder in the weapon_dir, rename the textures
        for folder in os.listdir(weapon_dir):
            rename_textures(os.path.join(weapon_dir, folder), folder)

        #for each folder in the weapon_dir, make an spc map by multiplying the mtl and col maps
        for folder in os.listdir(weapon_dir):
            if os.path.isfile(os.path.join(weapon_dir, folder, folder + "_mtl.png")) and os.path.isfile(os.path.join(weapon_dir, folder, folder + "_col.png")):
                print(f"Creating specular map for {folder}")
                with Image.open(os.path.join(weapon_dir, folder, folder + "_mtl.png")) as mtl:
                    with Image.open(os.path.join(weapon_dir, folder, folder + "_col.png")) as col:
                        mtl = mtl.convert("RGB")
                        col = col.convert("RGB")
                        mtl = ImageEnhance.Contrast(mtl).enhance(-0.15)
                        mtl = ImageEnhance.Brightness(mtl).enhance(0.15)
                        #multiply mtl and col together
                        mtl = Image.blend(mtl, col, 0.5)
                        mtl.save(os.path.join(weapon_dir, folder, folder + "_spc.png"))
            else:
                pass
        
        #for each folder in the weapon_dir, make an cav map by using isolate_cavity on the nml map
        for folder in os.listdir(weapon_dir):
            if os.path.isfile(os.path.join(weapon_dir, folder, folder + "_nml.png")):
                print(f"Creating cavity map for {folder}")
                isolate_cavity(os.path.join(weapon_dir, folder, folder + "_nml.png"), os.path.join(weapon_dir, folder, folder))
            else:
                pass

def output(w_dir):
    #copy all images in all subfolders of the w_dir to the output folder in the root directory
    #check if output folder exists, if not, create it
    if not os.path.exists("output"):
        os.makedirs("output")
    for folder in os.listdir(w_dir):
        for file in os.listdir(os.path.join(w_dir, folder)):
            if file.endswith(".png") and not file.endswith("ack.png"):
                print(f"Copying {file} to output folder")
                os.system(f"cp {os.path.join(w_dir, folder, file)} output/")
            else:
                pass

def convert_textures(asset_path):
     for filename in os.scandir(asset_path):
          if filename.name.endswith("nml.png"):
               os.system("texconv.exe -f BC5_UNORM -srgb -ft dds " + filename.path + " -o " + asset_path)
          else:
               if filename.name.endswith("gls.png"):
                    os.system("texconv.exe -f BC4_UNORM -srgbi -ft dds " + filename.path + " -o " + asset_path)
               else:
                    os.system("texconv.exe -f BC1_UNORM_SRGB -srgbi -ft dds " + filename.path + " -o " + asset_path)

def cleanup(asset_path):
        for filename in os.scandir(asset_path):
            if filename.name.endswith(".png") or filename.name.endswith("mtl.dds"):
                os.remove(filename.path)
            else:
                pass

def make_map(pakname, texname):
     temp_mat_string = str("")
     if not os.path.exists("maps"):
        os.makedirs("maps")
     #open "base_pak.json" and load contents as string called "temp_json"
     #replace all instances of "PAKNAME" with pakname variable and save as "temp_json"
     with open("base_pak.json", "r") as f:
          temp_json = f.read()
          temp_json = temp_json.replace("PAKNAME", pakname)
          with open("maps/" + pakname + "_map.json", "w") as f:
               f.write(temp_json)
     for i in texname:
          with open("material_include.json", "r") as f:
               temp_json = f.read()
               temp_json = temp_json.replace("TEXNAME", i)
               temp_json = temp_json.replace("PAKNAME", pakname)
               temp_mat_string += temp_json
     
     temp_mat_string = temp_mat_string[:-2]

    #check if the maps folder exists, if not, create it
     with open("maps/" + pakname + "_map.json", "r") as f:
          contents = f.readlines()
     contents.insert(9, temp_mat_string)
     with open("maps/" + pakname + "_map.json", "w") as f:
          contents = "".join(contents)
          f.write(contents)

def generate_repak_map(asset_path, name):
    #for each folder in the asset_path, append the list "tex_set" with the folder name
    tex_set = []
    for folder in os.listdir(asset_path):
        tex_set.append(folder)
    make_map(name, tex_set)

if __name__ == "__main__":
    in_dir = sys.argv[1]
    #clean up the output folder
    if os.path.exists("output"):
        for filename in os.scandir("output"):
            os.remove(filename.path)
    make_materials(in_dir)
    output(in_dir)
    convert_textures("output")
    cleanup("output")
    #get the name of the folder that the textures are in
    generate_repak_map(in_dir, in_dir)
    print("Done!\n\n")
    print("Sets generated:\n")
    for i in material_sets:
        print("texture/models/weapons_r2/" + in_dir + "/" + i + "\n")
