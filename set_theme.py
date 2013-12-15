import sublime
import sublime_plugin
import os

# General settings
ST3 = int(sublime.version()) >= 3000
PREFERENCES = "Preferences.sublime-settings"

# Theme specific settings
PLUGIN_SETTINGS = "Theme - Faceless.sublime-settings"
COMMON_FEATURES = [
    "faceless_active_bar",
    "faceless_solid_tab",
    "faceless_active_text",
    "faceless_dirty_bar",
    "faceless_dirty_button"
]
SIDEBAR_SIZES = ["xsmall", "small", "medium", "large", "xlarge"]
SIDEBAR_COMMON_FEATURE = "faceless_sidebar_tree_%s"


def get_theme(obj, default=None):
    """
    Get the theme for the theme object.
    See if ST2 or ST3 variant is avaliable,
    if not use the standard theme format.
    """
    special = "@st3" if ST3 else "@st2"
    theme = obj.get("theme", None)
    if theme is None:
        theme = default
    else:
        parts = os.path.splitext(theme)
        special_theme = parts[0] + special + parts[1]
        resources = sublime.find_resources(special_theme)
        for r in resources:
            if r == "Packages/Theme - Faceless/%s" % special_theme:
                theme = special_theme
                break
    return theme


def is_valid_theme(theme, theme_file, check_all=False):
    """
    Check if the theme is a valid variant (st2 or st3 specfic, and default format)
    """
    valid = False
    if theme is not None and theme_file is not None:
        special = "@st3" if ST3 else "@st2"
        parts = os.path.splitext(theme_file)
        valid_themes = [theme_file, parts[0] + special + parts[1]]
        if check_all:
            valid_themes.append(parts[0] + ("@st3" if not ST3 else "@st2") + parts[1])
        if theme in [valid_themes]:
            valid = True
    return valid


def clear_all_theme_colors(pref, themes, color_list_key, color_key):
    """
    Clear theme color variant settings
    """
    for k, v in themes.items():
        for c in v.get(color_list_key, []):
            key = v.get(color_key, None)
            if key is not None:
                pref.erase(key % c)


def clear_all_themes(pref, themes):
    """
    Clear theme from settings
    """
    for k, v in themes.items():
        theme = v.get("theme")
        if theme is not None:
            if is_valid_theme(pref.get("theme", None), theme):
                pref.erase("theme")


def clear_all_sizes(pref, themes):
    """
    Clear theme sidebar settings
    """
    for s in SIDEBAR_SIZES:
        pref.erase(SIDEBAR_COMMON_FEATURE % s)


def clear_all_widgets(themes):
    """
    Remove theme widget settings
    """
    widget_path = os.path.join(sublime.packages_path(), "User")
    for k, v in themes.items():
        widget = v.get("widget_settings")
        if widget is not None:
            widget_file = os.path.join(widget_path, widget)
            if os.path.exists(widget_file):
                os.remove(widget_file)


def clear_all_features(pref, themes):
    """
    Clear other theme feature settings
    """
    for feat in COMMON_FEATURES:
        pref.erase(feat)
    for k, v in themes.items():
        for feat in v.get("theme_specific_keys", []):
            pref.erase(feat)


class ClearFacelessThemeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        """
        Clear all settings
        """
        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        clear_all_themes(pref, themes)
        clear_all_theme_colors(pref, themes, "colors", "color_key")
        clear_all_theme_colors(pref, themes, "dirty_colors", "dirty_color_key")
        clear_all_sizes(pref, themes)
        clear_all_features(pref, themes)
        clear_all_widgets(themes)
        sublime.save_settings(PREFERENCES)


class SetFacelessThemeCommand(sublime_plugin.ApplicationCommand):
    def run(self, color, theme):
        """
        Setup and set the specified theme
        """

        # Get needed theme attributes etc.
        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("colors", [])
        widget_scheme = themes.get(theme, {}).get("widget_scheme", None)
        widget_settings = themes.get(theme, {}).get("widget_settings", None)
        theme_file = get_theme(themes.get(theme, {}), None)
        color_key = themes.get(theme, {}).get("color_key", None)

        # See if it is okay to continue
        if (
            color not in colors or color_key is None or widget_scheme is None or
            theme_file is None or widget_settings is None
        ):
            return

        # Setup theme
        pref.set("theme", theme_file)
        clear_all_theme_colors(pref, themes, "colors", "color_key")
        pref.set(color_key % color, True)
        sublime.save_settings(PREFERENCES)

        # Setup theme widget
        widget = sublime.load_settings(widget_settings)
        widget.set("color_scheme", widget_scheme % color)
        widget.set("draw_shadows", False)
        sublime.save_settings(widget_settings)

    def is_checked(self, color, theme):
        """
        Should menu option be check marked?
        """
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("colors", [])
        color_key = themes.get(theme, {}).get("color_key", None)
        pref = sublime.load_settings(PREFERENCES)
        if color_key is None or color not in colors:
            return False
        return pref.get(color_key % color, False) == True


class SetFacelessThemeDirtyCommand(sublime_plugin.ApplicationCommand):
    def run(self, color, theme):
        # Get needed theme attributes etc.
        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("dirty_colors", [])
        theme_file = get_theme(themes.get(theme, {}), None)
        dirty_key = themes.get(theme, {}).get("dirty_color_key", None)

        # See if it is okay to continue
        if (
            color not in colors or dirty_key is None or
            theme_file is None or is_valid_theme(pref.get("theme", None), theme_file)
        ):
            return

        # Set dirty color
        clear_all_theme_colors(pref, themes, "dirty_colors", "dirty_color_key")
        pref.set(dirty_key % color, True)
        sublime.save_settings(PREFERENCES)

    def is_checked(self, color, theme):
        """
        Should menu option be check marked?
        """
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("dirty_colors", [])
        theme_file = get_theme(themes.get(theme, {}), None)
        dirty_key = themes.get(theme, {}).get("dirty_color_key", None)
        pref = sublime.load_settings(PREFERENCES)
        if dirty_key is None or is_valid_theme(pref.get("theme", None), theme_file):
            return False
        if color not in colors:
            return False
        pref = sublime.load_settings(PREFERENCES)
        return pref.get(dirty_key % color, False) == True


class SetFacelessThemeSidbarSizeCommand(sublime_plugin.ApplicationCommand):
    sidebar_sizes = SIDEBAR_SIZES
    size_key = SIDEBAR_COMMON_FEATURE

    def run(self, size):
        """
        Set sidebar spacing
        """
        pref = sublime.load_settings(PREFERENCES)
        if size not in self.sidebar_sizes:
            return
        for s in self.sidebar_sizes:
            pref.erase(self.size_key % s)
        pref.set(self.size_key % size, True)
        sublime.save_settings(PREFERENCES)

    def is_checked(self, size):
        """
        Should menu option be check marked?
        """
        if size not in self.sidebar_sizes:
            return False
        pref = sublime.load_settings(PREFERENCES)
        return pref.get(self.size_key % size, False) == True


class ToggleFacelessThemeFeatureCommand(sublime_plugin.ApplicationCommand):
    def run(self, feature):
        """
        Toggle feature true or false (when false, the setting is erased)
        """
        if feature is not None:
            pref = sublime.load_settings(PREFERENCES)
            state = pref.get(feature, None)
            if state is None or state is False:
                pref.set(feature, True)
            else:
                pref.erase(feature)
            sublime.save_settings(PREFERENCES)

    def is_checked(self, feature):
        """
        Should menu option be check marked?
        """
        pref = sublime.load_settings(PREFERENCES)
        return pref.get(feature, False) == True
