Name:           howdy-authselect
Version:        1.0.0
Release:        2%{?dist}
Summary:        Enable howdy face authentication in authselect-managed PAM

License:        MIT
URL:            https://github.com/boltgolt/howdy

Source0:        howdy-authselect
Source1:        howdy-authselect.service
Source2:        howdy-authselect.path
Source3:        90-howdy-authselect.preset
Source4:        README.md

BuildArch:      noarch

BuildRequires:  systemd-rpm-macros

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
install -Dm 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/systemd/system-preset/90-howdy-authselect.preset
install -Dm 0644 %{SOURCE4} %{buildroot}%{_docdir}/%{name}/README.md

%post
%systemd_post howdy-authselect.path howdy-authselect.service
# On fresh install, enable the path unit and patch PAM
if [ $1 -eq 1 ]; then
    systemctl preset howdy-authselect.path >/dev/null 2>&1 || :
    systemctl start howdy-authselect.path >/dev/null 2>&1 || :
    %{_bindir}/howdy-authselect enable >/dev/null 2>&1 || :
fi

%preun
%systemd_preun howdy-authselect.path howdy-authselect.service
# On uninstall, remove howdy from PAM
if [ $1 -eq 0 ]; then
    %{_bindir}/howdy-authselect disable >/dev/null 2>&1 || :
fi

%postun
%systemd_postun_with_restart howdy-authselect.path howdy-authselect.service

%files
%{_bindir}/howdy-authselect
%{_unitdir}/howdy-authselect.service
%{_unitdir}/howdy-authselect.path
%{_prefix}/lib/systemd/system-preset/90-howdy-authselect.preset
%{_docdir}/%{name}/README.md

%changelog
* Sat Dec 06 2025 Ronny Pfannschmidt <packaging@ronnypfannschmidt.de> - 1.0.0-2
- Add systemd preset file to auto-enable the path unit on install
- Run howdy-authselect enable during post-install to patch PAM immediately
- Run howdy-authselect disable during pre-uninstall to clean up PAM

* Sat Dec 06 2025 Ronny Pfannschmidt <packaging@ronnypfannschmidt.de> - 1.0.0-1
- Initial package
