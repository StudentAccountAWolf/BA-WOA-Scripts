import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, ttk
import numpy as np


selected_column = None
transformation = None

def plot_data(df):
    global selected_column, transformation
    if selected_column in df.columns:
        # Überprüfen, ob die Spalte bereits numerische Werte enthält
        if pd.api.types.is_numeric_dtype(df[selected_column]):
            pass
        else:
            df[selected_column] = pd.to_numeric(df[selected_column].str.replace(',', '.'), errors='coerce')

        df['Species_GrowthType'] = df['WOA_Species'] + ' (' + df['WOA_GrowthType'] + ')'

        counts = df.groupby('Species_GrowthType')[selected_column].nunique()

        if transformation == "log10":
            df[selected_column] = np.log10(df[selected_column])
        elif transformation == "sqrt":
            df[selected_column] = np.sqrt(df[selected_column])

        # Ein neues Fenster für das Boxplot erstellen
        fig, ax = plt.subplots()
        sns.boxplot(x='Species_GrowthType', y=selected_column, data=df, showfliers=False, ax=ax)
        sns.stripplot(x='Species_GrowthType', y=selected_column, data=df, color='black', alpha=0.6, jitter=True, ax=ax)

        ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform', pad=15)
        ax.set_xlabel('Species (Growth type)', labelpad=16, fontsize = 12)
        if transformation == 'sqrt':
            ax.set_ylabel(f'Square Root of {selected_column}', labelpad=24, fontsize = 12)
        elif transformation == 'log10':
            ax.set_ylabel(f'Logarithm Base 10 of {selected_column}', labelpad=24, fontsize = 12)
        else:
            ax.set_ylabel(selected_column, labelpad=24, fontsize = 12)

        fig.canvas.manager.set_window_title(f'Boxplot von {selected_column} [transformation = {transformation}] nach Spezies und Wuchsform')  # Set window title to selected column name

        plt.setp(ax.get_xticklabels(), rotation=40, ha='right')  # Horizontal Alignment für Ticklabels einstellen
        fig.set_size_inches(1920/100, 1080/100)
        fig.tight_layout()

        show_column_values('Species_GrowthType', df['Species_GrowthType'].tolist(), selected_column, df[selected_column].tolist())
        plt.show()

    else:
        print("Ungültige Spaltenauswahl.")


# ------------------ Tkinter Funktionen für Auswahl und Ausgabe ------------------ 
def select_column_and_transformation(columns):
    global selected_column, transformation
    root = tk.Tk()
    root.title("Spalten- und Transformationsauswahl")
    root.geometry('450x300')

    def on_confirm():
        global selected_column, transformation
        selected_column = column_selected.get()
        transformation = transformation_selected.get()
        plot_data(df)

    label1 = tk.Label(root, text="Spalte:", font=("Helvetica", 12))
    label1.pack(pady=(20, 10))
    column_selected = ttk.Combobox(root, values=columns, width=60)
    column_selected.pack(pady=10)

    label2 = tk.Label(root, text="Transformation:", font=("Helvetica", 12))
    label2.pack(pady=(20, 10))
    transformation_selected = ttk.Combobox(root, values=["None", "log10", "sqrt"], width=15)
    transformation_selected.pack(pady=10)
    transformation_selected.current(0)

    tk.Button(root, text="Bestätigen", command=on_confirm).pack(pady=10)

    root.mainloop()

def show_column_values(column_name_1, values_1, column_name_2, values_2):
    global transformation
    values_window = tk.Toplevel()  # Ein neues Toplevel-Fenster erstellen
    values_window.title(f"{column_name_2} [transformation = {transformation}]")
    if transformation == None:
        values_window.title("Daten")
    elif transformation == "log10":
        values_window.title("Daten (log10)")
    elif transformation == "sqrt":
        values_window.title("Daten (sqrt)")

    tree = ttk.Treeview(values_window, columns=(column_name_1, column_name_2), show="headings")
    tree.heading(column_name_1, text=column_name_1)
    tree.heading(column_name_2, text=column_name_2)

    for value_1, value_2 in zip(values_1, values_2):
        tree.insert("", "end", values=(value_1, value_2))

    tree.pack(expand=True, fill="both")
    values_window.geometry("800x900")

root = tk.Tk()
root.withdraw()

file_path = r"G:\Bachelorarbeit_Daten\WOA_Datasheet - LeafMeasurements.tsv"

if file_path:
    df = pd.read_csv(file_path, sep='\t')
    all_columns = df.columns.tolist()

    if not all_columns:
        print("Keine Spalten in der Datei gefunden.")
    else:
        select_column_and_transformation(all_columns)

else:
    print("Keine Datei ausgewählt.")