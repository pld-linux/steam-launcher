
# TODO:
#	- port distribution-specific scripts to PLD

Summary:	Launcher for the Steam software distribution service
Name:		steam-launcher
Version:	1.0.0.47
Release:	0.1
License:	distributable
Group:		Applications
Source0:	http://repo.steampowered.com/steam/pool/steam/s/steam/steam_%{version}.tar.gz
# Source0-md5:	c6f75ebaa9e32f2565df620d1867f274
URL:		http://store.steampowered.com/
Requires:	curl
Requires:	glibc >= 2.15
Requires:	pld-release
Requires:	xterm
Requires:	xz
Requires:	zenity
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Steam is a software distribution service with an online store,
automated installation, automatic updates, achievements, SteamCloud
synchronized savegame and screenshot functionality, and many social
features.

%prep
%setup -qn steam

%build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_docdir}/steam/{README,steam_install_agreement.txt}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%update_desktop_database_postun
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%doc steam_install_agreement.txt
%attr(755,root,root) %{_bindir}/steam
%attr(755,root,root) %{_bindir}/steamdeps
%dir %{_libdir}/steam
%{_libdir}/steam/bootstraplinux*.tar.xz
%{_desktopdir}/steam.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_mandir}/man6/steam.6*
%{_pixmapsdir}/*.png
