# What it does

    My program will be a typing test program that:

        -   provides users with a working typing test
        -   returns a score measured in words per minute (wpm) at the end of the test
        -   returns a percentage indicating the percentage of people who got score lower than them at the end of the test

# High-level Architecture

    When the user runs the program:

        -   Two options appear:
                1.  Standard typing test
                2.  Custom typing test

    When the user selects custom typing test:

        -   a field to input a .txt file appears
        -   typing test is based on this .txt file

    When the user selects standard typing test:

        -   A countdown from 5 starts
        -   An easy typing test appears after 0 and a new timer of 45 seconds starts

    When the user is taking the test:

        -   correctly typed characters recolors them as green (for spaces, a green box the size of a letter will appear where the space would be)
        -   incorrectly typed characters recolors them as red (for spaces, a red box the size of a letter will appear where the space would be)

    After the user runs out of time or finishes the test:

        -   users wpm is printed
        -   a percentage of how many users they beat is printed under
        -   a selectable option to retry
        -   a selectable option to quit

    Controls:

        -   "enter key" -> select
        -   "esc key" -> quit program
        -   "arrow keys" -> movement

    Specifications:

        -   cli app
        -   built in python using standard libraries
        -   rules for custom .txt file:

            1.  The characters in the file must be valid characters found on a standard keyboard
            2.  Number of characters allowed: 40-400 characters
