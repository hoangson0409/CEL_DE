from typing import List, Tuple

from databases import Database
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import create_engine, select, MetaData, Table, and_
from starlette.responses import FileResponse
import pandas as pd
import sys
sys.path.append("db")

import database
import models
from database import get_database, sqlalchemy_engine
from models import (
    metadata,
    dateticker,
    DateTickerCreate,
    DateTickerDB,
    get_stock_data
)





app = FastAPI()


@app.on_event("startup")
async def startup():
    await get_database().connect()
    models.metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(99999, ge=0),
) -> Tuple[int, int]:
    capped_limit = min(99999, limit)
    return (skip, capped_limit)


async def get_dateticker_or_404(
    id: int, database: Database = Depends(get_database)
) -> models.DateTickerDB:
    select_query = models.dateticker.select().where(models.dateticker.c.id == id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return models.DateTickerDB(**raw_post)

@app.get("/stock")
async def returnTicker(
ticker:str
,database: Database = Depends(get_database)
, pagination: Tuple[int, int] = Depends(pagination),
) -> List[models.DateTickerDB]:

    skip, limit = pagination
    select_query = models.dateticker.select().where(and_(
    models.dateticker.columns.ticker == ticker
    )).offset(skip).limit(limit)
    rows = await database.fetch_all(select_query)
    results = [models.DateTickerDB(**row) for row in rows]
    return results

@app.post("/stock", response_model=models.DateTickerDB, status_code=status.HTTP_201_CREATED)
async def create_post_stock(
    ticker:str,
     database: Database = Depends(get_database)
) -> models.DateTickerDB:
    datetickerpost = get_stock_data(ticker)
    insert_query = models.dateticker.insert().values(datetickerpost)
    datetickerid = await database.execute(insert_query)

    datetickerdb = await get_dateticker_or_404(datetickerid, database)

    return datetickerdb

@app.post("/stockchart",  status_code=status.HTTP_201_CREATED)
async def create_post_stock2(
    ticker:str,
    time_past:int,
     database: Database = Depends(get_database),

) -> List[models.DateTickerDB]:

    delete_query = models.dateticker.delete().where(models.dateticker.columns.ticker == ticker)
    await database.execute(delete_query)

    datetickerpost = get_stock_data(ticker,time_past)
    insert_query = models.dateticker.insert().values(datetickerpost)
    datetickerid = await database.execute(insert_query)

    datetickerdb = await get_dateticker_or_404(datetickerid, database)

    select_query = models.dateticker.select().where(and_(
        models.dateticker.columns.ticker == ticker
    ))
    rows = await database.fetch_all(select_query)
    results = [models.DateTickerDB(**row) for row in rows]

    return results


@app.get("/csv_data")
def get_json_data():
    df = pd.read_csv('simcel.csv')
    df = df.fillna('')
    return df.to_dict(orient="records")


@app.get("/csv_analysis")
async def read_index():
    return FileResponse('celtet.html')




