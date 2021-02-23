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
with dotrelay.Relay(__file__): # changes to module import context are temporary
  import some_module_in_ancestor

```

### a strict mode
might want the default behavior to be to raise an exception if `.relay` is not found. makes sense because if relaying fails then the inner code block with the imports from ancestor context won't work

```py
import dotrelay
with dotrelay.Relay(__file__, strict=False): # default is strict=True, so this is if for some reason it doesn't matter if relaying fails, maybe just a warning here
  import some_module_in_ancestor
```

### good names

```py
import dotrelay
with dotrelay.Relay(origin_path=__file__, strict=False) as r:
  import some_module_in_ancestor
  logger.info(f'started in {r.origin_path} and found {r.resolved_path}')  
```

### but really you should call it

a `Receiver` because that what the `__file__` is, then the `.relay` file conceptually would be the `Relay`
> ### Disclaimer 
> The contents of this file is a fairly coherent stream of conscience brainstorm about different direction to take the design of this library, and intended to be documentation with accurate code examples that reflect how you would actually use the library. For that refer to `README.md`
