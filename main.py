import math
import random
import secrets
import string
import tkinter as tk
from tkinter import font as tkfont

# ----------------------------------------------------------------------
# Palette — soft watercolor sky, meadow greens, warm sun, dusty rose
# ----------------------------------------------------------------------
SKY_TOP = "#bfe3e8"
SKY_MID = "#eaf3d8"
SKY_BOTTOM = "#f6ecd9"
MEADOW = "#8fb98a"
MEADOW_DARK = "#6f9e6a"
PANEL = "#fbf6e9"
PANEL_EDGE = "#d8c9a3"
INK = "#4a4032"
INK_SOFT = "#6c6151"
SUN = "#f4c869"
CLOUD = "#ffffff"
ROSE = "#e2a0a0"
ROSE_DARK = "#c97b7b"
BLUE_BTN = "#7fb2b0"
BLUE_BTN_DARK = "#5f9491"
TOTORO_GREY = "#8f8b83"

FONT_TITLE = ("Georgia", 22, "bold")
FONT_LABEL = ("Georgia", 11)
FONT_LABEL_B = ("Georgia", 11, "bold")
FONT_MONO = ("Courier New", 15, "bold")
FONT_SMALL = ("Georgia", 9)


class GhibliPasswordGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ghibli Garden — Password Generator")
        self.geometry("600x760")
        self.minsize(560, 720)
        self.configure(bg=SKY_TOP)

        # ---- state -------------------------------------------------
        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.avoid_ambiguous_var = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar(value="")
        self.copied_var = tk.StringVar(value="")

        self._build_background()
        self._build_panel()
        self._float_clouds()
        self.generate_password()

    # ------------------------------------------------------------------
    # Background: painted sky, rolling meadow hill, drifting clouds
    # ------------------------------------------------------------------
    def _build_background(self):
        self.bg = tk.Canvas(self, highlightthickness=0, bd=0)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind("<Configure>", self._redraw_background)
        self._cloud_ids = []

    def _redraw_background(self, event=None):
        c = self.bg
        c.delete("all")
        w = c.winfo_width() or 560
        h = c.winfo_height() or 720

        # vertical watercolor gradient sky
        steps = 60
        for i in range(steps):
            t = i / steps
            if t < 0.6:
                tt = t / 0.6
                color = self._blend(SKY_TOP, SKY_MID, tt)
            else:
                tt = (t - 0.6) / 0.4
                color = self._blend(SKY_MID, SKY_BOTTOM, tt)
            y0 = int(h * t)
            y1 = int(h * (t + 1 / steps)) + 1
            c.create_rectangle(0, y0, w, y1, fill=color, outline=color)

        # sun
        c.create_oval(w - 120, 40, w - 40, 120, fill=SUN, outline="")
        c.create_oval(w - 130, 30, w - 30, 130, fill="", outline=SUN, width=1)

        # rolling meadow hills (back then front, Totoro-esque silhouettes)
        hill_back = self._hill_points(w, h, base=h * 0.86, amp=18, phase=0.0)
        c.create_polygon(hill_back, fill=self._blend(MEADOW, SKY_BOTTOM, 0.35), outline="")

        hill_front = self._hill_points(w, h, base=h * 0.93, amp=26, phase=1.7)
        c.create_polygon(hill_front, fill=MEADOW, outline="")

        # little tree + totoro-ish shrub silhouette on the hill for charm
        self._draw_tree(c, w * 0.14, h * 0.90)
        self._draw_shrub(c, w * 0.85, h * 0.955)

        self._cloud_ids = []
        for cx, cy, s in [(0.15, 0.16, 1.0), (0.55, 0.10, 0.7), (0.75, 0.22, 0.55)]:
            cid = self._draw_cloud(c, w * cx, h * cy, s)
            self._cloud_ids.append(cid)

        # keep panel on top
        if hasattr(self, "panel_frame"):
            self.panel_frame.tkraise()

    @staticmethod
    def _blend(hex1, hex2, t):
        r1, g1, b1 = int(hex1[1:3], 16), int(hex1[3:5], 16), int(hex1[5:7], 16)
        r2, g2, b2 = int(hex2[1:3], 16), int(hex2[3:5], 16), int(hex2[5:7], 16)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def _hill_points(w, h, base, amp, phase):
        pts = [0, h]
        n = 40
        for i in range(n + 1):
            x = w * i / n
            y = base + amp * math.sin(phase + i / n * math.pi * 2.3)
            pts += [x, y]
        pts += [w, h]
        return pts

    def _draw_cloud(self, c, x, y, scale=1.0):
        r = 18 * scale
        parts = []
        parts.append(c.create_oval(x - r * 1.8, y - r * 0.6, x + r * 1.8, y + r * 0.6,
                                    fill=CLOUD, outline=""))
        parts.append(c.create_oval(x - r * 1.1, y - r * 1.1, x + r * 0.5, y + r * 0.5,
                                    fill=CLOUD, outline=""))
        parts.append(c.create_oval(x - r * 0.2, y - r * 1.3, x + r * 1.4, y + r * 0.4,
                                    fill=CLOUD, outline=""))
        return parts

    def _draw_tree(self, c, x, y):
        c.create_rectangle(x - 4, y - 30, x + 4, y, fill="#6b5443", outline="")
        for dx, dy, r in [(0, -55, 26), (-16, -40, 20), (16, -40, 20)]:
            c.create_oval(x + dx - r, y + dy - r, x + dx + r, y + dy + r,
                          fill=MEADOW_DARK, outline="")

    def _draw_shrub(self, c, x, y):
        for dx, r in [(-14, 14), (0, 20), (14, 13)]:
            c.create_oval(x + dx - r, y - r * 1.2, x + dx + r, y + r * 0.4,
                          fill=MEADOW_DARK, outline="")

    def _float_clouds(self):
        # gentle horizontal drift for whimsy
        try:
            w = self.bg.winfo_width() or 560
            for group in self._cloud_ids:
                for part in group:
                    self.bg.move(part, 0.3, 0)
                    coords = self.bg.coords(part)
                    if coords and coords[0] > w + 60:
                        self.bg.move(part, -(w + 140), 0)
        except tk.TclError:
            pass
        self.after(60, self._float_clouds)

    # ------------------------------------------------------------------
    # Foreground panel — the "storybook card"
    # ------------------------------------------------------------------
    def _build_panel(self):
        self.panel_frame = tk.Frame(self, bg=SKY_TOP)
        self.panel_frame.place(relx=0.5, rely=0.5, anchor="center",
                                relwidth=0.88, relheight=0.86)

        card = RoundedCard(self.panel_frame, bg_color=PANEL, edge_color=PANEL_EDGE,
                            radius=28)
        card.pack(fill="both", expand=True)
        inner = card.inner

        # Title
        tk.Label(inner, text="🌿  Ghibli Garden  🌿", font=FONT_TITLE,
                 bg=PANEL, fg=INK).pack(pady=(18, 0))
        tk.Label(inner, text="a little spell for a strong password",
                 font=("Georgia", 10, "italic"), bg=PANEL, fg=INK_SOFT).pack(pady=(0, 14))

        # Password display "scroll"
        display_wrap = tk.Frame(inner, bg=PANEL_EDGE, bd=0)
        display_wrap.pack(fill="x", padx=26, pady=(0, 6))
        display_inner = tk.Frame(display_wrap, bg="#fffdf5")
        display_inner.pack(fill="x", padx=2, pady=2)

        self.pw_entry = tk.Entry(display_inner, textvariable=self.password_var,
                                  font=FONT_MONO, justify="center", bd=0,
                                  bg="#fffdf5", fg=INK, relief="flat",
                                  readonlybackground="#fffdf5", state="readonly")
        self.pw_entry.pack(fill="x", padx=10, pady=12)

        tk.Label(inner, textvariable=self.copied_var, font=FONT_SMALL,
                 bg=PANEL, fg=MEADOW_DARK).pack(pady=(0, 6))

        # Strength meter
        self.strength_canvas = tk.Canvas(inner, height=14, bg=PANEL,
                                          highlightthickness=0)
        self.strength_canvas.pack(fill="x", padx=26, pady=(0, 4))
        self._last_strength = (0, "#cccccc")
        self.strength_canvas.bind(
            "<Configure>",
            lambda e: self._draw_strength_bar(*self._last_strength))
        self.strength_label = tk.Label(inner, text="", font=FONT_SMALL,
                                        bg=PANEL, fg=INK_SOFT)
        self.strength_label.pack(pady=(0, 10))

        # Buttons row: generate / copy
        btn_row = tk.Frame(inner, bg=PANEL)
        btn_row.pack(pady=(0, 16))
        LeafButton(btn_row, text="✦ Cast a New Spell", command=self.generate_password,
                   base_color=BLUE_BTN, dark_color=BLUE_BTN_DARK).pack(side="left", padx=6)
        LeafButton(btn_row, text="🍃 Copy", command=self.copy_password,
                   base_color=ROSE, dark_color=ROSE_DARK).pack(side="left", padx=6)

        # Divider
        tk.Frame(inner, bg=PANEL_EDGE, height=1).pack(fill="x", padx=26, pady=(0, 14))

        # Length slider
        len_row = tk.Frame(inner, bg=PANEL)
        len_row.pack(fill="x", padx=30)
        tk.Label(len_row, text="Length", font=FONT_LABEL_B, bg=PANEL, fg=INK)\
            .pack(side="left")
        self.length_display = tk.Label(len_row, text=str(self.length_var.get()),
                                        font=FONT_LABEL_B, bg=PANEL, fg=MEADOW_DARK)
        self.length_display.pack(side="right")

        self.length_scale = tk.Scale(inner, from_=6, to=48, orient="horizontal",
                                      variable=self.length_var, showvalue=False,
                                      bg=PANEL, fg=INK, troughcolor="#e4ddc4",
                                      highlightthickness=0, bd=0,
                                      activebackground=MEADOW_DARK,
                                      command=self._on_length_change)
        self.length_scale.pack(fill="x", padx=30, pady=(2, 14))

        # Checkboxes ("ingredients")
        tk.Label(inner, text="Ingredients for the spell", font=FONT_LABEL_B,
                 bg=PANEL, fg=INK).pack(anchor="w", padx=30)

        opts = tk.Frame(inner, bg=PANEL)
        opts.pack(fill="x", padx=26, pady=(6, 4))

        self._make_check(opts, "🌼  Uppercase (A-Z)", self.upper_var, 0, 0)
        self._make_check(opts, "🍀  Lowercase (a-z)", self.lower_var, 1, 0)
        self._make_check(opts, "🌰  Numbers (0-9)", self.digits_var, 0, 1)
        self._make_check(opts, "🍂  Symbols (!@#$)", self.symbols_var, 1, 1)
        self._make_check(opts, "🕊  Avoid look-alikes (l1IO0)", self.avoid_ambiguous_var, 0, 2,
                          columnspan=2)

        for var in (self.upper_var, self.lower_var, self.digits_var,
                    self.symbols_var, self.avoid_ambiguous_var):
            var.trace_add("write", lambda *_: self.generate_password())

        tk.Label(inner, text="Soot sprites keep this password only on your screen —\n"
                              "nothing is sent anywhere.",
                 font=FONT_SMALL, bg=PANEL, fg=INK_SOFT, justify="center")\
            .pack(pady=(10, 4))

    def _make_check(self, parent, text, var, col, row, columnspan=1):
        cb = tk.Checkbutton(parent, text=text, variable=var,
                             font=("Georgia", 10),
                             bg=PANEL, fg=INK, activebackground=PANEL,
                             selectcolor="#fffdf5", anchor="w",
                             onvalue=True, offvalue=False, bd=0,
                             highlightthickness=0)
        cb.grid(row=row, column=col, sticky="w", padx=6, pady=4, columnspan=columnspan)
        parent.grid_columnconfigure(col, weight=1)

    def _on_length_change(self, _val=None):
        self.length_display.config(text=str(self.length_var.get()))
        self.generate_password()

    # ------------------------------------------------------------------
    # Password logic
    # ------------------------------------------------------------------
    def generate_password(self):
        length = self.length_var.get()
        pools = []
        required = []

        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        symbols = "!@#$%^&*()-_=+[]{};:,.<>?/"

        if self.avoid_ambiguous_var.get():
            ambiguous = set("lI1O0oB8S5Z2")
            upper = "".join(ch for ch in upper if ch not in ambiguous)
            lower = "".join(ch for ch in lower if ch not in ambiguous)
            digits = "".join(ch for ch in digits if ch not in ambiguous)

        if self.upper_var.get():
            pools.append(upper)
            required.append(secrets.choice(upper))
        if self.lower_var.get():
            pools.append(lower)
            required.append(secrets.choice(lower))
        if self.digits_var.get():
            pools.append(digits)
            required.append(secrets.choice(digits))
        if self.symbols_var.get():
            pools.append(symbols)
            required.append(secrets.choice(symbols))

        if not pools:
            self.password_var.set("")
            self.strength_label.config(text="Pick at least one ingredient 🌱")
            self._draw_strength_bar(0)
            return

        all_chars = "".join(pools)
        length = max(length, len(required))
        remaining = length - len(required)
        body = [secrets.choice(all_chars) for _ in range(remaining)]
        password_chars = required + body
        rnd = secrets.SystemRandom()
        rnd.shuffle(password_chars)
        password = "".join(password_chars)

        self.password_var.set(password)
        self.copied_var.set("")
        self._update_strength(password, pools)

    def copy_password(self):
        pw = self.password_var.get()
        if not pw:
            return
        self.clipboard_clear()
        self.clipboard_append(pw)
        self.copied_var.set("✓ copied to clipboard — like catching a falling star")

    # ------------------------------------------------------------------
    # Strength meter (Ghibli-flavoured labels)
    # ------------------------------------------------------------------
    def _update_strength(self, password, pools):
        pool_size = len(set("".join(pools)))
        entropy = len(password) * math.log2(pool_size) if pool_size > 1 else 0

        if entropy < 40:
            level, color, label = 1, "#e29a5a", "Soot Sprite — a bit fragile"
        elif entropy < 60:
            level, color, label = 2, "#e2c95a", "Catbus — sturdy and speedy"
        elif entropy < 80:
            level, color, label = 3, "#8bbf6b", "Totoro — big and dependable"
        else:
            level, color, label = 4, "#5f9491", "Spirit of the Forest — nearly unbreakable"

        self.strength_label.config(text=f"{label}  (~{int(entropy)} bits)")
        self._draw_strength_bar(level, color)

    def _draw_strength_bar(self, level, color="#cccccc"):
        self._last_strength = (level, color)
        c = self.strength_canvas
        c.delete("all")
        w = c.winfo_width()
        if w <= 1:
            w = 460
        segs = 4
        gap = 6
        seg_w = (w - gap * (segs - 1)) / segs
        for i in range(segs):
            x0 = i * (seg_w + gap)
            fill = color if i < level else "#e6dfc9"
            c.create_rectangle(x0, 0, x0 + seg_w, 14, fill=fill, outline="")


