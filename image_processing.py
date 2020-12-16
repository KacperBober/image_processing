from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from urllib import request

""" wykonane podpunkty:
    - wyrysowane histogramy dla odpowiednich kanałów kolorów oraz skali szarości
    - pobrany obrazek bezpośrednio z sieci
    - wykonanie konwersji do skali szarosci
    - Zaimplementowanie filtru Sobela i krzyża Roberts'a
    
    Uzyskane wyniki: Histogramy rysują się podobne jak w gotowych generatorach internetowych. 
    Konwersja do skali szarości wygląda przyzwoicie
    Filtry nie wykonują się szybko, ale poprawnie
"""


def rgb_histograms(image):
    """creates arrays of histogram from input image"""
    r, g, b = image.split()     # splits image into 3 separate images with one color values

    red_array = np.array(r.getdata())
    green_array = np.array(g.getdata())
    blue_array = np.array(b.getdata())


    r_histogram = histogram(red_array)
    g_histogram = histogram(green_array)
    b_histogram = histogram(blue_array)

    gray_array = np.array(gray_scale(red_array, green_array, blue_array)).astype(int)
    gray_historgram = histogram(gray_array)

    bins = range(0, 256)

    return r_histogram, g_histogram, b_histogram, gray_array, gray_historgram, bins


def histogram(array):
    """creates 255 bins with occurrences of RGB colors"""
    bins = np.zeros(256)
    for index in range(0, len(array)):
        bins[array[index]] += 1

    return bins


def gray_scale(r, g, b):
    """creates gray_scale array, scaling RGB colors with different factors"""
    gray_scale = np.zeros(len(r))
    for index in range(0, len(r)):
        gray_scale[index] = int(r[index] * 0.2989 + g[index] * 0.586 + b[index] * 0.113)

    return gray_scale


def plot_histograms(r, g, b, gray_scale, color_range, fig, axs):
    """creates figure with 4 histograms R/G/B colors and gray scale"""
    axs[0].bar(color_range, r, color=[1, 0, 0], alpha=0.8)
    axs[0].set_title("Czerwony")

    axs[1].bar(color_range, g, color=[0, 1, 0], alpha=0.8)
    axs[1].set_title("Zielony")

    axs[2].bar(color_range, b, color=[0, 0, 1], alpha=0.8)
    axs[2].set_title("Niebieski")

    axs[3].bar(color_range, gray_scale, color=[0, 0, 0], alpha=0.8)
    axs[3].set_title("Skala szarosci")

    fig.tight_layout()


def filters(pixel_array):

    width = pixel_array.shape[1]
    heigth = pixel_array.shape[0]

    sobel_image = np.zeros((heigth-1, width-1))
    roberts_image = np.zeros((heigth-1, width-1))

    for i in range(1, heigth-1):
        for j in range(1, width - 1):
            g_x = calculate_vertical_gradient(pixel_array, i, j)
            g_y = calculate_horizontal_gradient(pixel_array, i, j)

            gradient = int(np.sqrt(pow(g_x, 2) + pow(g_y, 2)))
            if gradient > 60:
                sobel_image[i, j] = gradient
            else:
                sobel_image[i, j] = 0
            #roberts
            tmp1 = pixel_array[i, j] - pixel_array[i+1, j+1]
            tmp2 = pixel_array[i+1, j] - pixel_array[i, j+1]

            roberts_image[i, j] = abs(tmp1) + abs(tmp2)

    return sobel_image.astype(int), roberts_image.astype(int)


def calculate_vertical_gradient(pixel_array, i, j):
    return pixel_array[i-1, j+1] * (-1) + pixel_array[i-1, j] * (-2) + pixel_array[i-1, j-1]*(-1) + pixel_array[i+1, j+1] \
        + pixel_array[i+1, j] * 2 + pixel_array[i+1, j - 1]


def calculate_horizontal_gradient(pixel_array, i, j):
    return pixel_array[i-1, j+1] * (-1) + pixel_array[i, j+1] * (-2) + pixel_array[i+1, j+1] * (-1) +\
        pixel_array[i-1, j-1] + pixel_array[i, j-1] * 2 + pixel_array[i+1, j-1]


def main():

    link = "https://media.comicbook.com/2020/08/cyberpunk-2077-1--1233341-1280x0.jpeg"
    image: Image.Image = Image.open(request.urlopen(link))

    # create arrays of histograms
    r_histogram, g_histogram, b_histogram, gray_array, gray_histogram, bins = rgb_histograms(image)

    fig, axs = plt.subplots(4)
    plot_histograms(r_histogram, g_histogram, b_histogram, gray_histogram, bins, fig, axs)

    # create gray image
    mat = np.reshape(gray_array, (image.size[1], image.size[0]))
    gray_pixels = np.uint8(mat)
    gray_image = Image.fromarray(gray_pixels, 'L')
    gray_image.show()

    # create filtered images
    sobel_pixels, roberts_pixels = filters(mat)

    sobel_contour = np.uint8(sobel_pixels)
    roberts_contour = np.uint8(roberts_pixels)

    sobel_image = Image.fromarray(sobel_contour, 'L')
    roberts_image = Image.fromarray(roberts_contour, 'L')

    sobel_image.show()
    roberts_image.show()

    plt.show()


if __name__ == '__main__':
    main()


