import tkinter as tk

# Configs
WIN_WIDTH, WIN_HEIGHT = 336, 476
BTN_FRM_WIDTH, BTN_FRM_HEIGHT = WIN_WIDTH, WIN_HEIGHT
BTN_WIDTH, BTN_HEIGHT = 4, 2
BORDER_THICKNESS = 0
INPUT_WIDTH, INPUT_HEIGHT = 40, 50
INPUT_PADY, INPUT_PADX = 4, 5
MAX_INPUT_CHARS = 23
FONT_SIZE = 18
FONT_FAMILY = "roboto"
COLOR_PRIMARY = "white"
COLOR_SECONDARY = "black"
COLOR_ACCENT = "grey"
COLOR_TERTIARY = "orange"
POINTER = "hand2"
FONT = (FONT_FAMILY, FONT_SIZE, "bold")
NUM_PAD = "()C/789*456-123+.0%="


class window:
    def __init__(self, master):
        master.title("PyCalc")
        master.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        master.resizable(False, False)

        # Input
        self.input_frm = tk.Frame(
            master,
            width=WIN_WIDTH,
            height=INPUT_HEIGHT,
            highlightbackground=COLOR_SECONDARY,
            highlightcolor=COLOR_ACCENT,
            highlightthickness=BORDER_THICKNESS,
            bg=COLOR_PRIMARY,
        )

        self.input_frm.pack(side=tk.TOP)

        self.input_txt = tk.StringVar(value="0")

        vcmd = root.register(self.validate)
        self.input_fld = tk.Entry(
            self.input_frm,
            font=(FONT_FAMILY, FONT_SIZE + 10, "normal"),
            textvariable=self.input_txt,
            width=INPUT_WIDTH,
            bg=COLOR_PRIMARY,
            bd=0,
            justify=tk.RIGHT,
            validate="key",
            validatecommand=(vcmd, "%P"),
        )

        self.input_fld.grid(row=0, column=0)
        self.input_fld.pack(ipady=INPUT_PADY, padx=INPUT_PADX)

        # Buttons
        self.btn_frm = tk.Frame(
            root, width=BTN_FRM_WIDTH, height=BTN_FRM_HEIGHT, bg=COLOR_PRIMARY
        )
        self.btn_frm.pack()

        self.btns = []
        idx = 0

        for y in range(1, 6):
            for x in range(4):
                if NUM_PAD[idx] in "-+/*=%":
                    bg_color = COLOR_TERTIARY
                    fg_color = COLOR_SECONDARY
                elif NUM_PAD[idx] in "()C":
                    bg_color = COLOR_ACCENT
                    fg_color = COLOR_PRIMARY
                else:
                    bg_color = COLOR_PRIMARY
                    fg_color = COLOR_SECONDARY

                self.btns.append(
                    tk.Button(
                        self.btn_frm,
                        width=BTN_WIDTH,
                        height=BTN_HEIGHT,
                        cursor=POINTER,
                        text=NUM_PAD[idx],
                        font=FONT,
                        bd=0,
                        fg=fg_color,
                        bg=bg_color,
                    )
                )
                self.btns[idx].grid(row=y, column=x, pady=1, padx=1)
                idx += 1

    def validate(self, P: str):
        """
        Checks if only allowed NUM_PAD characters have been entered.
        Allows user to enter only NUM_PAD characters.
        """
        if len(P) > MAX_INPUT_CHARS:
            return False
        for l in P:
            if l == "C" or l not in NUM_PAD:
                return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    window(root)
    root.mainloop()
