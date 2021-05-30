# Whats next


## NEXT
```py
import dotrelay
dotrelay.init(__file__) # very clean

dotrelay.flush() # 👃 better not though - this could potentially and unintentionally remove a module import path that was already there and should stay there!
```

### why it's safer to flush changes
under-the-hood, changing the module import context with `sys.path.append(special_mod_path)` has a global effect, meaning it becomes the module import context for all imports that follow, even ones in other files.

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

> ### Disclaimer 
> The contents of this file is a fairly coherent stream of conscience brainstorm about different direction to take the design of this library, and intended to be documentation with accurate code examples that reflect how you would actually use the library. For that refer to `README.md`
