# 📡 dotrelay
[![PyPI version](https://badge.fury.io/py/dotrelay.svg)](https://badge.fury.io/py/dotrelay)
[![Build Status](https://travis-ci.com/json2d/dotrelay.svg?branch=master)](https://travis-ci.com/json2d/dotrelay) [![Coverage Status](https://coveralls.io/repos/github/json2d/dotrelay/badge.svg?branch=master)](https://coveralls.io/github/json2d/dotrelay?branch=master)

enhance your module import context with brevity

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

