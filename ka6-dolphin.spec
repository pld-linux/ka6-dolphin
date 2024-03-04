#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.02.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		dolphin
Summary:	File manager
Name:		ka6-%{kaname}
Version:	24.02.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	78941922c7d755692ed7cfa7a656c23e
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.20
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kbookmarks-devel >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kitemmodels-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-knotifyconfig-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kpty-devel >= %{kframever}
BuildRequires:	kf6-kservice-devel >= %{kframever}
BuildRequires:	kf6-ktextwidgets-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	ruby-test-unit
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dolphin is a lightweight file manager. It has been designed with ease
of use and simplicity in mind, while still allowing flexibility and
customisation. This means that you can do your file management exactly
the way you want to do it.

Features

• Navigation (or breadcrumb) bar for URLs, allowing you to quickly
navigate through the hierarchy of files and folders. • Supports
several different kinds of view styles and properties and allows you
to configure the view exactly how you want it. • Split view, allowing
you to easily copy or move files between locations. • Additional
information and shortcuts are available as dock-able panels, allowing
you to move them around freely and display exactly what you want. •
Multiple tab support • Informational dialogues are displayed in an
unobtrusive way. • Undo/redo support • Transparent network access
through the KIO system.

%description -l pl.UTF-8
Dolphin to lekki zarządca plików. Zaprojektowany jako łatwy w użyciu,
choć zapewniający elastyczność i możliwości konfiguracji. To znaczy,
że możesz go używać dokładnie, tak jakbyś chciał.

Cechy

• Pasek nawigacyjny dla URLi pozwalający na szybkie przemieszczanie
się wśród hierarchi plików i folderów • Wspiera wiele różnych rodzajów
przeglądania plików pozwalając skonfigurować podgląd tak jak sobie
tego życzysz • Podzielony widok do łatwego kopiowania i przenoszenia
plików między lokacjami • Dodatkowe informacje i skróty klawiszowe są
dostępne jako dokowalne panele, pozwalając przemieszczać się do woli i
wyświetlać to co chcesz • Wiele kart • Informacyjne okna dialogowe nie
drażnią użytkownika • Wsparcie dla Cofnij/Powtórz • Przeźroczysty
dostęp do sieci korzystający z systemu KIO.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmake >= 2.6.0

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
RUBYLIB=%{_datadir}/gems/gems/test-unit-3.2.3/lib
export RUBYLIB
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
rm -rf $RPM_BUILD_ROOT%{_localedir}/ie
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dolphin
%attr(755,root,root) %{_bindir}/servicemenuinstaller
%{systemduserunitdir}/plasma-dolphin.service
%attr(755,root,root) %{_libdir}/libdolphinprivate.so.*.*
%ghost %{_libdir}/libdolphinprivate.so.6
%attr(755,root,root) %{_libdir}/libdolphinvcs.so.*.*
%ghost %{_libdir}/libdolphinvcs.so.6
%dir %{_libdir}/qt6/plugins/dolphin
%dir %{_libdir}/qt6/plugins/dolphin/kcms
%attr(755,root,root) %{_libdir}/qt6/plugins/dolphin/kcms/kcm_dolphingeneral.so
%attr(755,root,root) %{_libdir}/qt6/plugins/dolphin/kcms/kcm_dolphinviewmodes.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/parts/dolphinpart.so
%{_desktopdir}/org.kde.dolphin.desktop
%{_datadir}/config.kcfg/dolphin_compactmodesettings.kcfg
%{_datadir}/config.kcfg/dolphin_contentdisplaysettings.kcfg
%{_datadir}/config.kcfg/dolphin_contextmenusettings.kcfg
%{_datadir}/config.kcfg/dolphin_detailsmodesettings.kcfg
%{_datadir}/config.kcfg/dolphin_directoryviewpropertysettings.kcfg
%{_datadir}/config.kcfg/dolphin_generalsettings.kcfg
%{_datadir}/config.kcfg/dolphin_iconsmodesettings.kcfg
%{_datadir}/config.kcfg/dolphin_versioncontrolsettings.kcfg
%{_datadir}/dbus-1/interfaces/org.freedesktop.FileManager1.xml
%{_datadir}/dbus-1/services/org.kde.dolphin.FileManager1.service
%{_datadir}/dolphin/dolphinpartactions.desktop
%{_datadir}/kconf_update/dolphin_detailsmodesettings.upd
%{_datadir}/kglobalaccel/org.kde.dolphin.desktop
%{_datadir}/knsrcfiles/servicemenu.knsrc
%{_datadir}/metainfo/org.kde.dolphin.appdata.xml
%{_datadir}/qlogging-categories6/dolphin.categories
%{zsh_compdir}/_dolphin
%{_iconsdir}/hicolor/scalable/apps/org.kde.dolphin.svg

%files devel
%defattr(644,root,root,755)
%{_includedir}/Dolphin
%{_includedir}/dolphin_export.h
%{_includedir}/dolphinvcs_export.h
%{_libdir}/cmake/DolphinVcs
%{_libdir}/libdolphinvcs.so
