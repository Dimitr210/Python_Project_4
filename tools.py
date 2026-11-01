from database import SessionLocal, AccountModel, TransactionModel

def get_balance_and_limit(owner_name: str) -> dict:
    """Επιστρέφει το υπόλοιπο και το όριο κάρτας ενός χρήστη."""
    db = SessionLocal()
    account = db.query(AccountModel).filter(AccountModel.owner == owner_name).first()
    db.close()
    
    if not account:
        return {"error": f"Ο λογαριασμός για τον/την {owner_name} δεν βρέθηκε."}
    
    return {
        "owner": account.owner,
        "balance": account.balance,
        "card_limit": account.card_limit
    }
def update_card_limit(owner_name: str, new_limit: float) -> dict:
    """Ενημερώνει το ημερήσιο όριο κάρτας του χρήστη."""
    if new_limit < 0:
        return {"error": "Το όριο κάρτας δεν μπορεί να είναι αρνητικό."}
        
    db = SessionLocal()
    account = db.query(AccountModel).filter(AccountModel.owner == owner_name).first()
    
    if not account:
        db.close()
        return {"error": f"Ο λογαριασμός για τον/την {owner_name} δεν βρέθηκε."}
    
    # Ενημέρωση ορίου
    old_limit = account.card_limit
    account.card_limit = new_limit
    
    # Καταγραφή της κίνησης στο ιστορικό
    transaction = TransactionModel(
        account_id=account.id,
        type="limit_change",
        amount=new_limit
    )
    db.add(transaction)
    
    db.commit()
    db.refresh(account)
    db.close()
    
    return {
        "success": True,
        "owner": account.owner,
        "old_limit": old_limit,
        "new_limit": account.card_limit,
        "message": f"Το όριο κάρτας ενημερώθηκε επιτυχώς σε {new_limit}€."
    }
def update_card_limit(owner_name: str, new_limit: float) -> dict:
    """Ενημερώνει το ημερήσιο όριο κάρτας του χρήστη."""
    if new_limit < 0:
        return {"error": "Το όριο κάρτας δεν μπορεί να είναι αρνητικό."}
        
    db = SessionLocal()
    account = db.query(AccountModel).filter(AccountModel.owner == owner_name).first()
    
    if not account:
        db.close()
        return {"error": f"Ο λογαριασμός για τον/την {owner_name} δεν βρέθηκε."}
    
    # Ενημέρωση ορίου
    old_limit = account.card_limit
    account.card_limit = new_limit
    
    # Καταγραφή της κίνησης στο ιστορικό
    transaction = TransactionModel(
        account_id=account.id,
        type="limit_change",
        amount=new_limit
    )
    db.add(transaction)
    
    db.commit()
    
    # 1. Αποθηκεύουμε πρώτα τα δεδομένα που θέλουμε σε μεταβλητές
    updated_owner = account.owner
    updated_limit = account.card_limit
    
    # 2. Τώρα κλείνουμε τη βάση με ασφάλεια
    db.close()
    
    return {
        "success": True,
        "owner": account.owner,
        "old_limit": old_limit,
        "new_limit": account.card_limit,
        "message": f"Το όριο κάρτας ενημερώθηκε επιτυχώς σε {new_limit}€."
    }
def transfer_money(sender_name: str, recipient_name: str, amount: float) -> dict:
    """Μεταφέρει ένα χρηματικό ποσό από τον ένα λογαριασμό στον άλλο."""
    if amount <= 0:
        return {"error": "Το ποσό μεταφοράς πρέπει να είναι θετικό."}
        
    db = SessionLocal()
    
    sender = db.query(AccountModel).filter(AccountModel.owner == sender_name).first()
    recipient = db.query(AccountModel).filter(AccountModel.owner == recipient_name).first()
    
    if not sender:
        db.close()
        return {"error": f"Ο λογαριασμός αποστολέα ({sender_name}) δεν βρέθηκε."}
    if not recipient:
        db.close()
        return {"error": f"Ο λογαριασμός παραλήπτη ({recipient_name}) δεν βρέθηκε."}
        
    if sender.balance < amount:
        db.close()
        return {"error": f"Ανεπαρκές υπόλοιπο. Διαθέσιμο υπόλοιπο: {sender.balance}€."}
        
   # Εκτέλεση Μεταφοράς
    sender.balance -= amount
    recipient.balance += amount
    
    # Καταγραφή κινήσεων στο ιστορικό
    tx_sender = TransactionModel(account_id=sender.id, type="transfer_out", amount=amount)
    tx_recipient = TransactionModel(account_id=recipient.id, type="transfer_in", amount=amount)
    
    db.add(tx_sender)
    db.add(tx_recipient)
    
    db.commit()
    
    # Αποθήκευση τιμών πριν το db.close()
    sender_owner = sender.owner
    recipient_owner = recipient.owner
    new_sender_bal = sender.balance
    
    db.close()
    
    return {
        "success": True,
        "sender": sender_owner,
        "recipient": recipient_owner,
        "amount": amount,
        "new_sender_balance": new_sender_bal,
        "message": f"Η μεταφορά {amount}€ από {sender_owner} προς {recipient_owner} ολοκληρώθηκε."
    }
import json
import random
from database import PendingTransactionModel

def request_otp_for_action(owner_name: str, action_type: str, details_dict: dict) -> dict:
    """Δημιουργεί έναν κωδικό OTP και καταγράφει μια εκκρεμή συναλλαγή."""
    otp = str(random.randint(1000, 9999))
    db = SessionLocal()
    
    pending_tx = PendingTransactionModel(
        owner=owner_name,
        action_type=action_type,
        details=json.dumps(details_dict),
        otp_code=otp,
        status="PENDING"
    )
    db.add(pending_tx)
    db.commit()
    db.close()
    
    return {
        "status": "REQUIRES_OTP",
        "message": f"Η ενέργεια ({action_type}) είναι υψηλού ρίσκου και απαιτεί επιβεβαίωση OTP.",
        "otp_code": otp,  # Στην πράξη στέλνεται με SMS/email - εδώ τον εμφανίζουμε για τη δοκιμή
        "instructions": f"Παρακαλώ εισάγετε τον κωδικό OTP ({otp}) για να ολοκληρωθεί η συναλλαγή."
    }

def confirm_otp_and_execute(owner_name: str, otp_code: str) -> dict:
    """Επαληθεύει τον κωδικό OTP και εκτελεί την εκκρεμή συναλλαγή."""
    db = SessionLocal()
    
    pending_tx = db.query(PendingTransactionModel).filter(
        PendingTransactionModel.owner == owner_name,
        PendingTransactionModel.otp_code == otp_code,
        PendingTransactionModel.status == "PENDING"
    ).first()
    
    if not pending_tx:
        db.close()
        return {"error": "Μη έγκυρος ή ληγμένος κωδικός OTP."}
    
    # Ανάκτηση λεπτομερειών της συναλλαγής
    details = json.loads(pending_tx.details)
    action_type = pending_tx.action_type
    
    # Σημείωση ως ολοκληρωμένη
    pending_tx.status = "COMPLETED"
    db.commit()
    db.close()
    
    # Εκτέλεση της πραγματικής ενέργειας
    if action_type == "transfer":
        return transfer_money(
            sender_name=owner_name,
            recipient_name=details["recipient"],
            amount=details["amount"]
        )
    elif action_type == "limit_change":
        return update_card_limit(
            owner_name=owner_name,
            new_limit=details["new_limit"]
        )
    else:
        return {"error": "Άγνωστος τύπος ενέργειας."}