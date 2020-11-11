# The Human theme

This theme works with GTK 2.24+ *(with murrine)* and GTK 3.20+ (including 3.22 and 3.24).

Debian and Fedora packages submitted: [deb](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=974209), [rpm](https://bugzilla.redhat.com/show_bug.cgi?id=1893327). Ubuntu: [PPA](https://launchpad.net/~luigifab/+archive/ubuntu/packages).

## Installation for Debian and Ubuntu

* Run: `sudo apt install human-theme-gtk` (coming soon, or via PPA)
* Restart your session

## Installation for Fedora

* Run: `sudo dnf install human-theme-gtk` (coming soon)
* Restart your session

## Manual installation for Debian and Ubuntu

* Download archive and extract *src* subdirectories in `~/.themes/`
* Configure font rendering and GTK scrollbars and QT theme, add in `/etc/environment`:
```
FREETYPE_PROPERTIES="truetype:interpreter-version=35"
GTK_OVERLAY_SCROLLING=0
QT_QPA_PLATFORMTHEME=gtk2
```
* Install icons and cursors themes: `sudo apt install gnome-icon-theme dmz-cursor-theme`
* Install [gtk2-engines-murrine](https://packages.debian.org/search?keywords=gtk2-engines-murrine) for GTK 2 apps: `sudo apt install gtk2-engines-murrine`
* Install [qt5-gtk-platformtheme](https://packages.debian.org/search?keywords=qt5-gtk-platformtheme) for QT 5 apps: `sudo apt install qt5-gtk2-platformtheme qt5-gtk-platformtheme`
* Install [gtk3-nocsd](https://packages.debian.org/search?keywords=gtk3-nocsd) to restore the window title bar: `sudo apt install gtk3-nocsd`
* Restart your session

## Manual installation for Fedora

* Download archive and extract *src* subdirectories in `~/.themes/`
* Configure font rendering and GTK scrollbars and QT theme, add in `/etc/environment`:
```
FREETYPE_PROPERTIES="truetype:interpreter-version=35"
GTK_OVERLAY_SCROLLING=0
QT_QPA_PLATFORMTHEME=gtk2
```
* Install icons and cursors themes: `sudo dnf install gnome-icon-theme dmz-cursor-themes`
* Install gtk-murrine-engine for GTK 2 apps: `sudo dnf install gtk-murrine-engine`
* Restart your session

## Firefox/Thunderbird/Chromium

For Firefox and Thunderbird and Chromium, if font rendering is bad, try this:

```bash
cd /etc/fonts/conf.d/
sudo rm 10-hinting-slight.conf # /usr/share/fontconfig/conf.avail/10-hinting-slight.conf
sudo ln -s /usr/share/fontconfig/conf.avail/10-hinting-full.conf
```

## Screenshots

Default (gtk2/gtk3)

[![Theme preview - GTK 2 - Main window](images/thumbs/gtk2.png?raw=true)](images/gtk2.png?raw=true)
[![Theme preview - GTK 2 - Menu](images/thumbs/gtk2-menu.png?raw=true)](images/gtk2-menu.png?raw=true)
[![Theme preview - GTK 3 - Main window](images/thumbs/gtk3.png?raw=true)](images/gtk3.png?raw=true)
[![Theme preview - GTK 3 - Menu](images/thumbs/gtk3-menu.png?raw=true)](images/gtk3-menu.png?raw=true)

Orange variation (gtk2/gtk3)

[![Theme preview - GTK 2 - Orange variation - Main window](images/thumbs/gtk2-orange.png?raw=true)](images/gtk2-orange.png?raw=true)
[![Theme preview - GTK 2 - Orange variation - Menu](images/thumbs/gtk2-orange-menu.png?raw=true)](images/gtk2-orange-menu.png?raw=true)
[![Theme preview - GTK 3 - Orange variation - Main window](images/thumbs/gtk3-orange.png?raw=true)](images/gtk3-orange.png?raw=true)
[![Theme preview - GTK 3 - Orange variation - Menu](images/thumbs/gtk3-orange-menu.png?raw=true)](images/gtk3-orange-menu.png?raw=true)

Blue variation (gtk2/gtk3)

[![Theme preview - GTK 2 - Blue variation - Main window](images/thumbs/gtk2-blue.png?raw=true)](images/gtk2-blue.png?raw=true)
[![Theme preview - GTK 2 - Blue variation - Menu](images/thumbs/gtk2-blue-menu.png?raw=true)](images/gtk2-blue-menu.png?raw=true)
[![Theme preview - GTK 3 - Blue variation - Main window](images/thumbs/gtk3-blue.png?raw=true)](images/gtk3-blue.png?raw=true)
[![Theme preview - GTK 3 - Blue variation - Menu](images/thumbs/gtk3-blue-menu.png?raw=true)](images/gtk3-blue-menu.png?raw=true)

Green variation (gtk2/gtk3)

[![Theme preview - GTK 2 - Green variation - Main window](images/thumbs/gtk2-green.png?raw=true)](images/gtk2-green.png?raw=true)
[![Theme preview - GTK 2 - Green variation - Menu](images/thumbs/gtk2-green-menu.png?raw=true)](images/gtk2-green-menu.png?raw=true)
[![Theme preview - GTK 3 - Green variation - Main window](images/thumbs/gtk3-green.png?raw=true)](images/gtk3-green.png?raw=true)
[![Theme preview - GTK 3 - Green variation - Menu](images/thumbs/gtk3-green-menu.png?raw=true)](images/gtk3-green-menu.png?raw=true)

Screenshots created with [A widget factory 2](https://github.com/luigifab/awf-extended).

## Known issues

* For classic menu bar and menu items of [Firefox 74-82](https://www.mozilla.org/firefox) and [Thunderbird 68-82](https://www.mozilla.org/thunderbird), see [bug 1622545](https://bugzilla.mozilla.org/show_bug.cgi?id=1622545).
* The [status bar grip](https://developer.gnome.org/gtk2/stable/GtkStatusbar.html) was removed with GTK 3 ([note1](https://developer.gnome.org/gtk3/stable/ch26s02.html#id-1.6.3.4.17), [note2](https://developer.gnome.org/gtk3/stable/GtkWindow.html#gtk-window-set-has-resize-grip)).
* The treeview zebra/even-odd row styling was removed with GTK 3.19 ([note](https://gitlab.gnome.org/GNOME/gtk/issues/581#note_746153)).
* The tabs mouse scroll was removed with GTK 3.
* Can not change previous and next arrows of pathbar.

## Dev

Run [A widget factory 2](https://github.com/luigifab/awf-extended) with screenshot on theme reload:
```
awf-gtk2 -n -s ~/2.png
awf-gtk3 -n -s ~/3.png
awf-gtk4 -n -s ~/4.png
```

Run [Entr](https://github.com/clibs/entr) to send *sighup* signal to reload theme:
```
ls ~/.themes/ubuntu-human/gtk*/gtkrc | entr killall -s SIGHUP awf-gtk2
ls ~/.themes/ubuntu-human/gtk*/*.css | entr killall -s SIGHUP awf-gtk3
ls ~/.themes/ubuntu-human/gtk*/*.css | entr killall -s SIGHUP awf-gtk4
```

Run [Imagemagick](https://imagemagick.org) to generate the diff image:
```
killall -q eom
rm -f ~/diff3.png
compare -fuzz 1% -compose src -highlight-color blue -lowlight-color none ~/2.png ~/3.png ~/diff3.png
composite ~/diff3.png ~/2.png ~/diff3.png
eom ~/diff3.png &
```

Run *svg.sh* to update SVG images. See also [technical informations](https://github.com/mk-fg/clearlooks-phenix-humanity).

## Copyright and Credits

- Current version: 1.1.0 (11/11/2020)
- Compatibility: GTK 2.24 / 3.20 / 3.22 / 3.24
- Links: [Mate Look](https://www.mate-look.org/p/1376363/), [PPA](https://launchpad.net/~luigifab/+archive/ubuntu/packages)

This theme is provided under the terms of the *GNU GPLv3+* license.

GTK 2 theme *(CC-BY-SA-3.0+)*
* Created by Kenneth Wimer and Conn O'Griofa (see [human-theme](https://packages.ubuntu.com/search?keywords=human-theme) ubuntu package)

GTK 3 theme *(GNU GPLv3+)*
* Updated by Fabrice Creuzot (luigifab)
* Forked from [Clearlooks-Phénix](https://github.com/mk-fg/clearlooks-phenix) by Mike Kazantsev (mk-fg)
* Forked from [Clearlooks-Phénix](https://github.com/jpfleury/clearlooks-phenix) by Jean-Philippe Fleury (jpfleury) and Andrew Shadura

GTK 4 theme *(GNU GPLv3+)*
* Created by Fabrice Creuzot (luigifab) from the gtk3 theme

Metacity theme *(clearlooks, GNU LGPLv2.1+)*
* Created by Daniel Borgmann and Andrea Cimitan
