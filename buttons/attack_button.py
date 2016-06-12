from button import Button


class AttackButton(Button):
    def __init__(self, image, x, y, parent):
        super(AttackButton, self).__init__(image, x, y, parent)

    def get_clicked(self):
        self.parent.game_manager.state = self.parent.game_manager.states["3"]
        self.parent.reset_buttons()