import pandas as pd
from tkinter import *

churras = {
    "Nome": [],
    "Dieta": [],
    "Alcool": []
}
dicvar = {}
valores = {
    "carne": [14],
    "veg": [10],
    "alc": [9],
    "refri": [6]
}


def nome_check():
    lista = button_group1.grid_slaves()
    for item in lista:
        item.destroy()
    lista = button_group2.grid_slaves()
    for item in lista:
        item.destroy()
    global churras, dicvar
    churras = {
        "Nome": [],
        "Dieta": [],
        "Alcool": []
    }
    churras = pd.DataFrame(churras)
    churras["Nome"] = cvd.get().replace(" e ", ",").title().split(",")
    dicvar = {}
    for n in range(len(churras["Nome"])):
        dicvar["varc%s" % str(n)] = BooleanVar(janela)
        checks = Checkbutton(button_group1, text=churras["Nome"][n], font="Ivy 10", variable=dicvar["varc%s" % str(n)],
                             bg="#FF5959")
        checks.grid(row=n % 8, column=int(n/8), sticky=W, padx=10)

        dicvar["varb%s" % str(n)] = BooleanVar(janela)
        checks1 = Checkbutton(button_group2, text=churras["Nome"][n], font="Ivy 10", variable=dicvar["varb%s" % str(n)],
                              bg="#9DFF59")
        checks1.grid(row=n % 8, column=int(n/8), sticky=W, padx=10)
    scroll1()


def scroll1():
    barra1 = Scrollbar(button_group1, orient="horizontal", command=button_group1.xview)
    barra1.grid(row=8, column=0)
    button_group1.configure(xscrollcommand=barra1.set,
                            scrollregion=(0, 0, button_group1.winfo_width(), button_group1.winfo_height()))
    barra2 = Scrollbar(button_group2, orient="horizontal", command=button_group2.xview)
    barra2.grid(row=8, column=0)
    button_group2.configure(xscrollcommand=barra2.set,
                            scrollregion=(0, 0, button_group2.winfo_width(), button_group2.winfo_height()))


def calc_final():
    if churras["Nome"] == []:
        return
    lista = button_group3.grid_slaves()
    for item in lista:
        item.destroy()
    for n in range(len(churras["Dieta"])):
        churras.loc[n, "Dieta"] = dicvar["varc%s" % str(n)].get()
        churras.loc[n, "Alcool"] = dicvar["varb%s" % str(n)].get()
        if churras["Dieta"].loc[int(n)]:
            churras["Dieta"].loc[int(n)] = valores["carne"][0]
        else:
            churras["Dieta"].loc[int(n)] = valores["veg"][0]
    for n in range(len(churras["Alcool"])):
        if churras["Alcool"].loc[int(n)]:
            churras["Alcool"].loc[int(n)] = valores["alc"][0]
        else:
            churras["Alcool"].loc[int(n)] = valores["refri"][0]

    for n in range(len(churras["Nome"])):
        x = int(churras["Dieta"].loc[int(n)]) + int(churras["Alcool"].loc[int(n)])
        s_parc = Label(button_group3, text="%s deve pagar %d reais." % (churras["Nome"][n], x),
                       font="Ivy 8", bg="#FAFF59")
        s_parc.grid(row=n % 3, column=int(n/3), sticky=W, padx=10)
    tot = churras["Alcool"].sum()+churras["Dieta"].sum()
    s_tot.config(text="O total a arrecadar é: %d reais." % tot)
    scroll2()


def scroll2():
    barra3 = Scrollbar(button_group3, orient="horizontal", command=button_group3.xview)
    barra3.grid(row=4, column=0)
    button_group3.configure(yscrollcommand=barra3.set,
                            scrollregion=(0, 0, button_group3.winfo_width(), button_group3.winfo_height()))


def export_buttom():
    if churras["Nome"] == []:
        janela2 = Toplevel(bg="white")
        janela2.title("Exportar arquivo")
        janela2.geometry("350x115+380+160")
        janela2.focus()
        label_nome = Label(janela2, text="Não há nada a ser exportado.\n Primeiro, calcule os valores.",
                           font="Ivy 14 italic", bg="white")
        label_nome.place(relx=0.15, rely=0.25)
        return
    janela2 = Toplevel()
    janela2.title("Exportar arquivo")
    janela2.focus()
    label_nome = Label(janela2, text="Qual nome do arquivo?")
    label_nome.grid(row=0, column=0)
    entry_var = StringVar()
    entry_nome = Entry(janela2, width=50, textvariable=entry_var)
    entry_nome.grid(row=0, column=1, columnspan=2)
    entry_nome.focus()
    entry_nome.bind("<Return>", lambda x: save_and_close(entry_var.get(), janela2))
    botao_export = Button(janela2, text="Exportar",
                          command=lambda: save_and_close(entry_var.get(), janela2))
    botao_export.grid(row=1, column=1, sticky=E)
    botao_voltar = Button(janela2, text="Cancelar", command=janela2.destroy)
    botao_voltar.grid(row=1, column=2, sticky=W)


