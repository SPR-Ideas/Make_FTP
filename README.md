# Instant FTP server.

## Description
_The Project Instant Ftp server ,servers a file which is on your the local machine and tunnels to a public url,so that anybody on the internet can download the file which is on your local machine._

**Note :** The script can only work on unix and linux machines.we are not tested this script on windows. It will brought on  later revisions.

## Dependencies:

* pyngrok
* fastapi
* uvicorn

**External Dependencies**
### **Ngrok**
_Ngrok is simple tunneling tool ,Make sure it sholuld be installed and authentication key is set.Use this link to install [Ngrok](http://ngrok.com)_


## Installation

1. Clone the repository using git clone.
```
$ git clone https://github.com/SPR-Ideas/Make_FTP.git
```

2. Type make install. It installs the major dependencies but it won't install ngrok.
```
$ make install
```

## Remove
To remove the script just navigate to the file directory and run
```
$ make uninstall
```

## Usage

```
$ make-ftp <file_location>
```
It will give you a link with ngrok sub-domain which can be shared between the users to share the file.
