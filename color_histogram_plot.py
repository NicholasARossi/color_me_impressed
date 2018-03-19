import colorsys
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")  # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    return colorsys.rgb_to_hsv(r, g, b)

def main():
    with open('storage.pkl', 'rb') as f:
        storage = pickle.load(f)


    hlist = []
    for group in storage:
        for color in group:
            h,s,v=get_hsv(color)
            if s>0 and v>0:
                hlist.append(h)

    n=100
    bins = np.arange(-0.01,1.01,0.01)

    probs, bons = np.histogram(hlist, normed=1, bins=bins)
    vect=np.linspace(0.0, 2 * np.pi, n, endpoint=False)

    # vect=np.append(vect, vect[0])
    # probs=np.append(probs, probs[0])


    f2 = interp1d(vect, probs[1:], kind='cubic')



    # N = 1000
    # bottom = 8
    # max_height = 4

    xnew = np.linspace(min(vect), max(vect), 10000, endpoint=False)


    ax = plt.subplot(111, polar=True)
    ax.plot(xnew,np.ones(len(xnew))*2,color='black')
    ax.plot(xnew,np.ones(len(xnew))*10,color='black')

    # ax.plot(xnew, f2(xnew)*4)

    width = (2 * np.pi) / 10000
    ax = plt.subplot(111, polar=True)
    bars = ax.bar(xnew, f2(xnew), width=width, bottom=2,linewidth=0)

    # Use custom colors and opacity
    # for r, bar in zip(xnew, bars):
    #     bar.set_facecolor(colorsys.hsv_to_rgb(r, 1, 1))
    #     bar.set_alpha(0.8)

    # Use custom colors and opacity
    for r, bar in zip(xnew, bars):
        bar.set_facecolor(colorsys.hsv_to_rgb(r/( 2 * np.pi), 1, 1))
        bar.set_alpha(0.75)
    plt.axis('off')

    plt.savefig('figures/radial_colors.png',dpi=300)

if __name__ == "__main__":
    main()
