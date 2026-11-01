from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./bank.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class AccountModel(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)
    balance = Column(Float, default=0.0)
    card_limit = Column(Float, default=500.0)  # Όριο κάρτας για Project 4


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, index=True)
    type = Column(String)  # 'deposit', 'withdraw', 'transfer', 'limit_change'
    amount = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    Base.metadata.create_all(bind=engine) 
class PendingTransactionModel(Base):
    __tablename__ = "pending_transactions"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)
    action_type = Column(String)  # 'transfer' ή 'limit_change'
    details = Column(String)      # JSON string με τις λεπτομέρειες (π.χ. recipient, amount)
    otp_code = Column(String)     # 4ψήφιος κωδικός επιβεβαίωσης
    status = Column(String, default="PENDING")  # 'PENDING', 'COMPLETED', 'EXPIRED'
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))