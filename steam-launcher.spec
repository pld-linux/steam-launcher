Summary:	Launcher for the Steam software distribution service
Name:		steam-launcher
Version:	1.0.0.68
Release:	1
License:	distributable
Group:		Applications
Source0:	http://repo.steampowered.com/steam/pool/steam/s/steam/steam_%{version}.tar.gz
# Source0-md5:	5b1f5d233643f30cee2eba8ecaa78483
Source1:	%{name}.sysconfig
Patch0:		steamdeps.patch
Patch1:		desktop_path.patch
URL:		http://store.steampowered.com/
BuildRequires:	sed >= 4.0
Requires:	ca-certificates >= 20180409-3
Requires:	curl
Requires:	fonts-TTF-RedHat-liberation
Requires:	glibc >= 6:2.15
Requires:	libtxc_dxtn
Requires:	pld-release
Requires:	poldek
Requires:	python-modules
Requires:	rpm
Requires:	which
Requires:	xdg-user-dirs
Requires:	xterm
Requires:	xz
Requires:	zenity
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{x8664}
%define	poldek_sources	-n th -n th-i686
%else
%define	poldek_sources	-n th
%endif

%description
Steam is a software distribution service with an online store,
automated installation, automatic updates, achievements, SteamCloud
synchronized savegame and screenshot functionality, and many social
features.

%prep
%setup -qn steam-launcher
%patch0 -p1
%patch1 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' bin_steamdeps.py
%{__sed} -i -e '1s,/usr/bin/env bash,%{__bash},' bin_steam.sh

sed -i -e's/^ARCH\s*=.*$/ARCH = "%{_arch}"/' steamdeps

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/sysconfig

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_docdir}/steam/{README,steam_subscriber_agreement.txt}

# installed only when apt is installed on the build host
[ -d $RPM_BUILD_ROOT/etc/apt ] && rm -r $RPM_BUILD_ROOT/etc/apt

sed -e's/@SOURCES@/%{poldek_sources}/' %{SOURCE1} > $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%{__rm} $RPM_BUILD_ROOT%{_desktopdir}/steam.desktop
%{__mv} $RPM_BUILD_ROOT/usr/lib/steam/steam.desktop $RPM_BUILD_ROOT%{_desktopdir}/steam.desktop


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
%doc steam_subscriber_agreement.txt
%attr(755,root,root) %{_bindir}/steam
%attr(755,root,root) %{_bindir}/steamdeps
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir /usr/lib/steam
%attr(755,root,root) /usr/lib/steam/bin_steam.sh
%attr(755,root,root) /usr/lib/steam/bin_steamdeps.py
/usr/lib/steam/bootstraplinux*.tar.xz
%{_desktopdir}/steam.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_mandir}/man6/steam.6*
%{_pixmapsdir}/*.png
