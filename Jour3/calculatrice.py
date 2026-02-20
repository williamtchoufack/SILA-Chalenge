import tkinter as tk
import math

dark = False
expression = ""
memoire = 0

fenetre = tk.Tk()
fenetre.title("Calculatrice Erudi_X")
fenetre.geometry("320x450")
fenetre.resizable(True, True)
fenetre.configure(bg="#f0f0f0")

for i in range(4):
    fenetre.columnconfigure(i, weight=1)
for i in range(8):
    fenetre.rowconfigure(i, weight=1)

ecran_var = tk.StringVar()
ecran_var.set("0")

ecran = tk.Entry(fenetre, textvariable=ecran_var, font=("Arial", 20), justify="right", state="readonly", bg="white", fg="black", relief="flat", bd=5)
ecran.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10, ipady=12)

result_label = tk.Label(fenetre, text="", font=("Arial", 11), anchor="e", bg="#f0f0f0", fg="gray")
result_label.grid(row=1, column=0, columnspan=4, sticky="ew", padx=15)

theme_btn = tk.Button(fenetre, text="mode sombre", font=("Arial", 10), command=lambda: switch_theme(), relief="flat", bg="white", fg="black", cursor="hand2")
theme_btn.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=3)

btn_c = tk.Button(fenetre, text="C", font=("Arial", 12, "bold"), command=lambda: effacer(), bg="#f44336", fg="white", relief="flat", cursor="hand2")
btn_c.grid(row=2, column=2, sticky="nsew", padx=2, pady=3)

btn_del = tk.Button(fenetre, text="del", font=("Arial", 12, "bold"), command=lambda: supprimer(), bg="white", fg="black", relief="flat", cursor="hand2")
btn_del.grid(row=2, column=3, sticky="nsew", padx=2, pady=3)

btn_mc = tk.Button(fenetre, text="MC", font=("Arial", 12, "bold"), command=lambda: globals().update(memoire=0), bg="white", fg="black", relief="flat", cursor="hand2")
btn_mc.grid(row=3, column=0, sticky="nsew", padx=2, pady=2, ipady=4)

btn_mr = tk.Button(fenetre, text="MR", font=("Arial", 12, "bold"), command=lambda: mem_load(), bg="white", fg="black", relief="flat", cursor="hand2")
btn_mr.grid(row=3, column=1, sticky="nsew", padx=2, pady=2, ipady=4)

btn_ms = tk.Button(fenetre, text="MS", font=("Arial", 12, "bold"), command=lambda: mem_save(), bg="white", fg="black", relief="flat", cursor="hand2")
btn_ms.grid(row=3, column=2, sticky="nsew", padx=2, pady=2, ipady=4)

