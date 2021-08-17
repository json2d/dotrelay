# Whats next


## NEXT
```py
import dotrelay
dotrelay.init(__file__) # very clean

dotrelay.flush() # 👃 better not though - this could potentially and unintentionally remove a module import path that was already there and should stay there!
```

### why it's safer to flush changes
under-the-hood, changing the module import context with `sys.path.append(special_resolved_path)` has a global effect, meaning it becomes the module import context for all imports that follow, even ones in other files.

in the best cases you just end up polluting the context but everything still works as expected

in the worse cases you create conflicts between modules using the same namespace, potentially causing your app to import the wrong one at runtime


### best of both worlds
so ok the conclusion when it comes to not flushing is sometimes its okay, sometimes its not 

so if you just want brevity and you're feeling lucky you can:
```py
import dotrelay
dotrelay.init(__file__)

import some_module_in_ancestor
```

but if you need to a bit of protection for peace of mind:
```py
import dotrelay
with dotrelay.Radio(__file__): # changes to module import context are temporary
  import some_module_in_ancestor

```

### a strict mode
might want the default behavior to be to raise an exception if `.relay` is not found. makes sense because if relaying fails then the inner code block with the imports from ancestor context won't work

```py
import dotrelay
with dotrelay.Radio(__file__, strict=False): # default is strict=True, so this is if for some reason it doesn't matter if relaying fails, maybe just a warning here
  import some_module_in_ancestor
```

### good names

```py
import dotrelay
with dotrelay.Radio(origin_path=__file__, strict=False) as r:
  import some_module_in_ancestor
  logger.info(f'started in {r.origin_path} and found {r.resolved_path}')  
```

### but really you should call it

a `Receiver` because that's what the `__file__` is, then the `.relay` file conceptually would be the `Radio`

```py
import dotrelay
with dotrelay.Receiver(__file__) as receiver:
  logger.info(f'receiver picked up the relayed path {receiver.relay_path}! 🛰')  
  import some_module_in_relayed_path
```

a runner up more fun name would be `Radio`. also its 3 letters shorter than `Receiver` and has it's own emoji 📻

```py
import dotrelay
with dotrelay.Radio(__file__) as rad:
  logger.info(f'📻 radio picked up the relayed path {rad.relay_path}! 🛰')  
  import some_module_in_relayed_path
  ROOT_PATH = rad.relay_path

# this might be how we get to our static files
with open(os.path.join(ROOT_PATH, 'data', 'space_data.json'), 'r') as fp: SPACE_DATA = json.load(fp)
```

this reads alot better, more self documenting and intuitive

### parameterize the relay filename

`relay_filename` param would be useful maybe for some interesting usecases

```py
from dotrelay import Radio
with Radio(__file__, relay_filename='ROOT.relay') as rad:
  ROOT_PATH = rad.relay_path

with Radio(__file__, '🔥.relay') as rad:
  FIRE_PATH = rad.relay_path  
```

### another real usecase 

besides temporary module context extensions, might be useful just to get the relay path if that dir is special for some reason

```py
import dotrelay
with dotrelay.Radio(__file__) as rad:
  ROOT_PATH = rad.relay_path

```

the relay path might be how we get to our static files

```py
with open(os.path.join(ROOT_PATH, 'data', 'space_data.json'), 'r') as fp: SPACE_DATA = json.load(fp)
```

### top down
lets get crazy and let the `.relay` file specify more paths to extend the mod import path with

```
milky_way/sol/earth
```


```py
# andromeda/ufos.py

import dotrelay

with dotrelay.Radio(__file__):
  from earth import humans

def send_to_earth(agent, mission):
  agent.fly_to_earth()
  agent.disguise_as(humans.random())
  agent.do_mission(mission)

```

does this make the `.relay` file a more appealing a vector for some kind of cyber attack?

also probably doesnt make sense because it conflicts with the idea of a module heirarchy? not sure


> ### Disclaimer 
> The contents of this file is a fairly coherent stream of conscience brainstorm about different direction to take the design of this library, and intended to be documentation with accurate code examples that reflect how you would actually use the library. For that refer to `README.md`
