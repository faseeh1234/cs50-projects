#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;
const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // Command line arg validation
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Opening imagefile
    FILE *imagefile = fopen(argv[1], "r");
    if (imagefile == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    // Allocating memory for buffer
    uint8_t *buffer = malloc(512);

    FILE *img = NULL;
    char filename[8];
    int i = 0;

    // Reading imagefile in blocks
    while (fread(buffer, 1, BLOCK_SIZE, imagefile) == BLOCK_SIZE)
    {
        // Checking for start of new JPEG
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            // Checking if this is first JPEG to be found
            if (img == NULL)
            {
                // Creating new file with naming convention
                sprintf(filename, "%03i.jpg", i);
                img = fopen(filename, "w");

                // Writing buffer into file
                fwrite(buffer, 1, BLOCK_SIZE, img);

                i++;
            }
            else
            {
                // Closing previous JPEG file
                fclose(img);

                // Creating new file with naming convention
                sprintf(filename, "%03i.jpg", i);
                img = fopen(filename, "w");

                // Writing buffer into file
                fwrite(buffer, 1, BLOCK_SIZE, img);

                i++;
            }
        }
        else
        {
            // Checking if JPEG file has been found
            if (img != NULL)
            {
                fwrite(buffer, 1, BLOCK_SIZE, img);
            }
        }
    }

    // Closing remaining files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(imagefile);
    free(buffer);
    return 0;
}