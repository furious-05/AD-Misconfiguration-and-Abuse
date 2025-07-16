#!/usr/bin/env python3

import hashlib
import argparse
from binascii import unhexlify
import sys
from typing import List, Tuple

try:
    from tqdm import tqdm
except ImportError:
    print("Please install tqdm: pip install tqdm")
    sys.exit(1)


def md4(data: bytes) -> bytes:
    try:
        return hashlib.new('md4', data).digest()
    except ValueError:
        from passlib.utils.md4 import md4
        return md4(data)


def parse_hash_line(line: str) -> Tuple[str, bytes, bytes]:
    try:
        parts = line.strip().split('$')
        rid = parts[0].split(':')[0]
        hashval = bytes.fromhex(parts[2])
        salt = bytes.fromhex(parts[3])
        return rid, hashval, salt
    except Exception as e:
        print(f"[!] Invalid hash format: {line}")
        sys.exit(1)


def load_hashes_from_file(path: str) -> List[Tuple[str, bytes, bytes]]:
    with open(path, 'r') as f:
        return [parse_hash_line(line) for line in f if line.strip()]


def load_wordlist(path: str) -> List[str]:
    with open(path, 'r', encoding='latin-1') as f:
        return [line.strip() for line in f if line.strip()]


def try_password(password: str, hash_data: Tuple[str, bytes, bytes]) -> bool:
    rid, target_hash, salt = hash_data
    nt_hash = md4(password.encode('utf-16le'))
    calc = hashlib.md5(nt_hash + salt).digest()
    return calc == target_hash


def crack_hashes(hashes: List[Tuple[str, bytes, bytes]], wordlist: List[str]):
    for rid, hashval, salt in hashes:
        print(f"\n[*] Cracking RID {rid}...")
        found = False
        for word in tqdm(wordlist, desc=f"🔍 RID {rid}", unit="pw", ncols=70):
            if try_password(word, (rid, hashval, salt)):
                print(f"\n[+] Password for RID {rid}: {word}")
                found = True
                break

        if not found:
            print(f"[-] Password for RID {rid} not found in wordlist.")


def test_single_password(password: str, hashes: List[Tuple[str, bytes, bytes]]):
    for rid, hashval, salt in hashes:
        if try_password(password, (rid, hashval, salt)):
            print(f"[+] RID {rid} is cracked with password: {password}")
        else:
            print(f"[-] RID {rid} not matched with password: {password}")


def main():
    parser = argparse.ArgumentParser(
        description="🔥 Timeroast Password Cracker — Crack MS-SNTP hashes with a wordlist or single password.",
        epilog="Example: python3 timeroast_cracker.py -H hashes.txt -w rockyou.txt"
    )

    group_hash = parser.add_mutually_exclusive_group(required=True)
    group_hash.add_argument('-H', '--hashes', help='File containing $sntp-ms$ hashes')
    group_hash.add_argument('--hash', help='Single hash line in format: RID:$sntp-ms$HASH$SALT')

    group_word = parser.add_mutually_exclusive_group(required=True)
    group_word.add_argument('-w', '--wordlist', help='Wordlist to try (e.g., rockyou.txt)')
    group_word.add_argument('--password', help='Single password to try against all hashes')

    args = parser.parse_args()

    if args.hashes:
        hash_entries = load_hashes_from_file(args.hashes)
    else:
        hash_entries = [parse_hash_line(args.hash)]

    if args.wordlist:
        words = load_wordlist(args.wordlist)
        crack_hashes(hash_entries, words)

    elif args.password:
        test_single_password(args.password, hash_entries)


if __name__ == '__main__':
    main()