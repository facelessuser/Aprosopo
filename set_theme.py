import sublime
import sublime_plugin

PREFERENCES = "Preferences.sublime-settings"
PLUGIN_SETTINGS = "Theme - Faceless.sublime-settings"


def clear_all_theme_colors(pref, themes, color_list_key, color_key):
    for k, v in themes.items():
        for c in v.get(color_list_key, []):
            key = v.get(color_key, None)
            if key is not None:
                pref.erase(key % c)


class SetFacelessThemeDarkCommand(sublime_plugin.ApplicationCommand):
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


class SetFacelessThemeDarkDirtyCommand(sublime_plugin.ApplicationCommand):
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
