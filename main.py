from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard

import subprocess
import sys
import os
import random

players = {}
players = set(players)

KV = """
ScreenManager:
    id: screen_manager
    MainScreen:
    RegisterScreen:

<RegisterScreen>
    name: 'register'
    MDCard:
        
        size_hint: 1, None
        pos_hint: {'top': 0.93}
        orientation: 'horizontal'
        spacing: dp(10)
        MDTextField:
            id: research_field
            hint_text: 'rechercher un joueur'
            on_text: app.screen.get_screen('register').research(text=self.text)
        MDIconButton:
            icon: 'refresh'
            md_bg_color: 'blue'
            on_release: app.screen.get_screen('register').display_list()

    MDNavigationRailFabButton:
        icon: "arrow-left"
        pos_hint: {"top": 0.98, 'center_x':0.5}
        opacity: 1
        
        on_release:
            app.set_screen("main", "right")
    
    MDBoxLayout:
        orientation: 'vertical'
        padding: '70px'
        pos_hint: {'top': 0.85}
        ScrollView:
            scroll_timeout: 100

            MDList:
                id: list
    MDCard:
        size_hint: 1, None
        orientation: 'horizontal'
        MDCard:
        MDLabel:
            id: number
            text: '-0-'
            size_hint: None, None
            halign: 'center'
        MDCard:

<MainScreen>
    name: 'main'
    MDNavigationRailFabButton:
        icon: "arrow-right"
        pos_hint: {"top": 0.98,'center_x': 0.5}
        opacity: 1
        
        on_release:
            app.set_screen("register", "left")

    MDBoxLayout:
        orientation: 'vertical'
        spacing: '10px'
        padding: '70px'
        MDCard:
            size_hint: 1, None
            orientation: 'horizontal'
            MDCard:
            MDRectangleFlatButton:
                id: vs_text
                text: "1vs1"
                on_release: app.screen.get_screen('main').display_dropdown(self)
            MDCard:

        MDCard:
            id:vs_card
            size_hint: 1, None
            Card1v1:

        MDCard:
            size_hint: 1, None
            
            orientation: 'horizontal'
            MDCard:
                

            MDFillRoundFlatButton:
                id: next_round_button
                text: 'next round'
                size_hint: None, None
                pos_hint: {'center_y': 0.5}
                on_release:
                    app.next_round()
            MDCard:
                

<Card1v1>
    id: 1v1_card
    size_hint: 1, 1
    
    orientation: 'horizontal'
    halign: 'center'
    spacing: '10px'
    MDCard:
        size_hint_y: None
        MDFlatButton:
            id: player1_1v1
            size_hint: 1, None
            pos_hint: {'center_y': 0.5}
            text: 'player 1'
            md_bg_color: 'green'
            on_release: app.screen.get_screen('main').change_color(self)
    MDCard:
        size_hint_y: None        
        MDFlatButton:
            id: player2_1v1
            size_hint: 1, None
            pos_hint: {'center_y': 0.5}
            text: 'player 2'
            md_bg_color: 'green'
            on_release: app.screen.get_screen('main').change_color(self)

<Card2v2>
    id: 2v2_card
    size_hint: 1, None
    
    orientation: 'vertical'
    halign: 'center'
    spacing: '10px'
    MDCard:
        size_hint: 1, 1
        
        spacing: dp(10)
        MDCard:
            MDFlatButton:
                id: player1_2v2
                size_hint: 1, None
                text: 'player 1'
                md_bg_color: 'green'
                on_release: app.screen.get_screen('main').change_color(self)
        MDCard:     
            MDFlatButton:
                id: player2_2v2
                size_hint: 1, None
                text: 'player 2'
                md_bg_color: 'green'
                on_release: app.screen.get_screen('main').change_color(self)
    MDCard:
        size_hint: 1, 1
        spacing: dp(10)
        MDCard:
            MDFlatButton:
                id: player3_2v2
                size_hint: 1, None
                text: 'player 3'
                md_bg_color: 'green'
                on_release: app.screen.get_screen('main').change_color(self)
        MDCard:       
            MDFlatButton:
                id: player4_2v2
                size_hint: 1, None
                text: 'player 4'
                md_bg_color: 'green'
                on_release: app.screen.get_screen('main').change_color(self)
"""
class Card1v1(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Card2v2(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MainScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self):
        self.card_1v1 = Card1v1()
        self.card_2v2 = Card2v2()

    def set_vs_text(self, caller_item, texte):
        caller_item.text = texte
        self.dropdown_menu.dismiss()
        self.add_vs_card(caller_item)


    def display_dropdown(self, caller_item):
        menu_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": i,
                    "on_release": lambda x=(i) : self.set_vs_text(caller_item, x)
                }
                for i in ["1vs1", "2vs2"]
            ]

        self.dropdown_menu = MDDropdownMenu(caller=caller_item, items=menu_items, width_mult=3, position='top')

        self.dropdown_menu.open()

    def add_vs_card(self, caller_item):
        global players
        
        if "2" in caller_item.text:
            self.children[0].children[1].clear_widgets()
            self.children[0].children[1].add_widget(self.card_2v2)
            app.get_players()
            app.load_players(random.sample(list(players), k=4))

        elif "1" in caller_item.text:
            self.children[0].children[1].clear_widgets()
            self.children[0].children[1].add_widget(self.card_1v1)
            app.get_players()
            app.load_players(random.sample(list(players), k=2))

        

    def change_color(self, player_card):
        print(player_card.md_bg_color)
        if player_card.md_bg_color == [1.0, 0.0, 0.0, 1.0]: # red
            player_card.md_bg_color = [0.0, 0.5019607843137255, 0.0, 1.0]

        elif player_card.md_bg_color == [0.0, 0.5019607843137255, 0.0, 1.0]: # green
            player_card.md_bg_color = [1.0, 0.0, 0.0, 1.0]
        
class RegisterScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self):
        self.display_list()

    def on_leave(self):
        app.next_round()

    def research(self, text):
        if text == "":
            self.display_list()
            return

        temporary_item_text = []

        list_to_use = app.get_players()

        for list_item in list_to_use:
            if text in list_item:
                temporary_item_text.append(list_item)
        print(temporary_item_text)
        
        self.ids.list.clear_widgets()

        for name in temporary_item_text:
            self.ids.list.add_widget(OneLineListItem(text=name ,on_release=
                lambda x, name=name: self.display_dialog(name)))

    def display_list(self):
        global players

        app.get_players()

        liste = list(players)
        print(liste)

        self.ids.list.clear_widgets()

        for name in liste:

            item = OneLineListItem(text=name ,on_release=
                lambda x, name=name: self.display_dialog(name))

            self.ids.list.add_widget(item)

        self.ids.number.text = str(len(liste))

    def display_dialog(self, player_name):
        dialog = MDDialog(text= f"Voulez-vous Supprimer :{player_name} ?", buttons=[
                        MDFlatButton(
                            text="Non",
                            on_release=lambda x: close_dialog()
                        ),
                        MDFlatButton(
                            text="Oui",
                            id="OK_button",
                            on_release=lambda x: remove_player(player_name)
                        ),
                    ])
        dialog.open()

        def close_dialog():
            dialog.dismiss()
            self.display_list()

        def remove_player(player_name):
            print("removing from database...")
            self.ids.research_field.text = ""
            app.remove_player(player_name)
            close_dialog()

