import codecs
import ConfigParser
import vobject
import sys

if len(sys.argv) != 3:
    print """python kab-distlists-to-vcard-categories.py <distlists file> <vCard file>
    <distlists file> usually is ~/.kde/share/apps/kabc/distlists
    <vCard file> may be ~/.kde/share/apps/kabc/std.vcf if the standard resource is used
        
A tool to convert KAddressbook(<=4.3) mail distribution lists to vCard categories.
The resulting vCard file goes to stdout.
See http://github.com/meeee/kaddressbook-distslists-to-vcard-categories for more information.
        """
    exit(1)


vcard_input_file = sys.argv[1]
distlists_input_file = sys.argv[2]


def parse_distlists(distlists_input_file):
    distlists = ConfigParser.ConfigParser()
    distlists.optionxform = unicode # overwrite default lowercase conversion
    
    distlists_input_stream = codecs.open(distlists_input_file, 'r', 'utf-8')
    
    distlists.readfp(distlists_input_stream)

    uid_lists_map = {}

    for distlist in distlists.items('DistributionLists'):
        list_name = distlist[0]
        member_uids = distlist[1].split(",,")

        if not member_uids or not member_uids[-1]: # empty list/unknown format
            continue
    
        assert member_uids[-1][-1] == ','
        member_uids[-1] = member_uids[-1][:-1] # remove comma from last entry
    
        for member_uid in member_uids:
            if uid_lists_map.has_key(member_uid):
                uid_lists_map[member_uid].append(list_name)
            else:
                uid_lists_map[member_uid] = [list_name]

    return uid_lists_map




uid_lists_map = parse_distlists(distlists_input_file)


input_stream = codecs.open(vcard_input_file, 'r', 'utf-8')
contacts = vobject.readComponents(input_stream)

for contact in contacts:
    # add possibly missing full name to prevent serialization errors
    try:
        contact.fn
    except AttributeError:
        contact.add('fn').value = 'Full Name Missing'

    # TODO parse value correctly or fix vobject
    #   - escaped commas (\,) are not parsed correctly
    try:
        contact.categories.value = contact.categories.value[0].split(",")
    except AttributeError:
        pass

    if uid_lists_map.has_key(contact.uid.value):
        lists = uid_lists_map[contact.uid.value]
        lists_string = ','.join(lists)
    
        try:
            contact.categories.value += lists
        except AttributeError:
            contact.add('categories').value = lists
    print contact.serialize().replace(vobject.base.CRLF, vobject.base.LF)

