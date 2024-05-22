import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, ttk
import numpy as np


selected_column = None
transformation = None
nan_excluded = None

# df.dropna(subset=[selected_column, 'Species_GrowthType'], inplace=True)   # Entferne Zeilen mit NaN-Werten in den relevanten Spalten

def plot_data(df):
    global selected_column, transformation, nan_excluded
    df_temp = df.copy()
    if selected_column in df_temp.columns:
        # Überprüfen, ob die Spalte bereits numerische Werte enthält
        if pd.api.types.is_numeric_dtype(df_temp[selected_column]):
            pass
        else:
            df_temp[selected_column] = pd.to_numeric(df_temp[selected_column].str.replace(',', '.'), errors='coerce')

        df_temp['Species_GrowthType'] = df_temp['WOA_Species'] + ' (' + df_temp['WOA_GrowthType'] + ')'

        counts = df_temp.groupby('Species_GrowthType')[selected_column].nunique()
        
        if nan_excluded == "True":
            df_temp = df_temp.dropna(subset=[selected_column, 'Species_GrowthType'])   # Entferne Zeilen mit NaN-Werten in den relevanten Spalten

        if transformation == "log(10)":
            df_temp[selected_column] = np.log10(df_temp[selected_column])
        elif transformation == "log(e)":
            df_temp[selected_column] = np.log(df_temp[selected_column])
        elif transformation == "(x)^1/2":
            df_temp[selected_column] = np.sqrt(df_temp[selected_column])

        # Ein neues Fenster für das Boxplot erstellen
        fig, ax = plt.subplots()
        sns.boxplot(x='Species_GrowthType', y=selected_column, data=df_temp, showfliers=False, ax=ax)
        sns.stripplot(x='Species_GrowthType', y=selected_column, data=df_temp, color='black', alpha=0.6, jitter=True, ax=ax)

        ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform', pad=15, fontweight="bold")
        ax.set_xlabel('Species (Growth type)', labelpad=16, fontsize = 12, fontweight="bold")
        if transformation == '(x)^1/2':
            ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform - Transformation = Quadratwurzel', pad=15, fontweight="bold")
            ax.set_ylabel(f'{selected_column} - (x)^1/2', labelpad=24, fontsize = 12, fontweight="bold")
        elif transformation == 'log(10)':
            ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform - Transformation = Logarithmus(10)', pad=15, fontweight="bold")
            ax.set_ylabel(f'{selected_column} - log(10)', labelpad=24, fontsize = 12, fontweight="bold")
        elif transformation == 'log(e)':
            ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform - Transformation = Logarithmus(e)', pad=15, fontweight="bold")
            ax.set_ylabel(f'{selected_column} - log(e)', labelpad=24, fontsize = 12, fontweight="bold")
        else:
            ax.set_ylabel(selected_column, labelpad=24, fontsize = 11, fontweight="bold")

        fig.canvas.manager.set_window_title(f'Boxplot von {selected_column} [Transformation = {transformation}] nach Spezies und Wuchsform')  # Set window title to selected column name

        axis = plt.gca()
        x_labels = [item.get_text() for item in axis.get_xticklabels()]
        new_labels = [f'{label} [N = {counts[label]}]' for label in x_labels]   # Anfügen von Samplecount an Beschriftung
        axis.set_xticks(np.arange(len(new_labels)))     # 'Ticks' setzen um Matlibplot zufriedenzustellen, da manuelle änderungen an den Labels gemacht werden
        axis.set_xticklabels(new_labels, rotation=40, ha='right', fontweight="bold")  # Horizontal Alignment für Ticklabels einstellen
        fig.set_size_inches(1600/100, 1200/100)
        fig.tight_layout()

        show_column_values('Species_GrowthType', df_temp['Species_GrowthType'].tolist(), selected_column, df_temp[selected_column].tolist())
        plt.show()

    else:
        print("Ungültige Spaltenauswahl.")


# ------------------ Tkinter Funktionen für Auswahl und Ausgabe ------------------ 
def select_column_and_transformation(columns):
    global selected_column, transformation, nan_excluded
    root = tk.Tk()
    root.title("Spalten- und Transformationsauswahl")
    root.geometry('550x250')

    def on_confirm():
        global selected_column, transformation, nan_excluded
        selected_column = column_selected.get()
        transformation = transformation_selected.get()
        nan_excluded = nan_selected.get()
        plot_data(df)

    label1 = tk.Label(root, text="Spalte:", font=("Helvetica", 12))
    label1.pack(pady=(20, 10))
    column_selected = ttk.Combobox(root, values=columns, width=60)
    column_selected.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=(20, 10))

    label2 = tk.Label(frame, text="Transformation:", font=("Helvetica", 12))
    label2.grid(row=0, column=0, padx=(10, 10))
    transformation_selected = ttk.Combobox(frame, values=["None", "log(10)", "log(e)", "(x)^1/2"], width=15)
    transformation_selected.grid(row=0, column=1)
    transformation_selected.current(0)

    label3 = tk.Label(frame, text="NaN ausklammern:", font=("Helvetica", 12))
    label3.grid(row=0, column=2, padx=(10, 10))
    nan_selected = ttk.Combobox(frame, values=["False", "True"], width=15)
    nan_selected.grid(row=0, column=3)
    nan_selected.current(0)

    tk.Button(root, text="Bestätigen", command=on_confirm).pack(pady=10)

    root.mainloop()
# -------------------------------------------------------------------------------- 

def show_column_values(column_name_1, values_1, column_name_2, values_2):
    global transformation
    values_window = tk.Toplevel()  # Ein neues Toplevel-Fenster erstellen
    values_window.title(f"{column_name_2} [Transformation = {transformation}]")
    if transformation == None:
        values_window.title(f"{column_name_2}")
    elif transformation == "log(10)":
        values_window.title(f"{column_name_2} (log(10))")
    elif transformation == "ln":
        values_window.title(f"{column_name_2} (log(e))")
    elif transformation == "(x)^1/2":
        values_window.title(f"{column_name_2} ((x)^1/2)")

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