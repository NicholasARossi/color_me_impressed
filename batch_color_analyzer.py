import photo_colorbar as pcb
from os import listdir
import sys
import colorsys
import pickle

def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")  # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(r, g, b)

def main():


    imloc = sys.argv[1]

    ncolors = int(sys.argv[2])

    names = listdir(imloc)
    storage=[]
    with open('storage.pkl', 'wb') as f:
        pickle.dump(storage, f)

    if '.DS_Store' in names: #exception for mac junk files
        names.remove('.DS_Store')
    names = [imloc + '/' + name for name in names]

    for name in names[0:10]:
        with open('storage.pkl', 'rb') as f:
            storage = pickle.load(f)
        collist = list(pcb.colorz(name, n=ncolors))

        RGB_list = []
        for color in collist:
            RGB_list.append(get_hsv(color))

        s = sorted(RGB_list)
        sorted_colors = [colorsys.hsv_to_rgb(color[0], color[1], color[2]) for color in s]

        hexes=['#%02x%02x%02x' % tuple(int(255*c) for c in color) for color in sorted_colors]
        storage.append(hexes)
        with open('storage.pkl', 'wb') as f:    # We cache after every loop : Always Be Caching
             pickle.dump(storage, f)

if __name__ == "__main__":
    main()
