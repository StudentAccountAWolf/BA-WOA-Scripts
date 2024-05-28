import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, ttk
import numpy as np

# Globala Variablen
selected_column = None
transformation = None
nan_excluded = None
show_data = False

# ---------------------------------Plot bauen-------------------------------------
def plot_data(df):
    global selected_column, transformation, nan_excluded, show_data
    df_temp = df.copy() # Kopiert Originaldaten in temp. Dataframe -> Prevention von Berechnungsfehlern wenn neue Plots erstellt werden
   
    # Wenn ausgewählte Spalte vorhanden ist (sollte sein aber falls trotzdem was falsch ist..)
    if selected_column in df_temp.columns:

        # Überprüfen, ob die Spalte bereits numerische Werte enthält ("nur" wichtig falls deutsches Layout mit Kommata anstelle von Punkten)
        if pd.api.types.is_numeric_dtype(df_temp[selected_column]):
            pass
        else:
            df_temp[selected_column] = pd.to_numeric(df_temp[selected_column].str.replace(',', '.'), errors='coerce')

        # Extras für X-Achse
        df_temp['Species_GrowthType'] = df_temp['WOA_Species'] + ' (' + df_temp['WOA_GrowthType'] + ')' # Erstelle neue Spalte um auf X-Achse Spezies und Wuchsform anzeigen zu können
        counts = df_temp.groupby('Species_GrowthType')[selected_column].nunique()   # Einfachen Zähler um Samplesize auf X-Achse anzeigen zu können
        
        # Entfernen von NaN Werten um übersichtlichere Blots zu bauen
        if nan_excluded == "True":
            df_temp = df_temp.dropna(subset=[selected_column, 'Species_GrowthType'])   # Entferne Zeilen mit NaN-Werten in den relevanten Spalten

        # Alle Transformationen die möglich sind (falls keins ausgewählt ist, werden die Werte nicht transformiert): 
        if transformation == "log(10)":
            df_temp[selected_column] = np.log10(df_temp[selected_column])
        elif transformation == "log(e)":
            df_temp[selected_column] = np.log(df_temp[selected_column])
        elif transformation == "(x)^0.5":
            df_temp[selected_column] = np.sqrt(df_temp[selected_column])

        # Ein neues Fenster für das Boxplot erstellen
        fig, ax = plt.subplots()    # Erzeuge eine neue Figur und ein Axes-Objekt zum Zeichnen
        sns.boxplot(x='Species_GrowthType', y=selected_column, data=df_temp, showfliers=True, ax=ax) # showfliers=True: Anzeige von Ausreißern (outliers) im Boxplot | ax=ax: Verwendet das zuvor erstellte Axes-Objekt zum Zeichnen des Boxplots
        sns.stripplot(x='Species_GrowthType', y=selected_column, data=df_temp, color='black', alpha=0.6, jitter=True, ax=ax)    # Erstellt ein Stripplot über dem Boxplot | jitter=True erzeugt Datenpunkte willkürlich auf einer Ebene um sie besser erkennen zu können

        # Allgemeine Beschriftungen von Titel bis Achsen
        ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform', pad=15, fontweight="bold")
        ax.set_xlabel('Species (Growth type)', labelpad=16, fontsize = 12, fontweight="bold")
        if transformation == '(x)^0.5':
            ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform - Transformation = Quadratwurzel', pad=15, fontweight="bold")
            ax.set_ylabel(f'{selected_column} - (x)^0.5', labelpad=24, fontsize = 12, fontweight="bold")
        elif transformation == 'log(10)':
            ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform - Transformation = Logarithmus(10)', pad=15, fontweight="bold")
            ax.set_ylabel(f'{selected_column} - log(10)', labelpad=24, fontsize = 12, fontweight="bold")
        elif transformation == 'log(e)':
            ax.set_title(f'Boxplot von {selected_column} nach Spezies und Wuchsform - Transformation = Logarithmus(e)', pad=15, fontweight="bold")
            ax.set_ylabel(f'{selected_column} - log(e)', labelpad=24, fontsize = 12, fontweight="bold")
        else:
            ax.set_ylabel(selected_column, labelpad=24, fontsize = 11, fontweight="bold")

        fig.canvas.manager.set_window_title(f'Boxplot von {selected_column} [Transformation = {transformation}] nach Spezies und Wuchsform')  # Set window title to selected column name

        axis = plt.gca()    # Zugriff auf Achse
        x_labels = [item.get_text() for item in axis.get_xticklabels()] # Nimmt jede X-achsenbeschriftung und speichert sie in x_labels
        new_labels = [f'{label} [N = {counts[label]}]' for label in x_labels]   # Anfügen von Samplecount an jede Beschriftung der X-Achse
        axis.set_xticks(np.arange(len(new_labels)))     # Position der neuen Beschriftungen auf der X-Achse setzen
        axis.set_xticklabels(new_labels, rotation=40, ha='right', fontweight="bold")  # Horizontal Alignment für Ticklabels einstellen
        fig.set_size_inches(1600/100, 1200/100) 
        fig.tight_layout() # Passt Layout an die Größe des Fensters an

        # Zeigt Datentabelle wenn ausgewählt:
        if show_data == "True":
            show_column_values('Species_GrowthType', df_temp['Species_GrowthType'].tolist(), selected_column, df_temp[selected_column].tolist())

        plt.show()

    else:
        print("Ungültige Spaltenauswahl.")
# -------------------------------------------------------------------------------- 

# ------------------ Tkinter Funktionen für Auswahl und Ausgabe ------------------ 
def select_settings(columns):
    global selected_column, transformation, nan_excluded, show_data
    root = tk.Tk()
    root.title("Spalten- und Transformationsauswahl")
    root.geometry('550x280')  # Skalierung des Fensters für die Auswahl

    # Alle Daten die bei Bestätigung an die plot Funktion geschickt werden
    def on_confirm():
        global selected_column, transformation, nan_excluded, show_data
        selected_column = column_selected.get()
        transformation = transformation_selected.get()
        nan_excluded = nan_selected.get()
        show_data = show_data_selected.get()
        plot_data(df)

    # Auswahl der Spalten
    label1 = tk.Label(root, text="Spalte:", font=("Helvetica", 12))
    label1.pack(pady=(20, 10))
    column_selected = ttk.Combobox(root, values=columns, width=60)
    column_selected.pack(pady=10)

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

    # Auswahl Bestätigen - Button
    tk.Button(root, text="Bestätigen", command=on_confirm).pack(pady=10)

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

if file_path:
    df = pd.read_csv(file_path, sep='\t') # als tsv einlessen
    all_columns = df.columns.tolist() # Liste aus Spaltennamen erstellen

    if not all_columns:
        print("Keine Spalten in der Datei gefunden.")
    else:
        select_settings(all_columns)
else:
    print("Keine Datei ausgewählt.")