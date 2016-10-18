import json
import sys

from parse import parse

IGNORE = [u'{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}', u'{b9db16a4-6edc-47ec-a1f4-b86292ed211d}', u'easyscreenshot@mozillaonline.com', u'firebug@software.joehewitt.com', u'{20a82645-c095-46ed-80e3-08825760534b}', u'{73a6fe31-595d-460b-a920-fcc0f8843232}', u'{DDC359D1-844A-42a7-9AA1-88A850A938A8}', u'firefox@ghostery.com', u'{e4a8a97b-f2ed-450b-b12d-ee082ba24781}', u'adblockpopups@jessehakanen.net', u'artur.dubovoy@gmail.com', u'{a0d7ccb3-214d-498b-b4aa-0e8fda9a7bf7}', u'{19503e42-ca3c-4c27-b1e2-9cdb2170ee34}', u'{b9bfaf1c-a63f-47cd-8b9a-29526ced9060}', u'{dc572301-7619-498c-a57d-39143191b318}', u'uBlock0@raymondhill.net', u'elemhidehelper@adblockplus.org', u'{3d7eb24f-2740-49df-8937-200b1cc08f8a}', u'testpilot@labs.mozilla.com', u'translator@zoli.bod', u'{46551EC9-40F0-4e47-8E18-8E5CF550CFB8}', u'YoutubeDownloader@PeterOlayev.com', u'{bee6eb20-01e0-ebd1-da83-080329fb9a3a}', u'{1018e4d6-728f-4b20-ad56-37578a4de76b}', u'feca4b87-3be4-43da-a1b1-137c24220968@jetpack', u'info@youtube-mp3.org', u'{c45c406e-ab73-11d8-be73-000a95be3b12}', u'{d40f5e7b-d2cf-4856-b441-cc613eeffbe3}', u'{a7c6cf7f-112c-4500-a7ea-39801a327e5f}', u'{D4DD63FA-01E4-46a7-B6B1-EDAB7D6AD389}', u'{1BC9BA34-1EED-42ca-A505-6D2F1A935BBB}', u'client@anonymox.net', u'{fe272bd1-5f76-4ea4-8501-a05d35d823fc}', u'{81BF1D23-5F17-408D-AC6B-BD6DF7CAF670}', u'{5384767E-00D9-40E9-B72F-9CC39D655D6F}', u'personas@christopher.beard', u'{64161300-e22b-11db-8314-0800200c9a66}', u'ClassicThemeRestorer@ArisT2Noia4dev', u'jid1-F9UJ2thwoAm5gQ@jetpack', u'anttoolbar@ant.com', u'{E0B8C461-F8FB-49b4-8373-FE32E9252800}', u'firegestures@xuldev.org', u'firefoxdav@icloud.com', u'{e968fc70-8f95-4ab9-9e79-304de2a71ee1}', u'{b9acf540-acba-11e1-8ccb-001fd0e08bd4}', u'{195A3098-0BD5-4e90-AE22-BA1C540AFD1E}', u'{9AA46F4F-4DC7-4c06-97AF-5035170634FE}', u'foxmarks@kei.com', u'donottrackplus@abine.com', u'nosquint@urandom.ca', u'support@lastpass.com', u'foxyproxy@eric.h.jung', u'ich@maltegoetz.de', u'{b749fc7c-e949-447f-926c-3f4eed6accfe}', u'jid1-HAV2inXAnQPIeA@jetpack', u'{77b819fa-95ad-4f2c-ac7c-486b356188a9}', u'netvideohunter@netvideohunter.com', u'{7b1bf0b6-a1b9-42b0-b75d-252036438bdc}', u'{a62ef8ec-5fdc-40c2-873c-223b8a6925cc}', u'{1280606b-2510-4fe0-97ef-9b5a22eafe30}', u'{E6C1199F-E687-42da-8C24-E7770CC3AE66}', u'{6AC85730-7D0F-4de0-B3FA-21142DD85326}', u'{0b457cAA-602d-484a-8fe7-c1d894a011ba}', u'vk@sergeykolosov.mp', u'{5C655500-E712-41e7-9349-CE462F844B19}', u'{6c28e999-e900-4635-a39d-b1ec90ba0c0f}', u'youtubeunblocker@unblocker.yt', u'isreaditlater@ideashower.com', u'2.0@disconnect.me', u'jid1-xUfzOsOFlzSOXg@jetpack', u'mintrayr@tn123.ath.cx', u'{0545b830-f0aa-4d7e-8820-50a4629a56fe}', u'{f3bd3dd2-2888-44c5-91a2-2caeb33fb898}', u'{097d3191-e6fa-4728-9826-b533d755359d}', u'{25A1388B-6B18-46c3-BEBA-A81915D0DE8F}', u's3google@translator', u'{9AA46F4F-4DC7-4c06-97AF-6665170634FE}', u'{dd3d7613-0246-469d-bc65-2a3cc1668adc}', u'jid0-GXjLLfbCoAx0LcltEdFrEkQdQPI@jetpack', u'SQLiteManager@mrinalkant.blogspot.com', u'{cd617375-6743-4ee8-bac4-fbf10f35729e}', u'amznUWL2@amazon.com', u'helper@savefrom.net', u'lookout@aron.rubin', u'paulsaintuzb@gmail.com', u'{7f57cf46-4467-4c2d-adfa-0cba7c507e54}', u'{888d99e7-e8b5-46a3-851e-1ec45da1e644}', u'extra-cols@jminta_gmail.com', u'firefox-hotfix@mozilla.org', u'{B17C1C5A-04B1-11DB-9804-B622A1EF5492}', u'{8f8fe09b-0bd3-4470-bc1b-8cad42b8203a}', u'ffext_basicvideoext@startpage24', u'{1A2D0EC4-75F5-4c91-89C4-3656F6E44B68}', u'xthunder@lshai.com', u'{54BB9F3F-07E5-486c-9B39-C7398B99391C}', u'tabscope@xuldev.org', u'printPages2Pdf@reinhold.ripper', u'{53A03D43-5363-4669-8190-99061B2DEBA5}', u'smarterwiki@wikiatic.com', u'jid1-ZAdIEUB7XOzOJw@jetpack', u'pavel.sherbakov@gmail.com', u'{0538E3E3-7E9B-4d49-8831-A227C80A7AD3}']


