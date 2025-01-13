import os
import re

from config import ENCODINGS, LOADED_NOVEL_PATTERN, SAVING_NOVEL_PATTERN

class NovelManager:
  def __init__(self):
    self.novel_content = ''
    self.loaded_novel_path = ''
    self.saving_novel_path = ''
    self.loaded_novel_pattern = LOADED_NOVEL_PATTERN
    self.saving_novel_pattern = SAVING_NOVEL_PATTERN

  def load_novel(self, file_path):
    self.loaded_novel_path = file_path
    with open(file_path, 'rb') as f:
      raw_data = f.read()
      encoding = self.detect_encoding(raw_data)
      self.novel_content = raw_data.decode(encoding)

  def detect_encoding(self, raw_data):
    for enc in ENCODINGS:
      try:
        raw_data.decode(enc)
        return enc
      except UnicodeDecodeError:
        continue
    return 'utf-8'

  def save_novel(self, file_path, encoding='utf-8'):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding=encoding) as f:
      f.write(self.novel_content)

  def update_saving_novel_path(self):
    loaded_novel_regex_pattern = re.compile(re.sub(r'(<.+?>)', r'(?P\1.+?)', re.escape(self.loaded_novel_pattern)))
    match = loaded_novel_regex_pattern.search(self.loaded_novel_path)
    self.saving_novel_path = self.saving_novel_pattern
    if match:
      for key, value in match.groupdict().items():
        self.saving_novel_path = re.sub(f'<{key}>', value, self.saving_novel_path)
