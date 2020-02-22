.. contents::
  :backlinks: none


Overview
--------

Original `Clearlooks-Phénix project`_ by `Jean-Philippe Fleury`_ is a GTK3 port
of old GTK2/GNOME2 `Clearlooks style`_.

This project is an adaptation of that to look like old Ubuntu Human-Murrine
GTK2 theme, which can be found here too (gtk-2.0 dir) or in e.g. `Human Quarny theme`_.

Work in progress, not ready for general use yet.

.. _Clearlooks-Phénix project: https://github.com/jpfleury/clearlooks-phenix
.. _Jean-Philippe Fleury: http://www.jpfleury.net/en/contact.php
.. _Clearlooks style: https://en.wikipedia.org/wiki/Clearlooks
.. _Human Quarny theme: https://www.gnome-look.org/p/1013593/


Templating (.tpl.css files)
---------------------------

To avoid going insane from 100+ line selectors, simple custom templating is used
to transform \*.tpl.css into \*.css files via css-templater.py script.

Both source and destination files are in the repo, so it should be irrelevant
for simple theme usage, only for editing it.

Templating is intended to keep css clean and explicit wrt what is defined where.

Supported templating rules:

- ``-x-same-as``::

    toolbar -ext {
      -x-same-as: button:active, button:hover;
    }

  Removes this whole block, finds statements for "button:active" and
  "button:hover" selectors within same css and prepends "toolbar button:active,"
  and "toolbar button:hover," (prefixed) selectors to that.

  Needed because of css selector precedence logic, where e.g. overriding
  background in "toolbar button" will also affect "toolbar button:hover"
  background, and restoring those requires a lot of many-to-many prefixes.

- ``-x-same-rules``::

    toolbar button:toggle -ext {
      -x-same-rules: button:checked;
    }

  Same as ``-x-same-as``, but does not append selector(s) from rule value,
  i.e. will prepend "toolbar button:toggle," to "button:checked" block in this
  example.

  For logical grouping of elements sharing same rules, like all rules relating
  to toolbar buttons together, instead of spreading them as prefixes all over
  the place.

Other common CSS templating system - SASS/SCSS - doesn't handle all such cases
well, unfortunately, hence custom system.


Common differences between Clearlooks Gtk3 vs Human Gtk2
--------------------------------------------------------

All of these apply to looks after Gtk3 translation, with rough guess at which
original styles resulted in those looks, as per murrine_draw_rgba.c and such.

- Background gradients

  Clearlooks uses "glassy" glazed toolbars/menubars, with two gradients going up
  and down vertically from the base background color in the center.

  Human Quarny uses "gradient" toolbarstyle=2 menubarstyle=2 and such, which are
  simplier top-to-shade(0.95)-darker-bottom gradients.

- Borders

  Gtk3 Clearlooks translation uses shades of @theme_selected_bg for borders,
  while murrine engine's colors->shade[n] values derive shades from normal background,
  which have different hues in Human Quarny.

  Border size/presence do not seem to correspond very well either - missing
  completely on many clearlooks widgets, while Human Quarny ones mostly have
  lighter border on top/left and darker "shadow" bottom/right borders.

- Menus in awf-gtk3 don't seem to drop shadow.
- awf-gtk3 toolbar buttons do not have labels.


Notes on adapting murrine-engine GTK2 theme to GTK3
---------------------------------------------------

- Get the source code for Murrine and GTK2 theme in question:

  - `Murrine-0.98.2 GTK2 Theming Engine source at ftp.gnome.org`_ (https, not actual ftp)
  - gtk-2.0/gtkrc file in this repo

  .. _Murrine-0.98.2 GTK2 Theming Engine source at ftp.gnome.org: https://ftp.gnome.org/pub/GNOME/sources/murrine/0.98/murrine-0.98.2.tar.xz

- gtkrc in GTK2 style has main color definitions, e.g.::

    gtk_color_scheme = "fg_color:#101010\nbg_color:#E6DDD5\n
      base_color:#FFF\ntext_color:#1A1A1A\nselected_bg_color:#8F5F4A\n
      selected_fg_color:#FFF\ntooltip_bg_color:#F5F5B5\ntooltip_fg_color:#000"

    ...

    fg[NORMAL]        = @fg_color
    fg[PRELIGHT]      = @fg_color
    fg[ACTIVE]        = @fg_color
    fg[SELECTED]      = @selected_fg_color
    fg[INSENSITIVE]   = shade (0.65, @bg_color)

    bg[NORMAL]        = @bg_color
    bg[PRELIGHT]      = shade (1.02, @bg_color)
    bg[ACTIVE]        = shade (0.88, @bg_color)
    bg[SELECTED]      = @selected_bg_color
    bg[INSENSITIVE]   = @bg_color

    ...

  Note that base colors are defined in "gtk_color_scheme =", and pretty much all
  others derive from those.

  GTK3 supports same shade() and mix() color expressions as GTK2 - see `GTK+ CSS
  Overview - Colors`_ section for details.

  .. _GTK+ CSS Overview - Colors: https://developer.gnome.org/gtk3/stable/chap-css-overview.html#id-1.5.2.3.8

