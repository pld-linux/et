# TODO
# - create dedicated server subpackage
# - separate 2.60 and 2.60b - some servers needs different version
#
# Conditional build:
%bcond_without	data	# skip build of data subpackage (huge and resource consuming)
#
Summary:	Enemy Territory
Summary(pl.UTF-8):	Enemy Territory - Terytorium wroga
Name:		et
Version:	2.60
Release:	0.4
Epoch:		0
License:	RTCW-ETEULA
Group:		Applications/Games
Source0:	ftp://ftp.red.telefonica-wholesale.net/GAMES/ET/linux/%{name}-linux-%{version}.x86.run
# NoSource0-md5:	2d2373f29f02e18d365d7f1860eee435
Source1:	ftp://ftp.red.telefonica-wholesale.net/GAMES/ET/linux/%{name}-linux-%{version}-update.x86.run
# NoSource1-md5:	94a7036471b90955a88339d677e467c2
Source2:	ftp://ftp.red.telefonica-wholesale.net/GAMES/ET/linux/%{name}-%{version}b.zip
# NoSource2-md5:	fb83b8732fc7373c277180b663debf57
Source3:	%{name}.desktop
NoSource:	0
URL:		http://www.idsoftware.com/
# loose dependancy is intentional
BuildRequires:	unzip
Requires:	%{name}-data = %{version}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gamelibdir	%{_libdir}/games/et
%define		_gamedatadir	%{_datadir}/games/et

%description
Return to Castle Wolfenstein: Enemy Territory - standalone
multi-player game based on Return to Castle Wolfenstein.

%description -l pl.UTF-8
Return to Castle Wolfenstein: Enemy Territory jest to samodzielna gra
dla wielu graczy oparta na Return to Castle Wolfenstein.

%package data
Summary:	Enemy Territory data files
Summary(pl.UTF-8):	Pliki z danymi dla Enemy Territory
Group:		Applications/Games

%description data
This package contains the data files for Enemy Territory.

%description data -l pl.UTF-8
Pakiet ten zawiera pliki z danymi dla gry Enemy Territory.

%prep
%setup -qcT
sh %{SOURCE0} --tar xf
sh %{SOURCE1} --tar xf
unzip -j %{SOURCE2} "Enemy Territory 2.60b/linux/et*"
mv et*.x86 bin/Linux/x86
mv pb/PB_EULA.txt .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_gamelibdir}/{pb,etmain},%{_gamedatadir}/etmain}

install bin/Linux/x86/et.x86 $RPM_BUILD_ROOT%{_gamelibdir}/%{name}

cat << 'EOF' > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
# Needed to make symlinks/shortcuts work.
# the binaries must run with correct working directory
cd %{_gamelibdir}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.
exec ./%{name} ${1:+"$@"}
EOF

install ET.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.xpm
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install etmain/*.so $RPM_BUILD_ROOT%{_gamelibdir}/etmain

%if %{with data}
cp -a etmain/{video,*.{pk3,cfg,dat,txt}} $RPM_BUILD_ROOT%{_gamedatadir}/etmain
cd $RPM_BUILD_ROOT%{_gamedatadir}/etmain
for a in video *.{pk3,cfg,dat,txt}; do
	ln -s ../../../../share/games/et/etmain/$a $RPM_BUILD_ROOT%{_gamelibdir}/etmain
done
cd -
%endif

install pb/*.so $RPM_BUILD_ROOT%{_gamelibdir}/pb
install pb/*.x86 $RPM_BUILD_ROOT%{_gamelibdir}/pb
cp -a pb/*.db $RPM_BUILD_ROOT%{_gamelibdir}/pb
cp -a pb/htm $RPM_BUILD_ROOT%{_gamelibdir}/pb

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README Docs PB_EULA.txt
%attr(755,root,root) %{_bindir}/*

%dir %{_gamelibdir}
%attr(755,root,root) %{_gamelibdir}/et
%dir %{_gamelibdir}/etmain
%attr(755,root,root) %{_gamelibdir}/etmain/*.so

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
%{_gamelibdir}/etmain/*.cfg
%{_gamelibdir}/etmain/*.pk3
%{_gamelibdir}/etmain/description.txt
%{_gamelibdir}/etmain/hunkusage.dat
#%{_gamelibdir}/et/etmain/video
%endif
