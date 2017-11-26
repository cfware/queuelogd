%define npm_name @cfware/queuelogd
Name:       cfware-queuelogd
Version:    0.1.0
Release:    0.1%{?dist}
Summary:    CFWare Queue Logger Daemon
License:    MIT
URL:        https://www.cfware.com/
Source0:    %{name}-%{version}.tgz
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

BuildRequires:  nodejs-packaging
Requires:       nodejs

Requires(pre): shadow-utils
Requires: rsyslog, logrotate

BuildRequires: pkgconfig(systemd)

%systemd_requires

%description
CFWare Queue Logger Daemon


%prep
%setup -q -n package


%build
# nothing to do


%install
install -d \
	%{buildroot}%{nodejs_sitelib}/%{npm_name} \
	%{buildroot}%{_bindir} \
	%{buildroot}%{_unitdir} \
	%{buildroot}%{_sysconfdir}/logrotate.d \
	%{buildroot}%{_sysconfdir}/rsyslog.d

cp -pr %{name}.js package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}
ln -s %{nodejs_sitelib}/%{npm_name}/%{name}.js %{buildroot}%{_bindir}/%{name}
cp %{name}.service %{name}.socket %{buildroot}%{_unitdir}
cp %{name}.json %{buildroot}/%{_sysconfdir}
cp logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
cp rsyslog.conf %{buildroot}/%{_sysconfdir}/rsyslog.d/%{name}.conf


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
exit 0


%post
%systemd_post %{name}.socket %{name}.service


%preun
%systemd_preun %{name}.socket %{name}.service


%postun
%systemd_postun_with_restart %{name}.socket %{name}.service


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{nodejs_sitelib}/*
%attr(0644,-,-) %{_unitdir}/%{name}.socket
%attr(0644,-,-) %{_unitdir}/%{name}.service

%attr(0640,root,%{name}) %config(noreplace)    %{_sysconfdir}/%{name}.json
%config(noreplace)    %{_sysconfdir}/logrotate.d/%{name}
%config               %{_sysconfdir}/rsyslog.d/%{name}.conf
