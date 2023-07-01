import tuct

try:
    import uasyncio as asyncio
except:
    import asyncio


tuct_object = tuct.Tuct()

asyncio.run(tuct_object.main())
