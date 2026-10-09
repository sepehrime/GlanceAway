# GlanceAway

## Install on your Mac

1. Open `GlanceAway.dmg`.
2. Drag **GlanceAway** into **Applications**.
3. Eject the GlanceAway disk image, then open the app from **Applications**.

The app is not signed with a Developer ID or notarized, so macOS will warn
that it cannot check the app for malicious software. Only bypass this warning
if you trust the source and are sure the app has not been altered.

After trying to open the app:

1. Open **System Settings** and choose **Privacy & Security**.
2. Scroll to **Security** and click **Open Anyway** for GlanceAway.
3. Confirm that you want to open it in the warning dialog.

This approves this copy of the app on that Mac. For warning-free installation
on other Macs, the app needs to be signed with a Developer ID and notarized
with Apple.

## Build the Mac app

Run `./build_mac.sh` on a Mac with Python 3 and PyInstaller installed. The
script creates `release/GlanceAway.dmg`; running it again replaces that build.
The app is built for the Mac architecture used to run the script, so build it
on an Apple silicon Mac for Apple silicon users, or an Intel Mac for Intel
users.

If PyInstaller is missing from the Python interpreter the script selects,
install it with:

```sh
python3 -m pip install pyinstaller
```
