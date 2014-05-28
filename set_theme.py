import sublime
import sublime_plugin
import os

# General settings
ST3 = int(sublime.version()) >= 3000
ST2 = 3000 < int(sublime.version()) >= 2000
PREFERENCES = "Preferences.sublime-settings"

# Theme specific settings
PLUGIN_SETTINGS = "Theme - Aprosopo.sublime-settings"
COMMON_FEATURES = [
    "aprosopo_active_bar",
    "aprosopo_solid_tab",
    "aprosopo_active_text",
    "aprosopo_dirty_bar",
    "aprosopo_dirty_button",
    "aprosopo_no_file_icons",
    "aprosopo_show_tab_close_buttons",
    "aprosopo_show_tab_close_on_hover"
]
SIDEBAR_SIZES = ["xsmall", "small", "medium", "large", "xlarge"]
SIDEBAR_COMMON_FEATURE = "aprosopo_sidebar_tree_%s"


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
    elif ST3:
        parts = os.path.splitext(theme)
        special_theme = parts[0] + special + parts[1]
        resources = sublime.find_resources(special_theme)
        for r in resources:
            if r == "Packages/Theme - Aprosopo/%s" % special_theme:
                theme = special_theme
                break
    else:
        parts = os.path.splitext(theme)
        special_theme = parts[0] + special + parts[1]
        pkgs = sublime.packages_path()
        resource = os.path.join(pkgs, "Theme - Aprosopo", special_theme)
        if os.path.exists(resource):
            theme = special_theme

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
        print(valid_themes)
        print(theme)
        if check_all:
            valid_themes.append(parts[0] + ("@st3" if not ST3 else "@st2") + parts[1])
        if theme in valid_themes:
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
            special = "@st3" if ST3 else "@st2"
            parts = os.path.splitext(widget)
            widget_names = [widget, parts[0] + special + parts[1]]
            for w in widget_names:
                widget_file = os.path.join(widget_path, w)
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


class ClearAprosopoThemeCommand(sublime_plugin.ApplicationCommand):
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


class SetAprosopoThemeCommand(sublime_plugin.ApplicationCommand):
    def run(self, color, theme):
        """
        Setup and set the specified theme
        """

        # Get needed theme attributes etc.
        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("colors", [])
        theme_file = get_theme(themes.get(theme, {}), None)
        widget_settings = themes.get(theme, {}).get("widget_settings", None)
        widget_scheme = themes.get(theme, {}).get("widget_scheme", None)
        if theme_file.replace(".sublime-theme", '').endswith(("@st3", "@st2")):
            special = "@st3" if ST3 else "@st2"
            parts = os.path.splitext(widget_settings)
            widget_settings = parts[0] + special + parts[1]
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
        return pref.get(color_key % color, False) is True


class SetAprosopoThemeDirtyCommand(sublime_plugin.ApplicationCommand):
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
            theme_file is None or not (pref.get("theme", None) == theme_file)
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
        if dirty_key is None or (pref.get("theme", None) != theme_file):
            return False
        if color not in colors:
            return False
        pref = sublime.load_settings(PREFERENCES)
        return pref.get(dirty_key % color, False) is True


class SetAprosopoThemeSidbarSizeCommand(sublime_plugin.ApplicationCommand):
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
        return pref.get(self.size_key % size, False) is True


class ToggleAprosopoThemeFeatureCommand(sublime_plugin.ApplicationCommand):
    def run(self, feature, st_version=0):
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

    def is_visible(self, feature, st_version=0):
        """
        Show option if ST version matches
        """

        return st_version == 0 or (st_version == 3 and ST3) or (st_version == 2 and ST2)

    def is_checked(self, feature, st_version=0):
        """
        Should menu option be check marked?
        """

        pref = sublime.load_settings(PREFERENCES)
        return pref.get(feature, False) is True
