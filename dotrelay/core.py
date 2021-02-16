import logging
log = logging.getLogger("📡dotrelay")
log.addHandler(logging.NullHandler()) # ignore log messages by defualt

import os
import sys

MAX_DEPTH = 10

def init(path, max_depth=MAX_DEPTH):
  path = os.path.abspath(path)
  mod_path = None
  curr_path = path

  for depth in range(1, max_depth+1):
    curr_path = os.path.dirname(curr_path) # go up to parent path
    relay_file_path = os.path.join(curr_path, '.relay')
    if os.path.exists(relay_file_path):
      log.info(f'depth of {depth} reached - .relay file found in {mod_path} - adding to module import path...')
      mod_path = curr_path
      sys.path.append(mod_path)
      break
    else:
      log.info(f'depth of {depth} reached - .relay file not found in {curr_path} - checking parent path...')

  if not mod_path:    
    log.warn(f'max depth of {depth} reached - .relay file not found in any ancestor paths - no changes were made to module import path.')
