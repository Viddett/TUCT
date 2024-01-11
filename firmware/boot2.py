import tuct

try:
    import uasyncio as asyncio
except:
    import asyncio


if __name__ == '__main__':
    tuct_object = tuct.Tuct()
    asyncio.run(tuct_object.main())
