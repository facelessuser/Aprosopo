# Unnamed Theme #2 (until I come up with a better name)
A personal theme based loosely on Soda Theme by Ian Hill (http://buymeasoda.com/).

<img src="https://dl.dropboxusercontent.com/u/342698/UnnamedTheme2/Window%20Purple.png" border="0">

Except for the blatant reuse of the soda icons, all of the other graphics have been created from scratch, though styling takes inspiration from themes mentioned below.  Eventually I will get around to creating search icons...probably...

Unnamed Theme 2 takes inspiration from:

- Phoenix Theme: https://github.com/netatoo/phoenix-theme
- Nil Theme: https://github.com/nilium/st2-nil-theme
- Flatland Theme: https://github.com/thinkpixellab/flatland
- Tommorrow Night Eighties Color Scheme: https://github.com/chriskempson/tomorrow-theme

# Overview
It is highly configurable in regards to to setting colors and styles of `active` and `dirty` indicators.

Example of some tab style cominations (blue dark theme with red dirty color):

<img src="https://dl.dropboxusercontent.com/u/342698/UnnamedTheme2/TabCombos.png" border="0">

Sidebar (green dark theme with red dirty color):

<img src="https://dl.dropboxusercontent.com/u/342698/UnnamedTheme2/Sidebar%20Green.png" border="0">

Find panel (yellow dark theme with red dirty color):

<img src="https://dl.dropboxusercontent.com/u/342698/UnnamedTheme2/FindBar%20Yellow.png" border="0">

# Questions
## Package Control Distribution?
I don't know.  I really did this just for personal use, but I usually open up personal plugins to others.  If well received, then maybe.

## Light Option?
It is planned, but I don't really use light themes...so if/when I get around to it.  Maybe a pull request...

## ST3 and ST2?
As far as I know.

## Retina?
Theoretically, but I don't have a retina display to test on.

# Installation
Clone as `Theme - Faceless` in Sublime's `Packages` folder.  If I can ever think of a good name, this will change.

```bash
git clone https://github.com/facelessuser/UnnamedTheme2/ "Theme - Faceless"
```

# Setup
Everything is driven via the menu.  Go to `Preferences > Package Settings > Theme - Faceless` and set the theme with the color of your choice (a restart may be required after initially setting the theme, but subsequent color and feature changes shouldn't require a restart).  Themes can be unset from the menu as well which should completely cleanup all settings etc.

<img src="https://dl.dropboxusercontent.com/u/342698/UnnamedTheme2/Theme%20Menu.png" border="0">

# Features
- Theme and theme settings can all be set via the menu
- Select different theme color variations
- Select different dirty indicator colors
- Optionally highlight active tab text
- Optionally show a active tab bar
- Optionally highlight the entire active tab
- Optionally show a dirty tab bar (works with active bar as well)
- Configurable sidebar spacing

# Customizing
For personal tweaking, feel free to do whatever; fork it, mod it, and share it.  **There is no promise I will accept varations on the offical branch**, but if the desire is to add additional variations to the current set of themes on the offical repo, the following guidlines would need to be followed (assuming the proposed theme is accepted):

## Graphic Assets
Variations can have their own graphics, but shared assets with the current default theme(s) probably need to be moved to the `Common` folder location so as not to duplicate graphics with no reason.

## Themes with Tweaked Active and Dirty Colors
Creating themes that just change the highlight colors (active colors and dirty colors) can be tweaked without touching graphics since all colors are applied in the theme with `tint` attribute on the layers.  The colors should trigger off settings following the setting name template found in the [Theme Settings](#theme-settings) section.

## Theme Settings
Separate themes should use their own specifier for colors `faceless_<theme_subset>_<color>` and `faceless_<theme_subset>_dirty_<color>` etc., but they should generally try to honour the global settings of `faceless_sidebar_tree_<size>`, `faceless_active_bar`, `faceless_solid_tab`, `faceless_active_text`, `faceless_dirty_bar`, and `faceless_dirty_button`.  They can ignore these features if they really can't be applied, but they really shouldn't use different feature names.  Active and dirty colors attribute formats are defined in `Theme - Faceless.sublime-settings` along with other important theme settings.  These settings are used by the menu system plugin to set theme environments and clean up other theme settings when themes are switched.  A theme can add new feature settings, but they should be defined in `theme_specific_keys` so the cleanup function can remove them when unsetting the themes.

Example theme settings:
```javascript
        "dark": {
            "colors": ["aqua", "blue", "green", "orange", "purple", "red", "yellow"],
            "dirty_colors": ["aqua", "blue", "green", "orange", "purple","red", "yellow"],
            "widget_scheme": "Packages/Theme - Faceless/Dark/Widget - %s.stTheme",
            "widget_settings": "Widget - Faceless Dark.sublime-settings",
            "theme": "Faceless Dark.sublime-theme",
            "color_key": "faceless_dark_%s",
            "dirty_color_key": "faceless_dark_dirty_%s",
            "theme_specific_keys": []
        }
```

## Aggressive changes
For more aggressive theme tweaks to look and feel, graphics will have to be modified, but the themes should still play nice with the framework.  If the theme deviates too far from the general look and feel, it may just need to be distributed as a different theme.
