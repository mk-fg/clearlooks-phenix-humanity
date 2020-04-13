# The old Ubuntu Human theme

Work in progress.

## About

This is an adaptation of [Clearlooks-Phénix](https://github.com/jpfleury/clearlooks-phenix) theme, a GTK 3 port of old GTK 2 / GNOME 2 [Clearlooks style](https://en.wikipedia.org/wiki/Clearlooks). This is also a continuation of [Human Quarny](https://www.mate-look.org/p/1013593/) theme.

This theme works with GTK 2.24+ (*gtk2-engines-murrine* is required) and GTK 3.24+, it is tested and developped with *Mate 1.24.0* and *GTK 3.24.18* under *Debian Testing*.

* [technical informations](https://github.com/mk-fg/clearlooks-phenix-humanity)
* [human-theme](https://packages.ubuntu.com/search?keywords=human-theme) ubuntu package
* [gtk2-engines-murrine](https://packages.ubuntu.com/search?keywords=gtk2-engines-murrine) ubuntu package
* [gtk2-engines-murrine](https://packages.debian.org/search?keywords=gtk2-engines-murrine) debian package
* [a widget factory 2](https://github.com/luigifab/awf)

## Installation

* Download or clone the repository in `~/.themes/old-human-theme/`
* Configure the font rendering, add in `/etc/environment`: `FREETYPE_PROPERTIES="truetype:interpreter-version=35"`
* Configure the QT styles, add in `/etc/environment`: `QT_QPA_PLATFORMTHEME=gtk2`
* Install qt5-gtk2-platformtheme and qt5-gtk-platformtheme for QT apps: `sudo apt install qt5-gtk2-platformtheme qt5-gtk-platformtheme`
* Install gtk2-engines-murrine for GTK2 apps: `sudo apt install gtk2-engines-murrine`
* Install [gtk3-nocsd](https://github.com/PCMan/gtk3-nocsd) to restore the window title bar: `sudo apt install gtk3-nocsd`
* Restart your session/xserver

## Configuration

* button have icons: where?
* menu have icons: where?
* menu can change accels: where?
* show only icons in toolbars: where?

## Screenshots

See issue #2.

## Known issues

* For classic menu bar and menu items of [Firefox 74](https://www.mozilla.org/firefox) and [Thunderbird 68](https://www.mozilla.org/thunderbird), see [bug 1622545](https://bugzilla.mozilla.org/show_bug.cgi?id=1622545).
* The [status bar grip](https://developer.gnome.org/gtk2/stable/GtkStatusbar.html) was removed with GTK 3 ([note1](https://developer.gnome.org/gtk3/stable/ch26s02.html#id-1.6.3.4.17), [note2](https://developer.gnome.org/gtk3/stable/GtkWindow.html#gtk-window-set-has-resize-grip)).
* The treeview zebra/even-odd row styling was removed with GTK 3.19 ([note](https://gitlab.gnome.org/GNOME/gtk/issues/581#note_746153)).
* The tabs mouse scroll was removed with GTK 3 ([feature 2455 for Geany](https://github.com/geany/geany/issues/2455), [feature 896 for Caja](https://github.com/mate-desktop/caja/issues/896)...).
* Can not change previous and next arrows of pathbar.

## Dev

...

Run [a widget factory 2](https://github.com/luigifab/awf) with screenshot on theme reload:
```
awf-gtk2 -s ~/2.png
awf-gtk3 -s ~/3.png
```

Run [entr](https://github.com/clibs/entr) to send sighup signal to auto reload theme:
```
ls ~/.themes/old-human-theme/gtk-3.0/*.css | entr killall -s SIGHUP awf-gtk2
ls ~/.themes/old-human-theme/gtk-3.0/*.css | entr killall -s SIGHUP awf-gtk3
```

Run [imagemagick](https://imagemagick.org) to generate the diff image:
```
compare -fuzz 1% -compose src -highlight-color blue -lowlight-color none ~/2.png ~/3.png ~/diff.png
composite ~/diff.png ~/2.png ~/diff.png
eom ~/diff.png
```

You can also run entr to auto generate the diff image:
```
ls ~/3.png | entr bash ~/.themes/old-human-theme/dev.sh
```

...

## Copyright and Credits

Todo.
