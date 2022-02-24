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
## 5. Technical Details of Implementations
