# Aprosopo
A personal theme based loosely on Soda Theme by Ian Hill (http://buymeasoda.com/).

<img src="https://dl.dropboxusercontent.com/u/342698/UnnamedTheme2/Screenshot_Dark.png" border="0">

<img src="https://dl.dropboxusercontent.com/u/342698/UnnamedTheme2/Screenshot_Light.png" border="0">

Except for the blatant reuse of the soda icons, all of the other graphics have been created from scratch, though styling takes inspiration from themes mentioned below.  Eventually I will get around to creating search icons...probably...

Aprosopo takes inspiration from:

- Phoenix Theme: https://github.com/netatoo/phoenix-theme
- Nil Theme: https://github.com/nilium/st2-nil-theme
- Flatland Theme: https://github.com/thinkpixellab/flatland
- Tommorrow Color Schemes: https://github.com/chriskempson/tomorrow-theme

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

## ST3 and ST2?
As far as I know.

## I am using ST3 version < 3062 and I don't have sidebar icons?
ST3 version 3062 introduced new sidebar file icons.  With this new addition, the theme displays the icons differently.  If you are using an ST3 version < 3062, you can use the menu option `Disable Sidebar File Icons` to revert to the old way of displaying folder icons to restore them.

## Retina?
Theoretically, but I don't have a retina display to test on.

# Installation
Package Control is the preferred method: https://sublime.wbond.net/installation

# Manual Installation
Clone as `Theme - Aprosopo` in Sublime's `Packages` folder.

```bash
git clone https://github.com/facelessuser/Aprosopo/ "Theme - Aprosopo"
```

# Setup
Everything is driven via the menu.  Go to `Preferences > Package Settings > Theme - Aprosopo` and set the theme with the color of your choice (a restart may be required after initially setting the theme, but subsequent color and feature changes shouldn't require a restart).  Themes can be unset from the menu as well which should completely cleanup all settings etc.

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
For personal tweaking, feel free to do whatever; fork it, mod it, and share it.  **There is no promise I will accept varations on the offical branch**
