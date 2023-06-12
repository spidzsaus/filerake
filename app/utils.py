from pathlib import Path
import datetime
from random import randint


def filename_format(
    filepath: Path, 
    format: str, 
    timestamp: datetime.datetime = None
):
    '''
    Constructs a new file name according to the given
    format. 
    Supported keywords:
    - `name` - name of the file without the extension
    - `dir` - name of the final dir where source file is located
    - `extension` - file extension
    - `day` - current day
    - `month` - current month
    - `year` - current year
    - `hour` - current hour
    - `minute` - current minute
    - `second` - current second
    - `random` - a random number from 0 to 999999
    '''

    if timestamp is None:
        timestamp = datetime.datetime.now()

    return filepath.parent / (
        format.format(
            name=filepath.stem,
            dir=filepath.parent.name,
            extension=filepath.suffix,
            day=timestamp.day,
            month=timestamp.month,
            year=timestamp.year,
            hour=timestamp.hour,
            minute=timestamp.minute,
            second=timestamp.second,
            random=str(randint(0, 999999))
        ) + filepath.suffix
    )