%global optflags %{optflags} -Wno-error=incompatible-pointer-types-discards-qualifiers

%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api 1
%define major 0
%define libname %mklibname adwaita %{api} %{major}
%define giradwaitaname %mklibname adwaita-gir %{api}
%define devname %mklibname adwaita -d

#define	subversion	alpha.4

Name:		libadwaita
Version:	1.0.0
Release:	1
Summary:	The aim of the Adwaita library is to help with developing UI for mobile devices using GTK/GNOME (based/forked from libhandy).
License:	LGPLv2+
Group:		Development/GNOME and GTK+
URL:		https://gitlab.gnome.org/GNOME/libadwaita
Source0:	https://gitlab.gnome.org/GNOME/libadwaita/-/archive/%{version}/libadwaita-%{version}.tar.bz2

BuildRequires:	cmake
BuildRequires:	gtk-doc
BuildRequires:	sassc
BuildRequires:	meson
BuildRequires:	vala
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gi-docgen)
BuildRequires:	pkgconfig(gtk4)

%description
The aim of the Adwaita library is to help with developing UI for mobile devices
using GTK/GNOME. This package is based on libhandy 1.2.0 and fork it for GTK4, while libhandy support GTK+-3.0.

#------------------------------------------------
%package common
Summary:	A GTK+ library to develop UI for mobile devices
Group:		System/Libraries

%description common
This package provides the shared library for libadwaita, a library to
help with developing mobile UI using GTK4/GNOME.

#------------------------------------------------

%package -n %{libname}
Summary:	A GTK4 library to develop UI for mobile devices
Group:		System/Libraries
Requires:	%{name}-common

%description -n %{libname}
This package provides the shared library for libadwaita, a library to
help with developing mobile UI using GTK4/GNOME.

#------------------------------------------------

%package -n %{giradwaitaname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{giradwaitaname}
GObject Introspection interface description for %{name}.

#------------------------------------------------

%package -n %{devname}
Summary:	Development package for %{name}
Group:		Development/GNOME and GTK4
Requires:	%{libname} = %{version}-%{release}
Requires:	%{giradwaitaname} = %{version}-%{release}
Provides:	libadwaita-devel = %{version}-%{release}

%description -n	%{devname}
Header files for development with %{name}.

#------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%meson \
	-Dprofiling=false \
	-Dintrospection=enabled \
	-Dvapi=true \
	-Dgtk_doc=true \
	-Dtests=false \
	-Dexamples=false \
	%{nil}

%meson_build

%install
%meson_install

%find_lang %name

%files common -f %{name}.lang

%files -n %{libname}
%{_libdir}/libadwaita-%{api}.so.%{major}{,.*}
#{_libdir}/gtk-4.0/inspector/libadwaita-inspector-module%{api}.so.%{major}

%files -n %{giradwaitaname}
%{_libdir}/girepository-1.0/Adw-%{api}.typelib

%files -n %{devname}
%license COPYING
%doc AUTHORS README.md
#doc #{_datadir}/gtk-doc/html/libadwaita-%{api}/
%doc %{_docdir}/libadwaita-1/
%{_includedir}/libadwaita-%{api}/
%{_libdir}/libadwaita-%{api}.so
%{_libdir}/gtk-4.0/inspector/libadwaita-inspector-module%{api}.so
%{_libdir}/pkgconfig/libadwaita-%{api}.pc
%{_datadir}/gir-1.0/Adw-%{api}.gir
%{_datadir}/vala/vapi/libadwaita-%{api}.deps
%{_datadir}/vala/vapi/libadwaita-%{api}.vapi
