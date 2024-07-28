# Using CS50 library's getstring function only
from cs50 import get_string

# defining the main function and introducing text, letters, words and sentences as variables
def main():
    text = get_string("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Computing Coleman-Liau index
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Outputting grade level based on index
    if index > 0 and index <= 16:
        print(f"Grade: {index}")
    elif index > 16:
        print("Grade 16+")
    else:
        print("Before Grade 1")


# function to calculate letters
def count_letters(text):
    count = 0
    for char in text:
        if char.isalpha():
            count += 1

    return count


# function to calculate words
def count_words(text):
    count = 1
    i = 1
    length = len(text)
    while i < length:
        if text[i] == " " and text[i - 1] != " ":
            count += 1
        i += 1

    return count


# function to calculate sentences
def count_sentences(text):
    count = 0
    for char in text:
        if char in [".", "?", "!"]:
            count += 1

    return count


main()
