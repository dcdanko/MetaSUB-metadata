"""Constants used while generating metadata tables."""

from os.path import dirname, join
from .parsing import parse_csv


METADATA_DIR = join(dirname(dirname(__file__)), 'spreadsheets')

CITY_NAMES_FILE = join(METADATA_DIR, 'city_names.csv')
CITY_NAMES = [
    tkns[0].lower()
    for tkns in parse_csv(CITY_NAMES_FILE, assert_len=2, skip=1)
]

HA_IDS_TO_PLATE_POS_FILE = join(METADATA_DIR, 'HA Submissions-Grid view.csv')
PLATE_POS_TO_BC_FILE = join(METADATA_DIR, 'CSD2017_DAVID.csv')
CLEAN_KOBO_METADATA_CSD17_FILE = join(METADATA_DIR, 'cleaned_simplified_metadata.csv')
SL_NAME_TO_HA_ID_FILE = join(METADATA_DIR, 'filenames_HCY5HCCXY.tsv')
CONVERT_LONDON_IDS_FILE = join(METADATA_DIR, 'Conversion Tables-Table 1.csv')
LONDON_METADATA_FILE = join(METADATA_DIR, 'Metadata-Table 1.csv')
SAMPLE_NAMES_FILE = join(METADATA_DIR, 'sample_names.txt')

CSD16_CODE = 'CSD16'
CSD17_CODE = 'CSD17'
OLYMPIOME_CODE = 'OLY'
PATHOMAP_WINTER_CODE = 'PATHOMAP_WINTER'

NA_TOKEN = 'n/a'

PLATE_NUM = 'plate_number'
PLATE_POS = 'plate_pos'
BC = 'barcode'
CITY = 'city'
CITY_CODE = 'city_code'
SURFACE_MATERIAL = 'surface_material'
SURFACE = 'surface'
SETTING = 'setting'
ELEVATION = 'elevation'
TRAFFIC_LEVEL = 'traffic'
LAT = 'latitude'
LON = 'longitude'
METASUB_NAME = 'metasub_name'
HA_ID = 'ha_id'
SL_NAME = 'sl_name'
PROJECT = 'project'