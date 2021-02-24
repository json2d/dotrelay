# 📡 dotrelay
[![PyPI version](https://badge.fury.io/py/dotrelay.svg)](https://badge.fury.io/py/dotrelay)
[![Build Status](https://travis-ci.com/json2d/dotrelay.svg?branch=master)](https://travis-ci.com/json2d/dotrelay) [![Coverage Status](https://coveralls.io/repos/github/json2d/dotrelay/badge.svg?branch=master)](https://coveralls.io/github/json2d/dotrelay?branch=master)

enhance your module import context with brevity


## Quick install
```bash
pip install dotrelay
```

## Basic usage
out-of-the-box here's how to use `dotrelay` to import a module from an ancestor directory containing a `.relay` file:

```py
import dotrelay

with dotrelay.Radio(__file__): # 📻
  import some_relatively_external_module
```

## Problem

importing [relatively external] modules is hard (in Python)

don't believe? ask this 10+ years of discussion on the internet:
- https://stackoverflow.com/questions/6323860/sibling-package-imports


so forget about importing modules from [outer space/another galaxy]:

```
.
├── andromeda
│   └── ufos.py -- 🛸🛸🛸
└── milky_way
    └── sol
        └── earth
            ├── animals
            │   ├── __init__.py
            │   ├── birds.py
            │   └── fish.py
            ├── lands
            │   ├── __init__.py
            │   └── deserts.py
            └── waters
                ├── __init__.py
                └── oceans.py
```

in order to import `ufos` into `deserts` you'd need this bit of boilerplate:

```py
# deserts.py
import sys
import os

# get directory path containing andromeda (relatively from this module's file path)
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__) ) ) ) ) ) 

sys.path.append(root_path) # extend module import context 
from andromeda import ufos # import that thing we need
sys.path.remove(root_path) # cleanup 

ufos.abduct_cattle(mode='random') # finally the real work can begin

```

commonly referred to as a "`sys.path` hack", this is what we want to avoid. it's fairly low level, fairly ugly, noisy and just plain makes the code smelly 👃🏽



## Solution

so let's make this better - we have the technology

for starters let's create a `.relay` file in the directory containing `andromeda`, the module we want to import into `oceans`

> **_NOTE:_* this `.relay` file must be in one of `oceans` ancestor directories to be discoverable

```
.
├── .relay -- 📡
├── andromeda
│   └── ufos.py -- 🛸🛸🛸
└── milky_way
    └── sol
        └── earth
            ├── animals
            │   ├── __init__.py
            │   ├── birds.py
            │   └── fish.py
            ├── lands
            │   ├── __init__.py
            │   └── deserts.py
            └── waters
                ├── __init__.py
                └── oceans.py
```

now in `oceans` we can use a `dotrelay.Radio` to _discover the `.relay` file above it_ and _establish a kind of temporary bridge_ for us to import `andromeda` and/or other modules in the relay directory

```py
# deserts.py
import dotrelay
with dotrelay.Radio(__file__): # 📻
  from andromeda import ufos

ufos.abduct_cattle(mode='psuedo-random') # yes it happened
```

now this boilerplate is fairly high level, fairly clean, short and sweet

## Common scenarios
fun example aside, lets see how this fits into real world projects
### Testing modules
so here's a typical file structure for most python lib projects where there's the main module and some test modules

```
.
├── pything
│   ├── __init__.py
│   └── main.py
└── tests
    └── units.py
```

in order to test `pything` it needs to be imported into `units`, and you end up with that bloat:

```py
# units.py
import sys
import os
root_path = os.path.dirname( os.path.dirname( path.abspath(__file__) ) ) # the directory that contains pything
sys.path.append(root_path)

import pything

sys.path.remove(root_path) # cleanup

import unittest

# ...
```

an awkward thing to have to include this in every single test module

with `dotrelay` this becomes:

```
.
├── .relay -- 📡
├── pything
│   ├── __init__.py
│   └── main.py
└── tests
    └── units.py
```

and the boilerplate is reduced to:

```py
# tests/units.py
import dotrelay
with dotrelay.Radio(__file__): # 📻
  import pything
```

### Organizing modules

additionally, say `units` were to be moved deeper into the project:

```
.
├── .relay -- 📡
├── pything
│   ├── __init__.py
│   └── main.py
└── tests
    └── basic
        └── units.py
```

with a "`sys.path` hack" the code for getting the `root_path` would need to be updated since again it's relative to the module's own file path

so then overtime, as a project matures, this becomes something that needs to be manage. 

but that can all be avoided with `dotrelay`. no changes need to be made as long as the `.relay` file remains with one of `units` ancestor directories

### Reading static files

sometimes it's also useful just having the path of the relay directory

```
.
├── .relay -- 📡
├── pything
│   ├── __init__.py
│   └── main.py
└── fixtures
│   └── data.json -- 📝
└── tests
    └── units.py
```

so to read `fixtures/data.json` from `units`:

```py
# tests/units.py
import dotrelay
with dotrelay.Radio(__file__) as rad: # 📻
  ROOT_PATH = rad.relay_path

import os, json
DATA_PATH = os.path.join(ROOT_PATH, 'fixtures', 'data.json')
with open(DATA_PATH, 'r') as fp: 
  DATA = json.load(fp)

import unittest
# ...
```

echoing the point from the previous scenario, this works well when you need to move the static files around the project



