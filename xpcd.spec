Summary:	PhotoCD tool collection
Name:		xpcd
Version:	2.08
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Group(de):	X11/Applikationen/Grafik
Group(pl):	X11/Aplikacje/Grafika
Source0:	http://www.in-berlin.de/User/kraxel/dl/%{name}-%{version}.tar.gz
Patch0:		xpcd-gimp.patch
Patch1:		xpcd-FHS.patch
Patch2:		xpcd-shared.patch
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	autoconf
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	svgalib-devel
BuildRequires:	Xaw3d-devel
BuildRequires:	gimp-devel >= 0.99
Requires:	libpcd

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

%ifarch %ix86

%package svga
Group:		Applications/Graphics
Group(de):	Applikationen/Grafik
Group(pl):	Aplikacje/Grafika
Summary:	svgalib viewer for PhotoCD images
Requires:	libpcd

%description svga
svgalib viewer for PhotoCD images

%endif

%package gimp
Summary:	GIMP 0.99 plugin, makes xpcd and gimp work hand in hand.
Group:		X11/Applications/Graphics
Group(de):	X11/Applikationen/Grafik
Group(pl):	X11/Aplikacje/Grafika
Requires:	xpcd >= 2
Requires:	libpcd
%description gimp
This is a GIMP 0.99 plugin, it allows xpcd to load images directly
into The GIMP. If you'll open a PhotoCD file within gimp, it will be
passed to xpcd.

%package -n libpcd
Summary:	PCD shared library
Group:		Libraries
Group(de):	Libraries
Group(fr):	Librairies
Group(pl):	Biblioteki
Prereq:		/sbin/ldconfig

%description -n libpcd
This is PCD shared library.

%package -n libpcd-devel
Summary:	libpcd header files
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	libpcd = %{version}

%description -n libpcd-devel
libpcd header file.

%package -n libpcd-static
Summary:	libpcd static library
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	libpcd-devel = %{version}

%description -n libpcd-static
Static version of libpcd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
#export CFLAGS
autoconf
CFLAGS="%{?debug:-g -O0}%{!?debug:$RPM_OPT_FLAGS} -DGIMP_ENABLE_COMPAT_CRUFT"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT SUID_ROOT= install
%{__make} DESTDIR=$RPM_BUILD_ROOT install-lib -C libpcd

#install -d $RPM_BUILD_ROOT%{_includedir}
#install libpcd/pcd.h $RPM_BUILD_ROOT%{_includedir}

# move X stuff to _x*dir
install -d $RPM_BUILD_ROOT%{_xmandir}/man1
install -d $RPM_BUILD_ROOT%{_xbindir}
mv -f $RPM_BUILD_ROOT%{_mandir}/man1/xpcd.1 $RPM_BUILD_ROOT%{_xmandir}/man1
mv -f $RPM_BUILD_ROOT%{_bindir}/xpcd $RPM_BUILD_ROOT%{_xbindir}

gzip -9nf README bench

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libpcd -p	/sbin/ldconfig
%postun -n libpcd -p	/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_xbindir}/xpcd
%attr(755,root,root) %{_bindir}/pcdtoppm
%{_xmandir}/man1/xpcd.1*
%{_mandir}/man1/pcdtoppm.1*
%{_xprefix}/lib/X11/xpcd/system.xpcdrc
%{_xprefix}/lib/X11/app-defaults/Xpcd-2
%lang(de) %{_xprefix}/lib/X11/de/app-defaults/Xpcd-2
%lang(da) %{_xprefix}/lib/X11/da/app-defaults/Xpcd-2
%{_xprefix}/include/X11/pixmaps/xpcd-color.xpm
%{_xprefix}/include/X11/pixmaps/xpcd-gray.xpm
%doc *.gz

%ifarch %ix86
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
%{_libdir}/libpcd.la
%attr(644,root,root) %{_includedir}/pcd.h
%doc libpcd/README.html

%files -n libpcd-static
%defattr(644,root,root,755)
%{_libdir}/libpcd.a
