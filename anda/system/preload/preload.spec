Name:           preload
Version:        0.6.4
Release:        1%{?dist}
Summary:        Adaptive readahead daemon
Packager:       veuxit <erroor234@gmail.com> 

License:        GPL-2.0-only
URL:            http://sourceforge.net/projects/preload
Source0:        http://downloads.sourceforge.net/sourceforge/preload/%{name}-%{version}.tar.gz
Source1:        preload.service

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd-devel
BuildRequires:  glib2-devel
BuildRequires:  help2man
Requires:       glib2

%description
preload is an adaptive readahead daemon. It monitors applications that users 
run, and by analyzing this data, predicts what applications users might run, 
and fetches those binaries and their shared libraries into memory for faster 
startup times.

%prep
%autosetup

%build
%configure --prefix=%{_usr} \
              --localstatedir=%{_var} \
              --mandir=%{_mandir} \
              --sbindir=%{_bindir} \
              --sysconfdir=%{_sysconfdir}
%make_build

%install
%make_install sysconfigdir=%{_sysconfdir}/conf.d

install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

rm -rf %{buildroot}%{_etc}/rc.d
rm -rf %{buildroot}%{_var}/lib/preload/preload.state
rm -rf %{buildroot}%{_var}/log/preload.log

sed -r -i 's#^((map|exe)prefix =) (.+)$#\1 /opt;\3#' %{buildroot}%{_sysconfdir}/preload.conf

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license COPYING
%doc README NEWS AUTHORS ChangeLog
%{_sysconfdir}/conf.d/preload
%{_sbindir}/preload
%{_unitdir}/%{name}.service
%{_mandir}/man8/preload.8*
%dir %{_var}/lib/preload
%{_sysconfdir}/logrotate.d/preload
%{_sysconfdir}/rc.d/init.d/preload
%{_docdir}/%{name}-%{version}/*
%{_sysconfdir}/preload.conf


%changelog
* Sat Mar 14 2026 veuxit <erroor234@gmail.com> - 0.6.4-1
- Initial package