- murrine_style.c has murrine_style_realize, where most intermediate colors are
  defined, and are later used to draw widgets in murrine_draw_rgba.c and such.

  For example, murrine_rgba_draw_progressbar_fill draws animated
  diagonally-striped progress bars with following color definitions::

    MurrineRGB border = colors->spot[2];
    MurrineRGB effect;
    MurrineRGB fill = colors->spot[1];

    murrine_get_fill_color (&fill, &widget->mrn_gradient);
      // murrine_get_fill_color:
      //   if (mrn_gradient->has_gradient_colors)
      //     murrine_mix_color (&mrn_gradient->gradient_colors[1],
      //                        &mrn_gradient->gradient_colors[2],
      //                        0.5, color);
      // -- Note: gradient colors from gtkrc, if any

    murrine_shade (&fill, murrine_get_contrast(0.65, widget->contrast), &effect);
      // murrine_get_contrast:
      //   if (factor < 1.0) if (old < 1.0) return old+(1.0-old)*(1.0-factor);
      // -- Note: contrast factor defined in gtkrc, can be per-widget or global

    ...

    murrine_draw_glaze (cr, &fill,
      widget->glow_shade, widget->highlight_shade, widget->lightborder_shade, ...

    /* Draw strokes */
    ...
    murrine_set_color_rgba (cr, &effect, 0.15);
    cairo_fill (cr);

    /* Draw border */
    murrine_mix_color (&border, &fill, 0.28, &border);
    murrine_draw_border (cr, &border, ...

  Where "spot" colors are defined in murrine_style_realize as::

    double spots[] = {1.42, 1.00, 0.65};

    contrast = MURRINE_RC_STYLE (style->rc_style)->contrast;
    spots[2] = murrine_get_contrast(spots[2], contrast);

    spot_color = style->bg[GTK_STATE_SELECTED];
    murrine_shade (&spot_color, spots[0], &murrine_style->colors.spot[0]);
    murrine_shade (&spot_color, spots[1], &murrine_style->colors.spot[1]);
    murrine_shade (&spot_color, spots[2], &murrine_style->colors.spot[2]);

  Given "contrast = 0.9" in gtkrc, intermediate "spot" colors can be translated
  to GTK3 definitions as:

  - m_spot_0 shade(@selected_bg_color, 1.42);
  - m_spot_1 shade(@selected_bg_color, 1.00);
  - m_spot_2 shade(@selected_bg_color, 0.65 + (1 - 0.65) * (1 - 0.9) = 0.685);

  And actual fill / effect / border colors will be:

  - progressbar_fill @m_spot_1;
  - progressbar_effect alpha(shade(@progressbar_fill, 0.685), 0.15);
  - progressbar_border mix(@m_spot_2, @progressbar_fill, 0.28);

- background-image of that widget will be a bunch of gradients, as described by
  murrine_draw_glaze() in cairo-support.c - see `murrine-notes.txt`_ for rough
  translation.

- Stripes are semi-transparent sharp repeating-linear-gradient on top.

- Border is drawn with color from above translation.

gtk-color-translate.py script can be used to get result for various GTK3 color
expressions, e.g. ``./gtk-color-translate.py 'shade(#8f5f4a, 1.5)'`` -> ``#cf9277``.

See `murrine-notes.txt`_ for more details on how specific widget looks are composed.

.. _murrine-notes.txt: murrine-notes.txt


GTK+ Theming Documentation/Tool Links
-------------------------------------

- AWF_ (A Widget Factory) - tool to display GTK2/GTK3 themed widgets side-by-side.

  `awf-gtk3-wrapper.py`_ script can be used to start it with GTK_THEME and
  timestamped logging for output (theme syntax errors) and reload events,
  which can be triggered either by SIGQUIT (e.g. sent via ^\ in terminal) or SIGHUP,
  and debounced, in case they're triggered by e.g. staggered fanotify signals
  (sent by "fatrace-run_ -p ~user/.themes/clearlooks-phenix-humanity -f 'WD<>' --
  pkill -QUIT -F /tmp/awf-gtk3.pid" fatrace_ wrapper here).

  Specify -t/--rebuild-templates option for awf-gtk3-wrapper.py to also rebuild
  .css files from .tpl.css changes via `css-templater.py`_ script next to it.

- `GTK+ CSS Overview`_ - outlines what is possible in GTK3 CSS.
- `GTK+ CSS Properties`_ - reference for all supported CSS properties.
- `GTK+ Inspector`_ - "CSS" tab there allows to easily paste/override/test theme parts on the fly.

- `magnus (local fork with color tweaks)`_ - simple tool to zoom in on small theme elements.

  Also applies color correction to source pixels, to map relatively limited
  color range of this theme to a much large output color range, making e.g. various
  small border/gradient details much easier to distinguish visually (esp. on cheap displays).

- `Clearlooks-Phénix theme`_ - GTK3 theme which this rework is based on,
  as it looks quite like Human-Murrine GTK2 (which itself was based on
  Clearlooks), but with Clearlooks-y colors/effects.

- `Murrine GTK2 Theming Engine`_ - GTK2 engine that draws all widgets in
  Ubuntu Human-Murrine GTK2 theme (via `cairo graphics library`_).

.. _AWF: https://github.com/valr/awf
.. _awf-gtk3-wrapper.py: awf-gtk3-wrapper.py
.. _fatrace-run: https://github.com/mk-fg/fgtk/blob/master/fatrace-run
.. _fatrace: https://launchpad.net/fatrace
.. _css-templater.py: css-templater.py
.. _GTK+ CSS Overview: https://developer.gnome.org/gtk3/stable/chap-css-overview.html
.. _GTK+ CSS Properties: https://developer.gnome.org/gtk3/stable/chap-css-properties.html
.. _GTK+ Inspector: https://wiki.gnome.org/Projects/GTK/Inspector
.. _magnus (local fork with color tweaks): https://github.com/mk-fg/magnus
.. _Clearlooks-Phénix theme: https://github.com/jpfleury/clearlooks-phenix
.. _Murrine GTK2 Theming Engine: https://ftp.gnome.org/pub/GNOME/sources/murrine/0.98/murrine-0.98.2.tar.xz
.. _cairo graphics library: https://www.cairographics.org/
