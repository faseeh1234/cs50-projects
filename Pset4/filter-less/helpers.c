#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = (float) (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3;
            average = (int) round(average); // Final pixel value needs to be int

            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int originalRed;
    int originalGreen;
    int originalBlue;
    int sepiaRed;
    int sepiaGreen;
    int sepiaBlue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            originalRed = image[i][j].rgbtRed;
            originalGreen = image[i][j].rgbtGreen;
            originalBlue = image[i][j].rgbtBlue;

            // Sepia formula
            sepiaRed = (int) round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            sepiaGreen = (int) round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            sepiaBlue = (int) round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            // Pixel value range check
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            if (sepiaRed < 0)
            {
                sepiaRed = 0;
            }
            if (sepiaGreen < 0)
            {
                sepiaGreen = 0;
            }
            if (sepiaBlue < 0)
            {
                sepiaBlue = 0;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int mid;
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {

        // Checking for odd even cases
        if (width % 2 == 0)
        {
            mid = (width / 2);
        }
        else
        {
            mid = (width - 1) / 2;
        }

        for (int j = 0; j < mid; j++)
        {
            // Switching pixels horizontally
            temp.rgbtRed = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][width - (j + 1)].rgbtRed;
            image[i][width - (j + 1)].rgbtRed = temp.rgbtRed;

            temp.rgbtBlue = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][width - (j + 1)].rgbtBlue;
            image[i][width - (j + 1)].rgbtBlue = temp.rgbtBlue;

            temp.rgbtGreen = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][width - (j + 1)].rgbtGreen;
            image[i][width - (j + 1)].rgbtGreen = temp.rgbtGreen;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    // Initialisation of variables
    float pixel_count;
    float pixel_sum_red;
    float pixel_sum_green;
    float pixel_sum_blue;
    // looping through each pixel
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            pixel_count = 0;
            pixel_sum_red = 0;
            pixel_sum_green = 0;
            pixel_sum_blue = 0;

            // looping through box around each pixel
            for (int i = -1; i < 2; i++)
            {
                for (int j = -1; j < 2; j++)
                {
                    // Checking for boundary
                    if (h + i<0 | h + i> height - 1)
                    {
                        continue;
                    }
                    if (w + j<0 | w + j> width - 1)
                    {
                        continue;
                    }
                    // Adding pixel values
                    pixel_sum_red += image[h + i][w + j].rgbtRed;
                    pixel_sum_green += image[h + i][w + j].rgbtGreen;
                    pixel_sum_blue += image[h + i][w + j].rgbtBlue;
                    pixel_count++;
                }
            }
            // Calculating average as int
            temp[h][w].rgbtRed = round(pixel_sum_red / pixel_count);
            temp[h][w].rgbtGreen = round(pixel_sum_green / pixel_count);
            temp[h][w].rgbtBlue = round(pixel_sum_blue / pixel_count);
        }
    }

    // Copying blurred values back into image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }

    return;
}