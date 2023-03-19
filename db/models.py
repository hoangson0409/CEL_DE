from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field

import yfinance as yf
from datetime import datetime,timedelta





class DateTickerBase(BaseModel):
    date: datetime
    ticker: str
    close: float



class DateTickerCreate(DateTickerBase):
    pass


class DateTickerDB(DateTickerBase):
    id: int

metadata = sqlalchemy.MetaData()



dateticker = sqlalchemy.Table(
    "dateticker",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("date", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("ticker", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("close", sqlalchemy.Float(), nullable=False),
)


def get_stock_data(ticker
                   ,start_date = (datetime.now() +  timedelta(days=-20)).strftime('%Y-%m-%d')
                  ,end_date = datetime.now().strftime('%Y-%m-%d')):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    data = data.reset_index()
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    data['Ticker'] = ticker
    data = data[['Date','Ticker','Close']]
    data.columns = ['date','ticker','close']
    data_json = data.to_dict('records')
    return data_json
