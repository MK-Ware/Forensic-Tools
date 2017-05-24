# If the target device has USB debugging enabled:
____________________________________________________________________________
If the target device has USB debugging enabled, it doesn't matter whether or not it is locked with a PIN, pattern, or password.

1- Simply download Minimal ADB and Fastboot from:

https://androidmtk.com/download-minimal-adb-and-fastboot-tool

or

https://forum.xda-developers.com/showthread.php?t=2317790

portable version can be found here:

https://docs.google.com/file/d/0B2ghGhwyFr5hOWxvZWdBR3VkRlE/view

2- After installing/extracting it, connect the target phone to your computer (you need to have the drivers for the target device installed, hint: google), open cmd (start menu --> cmd --> enter). In the console, enter cd <full path of the directory containing adb and fastboot> assuming you installed it in D:\Program Files\Minimal ADB and Fastboot:

C:\Users\Investigator>cd D:\Program Files\Minimal ADB and Fastboot
C:\Users\Investigator>d:
D:\Program Files\Minimal ADB and Fastboot>adb shell

assuming the target device is a HTC One M8, you should see the following in the console window:

root@m8:/ #

3 -Now enter cp <full path of the database file on the android device> /sdcard/. For example to extract whatsapp msgstore.db database:

root@m7:/ # cp /data/data/com.whatsapp/databases/msgstore.db /sdcard/

Wait for the database file to be copied to sdcard, then enter:

root@m7:/ # exit

4- That should bring you back to the directory containing adb and fastboot binaries, enter adb pull /sdcard/<database name>:

D:\Program Files\Minimal ADB and Fastboot>adb pull /sdcard/msgstore.db

Wait for your computer to finish copying the database file from the target device to the working directory... Done! Check the working directory (D:\Program Files\Minimal ADB and Fastboot), it should contain the database file (in our example msgstore.db).

You can use these steps to copy any database file from an android device that has USB debugging enabled. If the target device doesn't have USB debugging enabled, you can enable it by going to settings --> developer options --> check USB debugging (or ADB debugging in some ROMs). If you can't see developer options, settings --> About --> Software Information --> More --> tap build number untill you see a toast saying developer options enabled or you are now a developer (usually you will need to tap it 7 times).
___________________________________________________________________________________________________________________________________________

# If the target device is Locked AND doesn't have USB debugging enabled:
____________________________________________________________________________
If the target device is locked, and doesn't have USB debugging enabled, you will have to install a custom recovery and then install aroma file manager. Usually that requires rooting your android device. You might find a way to unlock your android device without rooting it, but this is the rare exception, not the rule. For more info refer to google.

Aroma file manager allows you to browse your android device from recovery:

http://www.androidauthority.com/aroma-file-manager-recovery-mode-90778/

Once you have aroma file manager installed and ready, use it to navigate to the directory containing the database file, copy the file to an external microSD memory card or a USB flash drive (if your android device supports USB OTG which most devices do).

Note: some custom recoveries (like the latest versions of TWRP recovery) come with a file manager out of the box, in that case you don't have to bother with installing aroma file manager.
