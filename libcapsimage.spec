%define major	5
%define libname	%mklibname capsimage %{major}
%define devname	%mklibname capsimage -d

Summary:	SPS Decoder Library for IPF and CTR disk images
Name:		libcapsimage
Version:	5.1
Release:	2
License:	SPSFLA
Group:		System/Libraries
URL:		https://www.kryoflux.com/
Source0:	https://www.kryoflux.com/download/spsdeclib_%{version}_source.zip
BuildRequires:	unzip
BuildRequires:	make
BuildRequires:	gnu-config
Requires:	%{libname} = %{EVRD}

%description
libcapsimage (the SPS Decoder Library) lets emulators read low-level
floppy dumps in IPF, CTR and KryoFlux stream formats. It is required
for copy-protected Atari ST and Amiga disk images.

The library is free for non-commercial use only; see LICENCE.txt.

%package -n %{libname}
Summary:	Shared library for libcapsimage
Group:		System/Libraries

%description -n %{libname}
Shared SPS Decoder Library used to read IPF, CTR and KryoFlux floppy images.

%package -n %{devname}
Summary:	Development files for libcapsimage
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{name}-devel < %{EVRD}

%description -n %{devname}
Headers and pkg-config data for the SPS Decoder Library.

%prep
%setup -c -T
unzip -q %{SOURCE0}
unzip -q capsimg_source_linux_macosx.zip
# clang does not accept this gcc-only flag
sed -i 's/-fconserve-space//g' capsimg_source_linux_macosx/CAPSImg/configure
# MSVC leftover in public headers
sed -i 's/__cdecl//g' capsimg_source_linux_macosx/LibIPF/*.h
chmod +x capsimg_source_linux_macosx/CAPSImg/configure \
	capsimg_source_linux_macosx/CAPSImg/install-sh

%build
cd capsimg_source_linux_macosx/CAPSImg
export CXXFLAGS="%{optflags} -fno-exceptions -fno-rtti -std=c++11"
%configure
%make_build

%install
cd capsimg_source_linux_macosx/CAPSImg
%make_install
ln -s libcapsimage.so.%{version} %{buildroot}%{_libdir}/libcapsimage.so.%{major}
ln -s libcapsimage.so.%{major} %{buildroot}%{_libdir}/libcapsimage.so
install -d %{buildroot}%{_includedir}/caps
install -m 644 ../LibIPF/*.h ../Core/CommonTypes.h %{buildroot}%{_includedir}/caps
install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/capsimage.pc << EOF
Name: capsimage
Description: SPS Decoder Library (IPF/CTR)
Version: %{version}
Libs: -lcapsimage
EOF

%files
%doc HISTORY.txt RELEASE.txt DONATIONS.txt
%license LICENCE.txt

%files -n %{libname}
%{_libdir}/libcapsimage.so.%{major}*

%files -n %{devname}
%{_libdir}/libcapsimage.so
%{_includedir}/caps
%{_libdir}/pkgconfig/capsimage.pc
