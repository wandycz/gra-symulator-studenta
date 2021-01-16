import cx_Freeze

executables = [cx_Freeze.Executable("projekt_wandycz.py")]

cx_Freeze.setup(
    name="Symulator studenta",
    options={"build_exe": {"packages":["pygame", "random", "time"],
                           "include_files":["person.png", "5.png", "2.png", "3.png", "4.png", "tlo.png", "tloover.png", "koniec.mp3", "menu.mp3", "muzyka3.mp3" ]}},
    executables = executables

    )