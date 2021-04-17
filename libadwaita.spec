%global optflags %{optflags} -Wno-error=incompatible-pointer-types-discards-qualifiers

%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api 1
%define major 0
%define libname %mklibname handy %{api} %{major}
%define girhandyname %mklibname handy-gir %{api}
%define devname %mklibname handy -d

Name:		libhandy
Version:	1.2.1
Release:	1
Summary:	A GTK+ library to develop UI for mobile devices
License:	LGPLv2+
Group:		Development/GNOME and GTK+
URL:		https://source.puri.sm/Librem5/libhandy/
Source0:	https://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	gtk-doc
BuildRequires:	meson
BuildRequires:	vala
BuildRequires:	pkgconfig(gladeui-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.24.1

%description
libhandy is a library to help with developing UI for mobile devices
using GTK+/GNOME.

#------------------------------------------------
%package common
Summary:	A GTK+ library to develop UI for mobile devices
Group:		System/Libraries

%description common
This package provides the shared library for libhandy, a library to
help with developing mobile UI using GTK+/GNOME.

#------------------------------------------------

%package -n %{libname}
Summary:	A GTK+ library to develop UI for mobile devices
Group:		System/Libraries
Requires:	%{name}-common

%description -n %{libname}
This package provides the shared library for libhandy, a library to
help with developing mobile UI using GTK+/GNOME.

#------------------------------------------------

%package -n %{girhandyname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girhandyname}
GObject Introspection interface description for %{name}.

#------------------------------------------------

%package -n %{devname}
Summary:	Development package for %{name}
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girhandyname} = %{version}-%{release}
Provides:	handy-devel = %{version}-%{release}
Obsoletes:	__devname_ < 0.0.13

%description -n	%{devname}
Header files for development with %{name}.

#------------------------------------------------

%package -n %{name}-glade
Summary:	Glade (GTK+3) modules for %{name}
Group:		Graphical desktop/GNOME
Requires:	glade

%description -n %{name}-glade
This package provides a catalog for Glade (GTK+3) which allows the use
of the provided Handy widgets in Glade.

#------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%meson \
	-Dprofiling=false \
	-Dstatic=false \
	-Dintrospection=enabled \
	-Dvapi=true \
	-Dgtk_doc=true \
	-Dtests=false \
	-Dexamples=false \
	-Dglade_catalog=enabled \
	%{nil}

%meson_build

%install
%meson_install

%find_lang %name

%files common -f %{name}.lang

%files -n %{libname}
%{_libdir}/libhandy-%{api}.so.%{major}{,.*}

%files -n %{girhandyname}
%{_libdir}/girepository-1.0/Handy-%{api}.typelib

%files -n %{devname}
%license COPYING
%doc AUTHORS README.md
%doc %{_datadir}/gtk-doc/html/libhandy-%{api}/
%{_includedir}/libhandy-%{api}/
%{_libdir}/libhandy-%{api}.so
%{_datadir}/gir-1.0/Handy-%{api}.gir
%{_libdir}/pkgconfig/libhandy-%{api}.pc
%{_datadir}/vala/vapi/libhandy-%{api}.deps
%{_datadir}/vala/vapi/libhandy-%{api}.vapi

%files -n %{name}-glade
%{_libdir}/glade/modules/*.so
%{_datadir}/glade/catalogs/*.xml
