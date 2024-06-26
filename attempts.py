from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.transition import MDFadeSlideTransition
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRectangleFlatButton
from kivy.properties import BooleanProperty
from kivy.core.window import Window
import random
Window.size=(500,700)
nums = "123456789"
hidden_number = ''.join(random.sample(nums,4))

class Loginscreen(Screen):
    def log_in(self):
        #self.manager.current = "main_screen"
        if self.ids.username.text.isalpha() and self.ids.pw.text.isalnum():
            self.manager.current = "main_screen"
            self.manager.get_screen("main_screen").update_username(self.ids.username.text)
            self.manager.get_screen("victorypage").ids.win_txt.text=f"Congratulations {self.manager.get_screen("main_screen").ids.user_name.text}\n  You Won"

        else:
            self.error_dia = MDDialog(title="Error",
                                      text="invalid username or password",
                                      buttons=[MDRectangleFlatButton(text="OK",on_release=self.close_dia)])
            self.error_dia.open()
    def close_dia(self,obj):
        self.error_dia.dismiss()
    
class VictoryScreen(Screen):
    def switch_to_mainscreen(self):
        self.manager.current = "main_screen"
        playzone_screen = self.manager.get_screen("playzone")
        if hasattr(playzone_screen.ids, "attempt_history"):
            playzone_screen.ids.attempt_history.clear_widgets()
        if playzone_screen.clear_history_on_exit:
            playzone_screen.attempt_history = []
            if hasattr(playzone_screen.ids, "attempt_history"):
                playzone_screen.ids.attempt_history.text = ""
            if hasattr(playzone_screen.ids, "attempt"):
                playzone_screen.ids.attempt.text = ""
        
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
    def update_username(self,username):
        self.ids.user_name.text=username
class InfoScreen(Screen):
    def switch_to_mainscreen(self):
        self.manager.current = "main_screen"

class PlayzoneScreen(Screen):
    attempt_history = []
    clear_history_on_exit = BooleanProperty(default=True)
    def reset_game(self):
        self.attempt_history = []
        self.ids.attempt.text = ""  
        global hidden_number 
        hidden_number = ''.join(random.sample(nums, 4))
    
    def switch_to_mainscreen(self):
        self.manager.current = "main_screen"

    def attempt_processor(self):
        self.attempt = str(self.ids.attempt.text)
        id_count = str(sum(1 for digit in self.attempt if digit in hidden_number))
        pos_count = str(sum(1 for i in range(4) if self.attempt[i] == hidden_number[i]))
        self.attempt_history.append([self.attempt, id_count, pos_count])
        self.show_attempts()
        if self.attempt == hidden_number:
            self.manager.current = "victorypage"
        self.ids.attempt.text = ""

    def show_attempts(self):
        self.full_history_string = ""
        for attempt, id_count, pos_count in self.attempt_history:
            history_line = f"{'':<13} {attempt:<40} {id_count:<40} {pos_count:<10}\n"
            self.full_history_string += history_line
        self.ids.attempt_history.text = self.full_history_string

class Attempts(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        screen_manager = ScreenManager()
        screen_manager.add_widget(Loginscreen(name="login_screen"))
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