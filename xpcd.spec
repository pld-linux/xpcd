#
# Conditional build:
%bcond_without	gimp	# without xpcd-gate plugin (not ready for gimp 1.3)
%bcond_without	svga	# don't build svgalib viewer
#
%ifnarch %{ix86} alpha
%undefine	with_svga
%endif
Summary:	PhotoCD tool collection
Summary(pl):	Narzêdzia do obs³ugi formatu PhotoCD
Name:		xpcd
Version:	2.08
Release:	12
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://dl.bytesex.org/releases/xpcd/%{name}-%{version}.tar.gz
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
URL:		http://linux.bytesex.org/fbida/xpcd.html
BuildRequires:	Xaw3d-devel >= 1.3E
BuildRequires:	autoconf
%{?with_gimp:BuildRequires:	gimp-devel >= 1:1.2}
BuildRequires:	libjpeg-devel
BuildRequires:	libpcd-devel >= 1.0.1
BuildRequires:	libtiff-devel
BuildRequires:	libtool
%{?with_svga:BuildRequires:	svgalib-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with gimp}
%define		gimpplugindir	%(gimptool --gimpplugindir)/plug-ins
%endif
%define		_appdefsdir	/usr/X11R6/lib/X11/app-defaults
# TODO: move to %{_datadir}/xpcd if possible
%define		_xdatadir	/usr/X11R6/lib/X11
# TODO: move to %{_pixmapsdir} if possible
%define		_xpixmapsdir	/usr/X11R6/include/X11/pixmaps

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
	    %{!?with_svga:--without-svga}

%{__make} \
	SUBDIRS="xpcd test"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	SUBDIRS="xpcd test" \
	DESTDIR=$RPM_BUILD_ROOT \
	SUID_ROOT=

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README bench
%attr(755,root,root) %{_bindir}/pcdtoppm
%attr(755,root,root) %{_bindir}/xpcd
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_mandir}/man1/pcdtoppm.1*
%{_mandir}/man1/xpcd.1*
%dir %{_xdatadir}/xpcd
%{_xdatadir}/xpcd/system.xpcdrc
%{_appdefsdir}/Xpcd-2
%lang(da) %{_appdefsdir}/da/Xpcd-2
%lang(de) %{_appdefsdir}/de/Xpcd-2
%{_xpixmapsdir}/xpcd-color.xpm
%{_xpixmapsdir}/xpcd-gray.xpm

%if %{with svga}
%files svga
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pcdview
%{_mandir}/man1/pcdview.1*
%endif

%if %{with gimp}
%files gimp
%defattr(644,root,root,755)
%attr(755,root,root) %{gimpplugindir}/xpcd-gate
%endif
