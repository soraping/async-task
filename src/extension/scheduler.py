#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/7 16:40
# @Name    : scheduler.py
# @email   : 541251250@qq.com
# @Author  : caoping
# 定时任务

from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

if __name__ == '__main__':
    import asyncio


    async def job1():
        print(123)


    async def job2():
        print(456)


    scheduler.add_job(
        job1,
        'interval', seconds=5
    )
    scheduler.start()


    # https://github.com/agronholm/apscheduler/issues/660
    # async def main():
    #     pass
    #
    #
    # asyncio.run(main())

    asyncio.get_event_loop().run_forever()
