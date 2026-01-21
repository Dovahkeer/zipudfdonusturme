import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD


def resource_path(relative: str) -> str:
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return os.path.join(base_path, relative)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative)


def choose_save_path(zip_path: str, parent: tk.Misc) -> str | None:
    base_name = os.path.splitext(os.path.basename(zip_path))[0]
    default_name = f"{base_name}.udf"

    return filedialog.asksaveasfilename(
        title="Kaydet",
        defaultextension=".udf",
        initialfile=default_name,
        filetypes=[("UDF dosyası", "*.udf")],
        parent=parent,
    )


def convert_zip_to_udf(zip_path: str, parent: tk.Misc) -> str | None:
    dest_path = choose_save_path(zip_path, parent)
    if not dest_path:
        return None

    final_dir = os.path.dirname(dest_path)
    if final_dir and not os.path.isdir(final_dir):
        os.makedirs(final_dir, exist_ok=True)

    shutil.copyfile(zip_path, dest_path)
    return dest_path


def process_zip(zip_path: str, parent: tk.Misc) -> str | None:
    if not zip_path:
        raise ValueError("Dosya yolu boş")

    if not zip_path.lower().endswith(".zip"):
        raise ValueError("Lütfen .zip dosyası kullanın")

    if not os.path.isfile(zip_path):
        raise FileNotFoundError("Dosya bulunamadı")

    return convert_zip_to_udf(zip_path, parent)


def handle_zip_path(zip_path: str, root: tk.Misc) -> None:
    try:
        udf_path = process_zip(zip_path, root)
    except Exception as exc:  # noqa: BLE001
        messagebox.showerror("Hata", str(exc), parent=root)
        return

    if not udf_path:
        return

    messagebox.showinfo("Tamamlandı", f"Kaydedildi:\n{udf_path}", parent=root)


def handle_select_zip(root: tk.Misc) -> None:
    zip_path = filedialog.askopenfilename(
        title="ZIP seç",
        filetypes=[("ZIP dosyası", "*.zip")],
        parent=root,
    )

    if not zip_path:
        return

    handle_zip_path(zip_path, root)


def handle_drop(event: tk.Event, root: tk.Misc) -> None:
    paths = root.splitlist(event.data)
    if not paths:
        return

    first_path = paths[0]
    handle_zip_path(first_path, root)


def main():
    root = TkinterDnD.Tk()
    root.title("ZIP'ten UDF'ye")
    root.geometry("360x240")
    root.resizable(False, False)

    icon_path = resource_path(os.path.join("assets", "zip_to_udf.ico"))
    if os.path.isfile(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass

    heading = tk.Label(root, text="ZIP yükle, UDF indir", font=("Segoe UI", 12, "bold"))
    heading.pack(pady=(16, 8))

    desc = tk.Label(root, text="ZIP seç veya sürükleyip bırak; .udf için konum seçilecek.")
    desc.pack(pady=(0, 8))

    drop_zone = tk.Label(
        root,
        text="ZIP dosyasını buraya bırakın",
        relief="solid",
        bd=1,
        bg="#f2f2f2",
        fg="#333",
        width=32,
        height=4,
    )
    drop_zone.pack(pady=8)

    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", lambda event: handle_drop(event, root))
    drop_zone.drop_target_register(DND_FILES)
    drop_zone.dnd_bind("<<Drop>>", lambda event: handle_drop(event, root))

    select_btn = tk.Button(root, text="ZIP Seç", width=14, command=lambda: handle_select_zip(root))
    select_btn.pack(pady=12)

    root.mainloop()


if __name__ == "__main__":
    main()
