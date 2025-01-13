import tkinter as tk
from tkinter import filedialog

from config import ENCODINGS, LOADED_NOVEL_PATTERN, SAVING_NOVEL_PATTERN
from novel_manager import NovelManager

class Ui(tk.Tk):
  novel_manager = NovelManager()

  def __init__(self):
    super().__init__()
    self.title('Azuma Novel Manager')

    self.frame = tk.Frame(self)
    self.frame.pack(pady=10, fill=tk.BOTH, expand=True)

    self.add_file_frame()
    self.add_loaded_file_frame()
    self.add_saving_file_frame()
    self.add_loaded_file_pattern_frame()
    self.add_saving_file_pattern_frame()
    self.add_novel_content_frame()
    self.add_save_and_upload_buttons_frame()

  def add_file_frame(self):
    self.file_frame = tk.Frame(self.frame)
    self.file_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    self.file_frame.grid_columnconfigure(1, weight=1)

  def add_loaded_file_frame(self):
    label = tk.Label(self.file_frame, text='読込元パス:')
    label.grid(row=0, column=0, pady=10, sticky='e')

    self.loaded_novel_path_var = tk.StringVar(value='')
    self.loaded_novel_path_var.trace_add('write', self.update_saving_novel_path)

    self.loaded_novel_path = tk.Entry(self.file_frame, textvariable=self.loaded_novel_path_var)
    self.loaded_novel_path.grid(row=0, column=1, padx=5, sticky='ew')

    button = tk.Button(self.file_frame, text='開く', command=self.open_novel)
    button.grid(row=0, column=2, padx=5, sticky='e')

  def add_saving_file_frame(self):
    label = tk.Label(self.file_frame, text='保存先パス:')
    label.grid(row=1, column=0, pady=10, sticky='e')

    self.saving_novel_path = tk.Entry(self.file_frame)
    self.saving_novel_path.grid(row=1, column=1, padx=5, sticky='ew')

  def add_loaded_file_pattern_frame(self):
    label = tk.Label(self.file_frame, text='読込元パターン:')
    label.grid(row=2, column=0, pady=10, sticky='e')

    self.loaded_novel_pattern_var = tk.StringVar(value=LOADED_NOVEL_PATTERN)
    self.loaded_novel_pattern_var.trace_add('write', self.update_saving_novel_path)

    self.loaded_novel_pattern = tk.Entry(self.file_frame, textvariable=self.loaded_novel_pattern_var)
    self.loaded_novel_pattern.grid(row=2, column=1, padx=5, sticky='ew')

  def add_saving_file_pattern_frame(self):
    label = tk.Label(self.file_frame, text='保存先パターン:')
    label.grid(row=3, column=0, pady=10, sticky='e')

    self.saving_novel_pattern_var = tk.StringVar(value=SAVING_NOVEL_PATTERN)
    self.saving_novel_pattern_var.trace_add('write', self.update_saving_novel_path)

    self.saving_novel_pattern = tk.Entry(self.file_frame, textvariable=self.saving_novel_pattern_var)
    self.saving_novel_pattern.grid(row=3, column=1, padx=5, sticky='ew')

  def add_novel_content_frame(self):
    sub_frame = tk.Frame(self.frame)
    sub_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    label = tk.Label(sub_frame, text='小説の内容:')
    label.pack(side=tk.TOP, padx=5)

    self.novel_content = tk.Text(sub_frame, state=tk.DISABLED)
    self.novel_content.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

  def add_save_and_upload_buttons_frame(self):
    sub_frame = tk.Frame(self.frame)
    sub_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    label = tk.Label(sub_frame, text='保存するエンコーディング:')
    label.pack(side=tk.LEFT, padx=5)

    self.encoding_var = tk.StringVar(value='utf-8')
    encoding_options = ENCODINGS
    self.encoding_menu = tk.OptionMenu(sub_frame, self.encoding_var, *encoding_options)
    self.encoding_menu.pack(side=tk.LEFT, padx=5)

    save_button = tk.Button(sub_frame, text='保存する', command=self.save_novel)
    save_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

    upload_button = tk.Button(sub_frame, text='アップロードする')
    upload_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)

  def open_novel(self):
    file_path = filedialog.askopenfilename()
    if file_path:
      self.novel_manager.load_novel(file_path)
      self.loaded_novel_path_var.set(self.novel_manager.loaded_novel_path)
      self.novel_content.config(state=tk.NORMAL)
      self.novel_content.delete(1.0, tk.END)
      self.novel_content.insert(1.0, self.novel_manager.novel_content)
      self.novel_content.config(state=tk.DISABLED)

  def save_novel(self):
    if self.novel_manager.loaded_novel_path:
      self.novel_manager.save_novel(self.saving_novel_path.get(), self.encoding_var.get())

  def update_saving_novel_path(self, *_):
    self.novel_manager.loaded_novel_pattern = self.loaded_novel_pattern_var.get()
    self.novel_manager.saving_novel_pattern = self.saving_novel_pattern_var.get()
    self.novel_manager.update_saving_novel_path()
    self.saving_novel_path.delete(0, tk.END)
    self.saving_novel_path.insert(0, self.novel_manager.saving_novel_path)
