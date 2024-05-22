import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, ttk
import numpy as np

# ------------------ Tkinter Funktionen für Auswahl und Ausgabe ------------------ 
# FENSTER 1:    Auswahl der zu untersuchenden Spalten und Transformation in Auswahlfenster
def select_column_and_transformation(columns):
    def on_confirm(): # Beim bestätigen passiert...:
        global selected_column, transformation
        selected_column = column_selected.get()
        transformation = transformation_selected.get()
        root.quit()

    root = tk.Tk()
    root.title("Spalten- und Transformationsauswahl")
    root.geometry('450x300')   # Fenster skalieren

    # Spaltenauswahl
    label1 = tk.Label(root, text="Spalte:", font=("Helvetica", 12))
    label1.pack(pady=(20, 10))
    column_selected = ttk.Combobox(root, values=columns, width=60)     # Dropdown Menü für Spalten
    column_selected.pack(pady=10)
    # Transformationsauswahl
    label2 = tk.Label(root, text="Transformation:", font=("Helvetica", 12))
    label2.pack(pady=(20, 10))
    transformation_selected = ttk.Combobox(root, values=["None", "log10", "sqrt"], width=15)   # Dropdown Menü für Transformationen
    transformation_selected.pack(pady=10)
    transformation_selected.current(0)  # Standardwert = None

    tk.Button(root, text="Bestätigen", command=on_confirm).pack(pady=10)

    root.mainloop()

# FENSTER 2:    Anzeigen der Spaltenwerte in einem separaten Fenster
def show_column_values(column_name_1, values_1, column_name_2, values_2):
    values_window = tk.Toplevel()
    values_window.title("Spaltenwerte")

    tree = ttk.Treeview(values_window, columns=(column_name_1, column_name_2), show="headings")
    tree.heading(column_name_1, text=column_name_1)
    tree.heading(column_name_2, text=column_name_2)

    for value_1, value_2 in zip(values_1, values_2):
        tree.insert("", "end", values=(value_1, value_2))

    tree.pack(expand=True, fill="both")
    values_window.geometry("800x900")   # Fenster skalieren

# Datei-Auswahl-Dialog erstellen (Tkinter Initialisierung)
root = tk.Tk()
root.withdraw()

#file_path = filedialog.askopenfilename(title="Wähle eine TSV-Datei", filetypes=[("TSV-Dateien", "*.tsv")])
file_path = r"G:\Bachelorarbeit_Daten\WOA_Datasheet - LeafMeasurements.tsv"


# Konfiguration des Boxplots
if file_path:
    df = pd.read_csv(file_path, sep='\t')
    all_columns = df.columns.tolist()

    if not all_columns:
        print("Keine Spalten in der Datei gefunden.")
    else:
        selected_column = None
        transformation = None
        select_column_and_transformation(all_columns)

        if selected_column in all_columns:
            df[selected_column] = pd.to_numeric(df[selected_column].str.replace(',', '.'), errors='coerce')
            df['Species_GrowthType'] = df['WOA_Species'] + ' (' + df['WOA_GrowthType'] + ')'

            counts = df.groupby('Species_GrowthType')[selected_column].nunique()
            # Transformation der Werte je nach Einstellung
            if transformation == "log10":
                df[selected_column] = np.log10(df[selected_column])
            elif transformation == "sqrt":
                df[selected_column] = np.sqrt(df[selected_column])

            sns.boxplot(x='Species_GrowthType', y=selected_column, data=df, showfliers=False)   # Boxplot
            sns.stripplot(x='Species_GrowthType', y=selected_column, data=df, color='black', alpha=0.6, jitter=True)    # Datenpunkte einfügen

            plt.title(f'Boxplot von {selected_column} nach Spezies und Wuchsform', pad=15)
            plt.suptitle('')
            #Je nach Einstellung wird hier die Beschriftung der X-Achsen Labels angepasst
            plt.xlabel('Species (Growth type) [Sample count]', labelpad=10)
            if transformation == 'sqrt':
                plt.ylabel(f'Square Root of {selected_column}', labelpad=20)
            elif transformation == 'log10':
                plt.ylabel(f'Logarithm Base 10 of {selected_column}', labelpad=20)
            else:
                plt.ylabel(selected_column, labelpad=20)

            axis = plt.gca()
            x_labels = [item.get_text() for item in axis.get_xticklabels()]
            new_labels = [f'{label} [N = {counts[label]}]' for label in x_labels]   # Anfügen von Samplecount an Beschriftung
            axis.set_xticks(np.arange(len(new_labels)))     # 'Ticks' setzen um Matlibplot zufriedenzustellen, da manuelle änderungen an den Labels gemacht werden
            axis.set_xticklabels(new_labels, rotation=40, ha='right')   # 40° Beschriftung

            plt.gcf().set_size_inches(1920/100, 1080/100)   # Diagrammfenster skalieren
            plt.tight_layout()
            
            show_column_values('Species_GrowthType', df['Species_GrowthType'].tolist(), selected_column, df[selected_column].tolist())
            plt.show()

        else:
            print("Ungültige Spaltenauswahl.")
else:
    print("Keine Datei ausgewählt.")
