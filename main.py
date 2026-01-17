from tkinter import Tk
from db import init_db
from ui_login import start_login


def main():
    # Create main Tk root
    root = Tk()

    # Initialize database (tables + default admin)
    init_db()

    # Start login UI
    start_login(root)

    # Start Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
