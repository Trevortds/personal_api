import datetime
import math
import sys

import pytz
import requests

data = [
    33,
    49,
    61,
    39,
    48,
    55,
    40,
    63,
    52,
    68,
    52,
    41,
    56,
    47,
    46,
    36,
    45,
    35,
    55,
    74,
    45,
    51,
    38,
    83,
    48,
    54,
    46,
    33,
    39,
    41,
    50,
    36,
    40,
    48,
    42,
    47,
    47,
]

start_time = [
    10+14/60,
    10+3/60,
    9+53/60,
    10+10/60,
    10.0,
    9+45/60,
    9+15/60,
    9+55/60,
    9+54/60,
    9+34/60,
    9+6/60,
    9+25/60,
    8+5/6,
    9+52/60,
    9+48/60,
    10+11/60,
    8.5,
    9+48/60,
    10,
    8+47/60,
    9+32/60,
    9+5/60,
    9+11/60,
    10,
    9+39/60,
    8+47/60,
    9+23/60,
    9+53/60,
    8+25/60,
    10+29/60,
    9+10/60,
    9+8/60,
    9+8/60,
    8+37/60,
    9+5/60,
    9+2/60,
    10+7/60,
    ]

if len(data) != len(start_time):
    raise Exception("different lengths!")

print(len(data))

if len(sys.argv) != 2:
    print("please provide server name")
    sys.exit(1)

for start, length in zip(start_time, data):
    print(start, length)
    print((int((start-int(start))*60)))
    start_datetime = datetime.datetime(year=2017, month=10, day=15,
                                       hour=int(start), minute=(int((start-int(start))*60)))
    start_datetime = pytz.timezone("America/New_York").localize(start_datetime)
    end_datetime = start_datetime + datetime.timedelta(seconds=length*60)
    start_datetime = start_datetime.astimezone(tz=pytz.utc)
    end_datetime = end_datetime.astimezone(tz=pytz.utc)
    requests.post(sys.argv[1] + "/api/commute/work/", json={"start_time": start_datetime.isoformat(),
                                                            "arrive_time": end_datetime.isoformat()})

