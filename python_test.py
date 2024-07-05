import pandas as pd

dt = '9999-12-31 00:00:00'

try:
    dt = pd.to_datetime(dt)
except pd.errors.OutOfBoundsDatetime:
    dt = pd.to_datetime('2262-01-02')

print(dt)