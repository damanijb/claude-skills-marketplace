# bqapi — Bloomberg Async API Reference

## Overview

bqapi provides async/event-loop based access to Bloomberg data. Available in `bqnt-3` conda env.

## Core Classes

| Class | Description |
|-------|-------------|
| `bqapi.Session` | Main connection to Bloomberg API |
| `bqapi.EventLoop` | Async event loop for concurrent requests |
| `bqapi.TornadoEventLoop` | Tornado-based event loop variant |
| `bqapi.Promise` | Async future for pending responses |
| `bqapi.Subscription` | Market data subscription handle |
| `bqapi.Settings` | API connection settings |
| `bqapi.Format` | Response format configuration |

## Request Types

### Reference Data (bqapi.requests.refdata)
```python
from bqapi.requests import refdata

# BDP equivalent — snapshot reference data
refdata.ReferenceDataRequest(securities=[], fields=[])

# BDH equivalent — historical time series
refdata.HistoricalDataRequest(securities=[], fields=[], start_date='YYYYMMDD', end_date='YYYYMMDD')

# BDIB equivalent — bulk reference data
refdata.BulkReferenceDataRequest(securities=[], fields=[])

# Override fields
refdata.ReferenceDataRequest(
    securities=["AAPL US Equity"],
    fields=["IS_EPS"],
    overrides={"BEST_FPERIOD_OVERRIDE": "1BF"}
)
```

### Market Data (bqapi.requests.mktdata)
```python
from bqapi.requests import mktdata

# Real-time tick data
mktdata.IntradayTickRequest(
    security="AAPL US Equity",
    event_types=["TRADE", "BID", "ASK"],
    start_date_time="2024-01-01T09:30:00",
    end_date_time="2024-01-01T16:00:00"
)

# Intraday bar data
mktdata.IntradayBarRequest(
    security="AAPL US Equity",
    event_type="TRADE",
    interval=1,  # minutes
    start_date_time="2024-01-01T09:30:00",
    end_date_time="2024-01-01T16:00:00"
)
```

### VWAP (bqapi.requests.vwap)
```python
from bqapi.requests import vwap

vwap.VwapRequest(security="AAPL US Equity", date="20240101")
```

### Instruments (bqapi.requests.instruments)
```python
from bqapi.requests import instruments

# Security lookup
instruments.InstrumentListRequest(query="AAPL", max_results=10)
```

## Usage Patterns

### Synchronous (simplest)
```python
import bqapi
from bqapi.requests import refdata

with bqapi.Session() as session:
    req = refdata.ReferenceDataRequest(
        securities=["AAPL US Equity"],
        fields=["PX_LAST", "PE_RATIO", "CUR_MKT_CAP"]
    )
    response = session.send_and_receive(req)
    for security in response.securityData:
        print(security.ticker, security.fieldData)
```

### Async with EventLoop
```python
import bqapi

event_loop = bqapi.EventLoop()

@event_loop.run
async def get_data():
    async with bqapi.Session(event_loop) as session:
        from bqapi.requests import refdata
        req = refdata.ReferenceDataRequest(
            securities=["AAPL US Equity", "MSFT US Equity"],
            fields=["PX_LAST"]
        )
        promise = await session.send(req)   # bqapi.Promise
        response = await promise
        return response

result = get_data()
```

### Formatters
```python
import bqapi

# Convert response to pandas DataFrame
formatter = bqapi.data_frame()
with bqapi.Session() as session:
    req = refdata.ReferenceDataRequest(["AAPL US Equity"], ["PX_LAST", "PE_RATIO"])
    response = session.send_and_receive(req, formatter=formatter)
    df = response  # now a DataFrame

# Dictionary format
formatter = bqapi.dictionary()

# No format (raw Bloomberg message)
formatter = bqapi.no_format()
```

## Local Documentation
```
C:\blp\bqnt\environments\bqnt-3\Doc\html\bqapi\
  index.html               -- full API reference
  services.html            -- request types
  event_loop_integration.html -- async patterns
  formatters.html          -- response formatters
  coroutines.html          -- coroutine patterns
```
