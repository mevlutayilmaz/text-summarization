from PyQt5 import uic

with open("Gui.py","w",encoding="utf-8") as fout:
    uic.compileUi("untitled.ui",fout)