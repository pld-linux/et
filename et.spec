# TODO
# - create dedicated server subpackage
#
# Conditional build:
%bcond_without	data	# skip build of data subpackage (huge and resource consuming)
#
Summary:	Enemy Territory
Summary(pl):	Enemy Territory - Terytorium wroga
Name:		et
Version:	2.60
Release:	0.1
Epoch:		0
License:	RTCW-ETEULA
Group:		Applications/Games
Source0:	http://3dgamers.planetmirror.com/pub/3dgamers/games/wolfensteinet/et-linux-%{version}.x86.run
# NoSource0-md5:	2d2373f29f02e18d365d7f1860eee435
Source1:	%{name}.desktop
NoSource:	0
URL:		http://www.idsoftware.com/
# loose dependancy is intentional
Requires:	%{name}-data = %{version}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		no_install_post_chrpath 1
%define		_gamelibdir	%{_libdir}/games/et
%define		_gamedatadir	%{_datadir}/games/et

%description
Return to Castle Wolfenstein: Enemy Territory - standalone
multi-player game based on Return to Castle Wolfenstein.

%description -l pl
Return to Castle Wolfenstein: Enemy Territory jest to samodzielna gra
dla wielu graczy oparta na Return to Castle Wolfenstein.

%package data
Summary:	Enemy Territory data files
Summary(pl):	Pliki z danymi dla Enemy Territory
Group:		Applications/Games

%description data
This package contains the data files for Enemy Territory.

%description data -l pl
Pakiet ten zawiera pliki z danymi dla gry Enemy Territory.

%prep
%setup -qcT
sh %{SOURCE0} --tar xf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_gamelibdir},%{_gamedatadir}}

install bin/Linux/x86/et.x86 $RPM_BUILD_ROOT%{_gamelibdir}/%{name}

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
# Needed to make symlinks/shortcuts work.
# the binaries must run with correct working directory
cd %{_gamelibdir}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.
exec ./%{name} "\$@"
EOF

install ET.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.xpm
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
ln -s ../../../share/games/et/etmain $RPM_BUILD_ROOT%{_gamelibdir}

cp -a pb $RPM_BUILD_ROOT%{_gamelibdir}
# in DOCS
rm -f $RPM_BUILD_ROOT%{_gamelibdir}/pb/PB_EULA.txt

%if %{with data}
cp -a etmain $RPM_BUILD_ROOT%{_gamedatadir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README Docs pb/PB_EULA.txt
%attr(755,root,root) %{_bindir}/*

%dir %{_gamelibdir}
%attr(755,root,root) %{_gamelibdir}/et
%{_gamelibdir}/etmain

%dir %{_gamelibdir}/pb
%{_gamelibdir}/pb/htm
%attr(755,root,root) %{_gamelibdir}/pb/*.x86
%attr(755,root,root) %{_gamelibdir}/pb/*.so
%{_gamelibdir}/pb/*.db

%dir %{_gamedatadir}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.xpm

%if %{with data}
%files data
%defattr(644,root,root,755)
%{_gamedatadir}/*
%endif
