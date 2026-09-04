from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.database import get_db
from app.models.asset import Asset
from app.models.price import Price
from app.services.market_data import get_historical_range, get_asset_info

router = APIRouter(prefix="/assets", tags=["assets"])

VALID_RANGES = {"1M", "3M", "6M", "1Y", "5Y", "MAX"}

@router.get("/{ticker}/history")
def get_histroy(ticker: str, range: str = "1Y", db: Session = Depends(get_db)):
    if range not in VALID_RANGES:
        raise HTTPException(status_code=400, detail=f"range must be one of {VALID_RANGES}")

    asset = db.query(Asset).filter(Asset.ticker == ticker.upper()).first()
    if not asset:
       
        try:
            info = get_asset_info(ticker)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"Unknown ticker: {ticker}")

        asset = Asset(
            ticker=info.get("symbol", ticker.upper()),
            name=info.get("instrument_name", ticker.upper()),
            asset_type=info.get("instrument_type"),
            sector=info.get("sector"),
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)

        try:
           raw = get_historical_range(ticker, range)
        except ValueError as e:
           raise HTTPException(status_code=502, detail=str(e))

        for row in raw:
            stmt = insert(Price).values(
               asset_id=asset.id,
               date=row["datetime"],
               open=row.get("open"),
               high=row.get("high"),
               low=row.get("low"),
               close=row.get("close"),
               volume=row.get("volume"),
            ).on_conflict_do_nothing(index_elements=["asset_id", "date"])
            db.execute(stmt)
        db.commit()

        prices = (
           db.query(Price)
           .filter(Price.asset_id == asset.id)
           .order_by(Price.date.asc())
           .all()
        )
        return [{"date": p.date, "close": float(p.close)} for p in prices]