btn_xy = tk.Button(fenetre, text="x^y", font=("Arial", 12, "bold"), command=lambda: appuyer("**"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_xy.grid(row=3, column=3, sticky="nsew", padx=2, pady=2, ipady=4)

btn_7 = tk.Button(fenetre, text="7", font=("Arial", 13, "bold"), command=lambda: appuyer("7"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_7.grid(row=4, column=0, sticky="nsew", padx=2, pady=2, ipady=6)

btn_8 = tk.Button(fenetre, text="8", font=("Arial", 13, "bold"), command=lambda: appuyer("8"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_8.grid(row=4, column=1, sticky="nsew", padx=2, pady=2, ipady=6)

btn_9 = tk.Button(fenetre, text="9", font=("Arial", 13, "bold"), command=lambda: appuyer("9"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_9.grid(row=4, column=2, sticky="nsew", padx=2, pady=2, ipady=6)

btn_div = tk.Button(fenetre, text="/", font=("Arial", 13, "bold"), command=lambda: appuyer("/"), bg="#e0e0e0", fg="black", relief="flat", cursor="hand2")
btn_div.grid(row=4, column=3, sticky="nsew", padx=2, pady=2, ipady=6)

btn_4 = tk.Button(fenetre, text="4", font=("Arial", 13, "bold"), command=lambda: appuyer("4"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_4.grid(row=5, column=0, sticky="nsew", padx=2, pady=2, ipady=6)

btn_5 = tk.Button(fenetre, text="5", font=("Arial", 13, "bold"), command=lambda: appuyer("5"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_5.grid(row=5, column=1, sticky="nsew", padx=2, pady=2, ipady=6)

btn_6 = tk.Button(fenetre, text="6", font=("Arial", 13, "bold"), command=lambda: appuyer("6"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_6.grid(row=5, column=2, sticky="nsew", padx=2, pady=2, ipady=6)

btn_mul = tk.Button(fenetre, text="*", font=("Arial", 13, "bold"), command=lambda: appuyer("*"), bg="#e0e0e0", fg="black", relief="flat", cursor="hand2")
btn_mul.grid(row=5, column=3, sticky="nsew", padx=2, pady=2, ipady=6)

btn_1 = tk.Button(fenetre, text="1", font=("Arial", 13, "bold"), command=lambda: appuyer("1"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_1.grid(row=6, column=0, sticky="nsew", padx=2, pady=2, ipady=6)

btn_2 = tk.Button(fenetre, text="2", font=("Arial", 13, "bold"), command=lambda: appuyer("2"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_2.grid(row=6, column=1, sticky="nsew", padx=2, pady=2, ipady=6)

btn_3 = tk.Button(fenetre, text="3", font=("Arial", 13, "bold"), command=lambda: appuyer("3"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_3.grid(row=6, column=2, sticky="nsew", padx=2, pady=2, ipady=6)

btn_sub = tk.Button(fenetre, text="-", font=("Arial", 13, "bold"), command=lambda: appuyer("-"), bg="#e0e0e0", fg="black", relief="flat", cursor="hand2")
btn_sub.grid(row=6, column=3, sticky="nsew", padx=2, pady=2, ipady=6)

btn_0 = tk.Button(fenetre, text="0", font=("Arial", 13, "bold"), command=lambda: appuyer("0"), bg="white", fg="black", relief="flat", cursor="hand2")
btn_0.grid(row=7, column=0, sticky="nsew", padx=2, pady=2, ipady=6)

btn_dot = tk.Button(fenetre, text=".", font=("Arial", 13, "bold"), command=lambda: appuyer("."), bg="white", fg="black", relief="flat", cursor="hand2")
btn_dot.grid(row=7, column=1, sticky="nsew", padx=2, pady=2, ipady=6)

btn_egal = tk.Button(fenetre, text="=", font=("Arial", 13, "bold"), command=lambda: egal(), bg="#4CAF50", fg="white", relief="flat", cursor="hand2")
btn_egal.grid(row=7, column=2, sticky="nsew", padx=2, pady=2, ipady=6)

btn_add = tk.Button(fenetre, text="+", font=("Arial", 13, "bold"), command=lambda: appuyer("+"), bg="#e0e0e0", fg="black", relief="flat", cursor="hand2")
btn_add.grid(row=7, column=3, sticky="nsew", padx=2, pady=2, ipady=6)

# Parie ajouter par IA claude

def switch_theme():
    global dark
    dark = not dark
    if dark:
        fenetre.configure(bg="#1e1e1e")
        ecran.config(bg="#2d2d2d", fg="white")
        result_label.config(bg="#1e1e1e")
        theme_btn.config(text="mode clair", bg="#3a3a3a", fg="white")
        btn_mc.config(bg="#3a3a3a", fg="white")
        btn_mr.config(bg="#3a3a3a", fg="white")
        btn_ms.config(bg="#3a3a3a", fg="white")
        btn_xy.config(bg="#3a3a3a", fg="white")
        btn_del.config(bg="#3a3a3a", fg="white")
        btn_7.config(bg="#3a3a3a", fg="white")
        btn_8.config(bg="#3a3a3a", fg="white")
        btn_9.config(bg="#3a3a3a", fg="white")
        btn_div.config(bg="#555555", fg="white")
        btn_4.config(bg="#3a3a3a", fg="white")
        btn_5.config(bg="#3a3a3a", fg="white")
        btn_6.config(bg="#3a3a3a", fg="white")
        btn_mul.config(bg="#555555", fg="white")
        btn_1.config(bg="#3a3a3a", fg="white")
        btn_2.config(bg="#3a3a3a", fg="white")
        btn_3.config(bg="#3a3a3a", fg="white")
        btn_sub.config(bg="#555555", fg="white")
        btn_0.config(bg="#3a3a3a", fg="white")
        btn_dot.config(bg="#3a3a3a", fg="white")
        btn_add.config(bg="#555555", fg="white")
    else:
        fenetre.configure(bg="#f0f0f0")
        ecran.config(bg="white", fg="black")
        result_label.config(bg="#f0f0f0")
        theme_btn.config(text="mode sombre", bg="white", fg="black")
        btn_mc.config(bg="white", fg="black")
        btn_mr.config(bg="white", fg="black")
        btn_ms.config(bg="white", fg="black")
        btn_xy.config(bg="white", fg="black")
        btn_del.config(bg="white", fg="black")
        btn_7.config(bg="white", fg="black")
        btn_8.config(bg="white", fg="black")
        btn_9.config(bg="white", fg="black")
        btn_div.config(bg="#e0e0e0", fg="black")
        btn_4.config(bg="white", fg="black")
        btn_5.config(bg="white", fg="black")
        btn_6.config(bg="white", fg="black")
        btn_mul.config(bg="#e0e0e0", fg="black")
        btn_1.config(bg="white", fg="black")
        btn_2.config(bg="white", fg="black")
        btn_3.config(bg="white", fg="black")
        btn_sub.config(bg="#e0e0e0", fg="black")
        btn_0.config(bg="white", fg="black")
        btn_dot.config(bg="white", fg="black")
        btn_add.config(bg="#e0e0e0", fg="black")

#fin de la partie ajouter par claude IA. c'est beaucoup😭😭😭 NB : Pour faire apparaitre emojie sur windows (win + ;)

def appuyer(val):
    global expression
    expression += str(val)
    ecran_var.set(expression)
    try:
        res = calculer(expression)
        result_label.config(text="= " + str(res))
    except:
        result_label.config(text="")

def effacer():
    global expression
    expression = ""
    ecran_var.set("0")
    result_label.config(text="")

def supprimer():
    global expression
    expression = expression[:-1]
    if expression == "":
        ecran_var.set("0")
    else:
        ecran_var.set(expression)

def calculer(expr):
    expr2 = ""
    i = 0
    while i < len(expr):
        if expr[i:i+2] == "**": 
            expr2 += "**"
            i += 2
        else:
            expr2 += expr[i]
            i += 1

    res = eval(expr2, {"__builtins__": {}}, {
        "math": math,
        "__import__": None
    })
    return res

def egal():
    global expression
    try:
        res = calculer(expression)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        expression = str(res)
        ecran_var.set(expression)
        result_label.config(text="")
    except ZeroDivisionError:
        ecran_var.set("division par 0 !!")
        expression = ""
    except:
        ecran_var.set("erreur")
        expression = ""

def mem_save():
    global memoire
    try:
        memoire = float(eval(expression))
    except:
        pass

def mem_load():
    global expression
    expression += str(int(memoire) if memoire == int(memoire) else memoire)
    ecran_var.set(expression)

fenetre.mainloop()
