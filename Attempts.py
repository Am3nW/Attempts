from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.transition import MDFadeSlideTransition
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
import random

Window.size=(500,700)
nums = "123456789"
hidden_number = ''.join(random.sample(nums,4))

class VictoryScreen(Screen):
    def switch_to_mainscreen(self):
        self.manager.current = "main_screen"
class MainScreen(Screen):
    def switch_to_playzone(self):
        self.manager.current = "playzone"
    def switch_to_infopage(self):
        self.manager.current = "infopage"
    def close_app(self):
        self.warning_btn = MDDialog(text="Are you sure you want to Exit?",buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="Yes",
                    on_release=self.close_app_confirm
                )
            ])
        self.warning_btn.open()
        
    def close_app_confirm(self,obj):
        self.app = MDApp.get_running_app()
        self.app.stop()
    def close_dialog(self,obj):
        self.warning_btn.dismiss()
class InfoScreen(Screen):
    def switch_to_mainscreen(self):
        self.manager.current = "main_screen"

class PlayzoneScreen(Screen):
    attempt_history = []

    def switch_to_victoryscreen(self):
        self.manager.current = "victorypage"

    def switch_to_mainscreen(self):
        self.manager.current = "main_screen"

    def attempt_processor(self):
        user_attempt = str(self.ids.attempt.text)
        attempt = user_attempt
        id_count = str(sum(1 for digit in attempt if digit in hidden_number))
        pos_count = str(sum(1 for i in range(4) if attempt[i] == hidden_number[i]))
        self.attempt_history.append([attempt, id_count, pos_count])
        self.show_attempts()
    def show_attempts(self):
        full_history_string = ""
        for attempt, id_count, pos_count in self.attempt_history:
            history_line = f"{"":<13} {attempt:<40} {id_count:<40} {pos_count:<10}\n"
            full_history_string += history_line
        self.ids.attempt_history.text = full_history_string

class Attempts(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainScreen(name="main_screen"))
        screen_manager.add_widget(PlayzoneScreen(name="playzone"))
        screen_manager.add_widget(InfoScreen(name="infopage"))
        screen_manager.add_widget(VictoryScreen(name="victorypage"))
        return screen_manager
    def switch_theme(self, active):
        if active:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Teal"            
        else:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "LightBlue"
            
    
if __name__ == "__main__":
    Attempts().run()
