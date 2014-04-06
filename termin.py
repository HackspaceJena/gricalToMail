from icalendar import Calendar
import pytz

class Termin(object):
    #keys = ('DTSTAMP', 'DESCRIPTION', 'URL', 'SUMMARY', 'LOCATION', 'DTSTART', 'GEO', 'CLASS', 'CATEGORIES', 'UID')
    keys = ('DTSTAMP', 'DESCRIPTION', 'URL', 'SUMMARY', 'LOCATION', 'DTSTART', 'CLASS', 'CATEGORIES', 'UID')

    @staticmethod 
    def from_entry(entry):
        """
        baut aus einem iCalender eintrag ein Termin Objekt
        """
        termin = Termin()
        for key in Termin.keys:
            if key in entry:
                termin.value[key] = entry.decoded(key)
        return termin

    def __init__(self):
        self.value = {}

    def get(self, name):
        return self.value[name]

    def get_local_start_time(self):
        """
        x.get_local_start_time() -> datum

        Gibt start Zeitpunkt des begines von Termin x in lokaler Zeit zurueck
        datum ist ein Objekt.
        """
        datum = self.value["DTSTART"]
        # wenn keine Zeitzone angeben ist, nehme UTC an
        if not datum.tzinfo:
            src_zone = pytz.timezone("UTC")
            datum = src_zone.localize(datum)
        # und jetzt umwandeln
        dst_zone = pytz.timezone("Europe/Berlin")
        return datum.astimezone(dst_zone)

    def __str__(self):
        datum = self.get_local_start_time().strftime("%Y-%m-%d %H:%M")
        if "DESCRIPTION" in self.value:
            return "%s: %s - %s" % (datum, self.value["SUMMARY"], self.value["DESCRIPTION"])
        return "%s: %s" % (datum, self.value["SUMMARY"])

def load_from_str(data):
    """
    load_from_str(data) -> list

    Konvertiert eine gelesene iCalender Datei in eine nach Datum sortierte Liste von Termin Objekten.
    data is String
    list is a list from Termin objects
    """
    cal = Calendar.from_ical(data)
    # aus dem ical eine Liste von Termin Objekten bauen
    liste = [Termin.from_entry(entry) for entry in cal.subcomponents]
    # liste nach Datum sortieren
    liste.sort(key=lambda datum: datum.get("DTSTART").timetuple())
    return liste
