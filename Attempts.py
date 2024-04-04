from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.transition import MDFadeSlideTransition
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.core.window import Window
import random
Window.size=(500,700)
nums = "123456789"
hidden_number = ''.join(random.sample(nums,4))

class VictoryScreen(Screen):
    pass
class MainScreen(Screen):
    def switch_to_playzone(self):
        self.manager.current = "playzone"
    def switch_to_infopage(self):
        self.manager.current = "infopage"
    def close_app(self):
        app = MDApp.get_running_app()
        app.stop()
    
class InfoScreen(Screen):
    def switch_to_mainscreen(self):
        self.manager.current = "main_screen"
    
class PlayzoneScreen(Screen):
    attempt_history = []
    def switch_to_mainscreen(self):
        self.transition = MDFadeSlideTransition(direction='right')
        self.manager.current = "main_screen"
    def attempt_processor(self,obj):
        self.user_attempt = str(self.ids.attempt.text)
        self.attempt = self.user_attempt
        self.id_count = str(sum(1 for digit in self.attempt if digit in hidden_number))
        self.pos_count = str(sum(1 for i in range(4) if self.attempt[i] == hidden_number[i]))
        self.attempt_history.append([self.attempt, self.id_count, self.pos_count])
        print(self.attempt_history)
    def show_attempt(self,obj):
        self.ids.showattempt.text = self.attempt
    def show_id(self,obj):
        self.ids.showid.text = self.id_count
    def show_pos(self,obj):
        self.ids.showpos.text = self.pos_count
    
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
            
    
    
Attempts().run()