class RoundedCard(tk.Frame):
    """A frame drawn with a soft rounded rectangle (canvas-backed)."""

    def __init__(self, parent, bg_color, edge_color, radius=24, **kwargs):
        super().__init__(parent, bg=parent["bg"], **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=parent["bg"])
        self.canvas.pack(fill="both", expand=True)
        self.bg_color = bg_color
        self.edge_color = edge_color
        self.radius = radius
        self.inner = tk.Frame(self.canvas, bg=bg_color)
        self.canvas.bind("<Configure>", self._redraw)

    def _redraw(self, event):
        c = self.canvas
        c.delete("shape")
        w, h, r = event.width, event.height, self.radius
        c.create_round_rect = self._round_rect
        c.create_round_rect(c, 3, 3, w - 3, h - 3, r, fill=self.bg_color,
                             outline=self.edge_color, width=2, tags="shape")
        c.create_window(w / 2, h / 2, window=self.inner, width=w - 10, height=h - 10)

    @staticmethod
    def _round_rect(canvas, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)


class LeafButton(tk.Canvas):
    """A hand-drawn-feeling rounded button with a hover 'grow' effect."""

    def __init__(self, parent, text, command, base_color, dark_color,
                 width=190, height=46, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"],
                          highlightthickness=0, bd=0, **kwargs)
        self.command = command
        self.base_color = base_color
        self.dark_color = dark_color
        self.text = text
        self.w, self.h = width, height
        self._draw(base_color)
        self.bind("<Enter>", lambda e: self._draw(self.dark_color))
        self.bind("<Leave>", lambda e: self._draw(self.base_color))
        self.bind("<Button-1>", lambda e: self._on_click())

    def _draw(self, color):
        self.delete("all")
        r = self.h / 2
        self.create_oval(2, 2, self.h - 2, self.h - 2, fill=color, outline="")
        self.create_oval(self.w - self.h + 2, 2, self.w - 2, self.h - 2,
                          fill=color, outline="")
        self.create_rectangle(r, 2, self.w - r, self.h - 2, fill=color, outline="")
        self.create_text(self.w / 2, self.h / 2, text=self.text,
                          font=FONT_LABEL_B, fill="#fffdf5")

    def _on_click(self):
        self._draw("#4d7573")
        self.after(120, lambda: self._draw(self.base_color))
        if self.command:
            self.command()


if __name__ == "__main__":
    app = GhibliPasswordGenerator()
    app.mainloop()