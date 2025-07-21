import tkinter as tk

# Configs
WIN_WIDTH, WIN_HEIGHT = 346, 486
BTN_FRM_WIDTH, BTN_FRM_HEIGHT = WIN_WIDTH, WIN_HEIGHT
BTN_WIDTH, BTN_HEIGHT = 4, 2
BORDER_THICKNESS = 4
INPUT_WIDTH = 40
INPUT_PADY = 10
MAX_INPUT_CHARS = 23
FONT_SIZE = 18
FONT_FAMILY = "roboto"
COLOR_PRIMARY = "white"
COLOR_SECONDARY = "black"
COLOR_ACCENT = "grey"
POINTER = "hand2"
FONT = (FONT_FAMILY, FONT_SIZE, "bold")
NUM_PAD = "()%/789*456-123+.0C="

# Window
root = tk.Tk()
root.title("PyCalc")
root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
root.resizable(False, False)

# Input
input_frm = tk.Frame(
    root,
    width=WIN_WIDTH,
    height=50,
    highlightbackground=COLOR_SECONDARY,
    highlightcolor=COLOR_SECONDARY,
    highlightthickness=BORDER_THICKNESS,
)
input_frm.pack(side=tk.TOP)


def validate(P):
    if len(P) > MAX_INPUT_CHARS:
        return False
    for l in P:
        if l == "C" or l not in NUM_PAD:
            return False
    return True


input_txt = tk.StringVar(value="0")
vcmd = root.register(validate)
input_fld = tk.Entry(
    input_frm,
    font=FONT,
    textvariable=input_txt,
    width=INPUT_WIDTH,
    bg=COLOR_PRIMARY,
    bd=0,
    justify=tk.RIGHT,
    validate="key",
    validatecommand=(vcmd, "%P"),
)
input_fld.grid(row=0, column=0)
input_fld.pack(ipady=INPUT_PADY)

# Buttons
btn_frm = tk.Frame(root, width=BTN_FRM_WIDTH, height=BTN_FRM_HEIGHT, bg=COLOR_ACCENT)
btn_frm.pack()

btns = []
idx = 0

for y in range(1, 6):
    for x in range(4):
        btns.append(
            tk.Button(
                btn_frm,
                width=BTN_WIDTH,
                height=BTN_HEIGHT,
                cursor=POINTER,
                text=NUM_PAD[idx],
                font=FONT,
            )
        )
        btns[idx].grid(row=y, column=x, pady=1, padx=1)
        idx += 1

if __name__ == "__main__":
    root.mainloop()
