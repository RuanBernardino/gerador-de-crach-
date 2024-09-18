import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import xml.etree.ElementTree as ET

class CarteirinhaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Carteirinha")

        self.root.geometry("800x600")

        self.foto_path = None
        self.card_image = None
        self.background_image_path = "fundo.jpg"

        self.xml_file = 'alunos.xml'
        try:
            with open(self.xml_file, 'r') as f:
                pass
        except FileNotFoundError:
            with open(self.xml_file, 'w') as f:
                f.write('<alunos></alunos>')

        self.main_frame = ctk.CTkFrame(root, width=800, height=600)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        form_frame = ctk.CTkFrame(self.main_frame, width=400, height=300)
        form_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=20, pady=20, expand=True)

        ctk.CTkLabel(form_frame, text="Nome:").grid(row=0, column=0, sticky=ctk.W)
        self.nome_entry = ctk.CTkEntry(form_frame)
        self.nome_entry.grid(row=0, column=1)

        ctk.CTkLabel(form_frame, text="Sobrenome:").grid(row=1, column=0, sticky=ctk.W)
        self.sobrenome_entry = ctk.CTkEntry(form_frame)
        self.sobrenome_entry.grid(row=1, column=1)

        ctk.CTkLabel(form_frame, text="R.A:").grid(row=2, column=0, sticky=ctk.W)
        self.ra_entry = ctk.CTkEntry(form_frame)
        self.ra_entry.grid(row=2, column=1)

        ctk.CTkLabel(form_frame, text="Série:").grid(row=3, column=0, sticky=ctk.W)
        self.serie_entry = ctk.CTkEntry(form_frame)
        self.serie_entry.grid(row=3, column=1)

        ctk.CTkButton(form_frame, text="Selecionar Foto", command=self.select_photo).grid(row=4, column=0, columnspan=2, pady=5)

        ctk.CTkButton(form_frame, text="Gerar Carteirinha", command=self.generate_id_card).grid(row=5, column=0, columnspan=2, pady=5)

        self.preview_frame = ctk.CTkFrame(self.main_frame, width=400, height=300)
        self.preview_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, padx=20, pady=20, expand=True)

        self.image_label = ctk.CTkLabel(self.preview_frame)
        self.image_label.pack(expand=True)

        self.save_button = ctk.CTkButton(self.preview_frame, text="Salvar Carteirinha", command=self.save_image)
        self.save_button.pack(pady=10)
        self.save_button.pack_forget()  

        search_frame = ctk.CTkFrame(self.main_frame, width=800, height=100)
        search_frame.pack(side=ctk.BOTTOM, fill=ctk.X, padx=20, pady=10)

        ctk.CTkLabel(search_frame, text="Buscar R.A:").pack(side=ctk.LEFT)
        self.search_entry = ctk.CTkEntry(search_frame)
        self.search_entry.pack(side=ctk.LEFT, padx=5)
        
        ctk.CTkButton(search_frame, text="Buscar", command=self.search_students).pack(side=ctk.LEFT, padx=5)

        self.results_listbox = tk.Listbox(search_frame)
        self.results_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.results_listbox.bind('<Double-1>', self.on_listbox_select)

    def select_photo(self):
        self.foto_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    def generate_id_card(self):
        nome = self.nome_entry.get()
        sobrenome = self.sobrenome_entry.get()
        ra = self.ra_entry.get()
        serie = self.serie_entry.get()

        font_size = 15

        width, height = 350, 200
        card = Image.new('RGB', (width, height), color=(255, 255, 255))

        try:
            background = Image.open(self.background_image_path)
            background = background.resize((width, height))
            card.paste(background, (0, 0))
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {e}")

        draw = ImageDraw.Draw(card)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        ajuste_vertical = 25
        
        draw.text((70, 25), "EMIEF - Antônio Felix Gonçalves", font=font, fill=(0, 0, 0))

        draw.text((155, 45 + ajuste_vertical), f"Nome: {nome}", font=font, fill=(0, 0, 0))
        draw.text((155, 65 + ajuste_vertical), f"Sobrenome: {sobrenome}", font=font, fill=(0, 0, 0))
        draw.text((155, 85 + ajuste_vertical), f"R.A: {ra}", font=font, fill=(0, 0, 0))
        draw.text((155, 105 + ajuste_vertical), f"Série: {serie}", font=font, fill=(0, 0, 0))

        if self.foto_path:
            try:
                foto = Image.open(self.foto_path)
                foto = foto.resize((100, 100))
                card.paste(foto, (10, 50 + ajuste_vertical))
            except Exception as e:
                print(f"Erro ao carregar foto: {e}")

        self.card_image = card
        self.update_preview(card)
        
        self.store_student(nome, sobrenome, ra, serie, self.foto_path)

    def update_preview(self, card):
        card_tk = ImageTk.PhotoImage(card)
        self.image_label.configure(image=card_tk)
        self.image_label.image = card_tk

        self.save_button.pack(pady=10)

    def save_image(self):
        if self.card_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.card_image.save(file_path)

    def store_student(self, nome, sobrenome, ra, serie, foto_path):
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
        except ET.ParseError:
            root = ET.Element("alunos")
        
        aluno = ET.SubElement(root, "aluno")
        ET.SubElement(aluno, "nome").text = nome
        ET.SubElement(aluno, "sobrenome").text = sobrenome
        ET.SubElement(aluno, "ra").text = ra
        ET.SubElement(aluno, "serie").text = serie
        ET.SubElement(aluno, "foto").text = foto_path

        tree = ET.ElementTree(root)
        tree.write(self.xml_file)

    def search_students(self):
        ra_query = self.search_entry.get().strip()
        self.results_listbox.delete(0, tk.END)
        
        print(f"Procurando R.A: {ra_query}")  
        
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            
            found = False
            for aluno in root.findall('aluno'):
                aluno_ra = aluno.find('ra').text
                aluno_nome = aluno.find('nome').text
                print(f"Encontrado aluno com R.A: {aluno_ra}, Nome: {aluno_nome}")  
                
                if ra_query == aluno_ra:
                    self.results_listbox.insert(tk.END, f"{aluno_nome} (R.A: {aluno_ra})")
                    found = True
            
            if not found:
                self.results_listbox.insert(tk.END, "Nenhum aluno encontrado.")
                
        except Exception as e:
            print(f"Erro ao buscar alunos: {e}")

    def on_listbox_select(self, event):
        selected_index = self.results_listbox.curselection()
        if selected_index:
            aluno_info = self.results_listbox.get(selected_index[0])
            ra = aluno_info.split(' (R.A: ')[1].split(')')[0]
            self.generate_id_card_for_ra(ra)

    def generate_id_card_for_ra(self, ra):
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            for aluno in root.findall('aluno'):
                aluno_ra = aluno.find('ra').text
                if aluno_ra == ra:
                    nome = aluno.find('nome').text
                    sobrenome = aluno.find('sobrenome').text
                    serie = aluno.find('serie').text
                    foto_path = aluno.find('foto').text

                    self.nome_entry.delete(0, tk.END)
                    self.nome_entry.insert(0, nome)
                    self.sobrenome_entry.delete(0, tk.END)
                    self.sobrenome_entry.insert(0, sobrenome)
                    self.ra_entry.delete(0, tk.END)
                    self.ra_entry.insert(0, ra)
                    self.serie_entry.delete(0, tk.END)
                    self.serie_entry.insert(0, serie)
                    self.foto_path = foto_path

                    self.generate_id_card()
                    break
        except Exception as e:
            print(f"Erro ao gerar carteirinha para R.A {ra}: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = CarteirinhaApp(root)
    root.mainloop()
