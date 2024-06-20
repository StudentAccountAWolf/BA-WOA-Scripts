import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, ttk
import numpy as np
import sys

# Globale Variablen
selected_column = None
transformation = None
nan_excluded = None
show_data = False
selected_hoc_column : str

# ---------------------------------Plot bauen-------------------------------------
def plot_data(df, hoc_df):
    global selected_column, transformation, nan_excluded, show_data, y_position, selected_hoc_column
    df_temp = df.copy()  # Kopiert Originaldaten in temp. Dataframe -> Prevention von Berechnungsfehlern wenn neue Plots erstellt werden
    hoc_df_temp = hoc_df.copy()
    
    if selected_column in df_temp.columns:
        if pd.api.types.is_numeric_dtype(df_temp[selected_column]):
            pass
        else:
            df_temp[selected_column] = pd.to_numeric(df_temp[selected_column].str.replace(',', '.'), errors='coerce')
        
        df_temp['Species_GrowthType'] = df_temp['WOA_Species_short']# + ' (' + df_temp['GrowthType'] + ')'
        counts = df_temp.groupby('Species_GrowthType')[selected_column].nunique()
        
        if nan_excluded == "True":
            df_temp = df_temp.dropna(subset=[selected_column, 'Species_GrowthType'])
        
        if transformation == "log(10)":
            df_temp[selected_column] = np.log10(df_temp[selected_column])
        elif transformation == "log(e)":
            df_temp[selected_column] = np.log(df_temp[selected_column])
        elif transformation == "(x)^0.5":
            df_temp[selected_column] = np.sqrt(df_temp[selected_column])
        
        fig, ax = plt.subplots()
        sns.boxplot(x='Species_GrowthType', y=selected_column, data=df_temp, color='#79C',linewidth=1.5, medianprops={"linestyle": "-", "linewidth": 1.5, "color": "black"}, showfliers=False, ax=ax)
        sns.stripplot(x='Species_GrowthType', y=selected_column, data=df_temp, color='black', alpha=0.7, jitter=True, ax=ax)
        
        if y_position == "Rechts":
            ax.yaxis.tick_right()
            #ax.yaxis.set_label_position("right")
        
        
        # if transformation == '(x)^0.5':
        #     ax.set_ylabel(f'{selected_column} - (x)^0.5', labelpad=24, fontsize=14, fontweight="bold")
        # elif transformation == 'log(10)':
        #     ax.set_ylabel(f'{selected_column} - log(10)', labelpad=24, fontsize=14, fontweight="bold")
        # elif transformation == 'log(e)':
        #     ax.set_ylabel(f'{selected_column} - log(e)', labelpad=24, fontsize=14, fontweight="bold")
        # else:
        #     ax.set_ylabel(selected_column, labelpad=24, fontsize=14, fontweight="bold")
        
        for label in ax.get_yticklabels():
            label.set_fontweight("bold")
            label.set_fontsize(15)
        ax.set_xlabel(' ')
        ax.set_ylabel(" ")

        axis = plt.gca()
        x_labels = [item.get_text() for item in axis.get_xticklabels()]
        new_labels = []
        
        for label in x_labels:
            hoc_species_rows = hoc_df_temp[hoc_df_temp['Species_short'] == label]
            if not hoc_species_rows.empty:
                hoc_value = hoc_species_rows.iloc[0][selected_hoc_column]
                new_label = f'{label}\n [N = {counts[label]}]'
                new_labels.append(new_label)
                

                # Text am oberen Rand des Plots platzieren
                y_max = df_temp[selected_column].max()  # Maximaler y-Wert des gesamten Datensatzes
                offset = 0.025 * (df_temp[selected_column].max() - df_temp[selected_column].min())  # Berechne einen kleinen Offset
                ax.text(x=new_labels.index(new_label), y=y_max + offset, s=f'{hoc_value}', ha='center', fontweight='bold', fontsize=14.5)
            else:
                original_label = f'{label} [N = {counts[label]}]'
                new_labels.append(original_label)
        
        axis.set_xticks(np.arange(len(new_labels)))
        axis.set_xticklabels(new_labels, rotation=43, ha='right', fontweight="bold", fontsize=15)
        fig.set_size_inches(1570 / 100, 1250 / 100)
        fig.tight_layout()
        
        if show_data == "True":
            show_column_values('Species_GrowthType', df_temp['Species_GrowthType'].tolist(), selected_column, df_temp[selected_column].tolist())
        
        if y_position == "Rechts":
            #plt.subplots_adjust(left=0.143, bottom=0.23, top=0.988, wspace=0.2, hspace=0.2)
            plt.subplots_adjust(left=0.088, bottom=0.174, top=0.988, wspace=0.2, hspace=0.2)
        else:
            #plt.subplots_adjust(left=0.143, bottom=0.23, right=0.988, top=0.988, wspace=0.2, hspace=0.2)
            plt.subplots_adjust(left=0.088, bottom=0.174, right=0.988, top=0.988, wspace=0.2, hspace=0.2)
        plt.show()
    
    else:
        print("Ungültige Spaltenauswahl.")

# -------------------------------------------------------------------------------- 

