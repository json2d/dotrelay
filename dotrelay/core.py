import logging
log = logging.getLogger("📡dotrelay")
log.addHandler(logging.NullHandler()) # ignore log messages by defualt

import os
import sys

MAX_DEPTH = 10

def init(path, max_depth=MAX_DEPTH):
  relay = Relay(path, max_depth)
  relay.__enter__()
  return relay

# use context manager
class Relay():
  def __init__(self, path, max_depth=MAX_DEPTH):
    self.path = os.path.abspath(path)
    self.max_depth = max_depth
    self.mod_path = None
  
  def __enter__(self):
    curr_path = self.path

    for depth in range(1, self.max_depth+1):
      curr_path = os.path.dirname(curr_path) # go up to parent path
      relay_file_path = os.path.join(curr_path, '.relay')
      if os.path.exists(relay_file_path):
        log.info(f'depth of {depth} reached - .relay file found in {self.mod_path} - adding to module import path...')
        self.mod_path = curr_path
        sys.path.append(self.mod_path)
        break
      else:
        log.info(f'depth of {depth} reached - .relay file not found in {curr_path} - checking parent path...')

    if not self.mod_path:    
      log.warning(f'max depth of {depth} reached - .relay file not found in any ancestor paths - no changes were made to module import path.')
    
    return self

  def __exit__(self, type, value, traceback):
    if self.mod_path:
      log.debug(f'finished relaying {self.mod_path} to {self.path} - removing from module import path...')
      sys.path.remove(self.mod_path)