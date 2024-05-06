from sympy import *

#créer des caractères sympy
for l in list('abcdefghijklmnopqrstuvwxyz') + ["delta","alpha","beta","gamma","epsilon"]:
    exec(f"{l} = Symbol('{l}')")

