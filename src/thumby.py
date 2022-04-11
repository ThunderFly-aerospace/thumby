import os, subprocess
from PIL import Image


HEADER_BEG="; thumbnail begin "
HEADER_END="; thumbnail end"

WIDTH_NORMAL,   HEIGHT_NORMAL   = 220,  124
WIDTH_MINI,     HEIGHT_MINI     = 16,   16
WIDTH_LARGE,    HEIGHT_LARGE    = 240,  320


def insert_png_to_gcode_normal(path_to_png, path_to_gcode):
    '''
    Makes temp file from given png file and inserts it as thumbnail to given gcode.
    size of thumbnail: 220x124
    '''
    insert_png_to_gcode_custom(path_to_png, path_to_gcode, WIDTH_NORMAL, HEIGHT_NORMAL)


def insert_png_to_gcode_mini(path_to_png, path_to_gcode):
    '''
    Makes temp file from given png file and inserts it as thumbnail to given gcode.
    size of thumbnail: 16x16
    '''
    insert_png_to_gcode_custom(path_to_png, path_to_gcode, WIDTH_MINI, HEIGHT_MINI)


def insert_png_to_gcode_large(path_to_png, path_to_gcode):
    '''
    Makes temp file from given png file and inserts it as thumbnail to given gcode.
    size of thumbnail: 240x320
    '''
    insert_png_to_gcode_custom(path_to_png, path_to_gcode, WIDTH_LARGE, HEIGHT_LARGE)


def insert_png_to_gcode_custom(path_to_png, path_to_gcode, width=WIDTH_NORMAL, height=HEIGHT_NORMAL):
    '''
    Makes temp file from given png file and inserts it as thumbnail to given gcode.
    -> default size of thumbnail: 220x124
    recomanded sizes:
    -> normal   220x124
    -> mini     16x16
    -> large    240x320
    '''
    tmpFile = resize_and_save_image(path_to_png, width, height)
    thumbnail = wrap_as_thumbnail(
        generate_base64(tmpFile), width, height
    )
    remove_file(tmpFile)

    insert_header_to_gcode(thumbnail, path_to_gcode)


def resize_and_save_image(png_filepath, target_width=WIDTH_NORMAL, target_height=HEIGHT_NORMAL, tmpFile="tmp.png"):
    '''
    Saves resized file as tmpFile. Default name 'tmp.png'.
    Return value is 'tmpFile path'
    -> default size of thumbnail: 220x124
    recomanded sizes:
    -> normal   220x124
    -> mini     16x16
    -> large    240x320
    '''
    try:
        with Image.open(png_filepath) as img:
            size = img.size
            if size != [target_width,target_height]:
                img = img.resize((target_width,target_height))
            img.save(tmpFile)
        return tmpFile
    except FileNotFoundError as err:
        print(err)
        exit()


def insert_header_to_gcode(header, gcode_filepath):
    '''
    Insert given header into gcode.
    Skips comments and free spaces 
    '''
    index = 0
    try:
        with open(gcode_filepath, "r") as f:
            # skip comments on gcode file beg
            contents = f.readlines()
            while contents[index][0] == ';':
                index+=1

        contents.insert(index, header)

        with open(gcode_filepath, "w") as f:
            contents = "".join(contents)
            f.write(contents)
    except FileNotFoundError as e:
        print(e)
        exit()


def generate_base64(source_path):
    '''returns base64 generated from source path (.png)'''
    try:
        output = subprocess.run(["base64", source_path], capture_output=True, text=True)
        if (output.returncode != 0):
            print(output.stderr)
            exit()
        return output.stdout
    except Exception as e:
        print(e)
        exit()


def wrap_as_thumbnail(img_as_base64, img_w, img_h):
    '''returns wrapped content as str'''
    img_as_base64 = img_as_base64.replace("\n","")
    
    LINE_LEN = 78
    wrapped_content = "\n; \n"
    wrapped_content+= HEADER_BEG + str(img_w) + "x" + str(img_h) + " " + str(len(img_as_base64)) + '\n'
    while(True):
        wrapped_content+="; "
        line = img_as_base64[:LINE_LEN]
        img_as_base64 = img_as_base64[LINE_LEN:]
        wrapped_content+=line
        wrapped_content+='\n'
        if img_as_base64 == "":
            break
    wrapped_content+=HEADER_END + '\n'
    wrapped_content+= ";\n"

    return wrapped_content

def delete_thumbnail_normal(path_to_gcode):
    '''
    Delete space between HEADER_BEG and HEADER_END.
    Delete all thumbnails of size 220x124
    '''
    delete_thumbnail_custom(path_to_gcode, WIDTH_NORMAL, HEIGHT_NORMAL)

def delete_thumbnail_mini(path_to_gcode):
    '''
    Delete space between HEADER_BEG and HEADER_END.
    Delete all thumbnails of size 16x16
    '''
    delete_thumbnail_custom(path_to_gcode, WIDTH_MINI, HEIGHT_MINI)


def delete_thumbnail_large(path_to_gcode):
    '''
    Delete space between HEADER_BEG and HEADER_END.
    Delete all thumbnails of size 240x320
    '''
    delete_thumbnail_custom(path_to_gcode, WIDTH_LARGE, HEIGHT_LARGE)


def delete_thumbnail_custom(path_to_gcode, width=WIDTH_NORMAL, height=WIDTH_NORMAL):
    '''
    Delete space between HEADER_BEG and HEADER_END.
    Delete all thumbnails of given size.
    '''
    seeked_phrase = HEADER_BEG + str(width) + "x" + str(height)

    with open(path_to_gcode, "r+") as f:
        content = f.readlines()
        f.seek(0)
        delete = False
        for line in content:
            if seeked_phrase in line:
                delete = True
            elif HEADER_END in line: 
                delete = False
                continue
            
            if delete or line.strip(" ") == ";\n":
                continue
            else:
                f.write(line)
        f.truncate()


def remove_file(filepath):
    '''Delete file with given filepath'''
    try:
        os.remove(filepath)
    except Exception as e:
        print("file", filepath, "couldn't be removed:")
        print(e)
        exit()