#!/usr/bin/env python3.7

import os
import enum
import shlex
import subprocess


class CipherMode(enum.Enum):
    CBC = 'cbc'
    CCM = 'ccm'
    CFB = 'cfb'
    CTR = 'ctr'
    ECB = 'ecb'
    OFB = 'ofb'


class AES128:
    BLOCK_SIZE = 16

    def __init__(self, key, mode):
        self._key = key
        self._mode = mode

    def encrypt(self, plaintext):
        iv = None
        command = [
            '/usr/lib/ssl1.0/openssl',
            f'aes-128-{self._mode.value}',
            '-e', 
            '-nosalt',
            '-K', self._key
        ]
        if self._mode != CipherMode.ECB:
            iv = os.urandom(16).hex()
            command.extend(['-iv', iv])
        command = ' '.join(command)
        process = subprocess.Popen(
            shlex.split(command), 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(plaintext)
        return iv, self._make_output(stdout, stderr)

    def decrypt(self, ciphertext, iv=None):
        command = [
            '/usr/lib/ssl1.0/openssl',
            f'aes-128-{self._mode.value}',
            '-d',
            '-nosalt', 
            '-K', self._key
        ]
        if self._mode != CipherMode.ECB:
            if iv is None or len(iv) == 0 or iv.isspace():
                return 'please specify iv'
            command.extend(['-iv', iv])
        command = ' '.join(command)
        process = subprocess.Popen(
            shlex.split(command), 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(ciphertext)
        return self._make_output(stdout, stderr)

    def _make_output(self, stdout, stderr):
        try:
            stdout = stdout.decode().strip('\n')
        except Exception:
            stdout = stdout.hex()
        output = []
        if len(stderr) > 0:
            output.append(stderr.decode().strip('\n'))
        if len(stdout) > 0:
            output.append(stdout)
        return '\n'.join(output)
