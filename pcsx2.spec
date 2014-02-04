%define _disable_ld_no_undefined 1

%define revision 5875

Summary:	Sony PlayStation 2 Emulator
Name:		pcsx2
Version:	1.2.1
Release:	1
License:	GPLv2+
Group:		Emulators
Url:		http://pcsx2.net/
Source0:	%{name}-%{version}-r%{revision}-sources.tar.bz2
BuildRequires:	cmake
BuildRequires:	subversion
BuildRequires:	bzip2-devel
#BuildRequires:	cg-devel
BuildRequires:	jpeg-devel
BuildRequires:	sparsehash-devel
BuildRequires:	wxgtku-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
ExclusiveArch:	%{ix86}

%description
Sony PlayStation 2 emulator. Requires a BIOS image to run. Check 
http://www.pcsx2.net/guide.php#Bios for details on which files
you need and how to obtain them.

Very fast CPU is a must. Intel Core 2 Duo or better.

%prep
%setup -q -n %{name}-%{version}-r%{revision}-sources

%build
cp -r 3rdparty/SoundTouch 3rdparty/soundtouch
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DFORCE_INTERNAL_SOUNDTOUCH=TRUE \
	-DPACKAGE_MODE=TRUE

%make VERBOSE=1

%install
%makeinstall_std -C build

%find_lang %{name} --all-name

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

