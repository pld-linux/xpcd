Summary:	PhotoCD tool collection
Summary(pl):	Narzêdzia do obs³ugi formatu PhotoCD
Name:		xpcd
Version:	2.08
Release:	5
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://www.in-berlin.de/User/kraxel/dl/%{name}-%{version}.tar.gz
Patch0:		%{name}-gimp.patch
Patch1:		%{name}-FHS.patch
Patch2:		%{name}-shared.patch
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
%ifarch %{ix86} alpha
BuildRequires:	svgalib-devel
%endif
BuildRequires:	Xaw3d-devel
BuildRequires:	gimp-devel >= 0.99
Requires:	libpcd = %{version}

%define		_xprefix	/usr/X11R6
%define		_xbindir	%{_xprefix}/bin
%define		_xlibdir	%{_xprefix}/lib
%define		_xmandir	%{_xprefix}/man

%define		_prefix		/usr

%description
This is a PhotoCD tool collection. The main application - xpcd - is a
comfortable, X11-based PhotoCD decoding/viewing program. Also included
is pcdtoppm, this is a command line based PhotoCD-to-PPM/JPEG
converter.

%description -l pl
Zestaw narzêdzi do obróbki formatu PhotoCD. G³ówna aplikacja (xpcd)
jest programem pod X do dekodowania i ogl±dania obrazków PhotoCD.
pcdtoppm jest konwerterem na ppm i jpg dzia³aj±cym z linii poleceñ.

%package svga
Summary:	svgalib viewer for PhotoCD images
Summary(pl):	Przegl±darka PhotoCD korzystaj±ca z svgalib
Group:		Applications/Graphics
Requires:	libpcd = %{version}

%description svga
svgalib viewer for PhotoCD images.

%description svga -l pl
Przegl±darka obrazków PhotoCD korzystaj±ca z svgalib.

%package gimp
Summary:	GIMP plugin, makes xpcd and gimp work hand in hand.
Summary(pl):	Wtyczka do GIMP-a dodaj±ca obs³ugê xpcd.
Group:		X11/Applications/Graphics
Requires:	xpcd = %{version}
Requires:	libpcd = %{version}

%description gimp
This is a GIMP 0.99 plugin, it allows xpcd to load images directly
into The GIMP. If you'll open a PhotoCD file within gimp, it will be
passed to xpcd.

%description gimp -l pl
Wtyczka do GIMP-a >= 0.99, pozwalaj±ca wczytywaæ obrazki PhotoCD
bezpo¶rednio do GIMP-a. Otworzenie GIMP-em pliku PhotoCD spowoduje
przekazanie go do xpcd.

%package -n libpcd
Summary:	PhotoCD shared library
Summary(pl):	Biblioteka dzielona do obs³ugi PhotoCD
Group:		Libraries

%description -n libpcd
This is PhotoCD shared library.

%description -n libpcd -l pl
Biblioteka dzielona do obs³ugi PhotoCD.

%package -n libpcd-devel
Summary:	libpcd header files
Summary(pl):	Pliki nag³ówkowe do libpcd
Group:		Development/Libraries
Requires:	libpcd = %{version}

%description -n libpcd-devel
libpcd header file.

%description -n libpcd-devel -l pl
Pliki nag³ówkowe do biblioteki libpcd.

%package -n libpcd-static
Summary:	libpcd static library
Summary(pl):	Biblioteka statyczna libpcd
Group:		Development/Libraries
Requires:	libpcd-devel = %{version}

%description -n libpcd-static
Static version of libpcd.

%description -n libpcd-static -l pl
Statyczna wersja biblioteki libpcd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autoconf}
CFLAGS="%{rpmcflags} -DGIMP_ENABLE_COMPAT_CRUFT"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_xbindir},%{_xmandir}/man1}

%{__make} DESTDIR=$RPM_BUILD_ROOT SUID_ROOT= install
%{__make} DESTDIR=$RPM_BUILD_ROOT install-lib -C libpcd

# move X stuff to _x*dir
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/xpcd.1 $RPM_BUILD_ROOT%{_xmandir}/man1
mv -f $RPM_BUILD_ROOT%{_bindir}/xpcd $RPM_BUILD_ROOT%{_xbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libpcd -p /sbin/ldconfig
%postun	-n libpcd -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README bench
%attr(755,root,root) %{_xbindir}/xpcd
%attr(755,root,root) %{_bindir}/pcdtoppm
%{_xmandir}/man1/xpcd.1*
%{_mandir}/man1/pcdtoppm.1*
%dir %{_xprefix}/lib/X11/xpcd
%{_xprefix}/lib/X11/xpcd/system.xpcdrc
%{_xprefix}/lib/X11/app-defaults/Xpcd-2
%lang(de) %{_xprefix}/lib/X11/de/app-defaults/Xpcd-2
%lang(da) %{_xprefix}/lib/X11/da/app-defaults/Xpcd-2
%{_xprefix}/include/X11/pixmaps/xpcd-color.xpm
%{_xprefix}/include/X11/pixmaps/xpcd-gray.xpm

%ifarch %ix86 alpha
%files svga
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pcdview
%attr(644,root,root) %{_mandir}/man1/pcdview.1*
%endif

%files gimp
%defattr(644,root,root,755)
%attr(755,root,root) %{_xprefix}/lib/gimp/*/plug-ins/xpcd-gate

%files -n libpcd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpcd.so.*.*

%files -n libpcd-devel
%defattr(644,root,root,755)
%{_libdir}/libpcd.so
%attr(755,root,root) %{_libdir}/libpcd.la
%attr(644,root,root) %{_includedir}/pcd.h
%doc libpcd/README.html

%files -n libpcd-static
%defattr(644,root,root,755)
%{_libdir}/libpcd.a
