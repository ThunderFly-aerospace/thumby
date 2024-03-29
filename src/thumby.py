from io import TextIOWrapper
import os
from PIL import Image
import base64


HEADER_BEG = "; thumbnail begin "
HEADER_END = "; thumbnail end"

WIDTH_NORMAL,   HEIGHT_NORMAL = 220,  124
WIDTH_MINI,     HEIGHT_MINI = 16,   16
WIDTH_LARGE,    HEIGHT_LARGE = 240,  320


def extract_png_from_gcode_any_recommended(path_to_png: str, path_to_gcode: str):
    '''
    Search for thumbnail of recommended size in gcode file and extract it to given path_to_png.
    Args:
    - path_to_png: str - creates or overides file at given path
    - path_to_gcode: str - source of thumbnail

    recommended sizes (ordered by priority):
    -> normal   220x124
    -> mini     16x16
    -> large    240x320
    '''
    # base64 --decode

    # ; thumbnail begin 'width'x'height' 'len'
    # ; 'řádek z base64 dlouhý 78 znaků'
    # ; ...
    # ; 'i-tý řádek dlouhý 78 znaků'
    # ; ...
    # ; 'poslední řádek dlouhý max 78 znaků'
    # ; thumbnail end

    try:
        thumbnail_normal, thumbnail_large, thumbnail_mini = None, None, None
        with open(path_to_gcode, "r") as f:
            while not (thumbnail_normal and thumbnail_large and thumbnail_mini):
                width_curr, height_curr, thumbnail_curr = get_next_thumbnail(f) or (None, None, None)

                if width_curr == WIDTH_NORMAL and height_curr == HEIGHT_NORMAL:
                    thumbnail_normal = thumbnail_curr
                elif width_curr == WIDTH_MINI and height_curr == HEIGHT_MINI:
                    thumbnail_mini = thumbnail_curr
                elif width_curr == WIDTH_LARGE and height_curr == HEIGHT_LARGE:
                    thumbnail_large = thumbnail_curr
                elif not (width_curr and height_curr and thumbnail_curr):
                    break # no other thubnail found in file
        with open(path_to_png, "wb") as fh:
            if thumbnail_normal:
                fh.write(thumbnail_normal)
            elif thumbnail_mini:
                fh.write(thumbnail_mini)
            elif thumbnail_large:
                fh.write(thumbnail_large)
    except Exception as e:
        print(str(e))


def extract_png_from_gcode_normal(path_to_png, path_to_gcode):
    '''
    Search for thumbnail (of size "normal") in gcode file and extract it to given path_to_png.
    recommended size "normal": 220x124
    '''
    extract_png_from_gcode_custom(path_to_png, path_to_gcode, WIDTH_NORMAL, HEIGHT_NORMAL)



def extract_png_from_gcode_mini(path_to_png, path_to_gcode):
    '''
    Search for thumbnail (of size "normal") in gcode file and extract it to given path_to_png.
    recommended size "mini": 16x16
    '''
    extract_png_from_gcode_custom(path_to_png, path_to_gcode, WIDTH_MINI, HEIGHT_MINI)



def extract_png_from_gcode_large(path_to_png, path_to_gcode):
    '''
    Search for thumbnail (of size "normal") in gcode file and extract it to given path_to_png.
    recommended size "large": 240x320
    '''
    extract_png_from_gcode_custom(path_to_png, path_to_gcode, WIDTH_LARGE, HEIGHT_LARGE)


def extract_png_from_gcode_custom(path_to_png, path_to_gcode, width=WIDTH_NORMAL, height=HEIGHT_NORMAL):
    '''
    Search for thumbnail in gcode file and extract it to given path_to_png.
    -> default size of thumbnail: 220x124
    recommended sizes:
    -> normal   220x124
    -> mini     16x16
    -> large    240x320
    '''
    # TODO docstring
    try:
        thumbnail_seeked = None
        with open(path_to_gcode, "r") as f:
            while not thumbnail_seeked:
                width_curr, height_curr, thumbnail_curr = get_next_thumbnail(f) or (None, None, None)

                if width_curr == width and height_curr == height:
                    thumbnail_seeked = thumbnail_curr
                elif not (width_curr and height_curr and thumbnail_curr):
                    break # no other thubnail found in file
        if thumbnail_seeked:
            with open(path_to_png, "wb") as fh:
                fh.write(thumbnail_seeked)
    except Exception as e:
        print(str(e))


