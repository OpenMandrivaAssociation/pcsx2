%define _disable_ld_no_undefined 1
%define _disable_lto 1

# Using a snapshot for now to get 64-bit support
%define snapshot 20200714

Summary:	Sony PlayStation 2 Emulator
Name:		pcsx2
Version:	1.7.0
Release:	%{?snapshot:0.%{snapshot}.}1
License:	GPLv2+
Group:		Emulators
Url:		http://pcsx2.net/
%if 0%{?snapshot:1}
Source0:	https://github.com/beaumanvienna/pcsx2/archive/x86_64-support/%{name}-%{snapshot}.tar.gz
Source1:	https://github.com/google/googletest/archive/aee0f9d9b5b87796ee8a0ab26b7587ec30e8858e.tar.gz
%else
Source0:	https://github.com/PCSX2/pcsx2/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Patch0:         pcsx2-1.4.0-mga-allow-disabled-plugins.patch

BuildRequires:	cmake
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
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:  pkgconfig(udev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  wxgtku3.0-devel
#BuildRequires:  wxgtku2.8-devel

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
%if 0%{?snapshot:1}
%autosetup -p1 -n %{name}-x86_64-support -a 1
rmdir 3rdparty/gtest
mv googletest-aee0f9d9b5b87796ee8a0ab26b7587ec30e8858e 3rdparty/gtest
%else
%autosetup -p1 -n %{name}-%{version}
%endif

%build
%global ldflags %{ldflags} -Wl,-z,notext
%global ldflags %{ldflags} -fuse-ld=gold

%if 0
# Back to GCC. Because when running PCSX2 compiled with Clang I see: illegal instruction (memory dump) at launch.
# Do not switch back to Clang without testing if this issue is fixed! (angry)
export CC=gcc
export CXX=g++
%endif

# FIXME
# Do not switch -DDISABLE_ADVANCE_SIMD= to true, because then Clang build fail (angry)
# https://github.com/PCSX2/pcsx2/issues/3096
# and when switch it to TRUE, Clang and GCC gives me illegal instruction (memory dump) at launch.
# So for now we back to GCC and leave SIMD as True.

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
    -DGTK3_API=TRUE
   

%make_build

%install
%make_install -C build

%find_lang %{name} --all-name
