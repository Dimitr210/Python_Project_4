import os
from google import genai
from tools import (
    get_balance_and_limit,
    update_card_limit,
    transfer_money,
    request_otp_for_action,
    confirm_otp_and_execute
)

client = genai.Client()

# Λίστα με όλα τα διαθέσιμα εργαλεία (συμπεριλαμβανομένου του OTP)
my_tools = [
    get_balance_and_limit,
    update_card_limit,
    transfer_money,
    request_otp_for_action,
    confirm_otp_and_execute
]

def ask_agent(user_prompt: str, user_name: str = "Nikos") -> str:
    """Στέλνει την ερώτηση του χρήστη στον Gemini Agent με ενσωματωμένα Safety Guardrails (OTP)."""
    
    system_instruction = f"""
    Είσαι ένας ψηφιακός βοηθός τράπεζας (Banking Agent).
    Ο τρέχων ταυτοποιημένος χρήστης είναι ο/η: {user_name}.
    
    ΚΑΝΟΝΕΣ ΑΣΦΑΛΕΙΑΣ & ΚΛΗΗΣ ΕΡΓΑΛΕΙΩΝ (SAFETY GUARDRAILS):
    1. ΑΝΑΓΝΩΣΗ (get_balance_and_limit): Εκτελείται ΑΜΕΣΑ χωρίς OTP.
    
    2. ΜΕΤΑΦΟΡΑ ΧΡΗΜΑΤΩΝ (transfer_money):
       - Για ποσά έως και 100€: Εκτέλεσε ΑΜΕΣΑ τη μεταφορά με το `transfer_money`.
       - Για ποσά άνω των 100€ (>100€): ΜΗΝ καλέσεις απευθείας το `transfer_money`. Καάλεσε ΠΡΩΤΑ το `request_otp_for_action` με action_type='transfer' και details_dict={{"recipient": "...", "amount": ...}}. Ενημέρωσε τον χρήστη για τον κωδικό OTP που δημιουργήθηκε.
    
    3. ΑΛΛΑΓΗ ΟΡΙΟΥ ΚΑΡΤΑΣ (update_card_limit):
       - Για νέα όρια έως και 1000€: Εκτέλεσε ΑΜΕΣΑ την αλλαγή με το `update_card_limit`.
       - Για νέα όρια άνω των 1000€ (>1000€): ΜΗΝ καλέσεις απευθείας το `update_card_limit`. Καάλεσε ΠΡΩΤΑ το `request_otp_for_action` με action_type='limit_change' και details_dict={{"new_limit": ...}}. Ενημέρωσε τον χρήστη για τον κωδικό OTP.
    
    4. ΕΠΙΒΕΒΑΙΩΣΗ OTP:
       - Όταν ο χρήστης σου δώσει έναν κωδικό OTP (π.χ. "Ο κωδικός μου είναι 1234"), κάλεσε το εργαλείο `confirm_otp_and_execute` με τον κωδικό που έδωσε.
    
    Απάντησε πάντα με ευγένεια, σαφήνεια και επαγγελματισμό στα ελληνικά.
    """

    try:
        chat = client.chats.create(
            model="gemini-3.8-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=my_tools,
                temperature=0.1
            )
        )
        response = chat.send_message(user_prompt)
        return response.text
    except Exception as e:
        return f"Σφάλμα κατά την επικοινωνία με τον Agent: {str(e)}"