def mpc_list():
    parsed = parse()
    compat_count = {'undefined': []}
    for data in parsed:
        compat = data.get('compat', {}).get('e10s', 'undefined')
        compat_count.setdefault(compat, [])
        compat_count[compat].append(compat)

    for k, v in compat_count.items():
        print '%s: %s' % (k, len(v))


def addons_for_arewe10syet():
    """
    For bug https://bugzilla.mozilla.org/show_bug.cgi?id=1299251, find all
    addons with more than 2000 users and output a format that arewee10syet can
    understand.

    Skip a list of add-ons already in arewee10syet.com at this date.
    """
    parsed = parse()
    output = []
    for data in parsed:
        addon = data['addon']
        if addon['guid'] in IGNORE:
            continue

        users = addon.get('average_daily_users', 0)
        if users < 2000:
            continue

        output.append({
            'guid': addon['guid'],
            'testing': [],
            'bugs': [],
            'users':users
        })

    print json.dumps(output, indent=2)


def sdk_list():
    parsed = parse()
    compat_count = {'undefined': []}
    for data in parsed:
        compat = data.get('compat', {}).get('e10s', 'undefined')
        if compat == 'compatible':
            addon = data['addon']
            print '{},{},{}'.format(
                addon['name'], addon['guid'], addon['average_daily_users']
            )


if __name__ == '__main__':
    recipe = sys.argv[1]
    if recipe not in locals():
        print 'Unknown recipe:', recipe
        sys.exit()

    else:
        locals()[recipe]()
