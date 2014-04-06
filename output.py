import argparse
import termin

def output_format(termin_obj):
    datum = termin_obj.get_local_start_time().strftime("%Y-%m-%d %H:%M")
    name = termin_obj.get("SUMMARY")
    return "%s: %s" % (datum, name)

# Command Line Parser
parser = argparse.ArgumentParser(description="Process some iCalender files.")
parser.add_argument("--file", "-f", required=True, help="Some iCalender files")
args = parser.parse_args()

# Main
fobj = open(args.file,"rb")
data = fobj.read()
liste = termin.load_from_str(data)
# alle Termine ausgeben
for item in liste:
    print(output_format(item))
