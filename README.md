[READ in case you are using PYPI]: #
[Pypi doesn't render package/relative path images and not raw]: #
[Pypi doesn't render Emojis]: #
[Pypi doesn't render LaTeX]: #
[https://github.com/theacodes/cmarkgfm]: #
[https://github.com/pypi/warehouse/issues/5246]: #
[https://github.com/pypi/warehouse/issues/16134]: #
[Mainly it's because HTML tags are omitted according to theacodes]: #
[So I recommend you rendering mardown locally or check my gitlab/codeberg]: #

# :robot: Fdroid-auto
[https://github.com/f-droid/artwork]: #
<div align="center">
    <img align="center"
        src="https://codeberg.org/Sivefunc/fdroid_auto/raw/branch/main/readme_res/logo.svg"
        height="200"
        alt="Logo of Fdroid with some apps in the background"><br>
</div>

# :bookmark: Table of contents
1. [About](#about)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Output](#output)
5. [Options](#options)
6. [Notes](#notes)

## :question: About <a name="about"></a>
Fdroid-auto is a very little program that automates the process of uninstalling, downloading and installing [F-droid](https://f-droid.org) apk's through [ADB](https://developer.android.com/tools/adb).

This is useful when doing Factory resets or changing of :iphone: phone and don't want to deal with the :repeat: repetitive task of :scream: [bootloop](https://en.wikipedia.org/wiki/Booting#Bootloop) while uninstalling because you didn't :brain: remember it was an important package or manually downloading F-droid apks by typing them into the search bar :mag: and then manually installing it.

## :file_folder: Installation <a name="installation"></a>

### :penguin: Binary dependencies (Unix)
```sh
sudo apt-get install python3 python3-pip python3-setuptools adb
```

### :snake: Option 1: Pypi
```sh
python3 -m pip install fdroid-auto
```

### :hand: Option 2: Git repository (Still connects to Pypi)
```sh
git clone https://codeberg.org/Sivefunc/fdroid_auto
cd fdroid_auto
python3 -m pip install .
```

## :computer: Usage <a name="usage"></a>
1. Enable [USB Debugging](https://developer.android.com/studio/debug/dev-options#Enable-debugging) on your Android device :iphone:
2. Connect your Android device to the Host computer through the USB cable.
3. There are two files [apps/uninstall.txt](https://codeberg.org/Sivefunc/fdroid_auto/src/branch/main/src/apps/uninstall.txt) and [apps/download.txt](https://codeberg.org/Sivefunc/fdroid_auto/src/branch/main/src/apps/download.txt) which are examples files you can download and use.

usage: fdroid_auto [options](#options)

### :clipboard: Uninstalling
```sh
fdroid_auto -u apps/uninstall.txt       # Uninstall packages listed.
```
### :clipboard: Downloading
```sh
fdroid_auto -d apps/download.txt apps/  # Download packages listed
                                        # and saved them on apps/
```
### :clipboard: Installing
```sh
fdroid_auto -i apps/                    # Install packages listed
                                        # on directory apps/
```
### :handshake: Joined together
```sh
fdroid_auto.py -u apps/uninstall.txt \
               -d apps/download.txt apps/ \
               -i apps/
```

## :page_facing_up: Output <a name="output"></a>
| Uninstalling          | Downloading           | Installing
| :---:  		        | :---:    		        | :---:
| ![1](https://codeberg.org/Sivefunc/fdroid_auto/raw/branch/main/readme_res/uninstall.png)| ![2](https://codeberg.org/Sivefunc/fdroid_auto/raw/branch/main/readme_res/download.png)| ![3](https://codeberg.org/Sivefunc/fdroid_auto/raw/branch/main/readme_res/install.png)

## :gear: Options <a name="options"></a>
- `-h,              --help                        → show this help message
                                                        and exit.`
- `-v,              --version                     → show program's version
                                                        number and exit.`
- `-u [FILE],       --uninstall [FILE]            → Uninstall ALL packages
                                                        listed from FILE on
                                                        device using adb.`
- `-d [FILE] [DIR], --download [FILE] [DIR]       → Download ALL fdroid .apks
                                                        listed from FILE and
                                                        push them into DIR.`
- `-i [DIR],        --install [DIR]               → Install ALL packages .apk
                                                        listed from DIR on
                                                        device using adb.`
- `n,               --notation                    → Shows how to format the
                                                        FILE and exit.`
## :notebook: Notes <a name="notes"></a>
- :bangbang: The order of events occur in the following way:
    - Uninstall: `adb shell pm uninstall -k --user 0`
    - Download
    - Install:   `adb install`

- Suggested versions are the ones downloaded (not the latest unstable? version).
- :shield: [Official](https://f-droid.org/docs/All_our_APIs/) repository is the one being used.
- [Third party repositories](https://forum.f-droid.org/t/known-repositories/721) are not supported like [Bromite](https://www.bromite.org/fdroid)
- Uninstall/Install of apps is not limited to only F-droid, if these are installed or on a directory respectively.
- I haven't tested ADB through [Wi-Fi](https://developer.android.com/tools/adb#connect-to-a-device-over-wi-fi) only USB.
- Manuals I used: man adb or adb shell pm
- Read the source code to know things are done, specially [packages.py](https://codeberg.org/Sivefunc/fdroid_auto/src/branch/main/src/packages.py)
- The `-k` option on uninstall preserves app data, so you can reinstall with install-existing and not lose data.
- I recommend when looking for files to uninstall instead of the traditional `adb shell pm list packages` use [App Manager](https://f-droid.org/en/packages/io.github.muntashirakon.AppManager/)

## Made by :link: [Sivefunc](https://gitlab.com/sivefunc)
## Licensed under :link: [GPLv3](https://codeberg.org/Sivefunc/fdroid_auto/src/branch/main/LICENSE)
