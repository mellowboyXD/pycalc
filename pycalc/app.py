from ast import Div
import tkinter as tk
from enum import Enum

# Configs
WIN_WIDTH, WIN_HEIGHT = 336, 476
BTN_FRM_WIDTH, BTN_FRM_HEIGHT = WIN_WIDTH, WIN_HEIGHT
BTN_WIDTH, BTN_HEIGHT = 4, 2
BORDER_THICKNESS = 0
INPUT_WIDTH, INPUT_HEIGHT = 40, 50
INPUT_PADY, INPUT_PADX = 4, 5
MAX_INPUT_CHARS = 14
FONT_SIZE = 18
FONT_FAMILY = "roboto"
COLOR_PRIMARY = "white"
COLOR_SECONDARY = "black"
COLOR_ACCENT = "grey"
COLOR_TERTIARY = "orange"
POINTER = "hand2"
FONT = (FONT_FAMILY, FONT_SIZE, "bold")


class BUTTONS(Enum):
    hist = "\uf1da"
    open_brac = "("
    close_brac = ")"
    clear = "AC"
    div = "\u00f7"
    mul = "\u00d7"
    add = "+"
    sub = "-"
    equal = "="
    dot = "."
    nine = "9"
    eight = "8"
    seven = "7"
    six = "6"
    five = "5"
    four = "4"
    three = "3"
    two = "2"
    one = "1"
    zero = "0"


special = [BUTTONS.hist, BUTTONS.open_brac, BUTTONS.close_brac]
operators = [BUTTONS.div, BUTTONS.mul, BUTTONS.sub, BUTTONS.add, BUTTONS.equal]

# fmt: off
NUM_PAD = [
    BUTTONS.hist, BUTTONS.open_brac, BUTTONS.close_brac, BUTTONS.div,
    BUTTONS.seven, BUTTONS.eight, BUTTONS.nine, BUTTONS.mul,
    BUTTONS.four, BUTTONS.five, BUTTONS.six, BUTTONS.sub,
    BUTTONS.one, BUTTONS.two, BUTTONS.three, BUTTONS.add,
    BUTTONS.dot, BUTTONS.zero, BUTTONS.clear, BUTTONS.equal,
]
# fmt: on


class Window:
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
        # fmt: off
        self.btn_frm = tk.Frame(
            root, 
            width=BTN_FRM_WIDTH, 
            height=BTN_FRM_HEIGHT, 
            bg=COLOR_PRIMARY,
        )
        # fmt: on
        self.btn_frm.pack()
        self.render_buttons(self.btn_frm)

    def validate(self, P: str):
        """
        Checks if only allowed NUM_PAD characters have been entered.
        Allows user to enter only NUM_PAD characters.
        """
        if len(P) > MAX_INPUT_CHARS:
            return False
        for l in P:
            if l == BUTTONS.clear or l not in NUM_PAD or l == BUTTONS.hist:
                return False
        return True

    def render_buttons(self, master):
        self.buttons = []
        for i, b in enumerate(NUM_PAD):
            r, c = divmod(i, 4)
            if b in special:
                fg_color = COLOR_PRIMARY
                bg_color = COLOR_ACCENT
            elif b in operators:
                fg_color = COLOR_SECONDARY
                bg_color = COLOR_TERTIARY
            else:
                fg_color = COLOR_SECONDARY
                bg_color = COLOR_PRIMARY

            btn = tk.Button(
                master,
                width=BTN_WIDTH,
                height=BTN_HEIGHT,
                cursor=POINTER,
                text=b.value,
                font=FONT,
                bd=0,
                fg=fg_color,
                bg=bg_color,
                command=lambda x=b: self.insert_input(x),
            ).grid(row=r, column=c, padx=1, pady=1)
            self.buttons.append(btn)

    def insert_input(self, char: BUTTONS):
        match char:
            case BUTTONS.clear:
                self.input_txt.set(BUTTONS.zero.value)
            case BUTTONS.equal:
                self.evaluate()
            case BUTTONS.hist:
                self.get_history()
            case _:
                if len(self.input_txt.get()) <= MAX_INPUT_CHARS:
                    if self.input_txt.get() == BUTTONS.zero.value:
                        self.input_txt.set(char.value)
                    else:
                        self.input_txt.set(self.input_txt.get() + char.value)

    def evaluate(self):
        print("TODO: Evaluete", self.input_txt.get())

    def get_history(self):
        print("TODO: Get history")


if __name__ == "__main__":
    root = tk.Tk()
    Window(root)
    root.mainloop()
