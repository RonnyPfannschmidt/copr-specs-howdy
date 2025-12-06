# howdy-authselect

> **Warning**: This is a gruesome AI-dreamed hack.

## The Problem

Fedora's `authselect` manages PAM configuration through profiles. These profiles are "all or nothing" - you cannot extend an existing profile with additional features without copying and maintaining the entire profile.

The upstream profiles (sssd, local, etc.) include features like `with-fingerprint` for fprintd, but there's no `with-howdy` option. Adding one would require:

1. Copying the entire profile (system-auth, password-auth, fingerprint-auth, smartcard-auth, postlogin, nsswitch.conf, dconf-db, dconf-locks, README, REQUIREMENTS)
2. Adding our single line for pam_howdy.so
3. Maintaining this copy forever as upstream authselect evolves

This is unsustainable for a single PAM module addition.

## The Hack

Instead of maintaining full profile copies, this package:

1. Lets authselect manage PAM configuration normally
2. Patches in `pam_howdy.so` after the fact
3. Uses a systemd path unit to re-apply the patch whenever authselect regenerates the config

This is ugly but pragmatic. We inject one line:

```
auth        sufficient                                   pam_howdy.so
```

## Usage

```bash
# Enable howdy in PAM (run once after installing howdy)
sudo howdy-authselect enable

# Enable automatic re-patching after authselect changes
sudo systemctl enable --now howdy-authselect.path

# Check status
howdy-authselect status

# Disable if needed
sudo howdy-authselect disable
```

## Why Not Upstream?

The proper fix would be for authselect to support `with-howdy` natively, similar to `with-fingerprint`. This would require:

1. Acceptance of howdy as a supported authentication method in Fedora
2. Patches to the authselect package itself
3. Coordination with the authselect maintainers

Until then, we hack.

## Immutable Distros (Silverblue/Kinoite/Bazzite)

This hack should work on immutable Fedora variants because:

- `/etc/authselect/` is part of the writable `/etc` overlay
- The systemd path unit watches files in `/etc`, which is persistent
- `rpm-ostree install howdy howdy-authselect` layers both packages

After layering and rebooting:
```bash
sudo howdy-authselect enable
sudo systemctl enable --now howdy-authselect.path
```
