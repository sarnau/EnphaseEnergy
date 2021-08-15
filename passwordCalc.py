#!/usr/bin/python3

import hashlib
import time

serialNumber = b'122112123456'
userName = b'installer'

DEFAULT_REALM = b'enphaseenergy.com'
gSerialNumber = None

def emupwGetPasswdForSn(serialNumber, userName, realm):
    if serialNumber == None or userName == None:
        return None
    if realm == None:
        realm = DEFAULT_REALM
    return hashlib.md5(b'[e]' + userName + b'@' + realm + b'#' + serialNumber + b' EnPhAsE eNeRgY ').hexdigest()

def emupwGetPasswd(userName,realm):
    global gSerialNumber
    if gSerialNumber:
        return emupwGetPasswdForSn(gSerialNumber, userName, realm);
    return None;

def emupwGetPublicPasswd(serialNumber, userName, realm, expiryTimestamp=0):
    if expiryTimestamp==0:
        expiryTimestamp = int(time.time());
    return hashlib.md5(userName + b'@' + realm + b'#' + serialNumber + b'%d' % expiryTimestamp).hexdigest()

def emupwGetMobilePasswd(serialNumber,userName,realm=None):
    global gSerialNumber
    gSerialNumber = serialNumber
    digest = emupwGetPasswdForSn(serialNumber,userName,realm)
    countZero = digest.count('0')
    countOne = digest.count('1')
    password = ''
    for cc in digest[::-1][:8]:
        if countZero == 3 or countZero == 6 or countZero == 9:
            countZero = countZero -1
        if countZero > 20:
            countZero = 20
        if countZero < 0:
            countZero = 0

        if countOne == 9 or countOne == 15:
            countOne = countOne -1
        if countOne > 26:
            countOne = 26
        if countOne < 0:
            countOne = 0
        if cc == '0':
            password += chr(ord('f') + countZero)
            countZero = countZero - 1
        elif cc == '1':
            password += chr(ord('@') + countOne)
            countOne = countOne -1
        else:
            password += cc
    return password

print(emupwGetMobilePasswd(serialNumber,userName))
