%define _disable_ld_no_undefined 1
%define _disable_lto 1

# Using a snapshot for now to get 64-bit support
# Git tag are recommended to use for distro packaging.
%define git 20230824

Summary:	Sony PlayStation 2 Emulator
Name:		pcsx2
Version:	1.7.4940
Release:	1.%{git}.0
License:	GPLv2+
Group:		Emulators
Url:		http://pcsx2.net/
Source0:	https://github.com/PCSX2/pcsx2/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:    https://github.com/biojppm/rapidyaml/archive/refs/tags/v0.3.0/rapidyaml-0.3.0.tar.gz


BuildRequires:	cmake
BuildRequires:  c4project
BuildRequires:  gettext
BuildRequires:	subversion
BuildRequires:	bzip2-devel
BuildRequires:	jpeg-devel
BuildRequires:	libaio-devel
BuildRequires:  pcap-devel
BuildRequires:	sparsehash-devel
#BuildRequires:	wxgtku-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:  pkgconfig(fmt)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(openssl)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:  pkgconfig(udev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  wxgtku3.0-devel
#BuildRequires:  wxgtku2.8-devel

#Qt6
BuildRequires:	cmake(Qt6Multimedia)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Network)
BuildRequires:  cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Test)
BuildRequires:  cmake(VulkanHeaders)
BuildRequires:	qt6-qttools
BuildRequires:	cmake(qt6)
BuildRequires:	qmake-qt6

# 1.6.0 (may 2020) and x86_64 is still not ready (angry)
# re check it for future releases
#ExclusiveArch:	%{ix86}

%description
Sony PlayStation 2 emulator. Requires a BIOS image to run. Check 
http://www.pcsx2.net/guide.php#Bios for details on which files
you need and how to obtain them.

Very fast CPU is a must. Intel Core 2 Duo or better.

%files -f %{name}.lang
%doc COPYING.*
%doc %{_docdir}/%{name}/*.pdf
%{_bindir}/PCSX2
%{_bindir}/%{name}_*
%{_datadir}/applications/PCSX2.desktop
%{_datadir}/pixmaps/PCSX2.xpm
%{_datadir}/games/%{name}/cheats_ws.zip
%attr(0666,games,games) %{_datadir}/games/%{name}/GameIndex.dbf
%{_libdir}/games/%{name}/
%{_mandir}/man1/PCSX2.1*

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}

%build
#global ldflags %{ldflags} -Wl,-z,notext
#global ldflags %{ldflags} -fuse-ld=gold

# Back to GCC. Because when running PCSX2 compiled with Clang I see: illegal instruction (memory dump) at launch.
# Do not switch back to Clang without testing if this issue is fixed! (angry)
#export CC=gcc
#export CXX=g++


# FIXME
# Do not switch -DDISABLE_ADVANCE_SIMD= to true, because then Clang build fail (angry)
# https://github.com/PCSX2/pcsx2/issues/3096
# and when switch it to TRUE, Clang and GCC gives me illegal instruction (memory dump) at launch.
# So for now we back to GCC and leave SIMD as True.

%cmake \
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
    -DSDL2_API=TRUE
   

%make_build

%install
%make_install -C build

%find_lang %{name} --all-name
