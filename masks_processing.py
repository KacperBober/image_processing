from os import path
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


def rgb_histograms(image):
    """creates arrays of histogram from input image"""
    r, g, b = image.split()     # splits image into 3 separate images with one color values

    r_histogram = np.histogram(r, bins=256, range=(0, 256))[0]
    g_histogram = np.histogram(g, bins=256, range=(0, 256))[0]
    b_histogram = np.histogram(b, bins=256, range=(0, 256))[0]

    bins = range(0, 256)

    return r_histogram, g_histogram, b_histogram, bins


def plot_histograms(r, g, b, gray_scale, color_range, fig, axs):
    """creates figure with 4 histograms R/G/B colors and gray scale"""
    axs[0].fill(color_range, r, 'r')
    axs[0].set_title("Czerwony")
    axs[0].set_ylim(ymin=0)

    axs[1].fill(color_range, g, 'g')
    axs[1].set_title("Zielony")
    axs[1].set_ylim(ymin=0)

    axs[2].fill(color_range, b, 'b')
    axs[2].set_title("Niebieski")
    axs[2].set_ylim(ymin=0)

    axs[3].plot(color_range, gray_scale)
    axs[3].set_title("Skala szarosci")
    axs[3].set_ylim(ymin=0)

    fig.tight_layout()


def main():
    image_path = path.join("images", "zdjęcie.jpg")
    image = Image.open(image_path)
    gray_image = image.convert(mode='L')

    r_histogram, g_histogram, b_histogram, bins = rgb_histograms(image)
    gray_histogram = np.histogram(gray_image, bins=256, range=(0, 256))[0]

    fig, axs = plt.subplots(4)
    plot_histograms(r_histogram, g_histogram, b_histogram, gray_histogram, bins, fig, axs)

    image_pixels = gray_image.getdata()
    image_array = np.array(image_pixels)
    image_array = image_array.reshape(gray_image.size[0], gray_image.size[1])

    print(image_array)

#    plt.show()


if __name__ == '__main__':
    main()


