import sublime
import sublime_plugin
import os

PREFERENCES = "Preferences.sublime-settings"
PLUGIN_SETTINGS = "Theme - Faceless.sublime-settings"


def clear_all_theme_colors(pref, themes, color_list_key, color_key):
    for k, v in themes.items():
        for c in v.get(color_list_key, []):
            key = v.get(color_key, None)
            if key is not None:
                pref.erase(key % c)


def clear_all_themes(pref, themes):
    for k, v in themes.items():
        theme = v.get("theme")
        if theme is not None:
            if pref.get("theme", "") == theme:
                pref.erase("theme")


def clear_all_sizes(pref, themes):
    for s in ["xsmall", "small", "medium", "large", "xlarge"]:
        pref.erase("faceless_sidebar_tree_%s" % s)


def clear_all_widgets(themes):
    widget_path = os.path.join(sublime.packages_path(), "User")
    for k, v in themes.items():
        widget = v.get("widget_settings")
        if widget is not None:
            widget_file = os.path.join(widget_path, widget)
            if os.path.exists(widget_file):
                os.remove(widget_file)


def clear_all_features(pref, themes):
    common = [
        "faceless_active_bar",
        "faceless_solid_tab",
        "faceless_active_text",
        "faceless_dirty_bar",
        "faceless_dirty_button"
    ]
    for feat in common:
        pref.erase(feat)
    for k, v in themes.items():
        for feat in v.get("theme_specific_keys", []):
            pref.erase(feat)


class ClearFacelessThemeCommand(sublime_plugin.ApplicationCommand):
    def run(self):
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
        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("colors", [])
        widget_scheme = themes.get(theme, {}).get("widget_scheme", None)
        widget_settings = themes.get(theme, {}).get("widget_settings", None)
        theme_file = themes.get(theme, {}).get("theme", None)
        color_key = themes.get(theme, {}).get("color_key", None)
        if color not in colors or color_key is None or widget_scheme is None or theme_file is None or widget_settings is None:
            return
        pref.set("theme", theme_file)
        clear_all_theme_colors(pref, themes, "colors", "color_key")
        pref.set(color_key % color, True)
        sublime.save_settings(PREFERENCES)

        widget = sublime.load_settings(widget_settings)
        widget.set("color_scheme", widget_scheme % color)
        widget.set("draw_shadows", False)
        sublime.save_settings(widget_settings)

    def is_checked(self, color, theme):
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
        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("dirty_colors", [])
        theme_file = themes.get(theme, {}).get("theme", None)
        dirty_key = themes.get(theme, {}).get("dirty_color_key", None)
        if color not in colors or dirty_key is None or theme_file is None or pref.get("theme", "") != theme_file:
            return
        clear_all_theme_colors(pref, themes, "dirty_colors", "dirty_color_key")
        pref.set(dirty_key % color, True)
        sublime.save_settings(PREFERENCES)

    def is_checked(self, color, theme):
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("dirty_colors", [])
        theme_file = themes.get(theme, {}).get("theme", None)
        dirty_key = themes.get(theme, {}).get("dirty_color_key", None)
        pref = sublime.load_settings(PREFERENCES)
        if dirty_key is None or pref.get("theme", "") != theme_file:
            return False
        if color not in colors:
            return False
        pref = sublime.load_settings(PREFERENCES)
        return pref.get(dirty_key % color, False) == True


class SetFacelessThemeSidbarSizeCommand(sublime_plugin.ApplicationCommand):
    sidebar_sizes = ["xsmall", "small", "medium", "large", "xlarge"]
    size_key = "faceless_sidebar_tree_%s"

    def run(self, size):
        pref = sublime.load_settings(PREFERENCES)
        if size not in self.sidebar_sizes:
            return
        for s in self.sidebar_sizes:
            pref.erase(self.size_key % s)
        pref.set(self.size_key % size, True)
        sublime.save_settings(PREFERENCES)

    def is_checked(self, size):
        if size not in self.sidebar_sizes:
            return False
        pref = sublime.load_settings(PREFERENCES)
        return pref.get(self.size_key % size, False) == True


class ToggleFacelessThemeFeatureCommand(sublime_plugin.ApplicationCommand):
    def run(self, feature):
        if feature is not None:
            pref = sublime.load_settings(PREFERENCES)
            state = pref.get(feature, None)
            if state is None or state is False:
                pref.set(feature, True)
            else:
                pref.erase(feature)
            sublime.save_settings(PREFERENCES)

    def is_checked(self, feature):
        pref = sublime.load_settings(PREFERENCES)
        return pref.get(feature, False) == True
