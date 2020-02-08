Overview
--------

Original `Clearlooks-Phénix project`_ by `Jean-Philippe Fleury`_ is a GTK3 port
of old GTK2/GNOME2 `Clearlooks style`_.

This project is an adaptation of that to look like old Ubuntu "Human Clearlooks"
style, and GTK2 variant of `Human Quarny theme`_ in particular.

Work in progress, not ready for general use yet.

.. _Clearlooks-Phénix project: https://github.com/jpfleury/clearlooks-phenix
.. _Jean-Philippe Fleury: http://www.jpfleury.net/en/contact.php
.. _Clearlooks style: https://en.wikipedia.org/wiki/Clearlooks
.. _Human Quarny theme: https://www.gnome-look.org/p/1013593/


Notes on adapting murrine-engine GTK2 theme to GTK3
---------------------------------------------------

- Get the source code for Murrine and GTK2 theme in question:

  - `Murrine-0.98.2 GTK2 Theming Engine source at ftp.gnome.org`_ (https, not actual ftp)
  - `Human Quarny theme at gnome-look.org`_

  .. _Murrine-0.98.2 GTK2 Theming Engine source at ftp.gnome.org: https://ftp.gnome.org/pub/GNOME/sources/murrine/0.98/murrine-0.98.2.tar.xz
  .. _Human Quarny theme at gnome-look.org: https://www.gnome-look.org/p/1013593/

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

  Given "contrast = 0.9" in Human Quarny gtkrc, intermediate "spot" colors can
  be translated to GTK3 definitions as:

  - m_spot_0 shade(@selected_bg_color, 1.42);
  - m_spot_1 shade(@selected_bg_color, 1.00);
  - m_spot_2 shade(@selected_bg_color, 0.65 + (1 - 0.65) * (1 - 0.9) = 0.685);

  And actual fill / effect / border colors will be:

  - progressbar_fill @m_spot_1;
  - progressbar_effect alpha(shade(@progressbar_fill, 0.685), 0.15);
  - progressbar_border mix(@m_spot_2, @progressbar_fill, 0.28);

  background-image of that widget will be a bunch of gradients, as described by
  murrine_draw_glaze() in cairo-support.c, stripes are semi-transparent sharp
  repeating-linear-gradient on top, plus border with color from above.

- gtk-color-translate.py script can be used to get result for various GTK3 color
  expressions, e.g. ``./gtk-color-translate.py 'shade(#8f5f4a, 1.5)'`` -> ``#cf9277``.