class Ludo(MDApp):
    def build(self):
        self.title = 'Concours LUDO Polytech Days'
        self.screen = Builder.load_string(KV)
        self.get_players()
        self.load_players(random.sample(list(players), k=2))
        return self.screen

    def remplir_liste(self):
        liste = list(players)

        list_items = [
            {
                "viewclass": "OneLineListItem",
                "text": str(liste[i]),
                "on_release": lambda x=(str(liste[i])): self.remove_player(x)
            }
            for i in range(len(liste))
        ]

        for i in range(len(liste)):
            item = OneLineListItem(text=str(liste[i]), width='120px', on_release=lambda x=(str(liste[i])): self.remove_player(x))
            self.screen.get_screen('register').ids.liste.add_widget(item)

    def set_screen(self, screen, direction):
        self.screen.transition = SlideTransition(direction=direction)
        self.screen.current = screen

    def load_players(self, choosen):
        if '1' in self.screen.get_screen('main').ids.vs_text.text:
            #update UI des 1v1 card
            self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_1v1.text = choosen[0]
            self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_1v1.text = choosen[1]

        elif '2' in self.screen.get_screen('main').ids.vs_text.text:
            #update UI de 2v2 card
            self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_2v2.text = choosen[0]
            self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_2v2.text = choosen[1]
            self.screen.get_screen('main').ids.vs_card.children[0].ids.player3_2v2.text = choosen[2]
            self.screen.get_screen('main').ids.vs_card.children[0].ids.player4_2v2.text = choosen[3]

    def get_players(self):
        global players
        players = set({})

        with open("players.txt", "r") as f:
            line = f.readlines()
        
        for name in line:
            name = name.rstrip("\n")
            players.add(name)
        
        return players

    def next_round(self):
        global players

        def remove_players_from_card(self): # verifie les players à supprimer puis applique les modifs dans le fichier .txt
            if '1' in self.screen.get_screen('main').ids.vs_text.text:
                if self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_1v1.md_bg_color == [1.0, 0.0, 0.0, 1.0]: # red
                    self.remove_player(self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_1v1.text)

                if self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_1v1.md_bg_color == [1.0, 0.0, 0.0, 1.0]: # red
                    self.remove_player(self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_1v1.text)

            elif '2' in self.screen.get_screen('main').ids.vs_text.text:
                if self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_2v2.md_bg_color == [1.0, 0.0, 0.0, 1.0]: # red
                    self.remove_player(self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_2v2.text)

                if self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_2v2.md_bg_color == [1.0, 0.0, 0.0, 1.0]: # red
                    self.remove_player(self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_2v2.text)
                if self.screen.get_screen('main').ids.vs_card.children[0].ids.player3_2v2.md_bg_color == [1.0, 0.0, 0.0, 1.0]: # red
                    self.remove_player(self.screen.get_screen('main').ids.vs_card.children[0].ids.player3_2v2.text)

                if self.screen.get_screen('main').ids.vs_card.children[0].ids.player4_2v2.md_bg_color == [1.0, 0.0, 0.0, 1.0]: # red
                    self.remove_player(self.screen.get_screen('main').ids.vs_card.children[0].ids.player4_2v2.text)

        def update_UI(choosen):
            if '1' in self.screen.get_screen('main').ids.vs_text.text:
                #update UI des 1v1 card
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_1v1.text = choosen[0]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_1v1.md_bg_color = [0.0, 0.5019607843137255, 0.0, 1.0]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_1v1.text = choosen[1]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_1v1.md_bg_color = [0.0, 0.5019607843137255, 0.0, 1.0]

            elif '2' in self.screen.get_screen('main').ids.vs_text.text:
                #update UI de 2v2 card
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_2v2.text = choosen[0]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player1_2v2.md_bg_color = [0.0, 0.5019607843137255, 0.0, 1.0]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_2v2.text = choosen[1]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player2_2v2.md_bg_color = [0.0, 0.5019607843137255, 0.0, 1.0]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player3_2v2.text = choosen[2]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player3_2v2.md_bg_color = [0.0, 0.5019607843137255, 0.0, 1.0]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player4_2v2.text = choosen[3]
                self.screen.get_screen('main').ids.vs_card.children[0].ids.player4_2v2.md_bg_color = [0.0, 0.5019607843137255, 0.0, 1.0]
        
        remove_players_from_card(self)
        self.get_players()

        if len(players) < 4:
            choosen = random.sample(list(players), k=2)

            self.screen.get_screen('main').ids.vs_text.text = '1vs1'
            self.screen.get_screen('main').add_vs_card(self.screen.get_screen('main').ids.vs_text)

            update_UI(choosen)
            self.screen.get_screen('main').children[0].children[1].disabled = True
            self.screen.get_screen('main').ids.vs_text.disabled = True
            self.screen.get_screen('main').ids.next_round_button.disabled = True
            return

        if '1' in self.screen.get_screen('main').ids.vs_text.text:
            choosen = random.sample(list(players), k=2)

        elif '2' in self.screen.get_screen('main').ids.vs_text.text:
            choosen = random.sample(list(players), k=4)

        update_UI(choosen=choosen)
        
    def remove_player(self, player_name): # interagit seulement avec la liste .txt
        with open('players.txt', 'r') as f:
            contenu = f.read()

        nouveau_contenu = contenu.replace(player_name, ',')

        with open('players.txt', 'w') as f:
            f.write(nouveau_contenu)

        with open('players.txt', 'r') as f:
            contenu = f.read()

        nouveau_contenu = contenu.replace(',\n', '')

        with open('players.txt', 'w') as f:
            f.write(nouveau_contenu)

#programme principal
if __name__ == '__main__':
    def create_file(filename):
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write("Ce fichier contient le nom des joueurs. ATTENTION: 1 joueur par ligne, 1 saut de ligne à la fin du fichier pour ne pas causer d'erreur ")

    def verify_players_db(filename):
        with open(filename, 'r') as f:
            contenu = f.readlines()

        if len(contenu) <= 3:
            return False
        else: return True

    def open_file_with_default_editor(filename):
        try:
            if sys.platform == 'darwin':  # Pour macOS
                subprocess.run(['open', filename])
            elif sys.platform == 'win32':  # Pour Windows
                os.startfile(filename)
            elif sys.platform.startswith('linux'):  # Pour Linux
                subprocess.run(['xdg-open', filename])
            else:
                print("Le système d'exploitation n'est pas pris en charge.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    create_file('players.txt')

    if not verify_players_db('players.txt'):
        open_file_with_default_editor('players.txt')
    else:
        app = Ludo()
        app.run()