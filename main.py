import functions

print("███████████████████████████████")
print("█ 1. Convert BMM to VMD       █")
print("█ 2. Convert BMD to PMX (WIP) █")
print("███████████████████████████████")

user_choice = input("")
if user_choice == "1":
    functions.convBMM()
elif user_choice == "2":
    dj = input("Dump JSON (Y/N)? ")
    if dj == "Y":
        functions.convBMD(True)
    else:
        functions.convBMD()