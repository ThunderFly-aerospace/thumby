import sys
import thumby as tb


def print_help(err_msg=''):
    def bold(text):
        return '\033[1m'+text+'\033[0m'

    if len(err_msg) > 0:
        print(bold("Error:"), err_msg)
    
    print(bold("Usage:"), sys.argv[0], "OPTION", "FILE1", "[FILE2]")
    print(bold("Options:"))
    print(bold("Insert"),"- FILE1=png_file, FILE2=gcode_file - png file to gcode file:")
    print("--insert-all\t-iall\tFILE1\tFILE2\tall size (recommanded)")
    print("--insert-mini\t-imini\tFILE1\tFILE2\tmini size\t"+str(tb.WIDTH_MINI)+"x"+str(tb.HEIGHT_MINI))
    print("--insert-normal\t-inorm\tFILE1\tFILE2\tnormal size\t"+str(tb.WIDTH_NORMAL)+"x"+str(tb.HEIGHT_NORMAL))
    print("--insert-large\t-ilarge\tFILE1\tFILE2\tlarge size\t"+str(tb.WIDTH_LARGE)+"x"+str(tb.HEIGHT_LARGE))
    print(bold("Clear"),"- FILE1=gcode_file - delete current thumbnails from gcode")
    print("--clear\t\t-c\tFILE1\t(None)\tdeletes thumbnails from gcode file")

    exit()



def clear_gcode(fpath_gcode):
    tb.delete_thumbnail_mini(fpath_gcode)
    tb.delete_thumbnail_normal(fpath_gcode)
    tb.delete_thumbnail_large(fpath_gcode)


def insert_gcode(opt, fpath_png, fpath_gcode):
    if opt == '--insert-all' or opt == '--iall':
        tb.insert_png_to_gcode_mini(fpath_png, fpath_gcode)
        tb.insert_png_to_gcode_normal(fpath_png, fpath_gcode)
        tb.insert_png_to_gcode_large(fpath_png, fpath_gcode)
    elif opt == '--insert-mini' or opt == '--imini':
        tb.insert_png_to_gcode_mini(fpath_png, fpath_gcode)
    elif opt == '--insert-normal' or opt == '--inorm':
        tb.insert_png_to_gcode_normal(fpath_png, fpath_gcode)
    elif opt == '--insert-large' or opt == '--ilarge':
        tb.insert_png_to_gcode_large(fpath_png, fpath_gcode)
    else:
        print_help()  


if __name__=='__main__':
    if len(sys.argv) < 2:
        print_help()

    opt = sys.argv[1]

    # clear_code
    if len(sys.argv) >= 3 and (opt == '--clear' or opt == '-c'):
        fpath_gcode = sys.argv[2]
        if not fpath_gcode.lower().endswith('.gcode'):
            print_help("invalid filetype given " + fpath_gcode)
        clear_gcode(fpath_gcode)
    # insert gcode
    elif len(sys.argv) >= 4 and opt.startswith('--insert') or opt.startswith('-i'):
        fpath_png = sys.argv[2]
        fpath_gcode = sys.argv[3]

        if not fpath_gcode.lower().endswith('.gcode') or not fpath_png.lower().endswith('.png'):
            print_help("check format of given files: " + fpath_png + " " + fpath_gcode)
        
        insert_gcode(opt, fpath_png, fpath_gcode)
    else:
        print_help("wrong format of arguments: '" + opt+"'")