# Lightshow

Definition of a lightshow json file, that describes a *light-show* than can be exectuted.
Should make it possible to *design* a lightshow in another software and then uplooad to the tree.

## Lightshow format

The tree can run a *light-show* that is defined as 

```json
// T = Nr of time steps
// N = Nr of leds
light_show_obj = {
    time:float[T],
    leds:led_tuple[N,T]
}

led_tuple = (
    intensity:int,
    red:int,
    green:int,
    blue:int
)
```