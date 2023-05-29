# TUCT 2k22

*The Ultimate Cristmas Tree*

## Components

* `firmware` - Pico-W Running Micro-Python on the Tree-PCB
* `web` - Blazor-Container in cloud handling the interactions with the user


## Donwload to PICO

Only download the contents of the *firmware* folder!


# Website-Tree Protocoll

This section will describe the general protocoll between the website and tree.

The website makes HTTP Post request to the tree through the client browser, for now it will be assumed that the IP-address of the tree is known and that the user is on the same wifi as the tree.

The protocoll is based on JSON and the website sends a json-object through a HTTP request, the following requests are to be implemented on the pico.


## Retrive Current active lightshow
Request from website
```json
{
    "request":"get active LS"
}
```

Response from tree

```json
{
    "time":[0.0,...,4.0],
    "leds":[
        [[255,0,0],...,[255,1,1]],
        ...,
        [[255,0,0],...,[255,1,1]]
    ]
}
```

## Set custom lightshow

Request from website
```json
{
    "request":"set custom LS",
    "lightshow":lightshow_obj
}
```

Response from tree, if the LS is valid

```json
{
    "lightshow_valid": "OK"
}
```
