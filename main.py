from kivy.config import Config
Config.set('graphics', 'resizable', True)

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.logger import Logger
import os
import shutil

# Simulação resposta do Back
backend_response = {
    "images": [
        {
            "reference": {
                "key": "ref1",
                "name": "Reference Image 1",
                "id": "123",
                "longitude": "-123.456",
                "latitude": "45.678",
                "path": "assets/images/ref_img1.jpg"
            },
            "related": [
                {
                    "key": "rel1",
                    "name": "Related Image 1.1",
                    "id": "124",
                    "longitude": "-123.456",
                    "latitude": "45.678",
                    "path": "assets/images/img1_1.jpg"
                },
                {
                    "key": "rel2",
                    "name": "Related Image 1.2",
                    "id": "125",
                    "longitude": "-123.456",
                    "latitude": "45.678",
                    "path": "assets/images/img1_2.jpg"
                }
            ]
        },
        {
            "reference": {
                "key": "ref2",
                "name": "Reference Image 2",
                "id": "126",
                "longitude": "-123.456",
                "latitude": "45.678",
                "path": "assets/images/ref_img2.jpg"
            },
            "related": [
                {
                    "key": "rel3",
                    "name": "Related Image 2.1",
                    "id": "127",
                    "longitude": "-123.456",
                    "latitude": "45.678",
                    "path": "assets/images/img2_1.jpg"
                },
                {
                    "key": "rel4",
                    "name": "Related Image 2.2",
                    "id": "128",
                    "longitude": "-123.456",
                    "latitude": "45.678",
                    "path": "assets/images/img2_2.jpg"
                }
            ]
        }
    ]
}

