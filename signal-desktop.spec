%define version %(/workdir/copr/get-latest.sh | cut -c2-)

Name:		signal-desktop
Version:	%{version}
Release:	1%{?dist}
Summary:	Private messaging from your desktop
License:	GPLv3
URL:		https://github.com/signalapp/Signal-Desktop/

Source0:	https://github.com/signalapp/Signal-Desktop/archive/v%{version}.tar.gz

BuildRequires: binutils, git, python2, gcc, gcc-c++, openssl-devel, bsdtar, jq, zlib, xz, nodejs, ca-certificates, git-lfs

%if 0%{?fedora} > 35
BuildRequires: npm 
%endif

# new for AARCH64 builds
%ifarch aarch64
BuildRequires: rubygems, rubygem-json
%endif

AutoReqProv: no
Provides: signal-desktop
Requires: libnotify, libXtst, nss

%global __requires_exclude_from ^/%{_libdir}/%{name}/release/.*$
%define _build_id_links none

%description
Private messaging from your desktop

%prep
# https://bugzilla.redhat.com/show_bug.cgi?id=1793722
export SOURCE_DATE_EPOCH="$(date +"%s")"

# git-lfs hook needs to be installed for one of the dependencies
git lfs install

node --version
rm -rf Signal-Desktop-%{version}
tar xfz %{S:0}

pwd

cd Signal-Desktop-%{version}

# Allow higher Node versions
sed 's#"node": "#&>=#' -i package.json

# new for AARCH64 builds
# https://github.com/electron-userland/electron-builder-binaries/issues/49#issuecomment-1100804486
%ifarch aarch64
    gem install fpm
%endif

yarn install --frozen-lockfileyarn

%build
# https://bugzilla.redhat.com/show_bug.cgi?id=1793722
export SOURCE_DATE_EPOCH="$(date +"%s")"
echo $SOURCE_DATE_EPOCH

# https://github.com/electron-userland/electron-builder-binaries/issues/49#issuecomment-1100804486
%ifarch aarch64
    export USE_SYSTEM_FPM=true
%endif

cd %{_builddir}/Signal-Desktop-%{version} 

yarn generate
yarn build-release

%install

# Electron directory of the final build depends on the arch
%ifnarch x86_64
    %global PACKDIR linux-ia32-unpacked
%else
    %global PACKDIR linux-unpacked
%endif

# new for AARCH64 builds
%ifarch aarch64
    %global PACKDIR linux-arm64-unpacked
%endif

# copy base files
install -dm755 %{buildroot}/%{_libdir}/%{name}
cp -a %{_builddir}/Signal-Desktop-%{version}/release/%{PACKDIR}/* %{buildroot}/%{_libdir}/%{name}

install -dm755 %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/signal-desktop %{buildroot}%{_bindir}/signal-desktop

install -dm755 %{buildroot}%{_datadir}/applications/
# Changes from upstream:
# 1. Run signal WITH sandbox since it looks like there's no problems with fedora and friends
# 2. Use tray icon by default
# 3. Small fix for tray for Plasma users
cat << EOF > %{buildroot}%{_datadir}/applications/signal-desktop.desktop
[Desktop Entry]
Name=Signal
Exec=/usr/bin/signal-desktop --use-tray-icon %U
Terminal=false
Type=Application
Icon=signal-desktop
StartupWMClass=Signal
Comment=Private messaging from your desktop
MimeType=x-scheme-handler/sgnl;
Categories=Network;InstantMessaging;Chat;
EOF

for i in 16 24 32 48 64 128 256 512 1024; do
    install -dm755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
    install -Dm 644 %{_builddir}/Signal-Desktop-%{version}/build/icons/png/${i}x${i}.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_datadir}/*

%Changelog

* Wed Apr 26 2023 test   %{version}
- Auto Update
