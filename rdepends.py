#!/usr/bin/env python2
from __future__ import print_function
import os
import sys
import termcolor

# we use a global variable, because a class is overkill in this case
already_visited_packages = set()


def pprint_list(l):
    charlen = 0
    print("\t", end="")
    for word in l:
        if charlen > 50:
            charlen = 0
            print("\n", end="\t")
        charlen += len(word) + 1
        print(word, end="  ")
    print()


def list_rdepends(package, recurse_depth=0):
    """print all the reverse depends of a package"""
    if package in already_visited_packages:
        return
    else:
        already_visited_packages.add(package)
    rdepends = os.popen("""LANGUAGE=en_US pacman -Sii {0} | grep -im"""
            """ 1 "required by" | sed -r 's/^.+://'""".format(package)).read().strip()
    if rdepends == "None":
        return
    rdepends = rdepends.split()
    print(termcolor.colored(">> ", color="blue"),"rdepends of {} are: ".format(package))
    pprint_list(rdepends)
    if recurse_depth:
        for pac in rdepends:
            list_rdepends(pac, recurse_depth - 1)

if __name__ == "__main__":
    list_rdepends(sys.argv[1], 2)
