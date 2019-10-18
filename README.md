# activesync-curl
curl based tool to send messages using Microsoft Exchange ActiveSync protocol

# Description
This tool allows to send messages(and can be extended to more) using **Microsoft Exchange ActiveSync** protocol.
Networking mechanics are done using curl command line tool. The trickiest part is in conversion from readable xml format to binary wbxml. That is done using [libwbxml](https://github.com/libwbxml/libwbxml).

# As part of the implementation, following Microsoft Exchange AS commands are possible:
- Provision
- FolderSync
- SendMail

# How to use?
Suppose you have Mac. In case you have Ubuntu please fix accordingly, you would probably need to use *apt-get* instead of *brew*.

 1. Install using:

    ./install.sh

 2. Enter your credentials into *user.ini* file
 3. Login:

    ./ascurl.py login

 4. Enter you email into *send.mime* file
 5. Send that email using:
 

    ./ascurl.py send

# Known issues:
It' s probably [libwbxml](https://github.com/libwbxml/libwbxml) issue, it somehow misbehaves, when there are repeating text in xml. Basically, it skips some parts of it when there is repeating words. So, you may face issues when subject, mail body and recipient will contain the same word. Beware!

P.S. Maybe authors wanted to enforce diversity of language:)
