from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, MDList, IconLeftWidget
from kivymd.theming import ThemableBehavior

from screens import Screens, screen_manager


class ContentNavigationDrawer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "8dp"
        self.spacing = "16dp"
        scroll_view = ScrollView()
        scroll_view.add_widget(DrawerList())
        self.add_widget(scroll_view)


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))
    theme_text_color = "Primary"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(IconLeftWidget(icon=self.icon, theme_text_color="Custom", text_color=self.text_color))

    def on_release(self):
        self.parent.set_color_item(self)
        screen_manager.current = self.text


class DrawerList(ThemableBehavior, MDList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        icon_items = {
            "folder": Screens.REGISTER,
            "account-multiple": Screens.CALENDAR,
            "star": Screens.ASSIGN_QR,
            "history": Screens.READ_QR,
            "checkbox-marked": Screens.MISSING_DEVICES,
        }
        for icon_name in icon_items.keys():
            self.add_widget(ItemDrawer(icon=icon_name, text=icon_items[icon_name]))

    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class CustomLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = self.texture_size[1]
