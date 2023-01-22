
# TreeMaster

Container that handles all communications between the trees and web/frontend.

The container listens on port **1337**

## Msg format

Used by both trees and web request.

```
uint32 seq_nr // Sequence nr
uint32 msg_len // Msg len
byte[msg_len] msg // message, might be empty
```

See `Message.cs` for the structure.

## General flowchart 

![](../doc/tree_master_stateflow.drawio.png)

## Tree connection

Always start with emtpy message with seq 1.

## Web connection

Sends it's request with seq nr 30.
The data is a json object serialized as a utf-8 string.

### Read lightshow

```json
{
	"request_type":"read_lightshow",
	"light_show":{
		    "time":[t0,...,tN],
			"leds":[
				[rgb0,..., rgbN], // first LED
				...,
				[rgb0,..., rgbN] // 14th LED
					]
	}
}
```

### Write lightshow

```json
{
	"request_type":"write_lightshow",
	"light_show":{
		    "time":[t0,...,tN],
			"leds":[
				[rgb0,..., rgbN], // first LED
				...,
				[rgb0,..., rgbN] // 14th LED
					]
	}
}
```

## Hmmmmmmmmmm



