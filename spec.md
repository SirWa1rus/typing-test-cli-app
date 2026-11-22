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

        -   A difficulty menu appears with three options (Esc goes back to the main menu):
                1.  Easy
                2.  Medium
                3.  Hard
        -   A countdown from 5 starts
        -   A typing test of the chosen difficulty appears after 0 and a new timer of 45 seconds starts

    Difficulty levels (standard typing test only):

        -   Easy: short, common, lowercase words
        -   Medium: longer, less common, lowercase words
        -   Hard: long words written as sentences, with capital letters, punctuation
            (, . ? !) and numbers
        -   Every difficulty uses the same timer, word count, and "% of people beaten" scale

    Typing test screen layout (countdown and test screens):

        -   Text size: a terminal program cannot change the terminal's font, so the
            countdown and test screens show a tip telling the user how to zoom the
            terminal (hold Ctrl and scroll the mouse wheel, or press Ctrl+= / Ctrl+-).
            A shorter tip is shown on narrow screens, and none if it cannot fit
        -   When the terminal is zoomed or resized, the screen is redrawn to fit the new size
        -   The test text is a left-aligned block of lines at most 60 columns wide
            (narrower if the screen is narrower)
        -   The block is centered left-to-right between the screen edges
            (|-++-|: the text is the "++", the edges are the "|  |") and
            top-to-bottom, but never above the title and timer at the top

    When the user is taking the test:

        -   correctly typed characters recolors them as green (for spaces, a green box the size of a letter will appear where the space would be)
        -   incorrectly typed characters recolors them as red (for spaces, a red box the size of a letter will appear where the space would be)

    After the user runs out of time or finishes the test:

        -   users wpm is printed
        -   for a standard test, the difficulty is printed under the wpm
        -   a percentage of how many users they beat is printed under
        -   a selectable option to retry (a standard test retries at the same difficulty with new words)
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
