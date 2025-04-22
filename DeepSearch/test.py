import tkinter as tk
from tkinter import filedialog, messagebox
from docx import Document

def open_docx():
    file_path = filedialog.askopenfilename(
        filetypes=[("Word Documents", "*.docx")]
    )
    if not file_path:
        return

    try:
        doc = Document(file_path)
        text_content = "\n".join([para.text for para in doc.paragraphs])
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, text_content)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open document:\n{e}")

# Create GUI
root = tk.Tk()
root.title("Word Viewer")

open_button = tk.Button(root, text="Open Word Document", command=open_docx)
open_button.pack(pady=10)

text_widget = tk.Text(root, wrap=tk.WORD)
text_widget.pack(expand=True, fill=tk.BOTH)

root.geometry("600x500")
root.mainloop()
