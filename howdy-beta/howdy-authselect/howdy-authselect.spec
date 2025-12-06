Name:           howdy-authselect
Version:        1.0.0
Release:        1%{?dist}
Summary:        Enable howdy face authentication in authselect-managed PAM

License:        MIT
URL:            https://github.com/boltgolt/howdy

Source0:        howdy-authselect
Source1:        howdy-authselect.service
Source2:        howdy-authselect.path
Source3:        README.md

BuildArch:      noarch

Requires:       howdy
Requires:       authselect
Requires:       systemd

%{?systemd_requires}

%description
A gruesome hack to work around authselect's "all or nothing" profile problem.

Fedora's authselect does not support extending profiles - you must copy and
maintain entire profiles to add a single PAM module. This package instead
patches pam_howdy.so into the existing authselect-managed configuration and
uses a systemd path unit to re-apply the patch when authselect regenerates
the PAM config.

%prep
# Nothing to prep - sources are scripts

%build
# Nothing to build

%install
install -Dm 0755 %{SOURCE0} %{buildroot}%{_bindir}/howdy-authselect
install -Dm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/howdy-authselect.service
install -Dm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/howdy-authselect.path

%post
%systemd_post howdy-authselect.path howdy-authselect.service

%preun
%systemd_preun howdy-authselect.path howdy-authselect.service

%postun
%systemd_postun_with_restart howdy-authselect.path howdy-authselect.service

%files
%doc %{SOURCE3}
%{_bindir}/howdy-authselect
%{_unitdir}/howdy-authselect.service
%{_unitdir}/howdy-authselect.path

%changelog
* Sat Dec 06 2025 Ronny Pfannschmidt <packaging@ronnypfannschmidt.de> - 1.0.0-1
- Initial package
