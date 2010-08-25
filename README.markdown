# KAdressbook Mail Distribution Lists to vCard Categories

[KAddressbook](http://userbase.kde.org/Kontact), until version 4.3, provides a feature to create **mail distribution lists** which are saved in a non-standard format. I found for example no way to migrate these lists into [Evolution](http://projects.gnome.org/evolution/). This is the purpose of this tool.

This script reads the distribution lists from a KAddressbook configuration file and adds their names as categories to the corresponding contacts in a given vCard file. The matching is done via vCard UIDs, the way KAddressbook stores the recipients in a distribution list.

## Requirements
 * Python, tested using version 2.6 on Mac OS X 10.6 Snow Leopard.
 * Python module [vobject](http://vobject.skyhouseconsulting.com/) as vCard parser and generator: `easy_install vobject`

## Usage
    python kab-distlists-to-vcard-categories.py <distlists file> <vCard file>

        <distlists file> usually is ~/.kde/share/apps/kabc/distlists
        <vCard file> may be ~/.kde/share/apps/kabc/std.vcf if the standard resource is used

### Example
The output of the modified vCard data happens on the standard output so you may want to redirect it into a file:

    python kab-distlists-to-vcard-categories.py \
        ~/.kde/share/apps/kabc/distlists \
        ~/.kde/share/apps/kabc/std.vcf \
         > contacts-with-distlists-as-categories.vcf

## Known issues
 * *Commas (,)* in existing categories may result in split up category names. This is due to a workaround for an issue with the vCard parser which does not correctly split up existing categories.
 * *Missing full names* for existing contacts are set to "Full Name Missing". Otherwise the vCard generator would fail.
 * *Parse errors* - the vCard parser fails on non-standard compliant vCard files. In this case the output may stop half way and an error message is shown.
 * The parser converts all *vCard keys to uppercase*. Even keys like X-KAdressbook-... are converted - I don't know wether this is standard compliant or confuses some applications like KAddressbook