class ImageSelector(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageSelector, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.selected_images = []

        # Gerenciador de arquivos para selecionar imagens
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True  # Habilitar preview
        )
        self.file_manager.start_path = os.path.expanduser('~/Downloads')
        self.update_images()

    def open_file_manager(self, instance):
        self.file_manager.show(self.file_manager.start_path)

    def exit_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.preview_image(path)

    def preview_image(self, path):
        try:
            preview_content = BoxLayout(orientation='vertical', spacing=dp(10))
            img = Image(source=path, size_hint=(1, 0.8))
            button_box = BoxLayout(size_hint=(1, 0.2), spacing=dp(10))

            save_button = MDRaisedButton(text="Save", on_release=lambda x: self.save_image(path))
            delete_button = MDRaisedButton(text="Delete", on_release=lambda x: self.delete_image(path))
            close_button = MDRaisedButton(text="Close", on_release=lambda x: self.popup.dismiss())

            button_box.add_widget(save_button)
            button_box.add_widget(delete_button)
            button_box.add_widget(close_button)

            preview_content.add_widget(img)
            preview_content.add_widget(button_box)

            self.popup = Popup(title="Preview Image", content=preview_content, size_hint=(0.8, 0.8))
            self.popup.open()
        except Exception as e:
            Logger.error(f"Error in preview_image: {str(e)}")

    def save_image(self, path):
        try:
            if path not in self.selected_images:
                self.selected_images.append(path)
            self.popup.dismiss()
            Snackbar(text="Imagem salva com sucesso!").open()
            self.update_images()
        except Exception as e:
            Logger.error(f"Error in save_image: {str(e)}")

    def delete_image(self, path):
        try:
            if path in self.selected_images:
                self.selected_images.remove(path)
            self.popup.dismiss()
            Snackbar(text="Imagem deletada com sucesso!").open()
            self.update_images()
        except Exception as e:
            Logger.error(f"Error in delete_image: {str(e)}")

    def update_images(self):
        self.clear_widgets()
        self.add_widget(MDTopAppBar(title="Selecionar Imagem", elevation=10))
        self.add_widget(MDRaisedButton(text="Selecionar imagens", size_hint=(None, None), size=(dp(200), dp(50)),
                                       pos_hint={"center_x": 0.5, "center_y": 0.5}, on_release=self.open_image_selector))
        self.add_widget(MDRaisedButton(text="Upload imagens", size_hint=(None, None), size=(dp(200), dp(50)),
                                       pos_hint={"center_x": 0.5, "center_y": 0.5}, on_release=self.open_file_manager))

        # Carrega as imagens vindas da resposta do back
        for item in backend_response["images"]:
            reference = item["reference"]
            related = item["related"]

            # Verifica se as imagens existem antes de adicioná-las
            if not os.path.exists(reference["path"]):
                Logger.error(f"Image not found: {reference['path']}")
                continue

            # Cria Layout da referencia e da relacionada
            row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(200), spacing=dp(10))
            ref_box = BoxLayout(orientation='vertical', size_hint=(0.25, 1))
            ref_img = Image(source=reference["path"], size_hint=(1, 1))
            ref_box.add_widget(ref_img)
            row.add_widget(ref_box)

            for rel in related:
                if not os.path.exists(rel["path"]):
                    Logger.error(f"Image not found: {rel['path']}")
                    continue

                rel_box = BoxLayout(orientation='vertical', size_hint=(0.25, 1))
                rel_img = Image(source=rel["path"], size_hint=(1, 1))
                checkbox = CheckBox(size_hint=(1, None), height=dp(40))
                rel_box.add_widget(rel_img)
                rel_box.add_widget(checkbox)
                row.add_widget(rel_box)

            self.add_widget(row)

    def open_image_selector(self, instance):
        Logger.info("ImageSelector: Opening image selector")
        content = BoxLayout(orientation='vertical', spacing=10)

        images = [("assets/images/img1_1.jpg", "img1_1"), ("assets/images/img2_1.jpg", "img2_1"), ("assets/images/img3.jpg", "img3"), ("assets/images/img4.jpg", "img4")]
        images.extend([(img, os.path.basename(img)) for img in self.selected_images])
        self.checkboxes = {}

        for i in range(0, len(images), 2):
            row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(200))
            for img_path, img_name in images[i:i + 2]:
                if not os.path.exists(img_path):
                    Logger.error(f"Image not found: {img_path}")
                    continue

                box = BoxLayout(orientation='vertical', size_hint=(1, 1))
                img = Image(source=img_path, size_hint=(1, 1))
                checkbox = CheckBox(size_hint=(1, None), height=dp(40))
                self.checkboxes[img_name] = checkbox
                box.add_widget(img)
                box.add_widget(checkbox)
                row.add_widget(box)
            content.add_widget(row)

        buttons = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))
        copy_button = MDRaisedButton(text="Copiar Selecionada", on_release=self.copy_selected)
        delete_button = MDRaisedButton(text="Deletar Selecionada", on_release=self.confirm_delete_selected)
        close_button = MDRaisedButton(text="Close", on_release=lambda x: self.popup.dismiss())
        buttons.add_widget(copy_button)
        buttons.add_widget(delete_button)
        buttons.add_widget(close_button)

        root = BoxLayout(orientation='vertical')
        root.add_widget(content)
        root.add_widget(buttons)

        self.popup = Popup(title="Selecione as Imagens", content=root, size_hint=(0.8, 0.8))
        self.popup.open()

    def confirm_delete_selected(self, instance):
        confirm_dialog = MDDialog(
            text="Você realmente deseja deletar a imagem?",
            buttons=[
                MDRaisedButton(text="Cancelar", on_release=lambda x: confirm_dialog.dismiss()),
                MDRaisedButton(text="Deletar", on_release=lambda x: self.delete_selected(confirm_dialog))
            ]
        )
        confirm_dialog.open()

    def delete_selected(self, dialog):
        Logger.info("ImageSelector: Deleting selected images")
        for img_name, checkbox in self.checkboxes.items():
            if checkbox.active:
                try:
                    os.remove(f"assets/images/{img_name}.jpg")
                except FileNotFoundError:
                    if os.path.isabs(img_name):
                        os.remove(img_name)
        self.popup.dismiss()
        Snackbar(text="Imagem deletada com sucesso!").open()
        dialog.dismiss()

    def copy_selected(self, instance):
        confirm_dialog = MDDialog(
            text="Você realmente deseja copiar a imagem?",
            buttons=[
                MDRaisedButton(text="Cancelar", on_release=lambda x: confirm_dialog.dismiss()),
                MDRaisedButton(text="Copiar", on_release=lambda x: self.confirm_copy_selected(confirm_dialog))
            ]
        )
        confirm_dialog.open()

    def confirm_copy_selected(self, dialog):
        Logger.info("ImageSelector: Copying selected images")
        for img_name, checkbox in self.checkboxes.items():
            if checkbox.active:
                src = img_name if os.path.isabs(img_name) else f"assets/images/{img_name}.jpg"
                if os.path.exists(src):
                    dst = f"assets/images/copied_{os.path.basename(img_name)}.jpg"
                    shutil.copyfile(src, dst)
                else:
                    Logger.error(f"Image not found: {src}")
        self.popup.dismiss()
        Snackbar(text="Imagem copiada com sucesso!").open()
        dialog.dismiss()

class MainApp(MDApp):
    def build(self):
        Logger.info("MainApp: Building the app")
        self.title = "Comparador de relacionamento"
        Builder.load_file('kv/main.kv')
        return ImageSelector()

    def show_image_selector(self, instance):
        Logger.info("MainApp: Showing image selector")
        self.root.open_image_selector(instance)

if __name__ == '__main__':
    MainApp().run()

