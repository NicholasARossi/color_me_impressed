from collections import namedtuple
from math import sqrt
import random
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import colorsys
from PIL import Image
import sys


Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(filename, n=3):
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters


def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")  # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(r, g, b)

def main():
    imloc = sys.argv[1]
    ncolors = int(sys.argv[2])
    collist = list(colorz(imloc, n=ncolors))
    fig,ax = plt.subplots()
    img = mpimg.imread(imloc)

    ax.imshow(img)
    recs=[]



    RGB_list = []
    for color in collist:
        RGB_list.append(get_hsv(color))

    s = sorted(RGB_list)
    sorted_colors = [colorsys.hsv_to_rgb(color[0], color[1], color[2]) for color in s]


    for color in sorted_colors:
        recs.append(mpatches.Rectangle((0, 0), 1, 1, fc=color))
    ax.legend(recs, ['' for _ in range(len(recs))],loc='upper right')
    plt.axis('off')
    fig.savefig('out.png',bbox_inches='tight',pad_inches=0.0,dpi=300)


if __name__ == "__main__":
    main()