[app]

# (str) Title of your application
title = FuelStationInspection

# (str) Package name
package.name = fuelstationinspection

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,sqlite3,reportlab

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Path to the window icon
# icon.filename = %(source.dir)s/data/icon.png

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 30

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use
android.ndk = 21b

# (bool) Indicate if you want to enable Android logcat
android.logcat = 1

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.renpy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
#android.service = MyService

# (list) Pattern to whitelist for the compiled lib distribution
#android.whitelist =

# (str) Path to custom Java source
#android.src =

# (str) XML file to include as an intent filter in the main activity
#android.manifest.intent_filters =

# (str) XML file to include as a permissions for the application
#android.manifest.permissions =

# (str) Android additional libraries to copy into the libs directory
#android.add_libs_armeabi_v7a = libs/android/*.so

# (bool) Copy library instead of linking
#android.copy_libs = 1

# (list) Android compiled python files to package
#android.include_exts = py

# (list) Android additional AAR dependencies
#android.add_aars =

# (list) Put these files or directories in the apk's assets folder
#android.add_assets =

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (str) Custom command to run at the end of packaging the app
#android.post_package =

# (bool) Indicate whether to include Android TV intents
#android.android_tv = False

# (bool) Enable android's logcat viewing in kivy
#android.logcat_view = True

# (str) Android adb command
#android.adb = %(ANDROID_HOME)s/platform-tools/adb

# (bool) Android packaging command
#android.packaging = True

# (str) Android minimum sdk version to use
#android.sdk = 21

# (str) Android sdk directory
#android.sdk_dir = /home/user/.buildozer/android/platform/android-sdk-21

# (str) Android ndk directory
#android.ndk_dir = /home/user/.buildozer/android/platform/android-ndk-r21

# (str) android.cmake_dir =

# (list) Android add compile flags
#android.add_compile_flags =

# (str) Android theme
#android.theme = "Theme.NoTitleBar"

# (str) Source code where the main.py live
source.dir = .

# (str) Title of your application
title = FuelStationInspection

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Application version
version = 0.1

# (list) Application requirements
#comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,sqlite3,reportlab

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Supported orientations
orientation = portrait

# (int) Android API to use
android.api = 30

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*.png

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Path to the window icon
# icon.filename = %(source.dir)s/data/icon.png

# (str) Python version to use
#python3_version = 3.9.1
