%define _disable_ld_no_undefined 1
%define _disable_lto 1

# Using a snapshot for now to get 64-bit support
# Git tag are recommended to use for distro packaging.
#define git 20230824

Summary:	Sony PlayStation 2 Emulator
Name:		pcsx2
Version:	2.6.2
Release:	1
License:	GPLv2+
Group:		Emulators
Url:		http://pcsx2.net/
Source0:	https://github.com/PCSX2/pcsx2/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:  https://github.com/PCSX2/pcsx2_patches/archive/pcsx2_patches-latest.tar.gz


BuildRequires:  cmake(ECM)
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
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(sdl3)
BuildRequires:	pkgconfig(soundtouch)
BuildRequires:  pkgconfig(udev)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  wxgtku3.0-devel
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xdmcp)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libbacktrace)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libidn2)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(shaderc)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
#BuildRequires:  wxgtku2.8-devel

BuildRequires:  cmake(PulseAudio)
BuildRequires:  cmake(plutovg)
BuildRequires:  cmake(plutosvg)

#Qt6
BuildRequires:	cmake(KDDockWidgets-qt6)
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

#----------------------------------------------------------------------------

%prep

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

%autosetup -p1 -a1

mv pcsx2_patches-latest/patches ./
#rm -rf 3rdparty

#Taked fro AUR
# prevent march=native
sed -E -e 's@^(\s*)(add_compile_options\(.*march=native.*\))@\1message("skip: march=native")@' \
-i cmake/BuildParameters.cmake

# adjust data path
sed -E -e '/CMAKE_INSTALL_FULL_DATADIR/s@/PCSX2\b@/'"%{name}@" \
-i "pcsx2/CMakeLists.txt" \
"cmake/BuildParameters.cmake"

%build
%cmake \
  -GNinja \
  -DCMAKE_LINKER_TYPE=LLD \
  -DPACKAGE_MODE:BOOL=ON \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DX11_API:BOOL=ON \
  -DWAYLAND_API:BOOL=ON \
  -DENABLE_TESTS:BOOL=OFF \
  -DDISABLE_ADVANCE_SIMD:BOOL=ON
%cmake_build

%install
%cmake_install

install -Dp -m0644 %{name}-qt/resources/icons/AppIcon64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/PCSX2.png
install -Dp -m0644 bin/resources/icons/AppIconLarge.png %{buildroot}%{_iconsdir}/hicolor/512x512/apps/PCSX2.png
install -Dp -m0644 .github/workflows/scripts/linux/%{name}-qt.desktop %{buildroot}%{_datadir}/applications/%{name}-qt.desktop

mkdir -p %{buildroot}%{_datadir}/%{name}/resources
cp -a patches %{buildroot}%{_datadir}/%{name}/resources/

%files
%doc bin/docs/*.pdf
%caps(cap_net_admin,cap_net_raw=eip) %{_bindir}/pcsx2-qt
%{_datadir}/applications/pcsx2-qt.desktop
%{_datadir}/pcsx2/
%{_iconsdir}/hicolor/*/apps/PCSX2.png
