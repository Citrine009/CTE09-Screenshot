import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageGrab
from pathlib import Path
from datetime import datetime
import json
import ctypes


CONFIG_FILE = Path.home() / ".cte09_screenshot_config.json"


class ScreenshotTool:

    def __init__(self, root):
        self.root = root
        self.root.title("CTE09 Screenshot Tool")
        self.root.resizable(False, False)

        # Variables
        self.x_var = tk.StringVar(value="0")
        self.y_var = tk.StringVar(value="0")
        self.w_var = tk.StringVar(value="800")
        self.h_var = tk.StringVar(value="600")

        self.folder_var = tk.StringVar(
            value=str(Path.home() / "Pictures")
        )

        self.format_var = tk.StringVar(value="PNG")
        self.filename_var = tk.StringVar(value="Screenshot")

        self.load_config()
        self.create_ui()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    # =========================================================
    # CONFIG
    # =========================================================

    def load_config(self):
        if not CONFIG_FILE.exists():
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.x_var.set(str(data.get("x", 0)))
            self.y_var.set(str(data.get("y", 0)))
            self.w_var.set(str(data.get("width", 800)))
            self.h_var.set(str(data.get("height", 600)))

            folder = data.get("folder")
            if folder:
                self.folder_var.set(folder)

            fmt = data.get("format", "PNG")
            self.format_var.set(fmt)

        except Exception:
            pass

    def save_config(self):
        try:
            data = {
                "x": int(self.x_var.get()),
                "y": int(self.y_var.get()),
                "width": int(self.w_var.get()),
                "height": int(self.h_var.get()),
                "folder": self.folder_var.get(),
                "format": self.format_var.get()
            }

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

        except Exception:
            pass

    # =========================================================
    # UI
    # =========================================================

    def create_ui(self):

        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        title = ttk.Label(
            main,
            text="CTE09 Screenshot Tool",
            font=("Segoe UI", 11, "bold")
        )
        title.grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # X
        # -----------------------------------------------------

        ttk.Label(main, text="X").grid(
            row=1,
            column=0,
            sticky="w"
        )

        ttk.Entry(
            main,
            textvariable=self.x_var,
            width=10
        ).grid(
            row=1,
            column=1,
            padx=(5, 10)
        )

        # -----------------------------------------------------
        # Y
        # -----------------------------------------------------

        ttk.Label(main, text="Y").grid(
            row=1,
            column=2,
            sticky="w"
        )

        ttk.Entry(
            main,
            textvariable=self.y_var,
            width=10
        ).grid(
            row=1,
            column=3
        )

        # -----------------------------------------------------
        # WIDTH
        # -----------------------------------------------------

        ttk.Label(main, text="Width").grid(
            row=2,
            column=0,
            sticky="w"
        )

        ttk.Entry(
            main,
            textvariable=self.w_var,
            width=10
        ).grid(
            row=2,
            column=1,
            padx=(5, 10)
        )

        # -----------------------------------------------------
        # HEIGHT
        # -----------------------------------------------------

        ttk.Label(main, text="Height").grid(
            row=2,
            column=2,
            sticky="w"
        )

        ttk.Entry(
            main,
            textvariable=self.h_var,
            width=10
        ).grid(
            row=2,
            column=3
        )

        # -----------------------------------------------------
        # REGION BUTTON
        # -----------------------------------------------------

        ttk.Button(
            main,
            text="Set Region",
            command=self.set_region
        ).grid(
            row=3,
            column=0,
            columnspan=4,
            sticky="ew",
            pady=(10, 5)
        )

        # -----------------------------------------------------
        # FOLDER
        # -----------------------------------------------------

        ttk.Label(main, text="Save folder").grid(
            row=4,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(5, 2)
        )

        folder_frame = ttk.Frame(main)
        folder_frame.grid(
            row=5,
            column=0,
            columnspan=4,
            sticky="ew"
        )

        folder_entry = ttk.Entry(
            folder_frame,
            textvariable=self.folder_var,
            width=32
        )
        folder_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            folder_frame,
            text="...",
            width=4,
            command=self.choose_folder
        ).pack(
            side="left",
            padx=(5, 0)
        )
        
        # ----------------------------------------------------
        # FILENAME
        # -----------------------------------------------------

        ttk.Label(main, text="Filename").grid(
            row=6,
            column=2,
            sticky="w",
            pady=(8, 0)
        )

        filename_entry = ttk.Entry(
            main,
            textvariable=self.filename_var,
            width=20
        )
        filename_entry.grid(
            row=6,
            column=3,
            sticky="w",
            padx=(5, 0),
            pady=(8, 0)
        )

        # -----------------------------------------------------
        # FORMAT
        # -----------------------------------------------------

        ttk.Label(main, text="Format").grid(
            row=6,
            column=0,
            sticky="w",
            pady=(8, 0)
        )

        format_box = ttk.Combobox(
            main,
            textvariable=self.format_var,
            values=["PNG", "JPG"],
            state="readonly",
            width=8
        )

        format_box.grid(
            row=6,
            column=1,
            sticky="w",
            padx=(5, 0),
            pady=(8, 0)
        )

        # -----------------------------------------------------
        # CAPTURE
        # -----------------------------------------------------

        ttk.Button(
            main,
            text="CAPTURE",
            command=self.capture
        ).grid(
            row=7,
            column=0,
            columnspan=4,
            sticky="ew",
            pady=(12, 5),
            ipady=5
        )

        # -----------------------------------------------------
        # HOTKEY INFO
        # -----------------------------------------------------

        ttk.Label(
            main,
            text="Hotkey: Ctrl + Shift + S"
        ).grid(
            row=8,
            column=0,
            columnspan=4,
            pady=(5, 0)
        )

        self.root.bind(
            "<Control-Shift-s>",
            self.hotkey_capture
        )

    # =========================================================
    # VALUES
    # =========================================================

    def get_values(self):

        try:
            x = int(self.x_var.get())
            y = int(self.y_var.get())
            width = int(self.w_var.get())
            height = int(self.h_var.get())

        except ValueError:
            messagebox.showerror(
                "Error",
                "X, Y, Width và Height phải là số."
            )
            return None

        if width <= 0 or height <= 0:
            messagebox.showerror(
                "Error",
                "Width và Height phải lớn hơn 0."
            )
            return None

        return x, y, width, height

    # =========================================================
    # CAPTURE
    # =========================================================

    def capture(self):

        values = self.get_values()

        if values is None:
            return

        self.save_config()

        # Hide the UI first
        self.root.withdraw()

        # Force Windows/Tkinter to process the hide
        self.root.update_idletasks()
        self.root.update()

        # Wait before taking screenshot
        self.root.after(
            200,
            lambda: self.do_capture(values)
        )

    def do_capture(self, values):

        x, y, width, height = values

        try:

            bbox = (
                x,
                y,
                x + width,
                y + height
            )

            image = ImageGrab.grab(
                bbox=bbox
            )

            folder = Path(
                self.folder_var.get()
            ).expanduser()

            folder.mkdir(
                parents=True,
                exist_ok=True
            )

            base_name = self.filename_var.get().strip()

            if not base_name:
                base_name = "Screenshot"

            base_name = Path(base_name).stem

            fmt = self.format_var.get().upper()

            if fmt == "JPG":
                extension = ".jpg"
            else:
                extension = ".png"

            counter = 1

            while True:
                filename = f"{base_name}_{counter:03d}{extension}"
                path = folder / filename

                if not path.exists():
                    break

                counter += 1

            if fmt == "JPG":

                # JPG doesn't support RGBA
                if image.mode in ("RGBA", "LA"):
                    image = image.convert("RGB")

                image.save(
                    path,
                    "JPEG",
                    quality=95
                )

            else:

                image.save(
                    path,
                    "PNG"
                )

            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

            print(
                f"Saved: {path}"
            )

        except Exception as e:

            self.root.deiconify()
            self.root.lift()

            messagebox.showerror(
                "Screenshot Error",
                str(e)
            )

    # =========================================================
    # HOTKEY
    # =========================================================

    def hotkey_capture(self, event=None):
        self.capture()

    # =========================================================
    # REGION SELECTOR
    # =========================================================

    def set_region(self):

        self.root.withdraw()

        self.root.update_idletasks()
        self.root.update()

        self.root.after(
            100,
            self.open_region_selector
        )

    def open_region_selector(self):

        overlay = tk.Toplevel(self.root)

        overlay.overrideredirect(True)
        overlay.attributes(
            "-topmost",
            True
        )

        overlay.attributes(
            "-alpha",
            0.25
        )

        screen_w = overlay.winfo_screenwidth()
        screen_h = overlay.winfo_screenheight()

        overlay.geometry(
            f"{screen_w}x{screen_h}+0+0"
        )

        canvas = tk.Canvas(
            overlay,
            bg="black",
            cursor="crosshair",
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        state = {
            "start_x": None,
            "start_y": None,
            "rect": None
        }

        # -----------------------------------------------------
        # Mouse down
        # -----------------------------------------------------

        def mouse_down(event):

            state["start_x"] = event.x
            state["start_y"] = event.y

            if state["rect"] is not None:
                canvas.delete(
                    state["rect"]
                )

            state["rect"] = canvas.create_rectangle(
                event.x,
                event.y,
                event.x,
                event.y,
                outline="red",
                width=2
            )

        # -----------------------------------------------------
        # Mouse move
        # -----------------------------------------------------

        def mouse_move(event):

            if state["start_x"] is None:
                return

            canvas.coords(
                state["rect"],
                state["start_x"],
                state["start_y"],
                event.x,
                event.y
            )

        # -----------------------------------------------------
        # Mouse up
        # -----------------------------------------------------

        def mouse_up(event):

            if state["start_x"] is None:
                return

            x1 = min(
                state["start_x"],
                event.x
            )

            y1 = min(
                state["start_y"],
                event.y
            )

            x2 = max(
                state["start_x"],
                event.x
            )

            y2 = max(
                state["start_y"],
                event.y
            )

            width = x2 - x1
            height = y2 - y1

            if width < 5 or height < 5:

                overlay.destroy()

                self.root.deiconify()
                self.root.lift()

                return

            self.x_var.set(
                str(x1)
            )

            self.y_var.set(
                str(y1)
            )

            self.w_var.set(
                str(width)
            )

            self.h_var.set(
                str(height)
            )

            self.save_config()

            overlay.destroy()

            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

        # -----------------------------------------------------
        # Escape
        # -----------------------------------------------------

        def cancel(event=None):

            overlay.destroy()

            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

        canvas.bind(
            "<ButtonPress-1>",
            mouse_down
        )

        canvas.bind(
            "<B1-Motion>",
            mouse_move
        )

        canvas.bind(
            "<ButtonRelease-1>",
            mouse_up
        )

        overlay.bind(
            "<Escape>",
            cancel
        )

        overlay.focus_force()

    # =========================================================
    # FOLDER
    # =========================================================

    def choose_folder(self):

        folder = filedialog.askdirectory(
            title="Chọn thư mục lưu ảnh"
        )

        if folder:

            self.folder_var.set(
                folder
            )

            self.save_config()

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        self.save_config()

        self.root.destroy()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    # Make Tkinter and ImageGrab use physical screen pixels
    # instead of Windows DPI-scaled logical pixels.
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(
            ctypes.c_void_p(-4)
        )
    except Exception:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass

    root = tk.Tk()

    app = ScreenshotTool(root)

    root.mainloop()