# ------------------ Tkinter Funktionen für Auswahl und Ausgabe ------------------ 
def select_settings(columns, hoc_columns):
    global selected_column, transformation, nan_excluded, show_data, y_position, selected_hoc_column
    root = tk.Tk()
    root.title("Spalten- und Transformationsauswahl")
    root.geometry('550x340')  # Skalierung des Fensters für die Auswahl

    # Alle Daten die bei Bestätigung an die plot Funktion geschickt werden 
    def on_confirm():
        global selected_column, transformation, nan_excluded, show_data, y_position, selected_hoc_column
        selected_column = column_selected.get()
        selected_hoc_column = hoc_selected.get()
        transformation = transformation_selected.get()
        nan_excluded = nan_selected.get()
        show_data = show_data_selected.get()
        y_position = select_y_position.get()
        plot_data(df, hoc_df)

    # Beenden des Programms
    def on_exit():
        root.destroy()
        sys.exit()

    # Auswahl der Spalten
    label1 = tk.Label(root, text="Spalte:", font=("Helvetica", 12))
    label1.pack(pady=(20, 10))
    column_selected = ttk.Combobox(root, values=columns, width=60)
    column_selected.pack(pady=10)

    label0 = tk.Label(root, text="PostHoc Spalte:", font=("Helvetica", 12))
    label0.pack(pady=(0, 10))
    hoc_selected = ttk.Combobox(root, values=hoc_columns, width=60)
    hoc_selected.pack(pady=10)

    frame = tk.Frame(root)  # Frame, damit ein grid angewendet werden kann
    frame.pack(pady=(20, 10))

    # Auswahl der Transformation
    label2 = tk.Label(frame, text="Transformation:", font=("Helvetica", 12))
    label2.grid(row=0, column=0, padx=(10, 10))
    transformation_selected = ttk.Combobox(frame, values=["None", "log(10)", "log(e)", "(x)^0.5"], width=15)
    transformation_selected.grid(row=0, column=1)
    transformation_selected.current(0)

    # Auswahl zum Ausklammern der NaN Werte
    label3 = tk.Label(frame, text="NaN ausklammern:", font=("Helvetica", 12))
    label3.grid(row=0, column=2, padx=(10, 10))
    nan_selected = ttk.Combobox(frame, values=["False", "True"], width=15)
    nan_selected.grid(row=0, column=3)
    nan_selected.current(0)

    # Auswahl zum Anzeigen der Daten
    label4 = tk.Label(frame, text="Daten anzeigen:", font=("Helvetica", 12))
    label4.grid(row=2, column=2, padx=(29, 10))
    show_data_selected = ttk.Combobox(frame, values=["False", "True"], width=15)
    show_data_selected.grid(row=2, column=3)
    show_data_selected.current(0)

    label5 = tk.Label(frame, text="Y-Achse:", font=("Helvetica", 12))
    label5.grid(row=2, column=0, padx=(10, 10))
    select_y_position = ttk.Combobox(frame, values=["Links", "Rechts"], width=15)
    select_y_position.grid(row=2, column=1)
    select_y_position.current(0)

    # Auswahl Bestätigen - Button
    tk.Button(root, text="Bestätigen", command=on_confirm).pack(pady=10)
    # Beenden - Button
    tk.Button(root, text="Beenden", command=on_exit).pack(pady=0)

    # Solange loopen bis geschlossen wird (ggf. in Zunkunft extra Knopf einbauen)
    root.mainloop()
# -------------------------------------------------------------------------------- 

# ---------------------Datentabelle erstellen und anzeigen------------------------ 
def show_column_values(column_name_1, values_1, column_name_2, values_2):
    global transformation
    values_window = tk.Toplevel()  # Ein neues Fenster erstellen

    # Beschriftung des Fenstertitels
    values_window.title(f"{column_name_2} [Transformation = {transformation}]")
    if transformation == None:
        values_window.title(f"{column_name_2}")
    elif transformation == "log(10)":
        values_window.title(f"{column_name_2} (log(10))")
    elif transformation == "ln":
        values_window.title(f"{column_name_2} (log(e))")
    elif transformation == "(x)^0.5":
        values_window.title(f"{column_name_2} ((x)^0.5)")

    # Tabelle erstellen (links=Spezies | rechts=Spaltennamen)
    tree = ttk.Treeview(values_window, columns=(column_name_1, column_name_2), show="headings")
    tree.heading(column_name_1, text=column_name_1)
    tree.heading(column_name_2, text=column_name_2)
    for value_1, value_2 in zip(values_1, values_2):
        tree.insert("", "end", values=(value_1, value_2))

    tree.pack(expand=True, fill="both")
    values_window.geometry("800x900")
# -------------------------------------------------------------------------------- 


root = tk.Tk()
root.withdraw()

# Auswahl der Datendatei (Mass oder LeafMeasurements)
file_path = filedialog.askopenfilename()
posthoc_file = r"G:\Bachelorarbeit_Daten\Statistik\results\post hoc results\post hoc.csv"

if file_path:
    df = pd.read_csv(file_path, sep='\t') # als tsv einlessen
    all_columns = df.columns.tolist() # Liste aus Spaltennamen erstellen
    hoc_df = pd.read_csv(posthoc_file, sep=',')
    hoc_columns = hoc_df.columns.tolist()

    if not all_columns:
        print("Keine Spalten in der Datei gefunden.")
    else:
        select_settings(all_columns, hoc_columns)
else:
    print("Keine Datei ausgewählt.")