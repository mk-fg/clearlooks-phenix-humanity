Name:        human-theme-gtk
Version:     1.1.0
Release:     1%{?dist}
Summary:     Human theme for GTK
Summary(fr): Thème Human pour GTK
License:     GPLv3+ and LGPLv2+ and CC-BY-SA
URL:         https://github.com/luigifab/human-theme
Source0:     %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:   noarch

BuildRequires: hunspell-fr
Requires: gtk-murrine-engine
Recommends: gnome-icon-theme
Recommends: dmz-cursor-themes

%description %{expand:
This theme works with GTK 2.24+ (with gtk-murrine-engine) and
GTK 3.20+ (including 3.22 and 3.24).

After installation you must restart your session.}

%description -l fr %{expand:
Ce thème fonctionne avec GTK 2.24+ (avec gtk-murrine-engine) et
GTK 3.20+ (y compris 3.22 et 3.24).

Après l'installation vous devez redémarrer votre session.}


%prep
%setup -q -n human-theme-%{version}

%build

%install
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}%{_datadir}/themes/
install -p -m 644 debian/profile.sh %{buildroot}/etc/profile.d/human-theme-gtk.sh
cp -a src/human-theme/        %{buildroot}%{_datadir}/themes/
cp -a src/human-theme-blue/   %{buildroot}%{_datadir}/themes/
cp -a src/human-theme-green/  %{buildroot}%{_datadir}/themes/
cp -a src/human-theme-orange/ %{buildroot}%{_datadir}/themes/

%files
%config(noreplace) /etc/profile.d/human-theme-gtk.sh
%license LICENSE
%doc README.md
# the entire source code is GPL-3+, except metacity-1/* which is LGPL-2.1+, and gtk-2.0/* which is CC-BY-SA-3.0+
%{_datadir}/themes/human-theme/
%{_datadir}/themes/human-theme-blue/
%{_datadir}/themes/human-theme-green/
%{_datadir}/themes/human-theme-orange/


%changelog
* Wed Nov 11 2020 Fabrice Creuzot <code@luigifab.fr> - 1.1.0-1
- Initial fedora package release (Closes: #1893327)
