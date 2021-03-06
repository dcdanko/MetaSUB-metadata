from .parsing import parse_csv
from .constants import *
from .utils import (
    getOrNone,
    remove_leading_char,
    remove_trailing_char,
    clean_ha_id,
    mdata_dir,
)
from .table_mapper import (
    Table,
    token_mapper,
    token_specific_val_func,
)
from .ha_filename_tables import ha_filename_tables
from sys import stderr


################################################################################


haid_to_barcode_4959DB = Table(
    mdata_dir('4959DB_barcodes.csv'),
    {HA_ID: 0, BC: 1},
    token_mapper(BC, setter='4959DB_barcodes.csv'),
    name_func=lambda x, y: remove_trailing_char('R')(str(x).lower()),
    skip=1,
)


################################################################################

positions = {
    METASUB_NAME: 3,
    SETTING: 7,
    SURFACE_MATERIAL: 8,
    SURFACE: 9,
    LINE: 10,
    LON: 27,
    LAT: 28,
}
barcelona_csd16 = Table(
    mdata_dir('barcelona_csd16_metadata.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='barcelona_csd16_metadata.csv'),
)

################################################################################

positions = {
    HAUID: 0,
    READ_COUNTS: 1,
}
read_counts = Table(
    mdata_dir('read_counts.csv'),
    positions,
    token_mapper(READ_COUNTS, setter='read_counts.csv'),
    name_func=lambda x, y: str(x).lower(),
)


################################################################################


def normalize_plate_num(raw):
    raw = raw.lower()
    if 'zymo plate' in raw:
        plate_num = raw.split()[2]
        while len(plate_num) < 4:
            plate_num = '0' + plate_num
        return f'plate_{plate_num}'
    return raw


ha_name_to_pos = Table(
    mdata_dir('HA Submissions-Grid view.csv'),
    {HA_ID: 0, PLATE_NUM: 8, PLATE_POS: 14},
    token_mapper(PLATE_NUM, PLATE_POS, setter='HA Submissions-Grid view.csv'),
    val_func=token_specific_val_func(**{PLATE_NUM: normalize_plate_num}),
    assert_len=15
)


################################################################################


def airsample_ha_to_msub_mapper(sample, sample_id, vec):
    sample.setitem(METASUB_NAME, vec[METASUB_NAME], setter='airsamples_ha_id_to_msub_name.csv')
    sample.setitem(PROJECT, CSD17_AIR_CODE, setter='airsamples_ha_id_to_msub_name.csv')


airsample_ha_to_msub = Table(
    mdata_dir('airsamples_ha_id_to_msub_name.csv'),
    {HA_ID: 1, METASUB_NAME: 4},
    airsample_ha_to_msub_mapper,
    val_func=token_specific_val_func(**{METASUB_NAME: lambda x: x[1:]}),
    assert_len=5,
    skip=1

)


################################################################################


olympiome_metadata = Table(
    mdata_dir('samples_oly_meta_all_information_e.csv'),
    {
        METASUB_NAME: 0,
        PROJECT: 5,
        STATION: 6,
        LAT: 7,
        LON: 8,
        SURFACE: 9,
    },
    token_mapper(PROJECT, STATION, LAT, LON, SURFACE, setter='samples_oly_meta_all_information_e.csv'),
    name_func=lambda x, y: str(x).upper()
)


################################################################################


bc_to_meta = Table(
    mdata_dir('cleaned_simplified_metadata.csv'),
    {
        CITY: 0,
        BC: 1,
        SURFACE_MATERIAL: 2,
        SURFACE: 3,
        SETTING: 4,
        ELEVATION: 5,
        TRAFFIC_LEVEL: 6,
        LAT: 7,
        LON: 8,
        METASUB_NAME: 9,
        STATION: 10,
        LINE: 11,
    },
    token_mapper(
        CITY, SURFACE_MATERIAL, SURFACE, SETTING,
        ELEVATION, TRAFFIC_LEVEL, LAT, LON, METASUB_NAME,
        STATION, LINE, strict=False, setter='cleaned_simplified_metadata.csv'
    ),
    name_func=token_specific_val_func(**{METASUB_NAME: remove_leading_char('g')}),
    val_func=token_specific_val_func(**{METASUB_NAME: remove_leading_char('g')}),
)


################################################################################


positions = {
    HA_ID: 0,
    CONTROL_STATUS: 1,
    BC: 2,
}
promega_conrol_plate = Table(
    mdata_dir('CSD17_control_plate_promega.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='CSD17_control_plate_promega.csv'),
)


################################################################################


# positions = {
#     HA_ID: 3,
#     METASUB_NAME: 4,
# }
# kiu_samples = Table(
#     mdata_dir('KIU_samples_Shipment_Finallistwith_ID_June2017.csv'),
#     positions,
#     token_mapper(*list(positions.keys())),
# )


################################################################################

# positions = {
#     BC: 2,
#     CITY_CODE: 8,
#     CITY: 9,
#     LAT: 14,
#     LON: 15,
#     SURFACE: 16,
#     SURFACE_MATERIAL: 17,
#     TEMPERATURE: 18
# }
# csd16_benyoung = Table(
#     mdata_dir('CSD16&CSD17_MetaData_Final_V2.csv'),
#     positions,
#     token_mapper(*list(positions.keys())),
# )

positions = {
    METASUB_NAME: 0,
    CITY: 14,
    LAT: 19,
    LON: 20,
    SURFACE: 21,
    SURFACE_MATERIAL: 22,
}
csd16_benyoung = Table(
    mdata_dir('CSD16_benyoung__MASTER_MetaSUB_Metadata_W_YIELDS.csv'),
    positions,
    token_mapper(*list(positions.keys())),
)
# 
# 
# ################################################################################
# 
# 
# positions = {
#     CITY: 0,
#     BC: 1,
#     SETTING: 2,
#     ELEVATION: 3,
#     TRAFFIC_LEVEL: 4,
#     LAT: 5,
#     LON: 6,
#     SURFACE_MATERIAL: 7,
#     SURFACE: 8,
# }
# csd17_benyoung = Table(
#     mdata_dir('CSD17_benyoung__MASTER_MetaSUB_Metadata_W_YIELDS.csv'),
#     positions,
#     token_mapper(*list(positions.keys())),
# )


################################################################################


# positions = {
#     CITY: 0,
#     BC: 1,
#     HAUID: 2,
#     SL_NAME: 8,
#     INDEX_SEQ: 6,
#     STATION: 9,
#     SETTING: 10,
#     ELEVATION: 11,
#     TRAFFIC_LEVEL: 12,
#     LAT: 13,
#     LON: 14,
#     SURFACE_MATERIAL: 15,
#     SURFACE: 16,
# }
# ben_young_master_metadata = Table(
#     mdata_dir('MASTER_MetaSUB_Metadata_W_YIELDS.csv'),
#     positions,
#     token_mapper(*list(positions.keys())),
# )


################################################################################


def csd16_metadata_name_func(name, name_type):
    name = str(name).lower()
    name = '-'.join(name.split('_'))
    if 'csd2016' in name:
        name = 'csd16'.join(name.split('csd2016'))
    return name


csd16_metadata = Table(
    mdata_dir('collated_metadata_csd16.csv'),
    {
        METASUB_NAME: 31,
        CITY: 14,
        SURFACE_MATERIAL: 36,
        SURFACE: 35,
        TRAFFIC_LEVEL: 23,
        LAT: 17,
        LON: 20,
    },
    token_mapper(CITY, SURFACE, SURFACE_MATERIAL, TRAFFIC_LEVEL, LAT, LON, setter='collated_metadata_csd16.csv'),
    name_func=csd16_metadata_name_func,
)


################################################################################


akl_metadata_csd16 = Table(
    mdata_dir('auckland_csd16.csv'),
    {
        METASUB_NAME: 5,
        CITY: 32,
        SURFACE_MATERIAL: 9,
        SETTING: 8,
        LAT: 30,
        LON: 29,
    },
    token_mapper(CITY, SURFACE_MATERIAL, SETTING, LAT, LON, setter='auckland_csd16.csv'),
    name_func=lambda x, y: str(x).upper(),
    skip=1
)


################################################################################


def fairbanks_metadata_csd16_val_func(val, token):
    if token == SURFACE:
        return '_'.join(val.split())
    return val


fairbanks_metadata_csd16 = Table(
    mdata_dir('Fairbanks_corralled_CSD16.csv'),
    {
        METASUB_NAME: 0,
        SURFACE_MATERIAL: 5,
        SURFACE: 4,
    },
    token_mapper(SURFACE, SURFACE_MATERIAL, setter='Fairbanks_corralled_CSD16.csv'),
    name_func=lambda x, y: str(x).upper(),
    val_func=fairbanks_metadata_csd16_val_func,
    skip=1
)


################################################################################


oslo_air_metadata_csd16 = Table(
    mdata_dir('oslo_air_sample_metadata.csv'),
    {
        METASUB_NAME: 0,
        CITY: 1,
        STATION: 3,
        LAT: 4,
        LON: 5,
        LINE: 6,
        ELEVATION: 8,
        SETTING: 9,
        TRAFFIC_LEVEL: 10,
    },
    token_mapper(
        METASUB_NAME,
        CITY,
        STATION,
        LAT,
        LON,
        LINE,
        ELEVATION,
        SETTING,
        TRAFFIC_LEVEL,
        setter='oslo_air_sample_metadata.csv'
    ),
    name_func=token_specific_val_func(**{METASUB_NAME: remove_leading_char('g')}),
    val_func=token_specific_val_func(**{METASUB_NAME: remove_leading_char('g')}),
    skip=1
)


################################################################################


tigress_metadata = Table(
    mdata_dir('metadata.MetaSUB_UK2017.csv'),
    {
        HA_ID: 8,
        CITY: 0,
        LOCATION_TYPE: 1,
        LAT: 2,
        LON: 3,
        SETTING: 4,
        ELEVATION: 5,
        SURFACE: 6,
        SURFACE_MATERIAL: 7,
    },
    token_mapper(
        CITY, LOCATION_TYPE, LAT, LON, SETTING, ELEVATION, SURFACE,
        SURFACE_MATERIAL, setter='metadata.MetaSUB_UK2017.csv'
    ),
    name_func=lambda x, y: '-'.join(str(x).lower().split('_')),
)


################################################################################


tokyo_metadata = Table(
    mdata_dir('Tokyo_MetaSUB_2016_SA_HS_NM_.csv'),
    {
        METASUB_NAME: 0,
        LAT: 8,
        LON: 9,
        SURFACE_MATERIAL: 11,
        TEMPERATURE: 12,
    },
    token_mapper(
        METASUB_NAME, LAT, LON, SURFACE_MATERIAL, TEMPERATURE, setter='Tokyo_MetaSUB_2016_SA_HS_NM_.csv'
    )
)


################################################################################


boston_metadata = Table(
    mdata_dir('Boston_MetaSUB_2016_SA_TH_BGY_TH.csv'),
    {
        METASUB_NAME: 0,
        LINE: 9,
        LAT: 11,
        LON: 12,
        SURFACE_MATERIAL: 14,
        TEMPERATURE: 15,
    },
    token_mapper(
        METASUB_NAME, LINE, LAT, LON, SURFACE_MATERIAL, TEMPERATURE, setter='Boston_MetaSUB_2016_SA_TH_BGY_TH.csv'
    )
)


################################################################################


zurich_metadata = Table(
    mdata_dir('Zurich_MetaSUB_2016_SA.csv'),
    {
        METASUB_NAME: 0,
        LINE: 7,
        LAT: 10,
        LON: 11,
        SURFACE_MATERIAL: 13,
        TEMPERATURE: 14,
    },
    token_mapper(
        METASUB_NAME, LINE, LAT, LON, SURFACE_MATERIAL, TEMPERATURE, setter='Zurich_MetaSUB_2016_SA.csv'
    )
)


################################################################################


#csd16_metadata_bgy = Table(
#    mdata_dir('MASTER_MetaSUB_Metadata_BGY_csd16.csv'),
#    {
#        METASUB_NAME: 0,
#        LINE: 8,
#        LAT: 10,
#        LON: 11,
#        SURFACE: 12,
#        SURFACE_MATERIAL: 13,
#        TEMPERATURE: 14,
#    },
#    token_mapper(
#        METASUB_NAME, LINE, LAT, LON, SURFACE_MATERIAL, TEMPERATURE
#    )
#)


################################################################################


def handle_msub_name(msub_name, position):
    msub_name = str(msub_name)
    if position == HA_ID:
        return remove_trailing_char('R')(msub_name.lower())
    if position != METASUB_NAME:
        return str(msub_name).upper()
    msub_name = str(msub_name).upper()
    msub_name = '-'.join(msub_name.split('_'))
    if 'CSD-DENVER' in msub_name:
        return 'CSD16-DEN' + msub_name.split('CSD-DENVER')[-1]
    if 'CSD' not in msub_name:
        return ''
    return msub_name


positions = {
    HA_ID: 1,
    METASUB_NAME: 2,
    MAYBE_METASUB_NAME: 2,
    CITY: 3,
}
haid_to_csdid = Table(
    mdata_dir('collated_sample_sheets_ea_v3.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='collated_sample_sheets_ea_v3.csv'),
    name_func=handle_msub_name,
    val_func=handle_msub_name,
)


def map_func(sample, sample_id, vec):
    if sample[PROJECT]:
        return
    sample.setitem(PROJECT, vec[PROJECT], setter='collated_sample_sheets_ea_v3.csv')

positions = {
    HA_ID: 1,
    PROJECT: 4,
}
haid_to_csdid_2 = Table(
    mdata_dir('collated_sample_sheets_ea_v3.csv'),
    positions,
    map_func,
    name_func=handle_msub_name,
    val_func=handle_msub_name,
)


################################################################################


positions = {
    METASUB_NAME: 0,
    SURFACE: 2,
    STATION: 1,
}
pathomap_winter = Table(
    mdata_dir('PathoMAP_Winter2014_metadata.csv'),
    positions,
    token_mapper(*list(positions.keys()), last_resort=False, setter='PathoMAP_Winter2014_metadata.csv'),
)


################################################################################

pilot_sample_names = {}
with open(SAMPLE_NAMES_FILE) as snf:
    for line in snf:
        sample_name = line.strip()
        if 'pilot_' not in sample_name:
            continue
        original = sample_name.split('_')[2]
        pilot_sample_names[original] = sample_name


def pilot_name_func(name, name_type):
    if name_type == METASUB_NAME and 'CSD16-HON' in name.upper():
        return 'HKG'.join(name.upper().split('HON')).lower()
    if name_type != OTHER_PROJ_UID:
        return name
    if 'pilot_' in name:
        return name
    name = name.upper()
    val = pilot_sample_names.get(name, name)
    return val


positions = {
    OTHER_PROJ_UID: 0,
    METASUB_NAME: 1,
    LINE: 12,
    LAT: 14,
    LON: 15,
    SURFACE: 16,
    SURFACE_MATERIAL: 17,
}
pilot_metadata = Table(
    mdata_dir('pilot_study_metadata_010219.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='pilot_study_metadata_010219.csv'),
    val_func=pilot_name_func,
    name_func=pilot_name_func,
)


################################################################################


positions = {
    LAT: 0,
    LON: 1,
    METASUB_NAME: 5,
    SETTING: 8,
    SURFACE_MATERIAL: 9
}
porto_metadata = Table(
    mdata_dir('porto_metasub.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='porto_metasub.csv')
)


################################################################################

positions = {
    BC: 3,
    HA_ID: 4,
    HAUID: 5,
    QC_DNA_CONCENTRATION: 16,
    POST_PCR_QUBIT: 17,
    INDEX_SEQ: 18,
    CITY: 31,
    LOCATION_TYPE: 32,
    LINE: 33,
    LAT: 36,
    LON: 37,
    SURFACE: 38,
    SURFACE_MATERIAL: 39,
    TEMPERATURE: 40,
    PROJECT: 44,
    METASUB_NAME: 2,
}
yield_metadata = Table(
    mdata_dir('MetaSub_Complete_CSD16_17_with_HudsonAlpha_ID_v1_2_counts.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='MetaSub_Complete_CSD16_17_with_HudsonAlpha_ID_v1_2_counts.csv'),
    name_func=lambda x, y: str(x).lower(),
)


################################################################################


positions = {
    HAUID: 0,
    INDEX_SEQ: 2,
    BC: 8,
    METASUB_NAME: 6,
    HA_ID: 3,
}
dec13_metadata = Table(
    mdata_dir('Dec13_batch_with_uuids.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='Dec13_batch_with_uuids.csv'),
    name_func=lambda x, y: str(x).lower(),
    debug=False
)


positions = {
    BC: 0,
    HAUID: 1,
    CITY: 2,
    LINE: 3,
    LAT: 4,
    LON: 5,
    SURFACE: 6,
    SURFACE_MATERIAL: 7,
}
dec13_metadata_inbounds = Table(
    mdata_dir('Dec13_metadata_for_inbounds.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='Dec13_metadata_for_inbounds.csv'),
    name_func=lambda x, y: str(x).lower(),
    debug=False
)


################################################################################


positions = {
    BC: 0,
    HA_ID: 4,
    PROJECT: 17,
    CITY_CODE: 26,
    CITY: 27,
    LAT: 32,
    LON: 33,
    # ELEVATION: 34,
    LOCATION_TYPE: 36,
    SURFACE: 41,
    SURFACE_MATERIAL: 45,
    # TRAFFIC_LEVEL: 47,
    TEMPERATURE: 52,
    POST_PCR_QUBIT: 113,
    QC_DNA_CONCENTRATION: 102,
    HAUID: 122,
}
master_allsamples_v2 = Table(
    mdata_dir('MetaSUB_master_allsamples_v2.csv'),
    positions,
    token_mapper(*list(positions.keys()), setter='MetaSUB_master_allsamples_v2.csv'),
    name_func=lambda x, y: str(x).lower(),
    debug=False
)


################################################################################


SIMPLE_TABLES = [
    barcelona_csd16,
    haid_to_barcode_4959DB,
    airsample_ha_to_msub,
    # bc_to_meta,
    master_allsamples_v2,
    #csd16_metadata,
    csd16_benyoung,
    # dec13_metadata,
    # dec13_metadata_inbounds,
    #csd17_benyoung,
    akl_metadata_csd16,
    fairbanks_metadata_csd16,
    # oslo_air_metadata_csd16,
    promega_conrol_plate,
    olympiome_metadata,
    # kiu_samples,
    # tigress_metadata,
    boston_metadata,
    tokyo_metadata,
    zurich_metadata,
    #csd16_metadata_bgy,
    #ben_young_master_metadata,
    #haid_to_csdid,
    #haid_to_csdid_2,
    pathomap_winter,
    read_counts,
    porto_metadata,
    pilot_metadata,
    yield_metadata,
]
