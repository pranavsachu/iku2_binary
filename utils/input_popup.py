from tkinter.simpledialog import askstring

def prompt_for_letter():
    letter = askstring("Input", "Enter the letter/number for this gesture:")
    return letter
