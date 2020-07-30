# Design Diary

One particular struggle I dealt with in this assignment was interfacing my GUI application with the clippyr script it's made to run. Clippyr uses a module called click (Command-Line Interface Creation Kit) to make handling command-line options easier, which interfered with my ability to directly invoke its main function from Qlippyr. I solved this by restructuring Clippyr a bit without altering its command-line usage by moving most of the code from the function invoked by the click module to a separate main function, which the click module-invoked function would then call in turn. I realized after making this change that it actually solved another problem in the process, which was that the original function also called os.exit() when it was finished running, which would terminate any application calling it, including Qlippyr.

I have not yet managed to resolve the problem of UI scaling. Currently, resizing the window just adds padding around the main layout of UI elements.

To any other student building a graphical wrapper around another project, I would recommend considering making tweaks to the existing project, if possible, to make it as modular as possible, to avoid running into the problem I described above with invoking my Clippyr script from this application.

I found that I had the most fun on this assignment writing the code that managed the data input by the user, as opposed to the parts that just set up the UI.

