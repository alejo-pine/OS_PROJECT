import customtkinter as ctk
import math

# Configuración de la ventana principal
root = ctk.CTk()
root.title("Calculadora Científica")
root.geometry("400x600")

# Campo de entrada para mostrar números y resultados
entry_text = ctk.StringVar()
entry = ctk.CTkEntry(root, textvariable=entry_text, width=350, font=("Arial", 20), justify="right")
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

# Variables para el cálculo
current_input = ""
last_result = "0"  # Variable para almacenar el último resultado (ANS)

# Funciones para la calculadora
def on_click(button_value):
    global current_input
    current_input += str(button_value)
    entry_text.set(current_input)

def on_clear():
    global current_input
    current_input = ""
    entry_text.set("")

def on_equal():
    global current_input, last_result
    try:
        result = str(eval(current_input))
        entry_text.set(result)
        current_input = result
        last_result = result  # Almacenar el resultado en ANS
    except:
        entry_text.set("Error")
        current_input = ""

def on_sin():
    global current_input, last_result
    try:
        result = str(math.sin(math.radians(float(current_input))))
        entry_text.set(result)
        current_input = result
        last_result = result  # Almacenar el resultado en ANS
    except:
        entry_text.set("Error")
        current_input = ""

def on_cos():
    global current_input, last_result
    try:
        result = str(math.cos(math.radians(float(current_input))))
        entry_text.set(result)
        current_input = result
        last_result = result  # Almacenar el resultado en ANS
    except:
        entry_text.set("Error")
        current_input = ""

def on_tan():
    global current_input, last_result
    try:
        result = str(math.tan(math.radians(float(current_input))))
        entry_text.set(result)
        current_input = result
        last_result = result  # Almacenar el resultado en ANS
    except:
        entry_text.set("Error")
        current_input = ""

def on_ans():
    global current_input, last_result
    current_input += last_result  # Utilizar el último resultado (ANS)
    entry_text.set(current_input)

def on_10_pow():
    global current_input, last_result
    try:
        result = str(10 ** float(current_input))  # Calcular 10^x
        entry_text.set(result)
        current_input = result
        last_result = result  # Almacenar el resultado en ANS
    except:
        entry_text.set("Error")
        current_input = ""

# Botones científicos ubicados arriba
scientific_buttons = [
    ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2),
    ('log', 2, 0), ('ln', 2, 1), ('sqrt', 2, 2),
    ('^', 3, 0), ('10^x', 3, 1), ('ANS', 3, 2), ('C', 3, 3)
]

# Asignación de funciones a botones científicos
for (text, row, col) in scientific_buttons:
    if text == 'sin':
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=on_sin)
    elif text == 'cos':
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=on_cos)
    elif text == 'tan':
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=on_tan)
    elif text == 'C':
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=on_clear)
    elif text == 'ANS':
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=on_ans)
    elif text == '10^x':
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=on_10_pow)
    else:
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=lambda t=text: on_click(t))
    button.grid(row=row, column=col, padx=5, pady=5)

# Botones numéricos y operadores ubicados abajo
buttons = [
    ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3),
    ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3),
    ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3),
    ('0', 7, 0), ('.', 7, 1), ('+', 7, 2), ('=', 7, 3)
]

# Asignación de funciones a botones numéricos y operadores
for (text, row, col) in buttons:
    if text == '=':
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=on_equal)
    else:
        button = ctk.CTkButton(root, text=text, width=80, height=60, font=("Arial", 20), command=lambda t=text: on_click(t))
    button.grid(row=row, column=col, padx=5, pady=5)

# Iniciar la aplicación
root.mainloop()
