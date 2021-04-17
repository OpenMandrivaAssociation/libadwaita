%global optflags %{optflags} -Wno-error=incompatible-pointer-types-discards-qualifiers

%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api 1
%define major 0
%define libname %mklibname adwaita %{api} %{major}
%define giradwaitaname %mklibname adwaita-gir %{api}
%define devname %mklibname adwaita -d

%define git 20210409

Name:		libadwaita
# Until kids from this project choose version scheme and correct version, let's use low version 0.1. Just for sanity check and to be sure 
# that you don't have to lower the version later (because kids decided so) and add epochs unnecessarily.
# https://gitlab.gnome.org/GNOME/libadwaita/-/issues/44
# PS. the world doesn't end at Flatpak, which can be dangerous in many ways. People use the system repo! 
Version:	0.1
Release:	0.%{git}
Summary:	The aim of the Adwaita library is to help with developing UI for mobile devices using GTK/GNOME (based/forked from libhandy).
License:	LGPLv2+
Group:		Development/GNOME and GTK+
URL:		https://gitlab.gnome.org/GNOME/libadwaita
Source0:	https://gitlab.gnome.org/GNOME/libadwaita/-/archive/main/libadwaita-main.tar.bz2

BuildRequires:	cmake
BuildRequires:	gtk-doc
BuildRequires:	sassc
BuildRequires:	meson
BuildRequires:	vala
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	pkgconfig(gladeui-2.0)
BuildRequires:	pkgconfig(gnome-desktop-3.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
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
This package provides the shared library for libhandy, a library to
help with developing mobile UI using GTK4/GNOME.

#------------------------------------------------

%package -n %{girhandyname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girhandyname}
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

%package -n %{name}-glade
Summary:	Glade (GTK4) modules for %{name}
Group:		Graphical desktop/GNOME
Requires:	glade

%description -n %{name}-glade
This package provides a catalog for Glade (GTK4) which allows the use
of the provided Handy widgets in Glade.

#------------------------------------------------

%prep
%autosetup -p1 -n %{name}-main

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
%{_libdir}/adwaita-%{api}.so.%{major}{,.*}

%files -n %{girhandyname}
%{_libdir}/girepository-1.0/adwaita-%{api}.typelib

%files -n %{devname}
%license COPYING
%doc AUTHORS README.md
%doc %{_datadir}/gtk-doc/html/libadwaita-%{api}/
%{_includedir}/libadwaita-%{api}/
%{_libdir}/libhandy-%{api}.so
%{_datadir}/gir-1.0/adwaita-%{api}.gir
%{_libdir}/pkgconfig/libadwaita-%{api}.pc
%{_datadir}/vala/vapi/libadwaita-%{api}.deps
%{_datadir}/vala/vapi/libadwaita-%{api}.vapi

%files -n %{name}-glade
%{_libdir}/glade/modules/*.so
%{_datadir}/glade/catalogs/*.xml
