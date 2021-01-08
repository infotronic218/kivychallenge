import kivy

kivy.require('2.0.0')  # replace with your current kivy version !
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

# import regular expression module
import re

# These two variables are used to block changes made by the application and allow changes made by the user.
# They are the key to avoid the application running to main loop.


input_1_action = True
input_2_action = True
# RGBA Window color (The RGB color is divided by 255 to have a number between 0 and 1)
RED = 41 / 255
GREEN = 9 / 255
BLUE = 30 / 255
OPACITY = 1

Window.clearcolor = (RED, GREEN, BLUE, OPACITY)
Window.size = (500, 200)


class FloatInput(TextInput):
    """This class extends the TextInput class and filter the user
    inputs before adding to the total number.
    Only numbers are accepted """
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class MainLayout(GridLayout):
    """This is the main layout of the application that extends GridLayout.
     The TextInputs and the Labels are displayed in 2 columns and 2 rows.
    """

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.cols = 2
        self.row_force_default = True
        self.row_default_height = 40
        self.spacing = 10
        self.padding = 20

        self.add_widget(Label(text='Number 1'))
        self.number_1_input = FloatInput(multiline=False)
        self.number_1_input.bind(text=self.update_input_1)
        self.add_widget(self.number_1_input)

        self.add_widget(Label(text='Number 2'))
        self.number_2_input = FloatInput(multiline=False)
        self.number_2_input.bind(text=self.update_input_2)
        self.add_widget(self.number_2_input)

    def update_input_1(self, instance, text):
        """ This function is a callback function and is called when the TextInput 1 value changes.
        The new text is received here. Using the input_1_action and input_2_action variables,
        we can decide to update the TextInput_2.  If input_2_action equal to True, the TextInput 2 can
        be updated and before assigning the value, we block the TextInput 1 callback by
        putting input_1_action to False.
        Try except block are used to avoid error when the user type an empty char on the TextInput field.
        An empty char can not be converted into float and this operation will generate a ValueError code and the
        application clash.
        """
        global input_1_action, input_2_action
        if input_2_action:
            input_1_action = False
            try:
                number_1 = float(text)
                self.number_2_input.text = str(number_1 + 1)
            except ValueError:
                print("Value Error! Unable to convert the text to float")
                if str(text).__eq__(""):
                    self.number_2_input.text = ""
            input_1_action = True

        print(text)

    def update_input_2(self, instance, text):
        """ This function is a callback function and is called when the TextInput 2 value changes.
        The new text is received here. Using the input_1_action and input_2_action variables,
        we can decide to update the TextInput_1. If input_1_action equal to True, the TextInput 1 can
        be updated and Before assigning the value, we block the the TextInput 2 callback by
        putting input_2_action to False.
        Try except block are used to avoid error when the user type an empty char on the TextInput field.
        An empty char can not be converted into float and this operation will generate a ValueError code and the
        application clash.
        """
        global input_1_action, input_2_action
        if input_1_action:
            input_2_action = False
            try:
                number_2 = float(text)
                self.number_1_input.text = str((1 / number_2))
            except ValueError:
                print("Value Error! Unable to convert the text to float ")
                if str(text).__eq__(""):
                    self.number_1_input.text = ""
            input_2_action = True
        print(text)


class MyApp(App):

    def build(self):
        self.title = "My Homework"
        return MainLayout()


if __name__ == '__main__':
    MyApp().run()
