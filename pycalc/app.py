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


class Buttons(Enum):
    hist = "\u27f2"  # "\uf1da"
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


special = [Buttons.hist, Buttons.open_brac, Buttons.close_brac]
operators = [Buttons.div, Buttons.mul, Buttons.sub, Buttons.add, Buttons.equal]

# fmt: off
NUM_PAD = [
    Buttons.hist, Buttons.open_brac, Buttons.close_brac, Buttons.div,
    Buttons.seven, Buttons.eight, Buttons.nine, Buttons.mul,
    Buttons.four, Buttons.five, Buttons.six, Buttons.sub,
    Buttons.one, Buttons.two, Buttons.three, Buttons.add,
    Buttons.dot, Buttons.zero, Buttons.clear, Buttons.equal,
]
# fmt: on


class InvalidExpressionToken(Exception):
    pass


class Expression:
    operators = {
        Buttons.open_brac.value: 0,
        Buttons.close_brac.value: 0,
        Buttons.mul.value: 1,
        "*": 1,
        Buttons.div.value: 1,
        "/": 1,
        Buttons.add.value: 2,
        Buttons.sub.value: 2,
    }

    def __init__(self, exp: str):
        self.infix = self.__create_exp_list(exp)
        self.postfix = self.rpn()

    def __create_exp_list(self, infix: str) -> list[str]:
        lst = []
        temp = ""

        for c in infix:
            if c in self.operators.keys():
                if temp:
                    lst.append(temp)
                lst.append(c)
                temp = ""
            else:
                if str.isdigit(c) or c == Buttons.dot.value:
                    temp += c
                else:
                    raise InvalidExpressionToken(f"Invalid character: '{c}'")
        if temp:
            lst.append(temp)
        return lst

    def rpn(self, infix: list[str] | None = None) -> list[str]:
        stack = []
        if not infix:
            infix = self.infix
        postfix = []
        for c in infix:
            if c in self.operators.keys():
                if len(stack) < 1:
                    stack.append(c)
                elif c == Buttons.close_brac.value:
                    op = stack.pop()
                    while op != Buttons.open_brac.value and len(stack) > 0:
                        postfix.append(op)
                        op = stack.pop()
                    if op != Buttons.open_brac.value:
                        postfix = ["Syntax Error"]
                        break
                elif (
                    self.operators[c] < self.operators[stack[-1]]
                    or stack[-1] == Buttons.open_brac.value
                ):
                    stack.append(c)
                else:
                    postfix.append(stack.pop())
                    stack.append(c)
            else:
                postfix.append(c)

        for _ in range(len(stack)):
            postfix.append(stack.pop())

        return postfix

    # TODO: Im too lazy rn to do this, I'll proceed to just right some tests
    # for rpn()
    def evaluate(self, exp_lst: list[str] | None = None) -> str:
        if not exp_lst:
            exp_lst = self.postfix
        return "Hello World"

    def __str__(self) -> str:
        return "".join(self.infix)


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyCalc")
        self.root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.root.resizable(False, False)
        self.hist = None

        # Input
        self.input_frm = tk.Frame(
            self.root,
            width=WIN_WIDTH,
            height=INPUT_HEIGHT,
            highlightbackground=COLOR_SECONDARY,
            highlightcolor=COLOR_ACCENT,
            highlightthickness=BORDER_THICKNESS,
            bg=COLOR_PRIMARY,
        )

        self.input_frm.pack(side=tk.TOP)

        self.input_txt = tk.StringVar(value="0")

        vcmd = self.root.register(self.validate)
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

        self.input_fld.bind("<KeyPress>", self.on_key_press)

        # Buttons
        # fmt: off
        self.btn_frm = tk.Frame(
            self.root, 
            width=BTN_FRM_WIDTH, 
            height=BTN_FRM_HEIGHT, 
            bg=COLOR_PRIMARY,
        )
        # fmt: on
        self.btn_frm.pack()
        self.render_buttons(self.btn_frm)

    def on_key_press(self, event):
        match event.char:
            case "/":
                self.input_fld.insert(tk.INSERT, Buttons.div.value)
                return "break"
            case "*":
                self.input_fld.insert(tk.INSERT, Buttons.mul.value)
                return "break"
            case "c":
                self.clear()
                return "break"
            case "h":
                self.get_history()
                return "break"
            case Buttons.equal.value:
                self.evaluate()
                return "break"
            case "\b":
                pos = self.input_fld.index(tk.INSERT)
                self.input_fld.delete(pos - 1)
                return "break"
            case "":
                pos = self.input_fld.index(tk.INSERT)
                if event.keysym == "Left":
                    new_pos = max(0, pos - 1)
                elif event.keysym == "Right":
                    new_pos = max(0, pos + 1)
                else:
                    new_pos = pos
                self.input_fld.icursor(new_pos)
                return "break"
            case _:
                self.insert_input(event.char, kb=True)
                return "break"

    def validate(self, P: str):
        """
        Checks if only allowed NUM_PAD characters have been entered.
        Allows user to enter only NUM_PAD characters.
        """
        if len(P) > MAX_INPUT_CHARS:
            return False
        for l in P:
            if l not in [x.value for x in NUM_PAD]:
                return False
        return True

    def render_buttons(self, master):
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

            tk.Button(
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

    def insert_input(self, char: Buttons | str, kb=False):
        match char:
            case Buttons.clear:
                self.clear()
            case Buttons.equal:
                self.evaluate()
            case Buttons.hist:
                self.get_history()
            case _:
                if isinstance(char, Buttons):
                    c = char.value
                else:
                    c = char
                if self.validate(c):
                    if self.input_txt.get() == Buttons.zero.value and c not in [
                        x.value for x in operators
                    ]:
                        self.input_txt.set(c)
                    else:
                        if kb:
                            self.input_fld.insert(tk.INSERT, c)
                        else:
                            self.input_txt.set(self.input_txt.get() + c)

    def clear(self):
        self.input_txt.set(Buttons.zero.value)

    def evaluate(self):
        print("TODO: Evaluate", self.input_txt.get())

    def get_history(self):
        print("TODO: Get history")
        if self.hist and self.hist.winfo_exists():
            self.hist.destroy()
        else:
            self.hist = SidePanel(self.root)
            self.root.wait_window(self.hist)

    def run(self):
        self.root.mainloop()


class SidePanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLOR_ACCENT)
        self.grab_set()
        self.place(relx=0.0, rely=0.0, anchor="nw", relheight=1.0, relwidth=0.7)

        close_btn = tk.Button(
            self,
            width=3,
            font=(FONT_FAMILY, 10),
            text="Close",
            cursor=POINTER,
            command=self.close,
        )
        close_btn.pack(pady=10)

    def close(self):
        self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
