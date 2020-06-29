# The old Ubuntu Human theme

This is an adaptation of [Clearlooks-Phénix](https://github.com/jpfleury/clearlooks-phenix) theme, a GTK 3 port of old GTK 2 / GNOME 2 [Clearlooks style](https://en.wikipedia.org/wiki/Clearlooks). This is also a continuation of [Human Quarny](https://www.mate-look.org/p/1013593/) theme.

It works with GTK 2.24+ (*gtk2-engines-murrine* is required) and GTK 3.20+ (including 3.22 and 3.24) and GTK 3.98+, it is tested and developped with *Mate 1.24.0* and *GTK 3.24.18* under *Debian Testing*.

* [technical informations](https://github.com/mk-fg/clearlooks-phenix-humanity)
* [human-theme](https://packages.ubuntu.com/search?keywords=human-theme) ubuntu package
* [gtk2-engines-murrine](https://packages.ubuntu.com/search?keywords=gtk2-engines-murrine) ubuntu package
* [gtk2-engines-murrine](https://packages.debian.org/search?keywords=gtk2-engines-murrine) debian package
* [a widget factory 2](https://github.com/luigifab/awf-extended)

## Installation

* Download archive and extract *themes* subdirectories in `~/.themes/`
* Configure font rendering and scrollbars and QT styles, add in `/etc/environment`:
```
FREETYPE_PROPERTIES="truetype:interpreter-version=35"
GTK_OVERLAY_SCROLLING=0
QT_QPA_PLATFORMTHEME=gtk2
```
* Install qt5-gtk2/3-platformtheme for QT 5 apps: `sudo apt install qt5-gtk2-platformtheme qt5-gtk-platformtheme`
* Install gtk2-engines-murrine for GTK 2 apps: `sudo apt install gtk2-engines-murrine`
* Install [gtk3-nocsd](https://github.com/PCMan/gtk3-nocsd) to restore the window title bar: `sudo apt install gtk3-nocsd`
* Configure Firefox/Thunderbird/Chromium font rendering:
```bash
cd /etc/fonts/conf.d/
sudo rm 10-hinting-slight.conf #/usr/share/fontconfig/conf.avail/10-hinting-slight.conf
sudo ln -s /usr/share/fontconfig/conf.avail/10-hinting-full.conf
```
* Restart your session/xserver

## Screenshots

Default (gtk2/gtk3)

[![Theme preview - GTK 2 - Main window](images/thumbs/gtk2.png?raw=true)](images/gtk2.png?raw=true)
[![Theme preview - GTK 2 - Menu](images/thumbs/gtk2-menu.png?raw=true)](images/gtk2-menu.png?raw=true)
[![Theme preview - GTK 3 - Main window](images/thumbs/gtk3.png?raw=true)](images/gtk3.png?raw=true)
[![Theme preview - GTK 3 - Menu](images/thumbs/gtk3-menu.png?raw=true)](images/gtk3-menu.png?raw=true)

Orange variation (gtk2/gtk3)

[![Theme preview - GTK 2 - Main window](images/thumbs/gtk2-orange.png?raw=true)](images/gtk2-orange.png?raw=true)
[![Theme preview - GTK 2 - Menu](images/thumbs/gtk2-orange-menu.png?raw=true)](images/gtk2-orange-menu.png?raw=true)
[![Theme preview - GTK 3 - Main window](images/thumbs/gtk3-orange.png?raw=true)](images/gtk3-orange.png?raw=true)
[![Theme preview - GTK 3 - Menu](images/thumbs/gtk3-orange-menu.png?raw=true)](images/gtk3-orange-menu.png?raw=true)

Blue variation (gtk2/gtk3)

[![Theme preview - GTK 2 - Main window](images/thumbs/gtk2-blue.png?raw=true)](images/gtk2-blue.png?raw=true)
[![Theme preview - GTK 2 - Menu](images/thumbs/gtk2-blue-menu.png?raw=true)](images/gtk2-blue-menu.png?raw=true)
[![Theme preview - GTK 3 - Main window](images/thumbs/gtk3-blue.png?raw=true)](images/gtk3-blue.png?raw=true)
[![Theme preview - GTK 3 - Menu](images/thumbs/gtk3-blue-menu.png?raw=true)](images/gtk3-blue-menu.png?raw=true)

Green variation (gtk2/gtk3)

[![Theme preview - GTK 2 - Main window](images/thumbs/gtk2-green.png?raw=true)](images/gtk2-green.png?raw=true)
[![Theme preview - GTK 2 - Menu](images/thumbs/gtk2-green-menu.png?raw=true)](images/gtk2-green-menu.png?raw=true)
[![Theme preview - GTK 3 - Main window](images/thumbs/gtk3-green.png?raw=true)](images/gtk3-green.png?raw=true)
[![Theme preview - GTK 3 - Menu](images/thumbs/gtk3-green-menu.png?raw=true)](images/gtk3-green-menu.png?raw=true)

## Known issues

* For classic menu bar and menu items of [Firefox 74-77](https://www.mozilla.org/firefox) and [Thunderbird 68-77](https://www.mozilla.org/thunderbird), see [bug 1622545](https://bugzilla.mozilla.org/show_bug.cgi?id=1622545).
* The [status bar grip](https://developer.gnome.org/gtk2/stable/GtkStatusbar.html) was removed with GTK 3 ([note1](https://developer.gnome.org/gtk3/stable/ch26s02.html#id-1.6.3.4.17), [note2](https://developer.gnome.org/gtk3/stable/GtkWindow.html#gtk-window-set-has-resize-grip)).
* The treeview zebra/even-odd row styling was removed with GTK 3.19 ([note](https://gitlab.gnome.org/GNOME/gtk/issues/581#note_746153)).
* The tabs mouse scroll was removed with GTK 3.
* Can not change previous and next arrows of pathbar.

## Dev

Run [a widget factory 2](https://github.com/luigifab/awf) with screenshot on theme reload:
```
awf-gtk2 -n -s ~/2.png
awf-gtk3 -n -s ~/3.png
awf-gtk4 -n -s ~/4.png
```

Run [entr](https://github.com/clibs/entr) to send sighup signal to auto reload theme:
```
ls ~/.themes/old-ubuntu-human/gtk*/*.css | entr killall -s SIGHUP awf-gtk2
ls ~/.themes/old-ubuntu-human/gtk*/*.css | entr killall -s SIGHUP awf-gtk3
ls ~/.themes/old-ubuntu-human/gtk*/*.css | entr killall -s SIGHUP awf-gtk4
```

Run [imagemagick](https://imagemagick.org) to generate (*dev.sh*) the diff image:
```
rm -f ~/diff3.png
compare -fuzz 1% -compose src -highlight-color blue -lowlight-color none ~/2.png ~/3.png ~/diff3.png
composite ~/diff3.png ~/2.png ~/diff3.png
eom ~/diff3.png
```

Run *svg.sh* to update svg images.

## Copyright and Credits

This theme is provided under the terms of the *GNU GPLv3* license.

gtk2 theme *(feel free to modify and share)*
* Created by Kenneth Wimer and Conn O'Griofa

gtk3 theme *(GNU GPLv3)*
* Updated by Fabrice Creuzot (luigifab)
* Forked from [Clearlooks-Phénix](https://github.com/mk-fg/clearlooks-phenix) by Mike Kazantsev (mk-fg)
* Forked from [Clearlooks-Phénix](https://github.com/jpfleury/clearlooks-phenix) by Jean-Philippe Fleury (jpfleury) and Andrew Shadura

gtk4 theme *(GNU GPLv3)*
* Created by Fabrice Creuzot (luigifab) from the gtk3 theme

metacity theme *(clearlooks, GNU LGPLv2.1)*
* Created by Daniel Borgmann and Andrea Cimitan
