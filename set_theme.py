"""
Module for setting theme options.

Copyright (c) 2014 - 2015 Isaac Muse <isaacmuse@gmail.com>
License: MIT
"""
import sublime
import sublime_plugin
import os

# General settings
STV = int(sublime.version())
ST3 = int(STV) >= 3000
ST2 = 3000 < int(STV) >= 2000
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
    "aprosopo_show_tab_close_on_hover",
    "aprosopo_hide_folder_expand_icon",
    "aprosopo_hide_open_file_icons",
    "aprosopo_combined_dirty_active_bar",
    "aprosopo_popup_border"
]
SIDEBAR_SIZES = ["xsmall", "small", "medium", "large", "xlarge"]
SIDEBAR_FONT_SIZES = ["xsmall", "small", "medium", "large", "xlarge"]
SIDEBAR_COMMON_FEATURE = "aprosopo_sidebar_tree_%s"
SIDEBAR_FONT_COMMON_FEATURE = "aprosopo_sidebar_font_%s"
STATUSBAR_FONT_SIZES = ["xsmall", "small", "medium", "large", "xlarge"]
STATUSBAR_FONT_COMMON_FEATURE = "aprosopo_statusbar_font_%s"


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
    """Check if the theme is a valid variant (st2 or st3 specfic, and default format)."""

    valid = False
    if theme is not None and theme_file is not None:
        special = "@st3" if ST3 else "@st2"
        parts = os.path.splitext(theme_file)
        valid_themes = [theme_file, parts[0] + special + parts[1]]
        if check_all:
            valid_themes.append(parts[0] + ("@st3" if not ST3 else "@st2") + parts[1])
        if theme in valid_themes:
            valid = True
    return valid


def clear_all_theme_colors(pref, themes, color_list_key, color_key):
    """Clear theme color variant settings."""

    for v in themes.values():
        for c in v.get(color_list_key, []):
            key = v.get(color_key, None)
            if key is not None:
                pref.erase(key % c)


def clear_all_themes(pref, themes):
    """Clear theme from settings."""

    for v in themes.values():
        theme = v.get("theme")
        if theme is not None:
            if is_valid_theme(pref.get("theme", None), theme):
                pref.erase("theme")


def detect_current_theme(pref, themes):
    """Detect the current theme."""

    detected = None
    for k, v in themes.items():
        theme = v.get("theme")
        if theme is not None:
            theme_name = pref.get("theme", None)
            if is_valid_theme(theme_name, theme):
                detected = k
                break
    return detected


def clear_all_sizes(pref, sizes, feature):
    """Clear all sizes for feature."""

    for s in sizes:
        pref.erase(feature % s)


def clear_all_widgets(themes):
    """Remove theme widget settings."""

    widget_path = os.path.join(sublime.packages_path(), "User")
    for v in themes.values():
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
    """Clear other theme feature settings."""

    for feat in COMMON_FEATURES:
        pref.erase(feat)
    for v in themes.values():
        for feat in v.get("theme_specific_keys", []):
            pref.erase(feat)


class ClearAprosopoThemeCommand(sublime_plugin.ApplicationCommand):
    """Clear Aprosopo theme settings."""

    def run(self):
        """Clear all settings."""

        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        clear_all_themes(pref, themes)
        clear_all_theme_colors(pref, themes, "colors", "color_key")
        clear_all_theme_colors(pref, themes, "dirty_colors", "dirty_color_key")
        clear_all_sizes(pref, SIDEBAR_SIZES, SIDEBAR_COMMON_FEATURE)
        clear_all_sizes(pref, SIDEBAR_FONT_SIZES, SIDEBAR_FONT_COMMON_FEATURE)
        clear_all_sizes(pref, STATUSBAR_FONT_SIZES, STATUSBAR_FONT_COMMON_FEATURE)
        clear_all_features(pref, themes)
        clear_all_widgets(themes)
        sublime.save_settings(PREFERENCES)


class SetAprosopoThemeCommand(sublime_plugin.ApplicationCommand):
    """Set various Aprosopo theme settings."""

    def run(self, color, theme):
        """Setup and set the specified theme."""

        # Get needed theme attributes etc.
        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)

        themes = plug.get("themes", {})

        # Inherit color from alternate theme if possible
        current = detect_current_theme(pref, themes)

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

        self.set_theme_color(current, theme)

    def set_theme_color(self, current_theme, new_theme):
        """Set the theme color."""

        if current_theme is not None and current_theme != new_theme:
            sublime.run_command(
                "inherhit_aprosopo_dirty_color",
                {"old_theme": current_theme, "new_theme": new_theme}
            )
        elif current_theme is None:
            sublime.run_command(
                "set_aprosopo_theme_dirty",
                {"color": "red", "theme": new_theme}
            )

    def is_checked(self, color, theme):
        """Should menu option be check marked?."""

        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        colors = themes.get(theme, {}).get("colors", [])
        color_key = themes.get(theme, {}).get("color_key", None)
        pref = sublime.load_settings(PREFERENCES)
        if color_key is None or color not in colors:
            return False
        return pref.get(color_key % color, False) is True


