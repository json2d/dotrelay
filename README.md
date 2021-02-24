# 📡 dotrelay
[![PyPI version](https://badge.fury.io/py/dotrelay.svg)](https://badge.fury.io/py/dotrelay)
[![Build Status](https://travis-ci.com/json2d/dotrelay.svg?branch=master)](https://travis-ci.com/json2d/dotrelay) [![Coverage Status](https://coveralls.io/repos/github/json2d/dotrelay/badge.svg?branch=master)](https://coveralls.io/github/json2d/dotrelay?branch=master)

enhance your module import context with brevity

## Problem

importing modules locally is hard (in Python)

```
.
├── animals
│   ├── __init__.py
│   ├── birds.py
│   ├── fish.py
│   └── wolverines.py
├── lands
│   ├── __init__.py
│   └── deserts.py
└── waters
    ├── __init__.py
    └── oceans.py
```

in order to import `birds` and `fish` into `oceans` you'd need this bit of bloat:

```py
# oceans.py
import sys
from os
root_path = os.path.dirname( os.path.dirname( path.abspath(__file__) ) ) # the dir that contains animals, lands, and waters
sys.path.append(root_path)

from animals import birds, fish # that thing we need

sys.path.remove(root_path) # cleanup
```

[links to stackoverflow questions discussing various ways to best do some kind of imporrt]

so forget about importing modules locally from outer space (in Python)

```
.
├── .relay
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

to import `ufos` into `deserts`

```py
# deserts.py
import sys
from os
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__) ) ) ) ) ) # the dir that contains milky_way and andromeda
sys.path.append(root_path)

from andromeda import ufos # that thing we need

sys.path.remove(root_path) # cleanup

ufos.abduct_cattle(mode='random') # finally the real work can begin

```

## Solution

we can make this better - we have the technology. 

for starters let's create a `.relay` file in the directory containing `andromeda`, the module we want to import into `oceans`

[the `.relay` file also needs to be in one of `oceans` ancestor directories]

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

now in `oceans` we can use a `dotrelay.Radio` to _discover the `.relay` file above it_ and establish a temporary bridge for us to import `andromeda` and/or other modules in the relay directory

```py
# deserts.py
import dotrelay
with dotrelay.Radio(__file__) as rad: # 📻
  from andromeda import ufos

ufos.abduct_cattle(mode='psuedo-random') # yes it happened
```

## Common scenarios

### Testing
fun example aside, here's a typical file structure for most python lib projects, where there's the main module and some test modules

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
from os
root_path = os.path.dirname( os.path.dirname( path.abspath(__file__) ) ) # the dir that contains pything and tests
sys.path.append(root_path)

import pything

sys.path.remove(root_path) # cleanup

import unittest
# ...
```

an awkward thing to have to include this in every test that will be written

### Module Mobility

additionally, if `units.py` were to be moved somewhere the code for getting the `root_path` would need to be updated since its relative to the module's own path

so then overtime, as a project matures, this becomes something you may have to manage. but that can all be avoided.

### Reading static files

sometimes it's also useful just having the path of the relay directory

```
.
├── .relay -- 📡
├── pything
│   ├── __init__.py
│   └── main.py
└── fixtures
│   └── data.json
└── tests
    └── units.py
```

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


## Quick install
```bash
pip install dotrelay
```

## Basic usage

[decent pitch]. Let's dive in.

Out-of-the-box here's how to use `dotrelay` to import a module from an arbitrarily deep ancestor path containing a `.relay` file:

```py
import dotrelay

with dotrelay.begin(__file__):
  import some_module_in_ancestor
  import another_module_in_ancestor

```

## Boilerplate reduction

Here's what this suppose to replaced:

```py
import sys
from os

ancestor_path = os.path.dirname( os.path.dirname( path.abspath(__file__) ) ) # for ancestor path at depth=2
sys.path.append(ancestor_path)

import some_module_in_ancestor
import another_module_in_ancestor

sys.path.remove(ancestor_path)

```

