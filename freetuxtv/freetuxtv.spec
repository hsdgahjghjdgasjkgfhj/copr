%define version __VERSION__

Name:		freetuxtv
Version:	%{version}
Release:	1%{?dist}
Summary:	FreetuxTV is a Linux media player based on GTK+ and LibVLC for watching and recording free WebTV, WebRadio and WebCam channels on a PC.
License:	GPLv3
URL:		https://github.com/freetuxtv/freetuxtv

Source0:	https://github.com/freetuxtv/freetuxtv/archive/freetuxtv-%{version}.tar.gz

BuildRequires: git gcc autoconf automake make gettext gtk3-devel vlc vlc-devel sqlite-devel libcurl-devel libnotify-devel intltool dbus-glib-devel libtool dbus-glib-devel

Provides: freetuxtv
Requires: gtk3 glib libsqlite3x vlc libcurl libnotify

%global __requires_exclude_from ^/%{_libdir}/%{name}/release/.*$
%define _build_id_links none

%description
FreetuxTV is a Linux media player based on GTK+ and LibVLC for watching and recording free WebTV, WebRadio and WebCam channels on a PC.

%prep
# https://bugzilla.redhat.com/show_bug.cgi?id=1793722
export SOURCE_DATE_EPOCH="$(date +"%s")"
tar xfz %{S:0}
pwd
cd freetuxtv-freetuxtv-%{version}

%build
# https://bugzilla.redhat.com/show_bug.cgi?id=1793722
export SOURCE_DATE_EPOCH="$(date +"%s")"
echo $SOURCE_DATE_EPOCH

cd %{_builddir}/freetuxtv-freetuxtv-%{version} 

./autogen.sh --prefix=%{buildroot}/usr

%install
cd %{_builddir}/freetuxtv-freetuxtv-%{version}

make
make install 

cat << EOF > %{buildroot}%{_datadir}/applications/freetux.desktop
[Desktop Entry]
Name=FreetuxTV
Exec=/usr/bin/freetuxtv
Terminal=false
Type=Application
Icon=freetux
StartupWMClass=Freetux
Comment=IPTV for Linux
MimeType=x-scheme-handler/ftx;
Categories=Multimedia;TV;
EOF

for i in 16 22 32 48 64 128; do
    install -dm755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
    install -Dm 644 %{_builddir}/freetuxtv-freetuxtv-%{version}/data/icons/hicolor_apps_${i}x${i}_freetuxtv.png  %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/*
%Changelog

* Wed Apr 26 2023 test   %{version}
- Auto Update
