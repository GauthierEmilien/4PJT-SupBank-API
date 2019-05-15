def getPrivKeyFromECC(key):
    return key \
        .replace('-----BEGIN PRIVATE KEY-----', '') \
        .replace('\n', '') \
        .replace('-----END PRIVATE KEY-----', '')


def getPubKeyFromECC(key):
    return key \
        .replace('-----BEGIN PUBLIC KEY-----', '') \
        .replace('\n', '') \
        .replace('-----END PUBLIC KEY-----', '')
