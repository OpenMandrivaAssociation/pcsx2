%define _disable_ld_no_undefined 1
%define git    20190505


Summary:	Sony PlayStation 2 Emulator
Name:		pcsx2
Version:	1.5.0
Release:	1
License:	GPLv2+
Group:		Emulators
Url:		http://pcsx2.net/
#Source0:	https://github.com/PCSX2/pcsx2/archive/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}-%{git}.tar.gz

BuildRequires:	cmake
BuildRequires:  gettext
BuildRequires:	subversion
BuildRequires:	bzip2-devel
BuildRequires:	cg-devel
BuildRequires:	jpeg-devel
BuildRequires:	libaio-devel
BuildRequires:  pcap-devel
BuildRequires:	sparsehash-devel
BuildRequires:	wxgtku-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  wxgtku3.0-devel

ExclusiveArch:	%{ix86}

%description
Sony PlayStation 2 emulator. Requires a BIOS image to run. Check 
http://www.pcsx2.net/guide.php#Bios for details on which files
you need and how to obtain them.

Very fast CPU is a must. Intel Core 2 Duo or better.

%files -f %{name}.lang
%doc COPYING.*
%{_bindir}/%{name}
%{_bindir}/%{name}_*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/games/%{name}/cheats_ws.zip
%attr(0666,games,games) %{_datadir}/games/%{name}/GameIndex.dbf
%{_libdir}/games/%{name}
%{_mandir}/man1/%{name}.1*

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}-%{git}
%build
%cmake \
    -DPACKAGE_MODE=TRUE \
    -DXDG_STD=TRUE \
    -DFORCE_INTERNAL_SOUNDTOUCH=FALSE \
    -DBUILD_REPLAY_LOADERS=TRUE \
    -DDISABLE_ADVANCE_SIMD=TRUE \
    -DDISABLE_BUILD_TIME=TRUE \
    -DDISABLE_PCSX2_WRAPPER=TRUE \
    -DEXTRA_PLUGINS=TRUE \
    -DGAMEINDEX_DIR="%{_gamesdatadir}/%{name}" \
    -DPLUGIN_DIR="%{_libdir}/games/%{name}" \
    -DDOC_DIR="%{_docdir}/%{name}" \
    -DSDL2_API=TRUE \
    -DGTK3_API=FALSE

%make_build

%install
%make_install -C build

%find_lang %{name} --all-name

