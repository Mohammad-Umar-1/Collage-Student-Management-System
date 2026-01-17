from tkinter import *
from tkinter import ttk


class ScrollablePage(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        canvas = Canvas(self, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.content = Frame(canvas)

        self.content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # ---------- SAFE MOUSE SCROLL ----------
        def _on_mousewheel(event):
            if canvas.winfo_exists():
                canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        # bind only when mouse enters
        self.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