def save_and_close(nome, window):
    churras.to_csv("%s.csv" % nome, sep='\t', encoding='utf-8')
    window.destroy()


def config_screen():
    janela3 = Toplevel(width=200, height=100, bg="white")
    janela3.title("Mudar Parâmetros")
    janela3.focus()
    chng1 = Label(janela3, text="Valor com Carne:", bg="white")
    chng1.place(relx=0.15, y=10)
    v = IntVar()
    v.set(valores["carne"][0])
    modent1 = Spinbox(janela3, width=4, from_=0, to=200, textvariable=v,
                      command=lambda: editor_valores(v.get(), v2.get(), v3.get(), v4.get()))
    modent1.place(relx=0.65, y=10)
    chng2 = Label(janela3, text="Valor sem Carne:", bg="white")
    chng2.place(relx=0.15, y=30)
    v2 = IntVar()
    v2.set(valores["veg"][0])
    modent2 = Spinbox(janela3, width=4, from_=0, to=200, textvariable=v2,
                      command=lambda: editor_valores(v.get(), v2.get(), v3.get(), v4.get()))
    modent2.place(relx=0.65, y=30)
    chng3 = Label(janela3, text="Valor com Alcool:", bg="white")
    chng3.place(relx=0.15, y=50)
    v3 = IntVar()
    v3.set(valores["alc"][0])
    modent3 = Spinbox(janela3, width=4, from_=0, to=200, textvariable=v3,
                      command=lambda: editor_valores(v.get(), v2.get(), v3.get(), v4.get()))
    modent3.place(relx=0.65, y=50)
    chng4 = Label(janela3, text="Valor sem Alcool:", bg="white")
    chng4.place(relx=0.15, y=70)
    v4 = IntVar()
    v4.set(valores["refri"][0])
    modent4 = Spinbox(janela3, width=4, from_=0, to=200, textvariable=v4,
                      command=lambda: editor_valores(v.get(), v2.get(), v3.get(), v4.get()))
    modent4.place(relx=0.65, y=70)


def editor_valores(v, v2, v3, v4):
    valores["carne"][0] = v
    valores["veg"][0] = v2
    valores["alc"][0] = v3
    valores["refri"][0] = v4
    if not churras["Nome"] == []:
        calc_final()


# Criando a janela
janela = Tk()
janela.resizable(False, False)
janela.title("Calculadora de churrasco")
janela.geometry("550x515+300+60")
janela.configure(bg='white')
janela.iconphoto(False, PhotoImage(file='icon.png'))

# Frame 1 - Convidados
data_entry = Frame(janela, width=550, height=50, bg="#33FFE3")
data_entry.grid(row=0, column=0, columnspan=2)

conv = Label(data_entry, text="Quem vai no churrasco?", font="Ivy 14 italic", bg="#33FFE3")
conv.place(x=10, y=12)

cvd = StringVar()
cvd.set(" Insira aqui os nomes dos convidados")
cvd2 = Entry(data_entry, width=44, textvariable=cvd)
cvd2.bind("<Return>", lambda x: nome_check())
cvd2.place(x=240, y=18)
cvd2.focus()

icon2 = PhotoImage(file='engrenagem.png')
config_but = Button(data_entry,text="click", image=icon2, bg="#33FFE3", relief="flat", activebackground="#33FFE3",
                    command=config_screen)
config_but.place(x=510, y=9)

# Frame 2 - Quem vai comer carne
select = Frame(janela, width=275, height=300, bg="#FF5959")
select.grid(row=1, column=0)

carn = Label(select, text="Quem vai comer carne?", font="Ivy 14 italic", bg="#FF5959")
carn.place(x=10, y=12)

button_group1 = Canvas(select, width=271, height=236, bg="#FF5959", highlightthickness=0)
button_group1.place(relx=0, rely=0.2)

# Frame 3 - Quem vai beber alcool
beb = Frame(janela, width=275, height=300, bg="#9DFF59")
beb.grid(row=1, column=1)

alc = Label(beb, text="Quem vai beber alcool?", font="Ivy 14 italic", bg="#9DFF59")
alc.place(x=10, y=12)

button_group2 = Canvas(beb, width=271, height=236, bg="#9DFF59", highlightthickness=0)
button_group2.place(relx=0, rely=0.2)

Calc = Button(beb, text="Calcular", command=calc_final, bg="white", relief="raised")
Calc.place(relx=0.8, rely=0.9)

# Frame 4 - Resultado
result = Frame(janela, width=550, height=165, bg="#FAFF59")
result.grid(row=2, column=0, columnspan=2)

res1 = Label(result, text="Pagamento individual:", font="Ivy 14 italic", bg="#FAFF59")
res1.place(x=10, y=12)

s_tot = Label(result, text="O total a arrecadar é: 0 reais.", font="Ivy 14 italic", bg="#FAFF59")
s_tot.place(relx=0.018, rely=0.8)

export = Button(result, text="Exportar", command=export_buttom, bg="white", relief="raised")
export.place(x=493, y=137)

button_group3 = Canvas(result, width=546, height=86, bg="#FAFF59", highlightthickness=0)
button_group3.place(relx=0, rely=0.28)

janela.mainloop()
