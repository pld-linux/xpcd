#
# Conditional build:
%bcond_without	gimp	# without xpcd-gate plugin (not ready for gimp 1.3)
#
Summary:	PhotoCD tool collection
Summary(pl):	Narzêdzia do obs³ugi formatu PhotoCD
Name:		xpcd
Version:	2.08
Release:	12
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://bytesex.org/misc/%{name}-%{version}.tar.gz
# Source0-md5:	23881054e9c469197fc7cc806255754e
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-FHS.patch
# gimp updates from http://www.adap.org/~edsel/software/xpcd-2.08-gimp1.2.tar.gz
Patch1:		%{name}-gimp1.2.patch
Patch2:		%{name}-gimp.patch
Patch3:		%{name}-version.patch
Patch4:		%{name}-env-overflow.patch
Patch5:		%{name}-app-defaults.patch
URL:		http://bytesex.org/xpcd.html
BuildRequires:	Xaw3d-devel >= 1.3E
BuildRequires:	autoconf
%{?with_gimp:BuildRequires:	gimp-devel >= 1:1.2}
BuildRequires:	libjpeg-devel
BuildRequires:	libpcd-devel >= 1.0.1
BuildRequires:	libtiff-devel
BuildRequires:	libtool
%ifarch %{ix86} alpha
BuildRequires:	svgalib-devel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with gimp}
%define		gimpplugindir	%(gimptool --gimpplugindir)/plug-ins
%endif
# X11 resources must be installed with X11R6 prefix
%define		_xprefix	/usr/X11R6

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

%description svga
svgalib viewer for PhotoCD images.

%description svga -l pl
Przegl±darka obrazków PhotoCD korzystaj±ca z svgalib.

%package gimp
Summary:	GIMP plugin, makes xpcd and gimp work hand in hand
Summary(pl):	Wtyczka do GIMP-a dodaj±ca obs³ugê xpcd
Group:		X11/Applications/Graphics
Requires:	%{name} = %{version}

%description gimp
This is a GIMP 0.99 plugin, it allows xpcd to load images directly
into The GIMP. If you'll open a PhotoCD file within gimp, it will be
passed to xpcd.

%description gimp -l pl
Wtyczka do GIMP-a >= 0.99, pozwalaj±ca wczytywaæ obrazki PhotoCD
bezpo¶rednio do GIMP-a. Otworzenie GIMP-em pliku PhotoCD spowoduje
przekazanie go do xpcd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__autoconf}
%configure \
%ifnarch %{ix86} alpha
	    --without-svga
%endif

%{__make} \
	SUBDIRS="xpcd test"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_applnkdir}/Graphics,%{_pixmapsdir}}

%{__make} install \
	SUBDIRS="xpcd test" \
	DESTDIR=$RPM_BUILD_ROOT \
	SUID_ROOT=

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Graphics
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README bench
%attr(755,root,root) %{_bindir}/pcdtoppm
%attr(755,root,root) %{_bindir}/xpcd
%{_applnkdir}/Graphics/*
%{_pixmapsdir}/*
%{_mandir}/man1/pcdtoppm.1*
%{_mandir}/man1/xpcd.1*
%dir %{_xprefix}/lib/X11/xpcd
%{_xprefix}/lib/X11/xpcd/system.xpcdrc
%{_xprefix}/lib/X11/app-defaults/Xpcd-2
%lang(da) %{_xprefix}/lib/X11/app-defaults/da/Xpcd-2
%lang(de) %{_xprefix}/lib/X11/app-defaults/de/Xpcd-2
%{_xprefix}/include/X11/pixmaps/xpcd-color.xpm
%{_xprefix}/include/X11/pixmaps/xpcd-gray.xpm

%ifarch %{ix86} alpha
%files svga
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pcdview
%attr(644,root,root) %{_mandir}/man1/pcdview.1*
%endif

%if %{with gimp}
%files gimp
%defattr(644,root,root,755)
%attr(755,root,root) %{gimpplugindir}/xpcd-gate
%endif