def insert_png_to_gcode_normal(path_to_png, path_to_gcode):
    '''
    Makes temp file from given png file and inserts it as thumbnail to given gcode.
    size of thumbnail: 220x124
    '''
    insert_png_to_gcode_custom(
        path_to_png, path_to_gcode, WIDTH_NORMAL, HEIGHT_NORMAL)


def insert_png_to_gcode_mini(path_to_png, path_to_gcode):
    '''
    Makes temp file from given png file and inserts it as thumbnail to given gcode.
    size of thumbnail: 16x16
    '''
    insert_png_to_gcode_custom(
        path_to_png, path_to_gcode, WIDTH_MINI, HEIGHT_MINI)


def insert_png_to_gcode_large(path_to_png, path_to_gcode):
    '''
    Makes temp file from given png file and inserts it as thumbnail to given gcode.
    size of thumbnail: 240x320
    '''
    insert_png_to_gcode_custom(
        path_to_png, path_to_gcode, WIDTH_LARGE, HEIGHT_LARGE)


def insert_png_to_gcode_custom(path_to_png, path_to_gcode, width=WIDTH_NORMAL, height=HEIGHT_NORMAL):
    '''
    Makes temp file from given png file and inserts it as thumbnail to given gcode.
    -> default size of thumbnail: 220x124
    recommended sizes:
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
    recommended sizes:
    -> normal   220x124
    -> mini     16x16
    -> large    240x320
    '''
    try:
        with Image.open(png_filepath) as img:
            size = img.size
            if size != [target_width, target_height]:
                img = img.resize((target_width, target_height))
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
                index += 1

        contents.insert(index, header)

        with open(gcode_filepath, "w") as f:
            contents = "".join(contents)
            f.write(contents)
    except FileNotFoundError as e:
        print(e)
        exit()


def generate_base64(source_path):
    '''returns base64 generated from source path (.png)'''

    if not source_path.endswith('.png'):
        raise ValueError("The provided source path is not a .png file.")
    
    with open(source_path, 'rb') as image_file:
        image_data = image_file.read()
        base64_encoded = base64.b64encode(image_data)
    
    return base64_encoded.decode('utf-8')


def wrap_as_thumbnail(img_as_base64, img_w, img_h):
    '''returns wrapped content as str'''
    img_as_base64 = img_as_base64.replace("\n", "")

    LINE_LEN = 78
    wrapped_content = "\n; \n"
    wrapped_content += HEADER_BEG + \
        str(img_w) + "x" + str(img_h) + " " + str(len(img_as_base64)) + '\n'
    while(True):
        wrapped_content += "; "
        line = img_as_base64[:LINE_LEN]
        img_as_base64 = img_as_base64[LINE_LEN:]
        wrapped_content += line
        wrapped_content += '\n'
        if img_as_base64 == "":
            break
    wrapped_content += HEADER_END + '\n'
    wrapped_content += ";\n"

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
                print("true")
                print(line)
                delete = True
            elif HEADER_END in line:
                print("false")
                print(line)
                if delete:
                    delete = False
                    continue
                delete = False

            if delete:
                print(line)
                continue
            else:
                f.write(line)
        f.truncate()


def get_next_thumbnail(f: TextIOWrapper):
    '''
    arg: file at start seek location
    return: (width, height, binary thumbnail) or None (when EOF reached) 
    '''
    # looking for start of thumbnail
    while True:
        line = f.readline()
        
        if not line: # EOF
            return

        if line.startswith(HEADER_BEG):
            content = ""
            # get width, height, len from thumbnail header (= current line)
            present_width, present_height, present_lenght = [int(x) for x in line.replace(
                HEADER_BEG, "").replace("x", " ").split()]

            # looking for end of thumbnail
            while line: # while not EOF
                line = f.readline()

                if line.startswith(HEADER_END):
                    content = content.replace('\n', '')
                    # checksum OK
                    if len(content) == present_lenght:
                        png = base64.decodebytes(
                                str.encode(content)
                            )
                        return present_width, present_height, png
                    else: # wrong checksum
                        print("thumbnail of size width {} height {} may be corrupted. \
                            Checksum not correct. Expected thumbnail len: {}. Got {}.".format(
                            present_width, present_height, present_lenght, len(content)))
                        return
                else:
                    content += line.replace("; ", "")
        elif not line: # EOF
            return
            

def remove_file(filepath):
    '''Delete file with given filepath'''
    try:
        os.remove(filepath)
    except Exception as e:
        print("file", filepath, "couldn't be removed:")
        print(e)
        exit()
