from OutlookDataPull import OutlookDataPull
from datetime import datetime, timezone
from time import sleep
import asyncio




async def main():
    # write a loop that runs the pullData function every 5 minutes
    outlook = OutlookDataPull()

    for i in range(10):
        start_date = datetime.now(timezone.utc)
        sleep(180)
        await outlook.pullData(start_date)


asyncio.run(main())