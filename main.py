from PIL import Image
import matplotlib.pyplot as plt
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk

def compress_to_webp(input_image_path, output_image_path, quality=10):
    try:
        image = Image.open(input_image_path)
        image.save(output_image_path, 'webp', quality=quality)

        original_size = os.path.getsize(input_image_path) / (1024 * 1024)
        compressed_size = os.path.getsize(output_image_path) / (1024 * 1024)
        reduction_percentage = ((original_size - compressed_size) / original_size) * 100

        return {
            'Slika': input_image_path,
            'Originalna velicina (MB)':  round(original_size, 3),
            'Kompresovana velicina (MB)': round(compressed_size, 3),
            'Procenat umanjenja (%)': round(reduction_percentage, 1),
            'Putanja do kompresovane slike': output_image_path,
        }

    except Exception as e:
        return {
            'Slika': input_image_path,
            'Greška': str(e),
            'Originalna velicina (MB)': 'N/A',
            'Kompresovana velicina (MB)': 'N/A',
            'Procenat umanjenja (%)': 'N/A',
            'Putanja do kompresovane slike': 'N/A',
        }


def testiraj_kompresiju(slike):
    rezultati = []
    for slika_info in slike:
        input_path = slika_info['ime']
        output_path = f"izlazna_{slika_info['ime'][:-4]}.webp"

        rezultat = compress_to_webp(input_path, output_path)
        rezultati.append(rezultat)

    return rezultati
def sacuvaj_tabelu_kao_csv(rezultati, ime_datoteke='rezultati_kompresije.csv'):
    df = pd.DataFrame(rezultati)
    if 'Putanja do kompresovane slike' in df.columns:
        df = df.drop('Putanja do kompresovane slike', axis=1)
    df.to_csv(ime_datoteke, index=False)
    print(f"Tabela sa rezultatima je sačuvana kao '{ime_datoteke}'.")

def prikazi_slike_i_tabelu(rezultati):
    for rezultat in rezultati:
        input_image_path = rezultat['Slika']
        output_image_path = rezultat['Putanja do kompresovane slike']
        original_size = rezultat['Originalna velicina (MB)']
        compressed_size = rezultat['Kompresovana velicina (MB)']

        plt.figure(figsize=(13, 6))

        image = Image.open(input_image_path)
        width, height = image.size
        compressed_image = Image.open(output_image_path)

        plt.subplot(2, 2, 1)
        plt.imshow(image)
        plt.title('Originalna slika')
        plt.axis('off')

        plt.subplot(2, 2, 2)
        plt.imshow(compressed_image)
        plt.title('Kompresovana slika')
        plt.axis('off')

        plt.subplot(2, 2, 3)
        plt.imshow(image)
        plt.title('Zumirana originalna slika')
        plt.axis('on')
        plt.xlim(2*width/4,3*width/4)
        plt.ylim(3 * height / 4, 2 * height / 4)

        plt.subplot(2, 2, 4)
        plt.imshow(compressed_image)
        plt.title('Zumirana kompresovana slika')
        plt.axis('on')
        plt.xlim(2 * width / 4, 3 * width / 4)
        plt.ylim(3 * height / 4, 2 * height / 4)


        info_text = f"Veličina originalne slike: {original_size:.2f} MB\nVeličina kompresovane slike: {compressed_size:.2f} MB"

        # Dodavanje teksta na grafik
        plt.figtext(0.5, 0.01, info_text, wrap=True, horizontalalignment='center', fontsize=10)

        plt.tight_layout()
        plt.show()

    root = tk.Tk()
    root.title("Informacije o slikama")

    df = pd.DataFrame(rezultati)
    tree = ttk.Treeview(root)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    columns = df.columns.tolist()

    if 'Putanja do kompresovane slike' in columns:
        columns.remove('Putanja do kompresovane slike')

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=150)


    for index, row in df.iterrows():
        # Kreiranje reda podataka bez kolone 'Putanja do kompresovane slike'
        row_data = row.drop('Putanja do kompresovane slike')

        tree.insert("", "end", values=list(row_data))

    tree.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()


slike = [
    {'ime': 'slika1.jpg'},
    {'ime': 'slika2.jpg'},
    {'ime': 'slika3.png'},
    {'ime': 'slika4.png'},
    {'ime': 'slika5.jpg'},
    {'ime': 'slika6.jpg'},
    {'ime': 'slika7.jpg'},
    {'ime': 'slika8.jpg'},
    {'ime': 'slika9.jpg'},
    {'ime': 'slika10.jpg'},
    {'ime': 'slika11.gif'},
    {'ime': 'slika12.gif'},
    {'ime': 'slika13.jpg'},
    {'ime': 'slika14.jpg'},
    {'ime': 'slika15.jpeg'},


]

rezultati_testiranja = testiraj_kompresiju(slike)
prikazi_slike_i_tabelu(rezultati_testiranja)
sacuvaj_tabelu_kao_csv(rezultati_testiranja)