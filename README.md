Becky IVR
=========

Becky IVR, the voice menu from hell ! A small project written during the
weekend for fun :)

Inspired by Marc Labreche's Soap Opera Parody 'Le coeur a ses raisons'. Brett
attempts to call Becky but reaches her voicemail, and gets lost trying to
navigate the very confusing phone menu ;) The original sketch can be viewed on
youtube (https://www.youtube.com/watch?v=IzJbo1DlJSQ)

This is an attempt at recreating Becky's voicemail menu using free and open source
software. The IVR is written using asterisk dialplan. (I've also
included a small python script used for spam protection). 

As a side note, this project can easily be reused as a comedic example on how
to write IVRs using asterisk !

Requirements
============

 * Asterisk 1.8 or later

Optional, but needed for the spam protection script:

 * python 2.6 or later
 * python-sqlite


Installation
============

1. Copy files
2. Create the database (if you want to use spam protection)
3. Add the sound prompts
3. Add diaplan to extensions.conf

Copying files
-------------

The files need to be somewhere with read/write permissions for asterisk. By
default the script assumes you will copy files in /var/lib/asterisk/becky.
Don't forget to change the constants in becky.conf if you put the files
somewhere else.

    cp -R becky /var/lib/asterisk
    chown -R asterisk:asterisk /var/lib/asterisk/becky

Create database
---------------

Execute the script in the database folder 

    cd /var/lib/asterisk/becky/database
    ./createdb.sh

Sound prompts
-------------

Unfortunately, for copyright reasons, I cannot include the original sound
prompts in the project. However, you can make your own ! More details in the
README under the sounds directory.

Once you have your prompts, you need to put them somewhere asterisk can find
them.  A link placed inside asterisk's sounds directory usually does the trick.

    ln -s /var/lib/asterisk/sounds/becky /path/to/becky/sounds

*WARNING*: Currently on ubuntu/debian, paths to custom sound prompts are buggy.
A workaround is to place the link directly in /usr/share/asterisk/sounds

Dialplan
--------

Add this line somewhere in /etc/asterisk/extensions.conf (the # isn't a comment !)

    #include /var/lib/asterisk/becky/dialplan/becky.conf

Then add an extension that redirects towards the IVR

    exten => 1000,1,Goto(becky-answer,s,1)

If you want to use the spam protection script, use this line instead

    exten => 1000,1,Goto(becky-spam-protect)

Contributions
=============

Want to make Becky even better ? Feel free to fork and submit a pull request !

Currently, I would be really interested in some freely distributable sound prompts.
See the README under the sounds directory for more details.

License
=======

This project is released under the MIT license. See LICENSE for more details.
