from agent import ask_agent

if __name__ == "__main__":
    print("=== ΔΟΚΙΜΗ 1: Μικρή Μεταφορά 50€ (Χωρίς OTP) ===")
    res1 = ask_agent("Μετάφερε 50 ευρώ στη Μαρία.", user_name="Nikos")
    print(f"Agent: {res1}\n")

    print("=== ΔΟΚΙΜΗ 2: Μεγάλη Μεταφορά 300€ (Απαιτεί OTP) ===")
    res2 = ask_agent("Μετάφερε 300 ευρώ στη Μαρία.", user_name="Nikos")
    print(f"Agent: {res2}\n")

    # ΣΗΜΕΙΩΣΗ: Στη Δοκιμή 2 ο Agent θα επιστρέψει τον κωδικό OTP στο κείμενό του.
    # Για τη Δοκιμή 3, προσομοιώνουμε τον χρήστη που διαβάζει τον κωδικό και απαντάει.
    print("=== ΔΟΚΙΜΗ 3: Επιβεβαίωση OTP από τον Χρήστη ===")
    # Ο χρήστης απαντάει δίνοντας τον κωδικό που του ζητήθηκε
    prompt_confirm = input("Πληκτρολόγησε τον κωδικό OTP που σου εμφάνισε ο Agent παραπάνω: ")
    res3 = ask_agent(f"Ο κωδικός επιβεβαίωσης OTP είναι {prompt_confirm}", user_name="Nikos")
    print(f"Agent: {res3}\n")