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
        -   A countdown from 5 starts on the animated "Get ready" screen (see below)
        -   A typing test of the chosen difficulty appears after 0 and a new timer of 45 seconds starts

    Difficulty levels (standard typing test only):

        -   Easy: short, common, lowercase words
        -   Medium: longer, less common, lowercase words
        -   Hard: long words written as sentences, with capital letters, punctuation
            (, . ? !) and numbers
        -   Every difficulty uses the same timer, word count, and "% of people beaten" scale

    "Get ready" screen (the 5-second countdown before every test, standard and custom):

        -   An animation plays for the whole countdown, about 20 frames per second
        -   Rocket: pixel art made of colored filled boxes, shaped like the 🚀
            emoji and pointing up and to the right (red nose and fins, white body,
            light-blue window), 5 rows tall. Each pixel is 2 columns wide so it
            looks square. It flies in the direction it points: up and to the right.
            (The real emoji does not display in Git Bash, so it is not used.)
        -   The rocket stays near the middle of the screen and shakes a little
            (one column or row each frame); the world moving past it shows the flight
        -   Fire trail: a thick trail streams out of the rocket's engine (its
            bottom-left), down and to the left, and gets thinner farther away. It is made of solid filled boxes
            (no characters) that flicker, mixing white, yellow, and orange:
            hottest (white/yellow) next to the rocket, orange at the end
        -   Stars: streaking stars move down and to the left past the rocket, each
            with a short tail, so the rocket looks like it is moving fast
        -   Planet: a very large planet designed to look like Jupiter, in shades of
            purple and blue, centered behind the rocket. It has many thin bands whose
            edges wave up and down, and a big oval "Great Spot" (a bright purple core
            with a dark purple rim) below the middle, right of center. It stays still
            in the center (it is far away)
        -   Drawn back to front: planet, stars, fire trail, rocket, then the text
        -   No black boxes: anything drawn on top of the planet (stars, the text)
            has the planet's color behind it instead of the terminal's
            background color
        -   Text: "Get ready..." and the countdown number at the top, the zoom tip
            and "Esc: quit" at the bottom, so they never cover the rocket
        -   Terminals with fewer than 256 colors use the closest ones (orange
            becomes yellow, the purple shades become magenta, the blue shades blue)

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
        -   a selectable option to go back to the main menu
        -   a selectable option to quit

    Selectable buttons (main menu, difficulty menu, results screen):

        -   The option the user is currently on (hovering over) has a white box
            behind it, with black text, on any terminal color theme. A terminal
            without colors uses reverse video instead
        -   Every button in one menu is the same width (the longest label plus one
            space on each side), so the box keeps its size as the user moves
        -   The results screen shows only the white box (no [ ] brackets) to mark
            the current option
        -   The custom-file path field is a text field, not a button, so it has no box

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
