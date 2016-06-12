from button import Button

class WaitButton(Button):
    def __init__(self, image, x, y, parent):
        super(WaitButton, self).__init__(image, x, y, parent)

    def get_clicked(self):
        self.parent.game_manager.selected_hero.has_moved = True
        self.parent.game_manager.selected_hero.image = self.parent.game_manager.selected_hero.moved_image
        self.parent.game_manager.selected_hero.has_reached_goal = False
        self.parent.game_manager.selected_hero.origin = None
        self.parent.game_manager.selected_hero = None
        self.parent.state = self.parent.states["0"]

        self.parent.reset_buttons()

        self.parent.game_manager.state = self.parent.game_manager.states["0"]


