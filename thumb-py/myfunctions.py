import os, subprocess, sys
from sys import argv
from PIL import Image



def generate_base64(source_path):
    """returns base64 generated from source path (should be .png)"""
    # TODO make comments fancy
    try:
        output = subprocess.run(["base64", source_path], capture_output=True, text=True)
        if (output.returncode != 0):
            print(output.stderr)
            exit()
        return output.stdout
    except Exception as e:
        print(e)
        exit()


def save_and_resize_image(png_filepath, target_width, target_height):
    try:
        with Image.open(png_filepath) as img:
            size = img.size
            if size != [target_width,target_height]:
                print("resized") # debug print
                img = img.resize((target_width,target_height))
            img.save(TMP_PNG)
    except FileNotFoundError as err:
        print(err)
        exit()