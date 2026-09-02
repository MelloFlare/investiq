from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse

router = APIRouter(prefix="/portfolios", tags=["portfolios"])

@router.post("", response_model=PortfolioResponse)
def create_portfolio(payload: PortfolioCreate, db: Session = Depends(get_db)):
    portfolio = Portfolio(**payload.model_dump())
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio

@router.get("", response_model=list[PortfolioResponse])
def list_portfolios(db: Session = Depends(get_db)):
    return db.query(Portfolio).all()

@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio(portfolio_id: UUID, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.delete("/{portfolio_id}", status_code=204)
def delete_portfolio(portfolio_id: UUID, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    db.delete(portfolio)
    db.commit()