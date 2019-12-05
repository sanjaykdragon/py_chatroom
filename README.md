### py_chatroom - python chat client
created by @sanjaykdragon and @ve123 for the Massively Multiplayer Hackathon on repl.it. Theme is sharing, so we did a chatroom to "share" messages

#### description
This is a python chat client written with > 200 lines of code. The code quality here is OK, nothing amazing. This also relies on a php backend, which isn't great code, but it functions fine. I would recode this to support sockets and such, but as far as I know, repl.it doesn't support TCP / UDP sockets (or I don't know how to write them to work with repl's standards). Users can register by entering a username that doesn't exist. There are 2 admin accounts, me and @ve123 's.

#### technical information
multithreading was used to consistently update the chat messages on your screen. The comments on the functions in chat.py explain basically everything you need to know, such as:
- call hierarchy (what calls this function, what this function calls)
- import dependencies (in case you want to shorten / debloat the output, you can look through and find which functions use the most dependencies)
- function name and args explanation
- function description

#### links
php backend - https://github.com/sanjaykdragon/py_chatroom_backend

~170 LOC (although very unclean code, this could probably be shortened way more)

python client - https://github.com/sanjaykdragon/py_chatroom

more than 200 LOC (nicely commented, pretty clean)

#### features
- multithreaded chat system - chat automatically updates every few seconds
- account registry - register an account so that other people can't be an imposter of you
 - passwords not saved in plaintext - hashed passwords. should be basic security on this site.
- different message colors depending on admin, normal user, or if you were mentioned in the message! (like discord)
- code is commented well for future maintainability
- there is an optional encryption module, this was not used because it used pbkdf2 which is VERY slow, like 20 seconds per decryption / encryption. You are welcome to reimplement it, or find an alternative. The class for encryption is still there. 
- block user option (hides their messages, discord style)
- unblock user

#### other credits / mentions
- https://github.com/andrewcooke/simple-crypt - unused encryption
- https://github.com/areebbeigh/profanityfilter - profanity filter (not good)
the rest of the imports are more or less general / internal imports.

#### commands
/unblock user - unblocks a user

/block user - blocks a user

/lb - list blocked users

#### admin commands
/reset or /clear - clear chat