class InherhitAprosopoDirtyColorCommand(sublime_plugin.ApplicationCommand):
    """Inherit the dirty color from light or dark when switching between them."""

    def run(self, old_theme, new_theme):
        """Run command."""

        # Get needed theme attributes etc.
        pref = sublime.load_settings(PREFERENCES)
        plug = sublime.load_settings(PLUGIN_SETTINGS)
        themes = plug.get("themes", {})
        old_colors = themes.get(old_theme, {}).get("dirty_colors", [])
        new_colors = themes.get(new_theme, {}).get("dirty_colors", [])
        old_dirty_key = themes.get(old_theme, {}).get("dirty_color_key", None)
        new_dirty_key = themes.get(new_theme, {}).get("dirty_color_key", None)

        for color in old_colors:
            if pref.get(old_dirty_key % color, False):
                if color in new_colors:
                    pref.erase(old_dirty_key % color)
                    pref.set(new_dirty_key % color, True)
                    sublime.save_settings(PREFERENCES)
                break


class SetAprosopoThemeDirtyCommand(sublime_plugin.ApplicationCommand):
    """Set the dirty theme setting."""

    def run(self, color, theme):
        """Run command."""

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
        """Check if menu option be checkmarked."""

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


class _SetAprosopoSizeFeature(sublime_plugin.ApplicationCommand):
    """Set Arposopo size."""

    sizes = []
    size_key = "%s"

    def run(self, size):
        """Set size."""

        pref = sublime.load_settings(PREFERENCES)
        if size not in self.sizes:
            return
        for s in self.sizes:
            pref.erase(self.size_key % s)
        pref.set(self.size_key % size, True)
        sublime.save_settings(PREFERENCES)

    def is_checked(self, size):
        """Check if menu option be checkmarked."""

        if size not in self.sizes:
            return False
        pref = sublime.load_settings(PREFERENCES)
        return pref.get(self.size_key % size, False) is True


class SetAprosopoThemeSidebarSizeCommand(_SetAprosopoSizeFeature):
    """Configure sidebar size."""

    sizes = SIDEBAR_SIZES
    size_key = SIDEBAR_COMMON_FEATURE


class SetAprosopoThemeSidebarFontSizeCommand(_SetAprosopoSizeFeature):
    """Configure sidebar font size."""

    sizes = SIDEBAR_FONT_SIZES
    size_key = SIDEBAR_FONT_COMMON_FEATURE


class SetAprosopoThemeStatusbarFontSizeCommand(_SetAprosopoSizeFeature):
    """Configure statusbar font size."""

    sizes = STATUSBAR_FONT_SIZES
    size_key = STATUSBAR_FONT_COMMON_FEATURE


class ToggleAprosopoThemeFeatureCommand(sublime_plugin.ApplicationCommand):
    """Toggle various Aprosopo theme features."""

    def run(
        self, feature,
        set_when_true=[], set_when_false=[],
        unset_when_true=[], unset_when_false=[],
        st_version=0
    ):
        """Toggle feature true or false (when false, the setting is erased)."""

        self.pref = sublime.load_settings(PREFERENCES)
        self.modified = False
        if feature is not None:
            state = self.pref.get(feature, None)
            self.handle_dependants(
                set_when_true, set_when_false,
                unset_when_true, unset_when_false, state
            )
            self.toggle_feature(feature, state)

        if self.modified:
            sublime.save_settings(PREFERENCES)

    def toggle_feature(self, feature, state):
        """Toggle a feature."""

        if state is None or state is False:
            self.pref.set(feature, True)
            self.modified = True
        elif state is not None:
            self.pref.erase(feature)
            self.modified = True

    def set_feature(self, feature, value):
        """Set the feature."""

        state = self.pref.get(feature, None)
        if value:
            if state is None or state is False:
                self.pref.set(feature, True)
                self.modified = True
        elif state is not None:
            self.pref.erase(feature)
            self.modified = True

    def handle_dependants(
        self, set_when_true, set_when_false,
        unset_when_true, unset_when_false, state
    ):
        """Handle dependants."""

        if state is None or state is False:
            for feature in set_when_true:
                self.set_feature(feature, True)

            for feature in unset_when_true:
                self.set_feature(feature, False)
        elif state is not None:
            for feature in set_when_false:
                self.set_feature(feature, True)

            for feature in unset_when_false:
                self.set_feature(feature, False)

    def is_visible(
        self, feature,
        set_when_true=[], set_when_false=[],
        unset_when_true=[], unset_when_false=[],
        st_version=0
    ):
        """Show option if ST version matches."""

        if isinstance(st_version, list):
            size = len(st_version)
            if size > 2:
                st_version = st_version[:2]
            elif size < 2:
                st_version += [None] * (2 - size)
            minimum, maximum = st_version
        else:
            minimum = st_version
            maximum = None

        return (
            STV == 0 or
            (
                minimum <= STV and
                (
                    maximum is None or STV <= maximum
                )
            )
        )

    def is_checked(
        self, feature,
        set_when_true=[], set_when_false=[],
        unset_when_true=[], unset_when_false=[],
        st_version=0
    ):
        """Determine if the menu option be checkmarked."""

        pref = sublime.load_settings(PREFERENCES)
        return pref.get(feature, False) is True
