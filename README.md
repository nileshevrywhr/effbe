# efFBe Scanner
Firebase is one of the widely used data stores for mobile applications. This is a Python3 rewrite of the original tool [FirebaseScanner](https://github.com/shivsahni/FireBaseScanner) which has the necessary research and history justifying the creation of this tool. 

## Getting Started

### Prerequisites
* Support for Python 3.9

### Usage

Say what the step will be

```
git clone https://github.com/NileshEvrywhr/effbe.git
```
Once the script is downloaded, run the script with the required arguments. We can either provide the APK file as an input as shown below:
```
python3 FirebaseMisconfig.py --path /home/nileshevrywhr/TestAPK/test.apk
or
python3 FirebaseMisconfig.py -p /home/nileshevrywhr/TestAPK/test.apk
```
Or we can provide the comma sperated firebase project names as shown below:
```
python3 FirebaseMisconfig.py --firebase project1,project2,project3
or
python3 FirebaseMisconfig.py -f project1,project2,project3
```
Or we can provide a file containing newline-separated firebase project names as shown below:
```
python3 FirebaseMisconfig.py --list filename
or
python3 FirebaseMisconfig.py -l filename

## Authors

* **Nilesh Kumar** - [LinkedIn](https://www.linkedin.com/in/NileshEvrywhr/)
