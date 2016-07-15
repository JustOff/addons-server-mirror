import sys

from parse import parse

def mpc_list():
    parsed = parse()
    compat_count = {'undefined': []}
    for data in parsed:
        compat = data.get('compat', {}).get('e10s', 'undefined')
        compat_count[compat].append(data)

    for k, v in compat_count.items():
        print '%s: %s' % (k, len(v))
# If you want to print out the URL for the add-on.
#        for addon in v:
#            print addon['addon']['url']
#        print


if __name__ == '__main__':
    recipe = sys.argv[1]
    if recipe not in locals():
        print 'Unknown recipe:', recipe
        sys.exit()

    else:
        locals()[recipe]()
