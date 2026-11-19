# What it does

    My program will be a typing test program that:

        -   provides users with a working typing test
        -   returns a score measured in words per minute (wpm) at the end of the test
        -   returns a percentage indicating the percentage of people who got score lower than them at the end of the test

# High-level Architecture

    When the user runs the program:

        -   A countdown from 5 starts
        -   An easy typing test appears after 0 and a new timer of 45 seconds starts

    When the user is taking the test:

        -   correctly typed characters recolors them as green (for spaces, a green box the size of a letter will appear where the space would be)
        -   incorrectly typed characters recolors them as red (for spaces, a green box the size of a letter will appear where the space would be)

    After the user runs out of time or finishes the test:

        -   users wpm is printed
        -   a percentage of how many users they beat is printed under
        -   a selectable option to retry
        -   a selectable option to quit

    Controls:

        -   "enter key" -> select
        -   "esc key" -> quit program
        -   "left/right arrow keys" -> left/right movement

    Specifications:

        -   cli app
        -   built in python using standard libraries
