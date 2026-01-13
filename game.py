# Ethical Visual Novel - Interactive Project
# For university assignment on Ethics in Computer Science

ethics = 0
career = 0

def choice_input(options):
    while True:
        choice = input("Διάλεξε: ")
        if choice in options:
            return choice
        else:
            print("Μη έγκυρη επιλογή.")

def chapter1():
    global ethics, career
    print("\nΚΕΦΑΛΑΙΟ 1 – Η Πόλη που Βλέπει")
    print("Το αφεντικό σου ζητά να φτιάξεις σύστημα facial recognition για όλη την πόλη.")
    print("1. Δέχομαι χωρίς αντίρρηση")
    print("2. Εκφράζω ηθικές ανησυχίες")
    print("3. Προτείνω privacy-by-design λύση")

    c = choice_input(["1", "2", "3"])

    if c == "1":
        ethics -= 1
        career += 1
        print("Παίρνεις προαγωγή, αλλά νιώθεις άβολα.")
    elif c == "2":
        ethics += 1
        print("Το αφεντικό ενοχλείται, αλλά νιώθεις σωστός.")
    elif c == "3":
        ethics += 2
        career -= 1
        print("Η λύση σου προστατεύει τους πολίτες αλλά καθυστερεί το project.")

def chapter2():
    global ethics, career
    print("\nΚΕΦΑΛΑΙΟ 2 – Το Ιατρικό AI με Bias")
    print("Το dataset έχει σχεδόν μόνο δεδομένα από λευκούς άντρες.")
    print("1. Συνεχίζω κανονικά")
    print("2. Ζητάω καλύτερα δεδομένα")
    print("3. Προσπαθώ να διορθώσω το bias μόνος μου")

    c = choice_input(["1", "2", "3"])

    if c == "1":
        ethics -= 2
        career += 1
        print("Το σύστημα αποτυγχάνει σε μειονότητες. Άσχημα νέα.")
    elif c == "2":
        ethics += 2
        career -= 1
        print("Καθυστερεί το project αλλά σώζεται ένας ασθενής.")
    elif c == "3":
        ethics += 1
        print("Μερική βελτίωση, αλλά το πρόβλημα παραμένει.")

def chapter3():
    global ethics, career
    print("\nΚΕΦΑΛΑΙΟ 3 – Ο Αλγόριθμος των Social Media")
    print("Σου ζητούν να ενισχύσεις posts που προκαλούν θυμό για περισσότερα clicks.")
    print("1. Βελτιστοποιώ για engagement")
    print("2. Προσπαθώ να κάνω τον αλγόριθμο πιο ουδέτερο")
    print("3. Διαρρέω πληροφορίες ανώνυμα")

    c = choice_input(["1", "2", "3"])

    if c == "1":
        ethics -= 2
        career += 1
        print("Η κοινωνία πολώνεται, αλλά τα metrics εκτοξεύονται.")
    elif c == "2":
        ethics += 1
        career -= 1
        print("Χαμηλότερα κέρδη, αλλά καλύτερο περιβάλλον.")
    elif c == "3":
        ethics += 2
        career -= 2
        print("Ξεκινά έρευνα. Ρισκάρεις σοβαρά.")

def chapter4():
    global ethics, career
    print("\nΚΕΦΑΛΑΙΟ 4 – Smart City, Άνιση Πόλη")
    print("Το σύστημα ευνοεί πλούσιες περιοχές εις βάρος φτωχών.")
    print("1. Δεν επεμβαίνω")
    print("2. Τροποποιώ κρυφά τον αλγόριθμο")
    print("3. Το αναφέρω ανοιχτά στη διοίκηση")

    c = choice_input(["1", "2", "3"])

    if c == "1":
        ethics -= 1
        career += 1
        print("Η πόλη γίνεται πιο άνιση.")
    elif c == "2":
        ethics += 2
        print("Ρισκάρεις, αλλά βοηθάς χιλιάδες ανθρώπους.")
    elif c == "3":
        ethics += 1
        career -= 1
        print("Συγκρούεσαι με τη διοίκηση.")

def chapter5():
    global ethics, career
    print("\nΚΕΦΑΛΑΙΟ 5 – Το Αρχείο")
    print("Έχεις αποδείξεις για σοβαρές παραβιάσεις.")
    print("1. Τα δημοσιοποιώ όλα (whistleblower)")
    print("2. Τα δίνω ανώνυμα σε ΜΚΟ")
    print("3. Παραιτούμαι σιωπηλά")
    print("4. Τα αγνοώ")

    c = choice_input(["1", "2", "3", "4"])

    if c == "1":
        ethics += 3
        career -= 3
        print("Η αλήθεια βγαίνει στο φως. Πληρώνεις τίμημα.")
    elif c == "2":
        ethics += 2
        career -= 1
        print("Η υπόθεση ερευνάται χωρίς να αποκαλυφθείς.")
    elif c == "3":
        ethics += 1
        print("Φεύγεις με ήσυχη συνείδηση.")
    elif c == "4":
        ethics -= 2
        career += 1
        print("Συνεχίζεις τη ζωή σου... αλλά κάτι σε βαραίνει.")

def ending():
    print("\nΤΕΛΙΚΟ ΑΠΟΤΕΛΕΣΜΑ")
    print("Ηθικό σκορ:", ethics)
    print("Καριέρα:", career)

    if ethics >= 6:
        print("\nENDING: Ο Ηθικός Προγραμματιστής")
        print("Έγινες σύμβολο ηθικής. Ενέπνευσες άλλους.")
    elif ethics >= 2:
        print("\nENDING: Ο Ρεαλιστής")
        print("Έκανες συμβιβασμούς αλλά προσπάθησες.")
    elif ethics < 2 and career > 2:
        print("\nENDING: Ο Επιτυχημένος αλλά Κενός")
        print("Ανέβηκες ψηλά... αλλά με κόστος.")
    else:
        print("\nENDING: Burnout")
        print("Το σύστημα σε συνέτριψε. Ξεκινάς από την αρχή.")

def main():
    print("LINES OF CODE, LINES OF CONSCIENCE")
    print("Ένα interactive visual novel για την ηθική στην Πληροφορική")

    chapter1()
    chapter2()
    chapter3()
    chapter4()
    chapter5()
    ending()

main()

