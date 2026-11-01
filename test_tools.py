from database import engine, Base, SessionLocal, AccountModel
from tools import get_balance_and_limit, update_card_limit, transfer_money

def init_db():
    """Δημιουργεί τους πίνακες και προσθέτει αρχικούς δοκιμαστικούς λογαριασμούς."""
    # Δημιουργία όλων των πινάκων στη βάση (αν δεν υπάρχουν)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Έλεγχος αν υπάρχουν ήδη λογαριασμοί
    if db.query(AccountModel).count() == 0:
        acc1 = AccountModel(owner="Nikos", balance=1500.0, card_limit=500.0)
        acc2 = AccountModel(owner="Maria", balance=300.0, card_limit=300.0)
        db.add(acc1)
        db.add(acc2)
        db.commit()
        print("✅ Δημιουργήθηκαν οι δοκιμαστικοί λογαριασμοί: Nikos (€1500) & Maria (€300)")
    db.close()

if __name__ == "__main__":
    init_db()
    
    print("\n--- 1. Δοκιμή get_balance_and_limit ---")
    print(get_balance_and_limit("Nikos"))
    
    print("\n--- 2. Δοκιμή update_card_limit ---")
    print(update_card_limit("Nikos", 1000.0))
    
    print("\n--- 3. Δοκιμή transfer_money ---")
    print(transfer_money("Nikos", "Maria", 200.0))
    
    print("\n--- 4. Τελικό Υπόλοιπο Maria ---")
    print(get_balance_and_limit("Maria"))