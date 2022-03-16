# thumb-py
## 1. Annotation
Simple python library for inserting .png thumbnails into gcode files.
## 2. Example of Usage
Recommanded way of using when working with multiple gcodes is [this code](#recommanded-usage).
There are 3 recommanded size of thumbnails (width x height):
- normal   220x124
- mini     16x16
- large    240x320
Other formats may not display on 3D printers.

### Insert Thumbnails
To insert all tree sizes use script bellow.
```python
import thumby

# image you want insert into gcode
pathToPng = "path/to/png/file.png"
# gcode file into which you want to insert the image
pathToGcode = "path/to/gcodeFile.gcode"

insert_png_to_gcode_normal(pathToPng, pathToGcode)
insert_png_to_gcode_large(pathToPng, pathToGcode)
insert_png_to_gcode_mini(pathToPng, pathToGcode)
```
You can also insert thumbnail of other size for advanced purposes (not recommanded):
```python
import thumby

pathToPng = "path/to/png/file.png"
pathToGcode = "path/to/gcodeFile.gcode"

insert_png_to_gcode_custom(pathToPng, pathToGcode)
```
### Delete Thumbnails
To delete all tree sizes use script bellow. Functions `delete thumbnail_*()` will delete all thumbnails of set size found in given gcode.
```python
import thumby

# gcode file where thumbnails will be deleted
pathToGcode = "path/to/gcodeFile.gcode"

delete_thumbnail_normal(path_to_gcode)
delete_thumbnail_large(path_to_gcode)
delete_thumbnail_mini(path_to_gcode)
```
To delete thumbnail of other size:
```python
import thumby

pathToGcode = "path/to/gcodeFile.gcode"
delete_thumbnail_custom(path_to_gcode, width, height)
```
### Recommanded Usage
A script for inserting and replacing thumbnails into your gcodes.
```python
import thumby

pathToPng = "path/to/png/file.png"
pathToGcode = "path/to/gcodeFile.gcode"

# this makes sure there are no thumbnails in gcode file
delete_thumbnail_normal(path_to_gcode)
delete_thumbnail_large(path_to_gcode)
delete_thumbnail_mini(path_to_gcode)

# than insert thumbnail of all 3 recommanded sizes
insert_png_to_gcode_normal(pathToPng, pathToGcode)
insert_png_to_gcode_large(pathToPng, pathToGcode)
insert_png_to_gcode_mini(pathToPng, pathToGcode)
```

## 3. Install
## 4. List of Functions

```python
insert_png_to_gcode_normal(path_to_png, path_to_gcode)
```
Makes temp file from given png file and inserts it as thumbnail to given gcode.
size of thumbnail: 220x124


```python
insert_png_to_gcode_mini(path_to_png, path_to_gcode)
```
Makes temp file from given png file and inserts it as thumbnail to given gcode.
size of thumbnail: 16x16

```python
insert_png_to_gcode_large(path_to_png, path_to_gcode)
```
Makes temp file from given png file and inserts it as thumbnail to given gcode.
size of thumbnail: 240x320

```python
insert_png_to_gcode_custom(path_to_png, path_to_gcode, width=WIDTH_NORMAL, height=HEIGHT_NORMAL)
```
Makes temp file from given png file and inserts it as thumbnail to given gcode.
-> default size of thumbnail: 220x124
recomanded sizes:
-> normal   220x124
-> mini     16x16
-> large    240x320

```python
resize_and_save_image(png_filepath, target_width=WIDTH_NORMAL, target_height=HEIGHT_NORMAL, tmpFile="tmp.png")
```
Saves resized file as tmpFile. Default name 'tmp.png'.
Return value is 'tmpFile path'
-> default size of thumbnail: 220x124
recomanded sizes:
-> normal   220x124
-> mini     16x16
-> large    240x320

```python
insert_header_to_gcode(header, gcode_filepath)    
````
Insert given header into gcode.
Skips comments and free spaces 
    
```python
generate_base64(source_path)
```
returns base64 generated from source path (.png)

```python
wrap_as_thumbnail(img_as_base64, img_w, img_h)
```
returns wrapped content as str

```python
delete_thumbnail_normal(path_to_gcode)
```
Delete space between HEADER_BEG and HEADER_END.
Delete all thumbnails of size 220x124

```python
delete_thumbnail_mini(path_to_gcode)
```
Delete space between HEADER_BEG and HEADER_END.
Delete all thumbnails of size 16x16


```python
delete_thumbnail_large(path_to_gcode)
```
Delete space between HEADER_BEG and HEADER_END.
Delete all thumbnails of size 240x320

```python
delete_thumbnail_custom(path_to_gcode, width=WIDTH_NORMAL, height=WIDTH_NORMAL)
```
Delete space between HEADER_BEG and HEADER_END.
Delete all thumbnails of given size.

```python
remove_file(filepath)
```
Delete file with given filepath

## 5. Technical Details of Implementations
