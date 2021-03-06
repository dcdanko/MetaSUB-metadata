from .parsing import parse_csv
from .constants import *
from .utils import (
    getOrNone,
    clean_ha_id,
    mdata_dir,
)
from .ha_filename_tables import HA_FILENAME_TABLES
from .simple_tables import SIMPLE_TABLES
from sys import stderr
import pandas as pd


class CityMetadataMapper:

    def __init__(self):
        self.tbl = pd.read_csv(mdata_dir('city_metadata.csv'), index_col=0)

    def map(self, sample):
        if not sample[CITY]:
            return
        if sample[CITY] == 'são_paulo':
            sample[CITY] = 'sao_paulo'
        elif sample[CITY].lower() == 'sweden':
            sample[CITY] = 'stockholm'
        elif sample[CITY] == 'john_o\'_groats':
            sample[CITY] = 'john_o_groats'
        elif sample[CITY] == 'ofa':
            sample[CITY] = 'offa'
        elif sample[CITY] == 'bogotá':
            sample[CITY] = 'bogota'
        city_name = sample[CITY].lower()
        if city_name == 'antarctica':
            sample[CITY] = 'honolulu'
            city_name = 'honolulu'
        if city_name == 'SCL':
            sample[CITY] = 'santiago'
            city_name = 'santiago'
        if city_name not in self.tbl.index:
            if city_name in ['other', 'pos_control', 'neg_control', 'other_control', 'control', 'na', 'ctrl']:
                return
            if sample[CONTROL_STATUS]:
                return
            assert False, f'{city_name} not found in cities table.'

        sample[CITY_LAT] = self.tbl['latitude'][city_name]
        sample[CITY_LON] = self.tbl['longitude'][city_name]
        sample[CITY_COASTAL] = self.tbl['coastal'][city_name]
        sample[CITY_POP] = self.tbl['total_population'][city_name]
        sample[CITY_DENSITY] = self.tbl['population_density_km2'][city_name]
        sample[CITY_AREA] = self.tbl['land_area_km2'][city_name]
        sample[CITY_TEMP] = self.tbl['ave_june_temp_celsius'][city_name]
        sample[CITY_ELEV] = self.tbl['elevation_meters'][city_name]
        sample[CITY_CONTINENT] = self.tbl['continent'][city_name]
        sample[CITY_KOPPEN_CLIMATE] = self.tbl['koppen_climate'][city_name]


class CoreProjMapper:

    def map(self, sample):
        if not sample[PROJECT]:
            return
        proj = sample[PROJECT]
        if proj in [CSD16_CODE, CSD17_CODE, PILOT_CODE]:
            if sample[CITY] != 'antarctica':
                sample[CORE_PROJECT] = 'core'
        else:
            sample[CORE_PROJECT] = 'not_core'


class OtherProjToBarcelona:

    def map(self, sample):
        if not sample[OTHER_PROJ_UID]:
            return
        if 'sossowski' in sample[OTHER_PROJ_UID].lower():
            sample[CITY] = 'barcelona'
            if 'ms0' in  sample[OTHER_PROJ_UID].lower():
                sample[PROJECT] = PILOT_CODE


class ControlAsCity:

    def map(self, sample):
        if sample[CITY]:
            return
        if sample[CONTROL_STATUS]:
            sample.setitem(CITY, 'other_control', setter='Mapper::ControlAsCity')
        elif sample[METASUB_NAME] and 'control' in sample[METASUB_NAME].lower():
            sample.setitem(CITY, 'other_control', setter='Mapper::ControlAsCity')
        elif sample[HA_ID] and sample[HA_ID].upper() == '4959-DB_PC':
            sample.setitem(CITY, 'other_control', setter='Mapper::ControlAsCity')
            # sample[CONTROL_STATUS] = POSITIVE_CONTROL


class MapUUID:

    def map(self, sample):
        if sample[HAUID] and not sample[OTHER_PROJ_UID]:
            sample[GENERIC_UID] = sample[HAUID]
        elif sample[OTHER_PROJ_UID] and not sample[HAUID]:
            sample[GENERIC_UID] = sample[OTHER_PROJ_UID]


class MSubToCity:
    """Guess the city or city code from the MetaSUB name."""

    def map(self, sample):
        if not sample[METASUB_NAME]:
            return
        codes = {
            'oly': 'rio_de_janeiro',
            'porto': 'porto',
        }
        if sample[CITY_CODE] and sample[CITY]:
            return
        for code, city_name in codes.items():
            if code in str(sample[METASUB_NAME]).lower():
                sample.setitem(CITY, city_name, setter='Mapper::MSubToCity')
                return

        if 'csd' in sample[METASUB_NAME].lower():
            if 'csd_denver' in str(sample[METASUB_NAME]).lower():
                sample.setitem(CITY_CODE, 'DEN', setter='Mapper::MSubToCity')
                sample.setitem(PROJECT, CSD16_CODE, setter='Mapper::MSubToCity')
                return
            tkns = sample[METASUB_NAME].split('-')
            if len(tkns) == 3:
                sample.setitem(CITY_CODE, tkns[1], setter='Mapper::MSubToCity')
            return
        tkns = sample[METASUB_NAME].split('_')
        if 'INBOUNDCONTROL' not in sample[METASUB_NAME] and len(tkns) == 3:
            sample.setitem(CITY, 'berlin', setter='Mapper::MSubToCity')


class MetaSUBNameToProject:

    def map(self, sample):
        code_map = {
            'CSD-16': CSD16_CODE,
            'CSD16': CSD16_CODE,
            'CSD17': CSD17_CODE,
            'CSD-17': CSD17_CODE,
            'WINTER_NYC': PATHOMAP_WINTER_CODE,
        }
        if sample[METASUB_NAME]:
            for key, val in code_map.items():
                if key.lower() in sample[METASUB_NAME].lower():
                    sample.setitem(PROJECT, val, setter='Mapper::MetaSUBNameToProject')
                    break


class CityCodeToCity:

    def map(self, sample):
        code_map = {
            'FAI': 'fairbanks',
            'NYC': 'new_york_city',
            'OFA': 'ofa',
            'AKL': 'auckland',
            'HAM': 'hamilton',
            'SAC': 'sacramento',
            'SCL': 'santiago',
            'BOG': 'bogota',
            'ILR': 'ilorin',
            'TOK': 'tokyo',
            'LON': 'london',
            'HKG': 'hong_kong',
            'OSL': 'oslo',
            'DEN': 'denver',
            'STO': 'stockholm',
            'RIO': 'rio_de_janeiro',
            'POR': 'porto',
            'BER': 'berlin',
            'SAP': 'sao_paulo',
            'KL':  'kuala_lumpur',
            'TPE': 'taipei',
            'SIN': 'singapore',
            'VIE': 'vienna',
            'DOH': 'doha',
            'MRS': 'marseille',
            'MSP': 'minneapolis',
            'BNE': 'brisbane',
            'SEL': 'seoul',
            'LSB': 'lisbon',
            'MXC': 'mexico_city',
            'MVD': 'montevideo',
            'SHG': 'shanghai',
            'BCN': 'barcelona',
            'LIS': 'lisbon',
            'BOS': 'boston',
            'MEL': 'melbourne',
            'NAP': 'naples',
            'PAR': 'paris',
            'PXO': 'porto',
            'RAO': 'ribeirao_preto',
            'SYD': 'sydney',
        }
        city_map = {v: k for k, v in code_map.items()}
        if sample[CITY] and sample[CITY] == 'são_paulo':
            sample[CITY] = 'sao_paulo'
        if sample[CITY] and sample[CITY] == 'sweden':
            sample[CITY] = 'stockholm'
        if sample[CITY_CODE] and sample[CITY_CODE].upper() == 'SWE':
            sample[CITY_CODE] = 'SWE'        
        if sample[CITY_CODE] and sample[CITY_CODE].upper() == 'BAR':
            sample[CITY_CODE] = 'BCN'
        if sample[CITY_CODE]:  #and not sample[CITY]:
            try:
                sample.setitem(CITY, code_map[sample[CITY_CODE].strip().upper()], setter='Mapper::CityCodeToCity::A')
            except KeyError:
                if sample[CITY_CODE].lower() != 'csd':
                    pass  #raise
        elif sample[CITY] and not sample[CITY_CODE]:
            try:
                code = city_map[sample[CITY]]
                if code == 'LSB':
                    code = 'LIS'
                if code == 'BAR':
                    code = 'BCN'
                sample.setitem(CITY_CODE, code, setter=f'Mapper::CityCodeToCity::B::{code}')
            except KeyError:
                pass


class Handle5106HANames:
    """HA IDs matching 5106-CEM come from either London gCSD17
    or NYC winter   ap.
    """

    def __init__(self):
        self.conv_tbl = {
            tkns[5]: (tkns[0], (tkns[1], tkns[2]))
            for tkns in parse_csv(
                mdata_dir('Conversion Tables-Table 1.csv')
            )
        }
        self.pathomap_winter_coversion = [
            tkns[0] for tkns in parse_csv(mdata_dir('winter_pathomap_conversion.csv'))
        ]

        self.mdata_tbl = {
            tkns[0]: [
                (CITY, 'london'),
                (SETTING, tkns[31]),
                (PROJECT, CSD17_CODE),
                (LAT, tkns[26]),
                (LON, tkns[27]),
                (SURFACE_MATERIAL, tkns[37]),
                (SURFACE, tkns[33]),
                (ELEVATION, tkns[32]),
            ]
            for tkns in parse_csv(mdata_dir('Metadata-Table 1.csv'))
        }

    def map(self, sample):
        if not sample[HA_ID]:
            return
        if sample[HA_ID].lower() not in self.conv_tbl:
            if '5106-cem' in sample[HA_ID].lower():
                sample.setitem(CITY, 'new_york_city', setter='Mapper::Handle5106HANames')
                sample.setitem(PROJECT, PATHOMAP_WINTER_CODE, setter='Mapper::Handle5106HANames')
                snum = int(sample[HA_ID].split('-')[2])
                code = self.pathomap_winter_coversion[snum - 1]
                sample.setitem(METASUB_NAME, code, setter='Mapper::Handle5106HANames')
                if code == 'pos':
                    sample.setitem(CONTROL_STATUS, POSITIVE_CONTROL, setter='Mapper::Handle5106HANames')
                elif code == 'neg':
                    sample.setitem(CONTROL_STATUS, 'negative_control', setter='Mapper::Handle5106HANames')
            return

        internal_name, pos = self.conv_tbl[sample[HA_ID].lower()]
        if '_pos' in internal_name.lower():
            sample.setitem(CONTROL_STATUS, POSITIVE_CONTROL, setter='Mapper::Handle5106HANames')
        elif '_neg' in internal_name.lower():
            sample.setitem(CONTROL_STATUS, NEGATIVE_CONTROL, setter='Mapper::Handle5106HANames')

        sample[PLATE_NUM] = pos[0]
        sample[PLATE_POS] = pos[1]
        for k, v in self.mdata_tbl[internal_name]:
            sample.setitem(k, v, setter='Mapper::Handle5106HANames')


class OtherProjUidToMetaSubName:

    def map(self, sample):
        if not sample[OTHER_PROJ_UID]:
            return
        uid = sample[OTHER_PROJ_UID].lower()
        if 'csd16' in uid.lower():
            msub = 'csd16' + uid.split('csd16')[1].split('_')[0]
            msub = '-'.join(msub.split('-')[:3])
            sample.setitem(METASUB_NAME, msub, setter='Mapper::OtherProjUidToMetaSubName')


class OtherProjUidToCity:

    def map(self, sample):
        if not sample[OTHER_PROJ_UID]:
            return
        uid = sample[OTHER_PROJ_UID].lower()
        if 'pilot' not in uid:
            return
        pilot_cities = [
            ('hong_kong', 'HKG'),
            ('lisbon', 'LIS'),
            ('mexico_city', 'MXC'),
            ('montevideo', 'MVD'),
            ('oslo', 'OSL'),
            ('sacramento', 'SAC'),
            ('seoul', 'SEL'),
            ('shanghai', 'SHG')
        ]
        for city_name, city_code in pilot_cities:
            city_name_viz = ''.join(city_name.split('_'))
            if city_name_viz in uid:
                sample[CITY] = city_name
                sample[CITY_CODE] = city_code
                break

class PosToBC:
    '''Return a table mapping position to a barcode.

    This function returns a map from tuples of the form
    (plate-name, plate-position) to barcodes.
    '''
    def __init__(self):
        self.pos_to_bc = {
            (tkns[2], tkns[3]): tkns[4]
            for tkns in parse_csv(mdata_dir('CSD2017_DAVID.csv'))
        }
        assert len(self.pos_to_bc) > 0

    def map(self, sample):
        bc = getOrNone(
            self.pos_to_bc,
            (sample[PLATE_NUM], sample[PLATE_POS])
        )
        if bc:
            sample.setitem(BC, bc, setter='CSD2017_DAVID.csv')


class GuessProjFromMSUBName:
    """Use the MetaSUB name to guess the project."""

    def map(self, sample):
        if not sample[METASUB_NAME]:
            return
        codes = {
            'oly': OLYMPIOME_CODE,
            'csd16': CSD16_CODE,
            'porto': CSD16_CODE,
        }
        for key, code in codes.items():
            if code in sample[METASUB_NAME].lower():
                sample.setitem(PROJECT, code, setter='Mapper::GuessProjFromMSUBName')

        if len(sample[METASUB_NAME].split('_')) == 3:
            sample.setitem(PROJECT, CSD16_CODE, setter='Mapper::GuessProjFromMSUBName')
            return


class GuessProj:
    """Use the MetaSUB name to guess the project."""

    def map(self, sample):
        if sample[PROJECT]:
            return  # use this as a last resort
        if sample[OTHER_PROJ_UID] and 'pilot_' in sample[OTHER_PROJ_UID]:
            sample.setitem(PROJECT, PILOT_CODE, setter='Mapper::GuessProj_A')
            return
        if sample[METASUB_NAME] and 'porto_' in sample[METASUB_NAME].lower():
            sample.setitem(PROJECT, PILOT_CODE, setter='Mapper::GuessProj_B')
            return
        if sample[METASUB_NAME] and 'csd_denver' in sample[METASUB_NAME].lower():
            sample.setitem(PROJECT, CSD16_CODE, setter='Mapper::GuessProj_C')
            return
        if sample[HA_ID] and '5080-cem' in sample[HA_ID]:
            ha_num = int(sample[HA_ID].split('-')[2])
            if 1 <= ha_num <= 79:
                sample.setitem(PROJECT, TIGRESS_CODE, setter='Mapper::GuessProj_D')
                return
        if sample[BC]:
            sample.setitem(PROJECT, CSD17_CODE, setter='Mapper::GuessProj_E')
            return

class AirSamplingProj:
    """Use the MetaSUB name to guess the project."""

    def map(self, sample):
        msub = sample[METASUB_NAME]
        if msub and 'csd17' in msub.lower() and '-as' in msub.lower():
            sample.setitem(PROJECT, CSD17_AIR_CODE, setter='Mapper::AirSamplingProj')

class SampleType:

    def __init__(self):
        self.stype_map = {}
        parsed = parse_csv(
            mdata_dir('sample_names_types.tsv'),
            assert_len=2,
            sep='\t'
        )
        for tkns in parsed:
            name = tkns[0].lower()
            stype = tkns[1]
            if name and stype:
                self.stype_map[name] = stype

    def map(self, sample):
        if sample[HA_ID] and sample[HA_ID].lower() in self.stype_map:
            sample.setitem(SAMPLE_TYPE, self.stype_map[sample[HA_ID].lower()], setter='Mapper::SampleType')
        elif sample[METASUB_NAME] and sample[METASUB_NAME].lower() in self.stype_map:
            sample.setitem(SAMPLE_TYPE, self.stype_map[sample[METASUB_NAME].lower()], setter='Mapper::SampleType')
        elif sample[SL_NAME] and  sample[SL_NAME].lower() in self.stype_map:
            sample.setitem(SAMPLE_TYPE, self.stype_map[sample[SL_NAME].lower()], setter='Mapper::SampleType')


class HAUIDSplitter:

    def map(self, sample):
        if not sample[HAUID]:
            return
        try:
            ha_proj, ha_flowcell, sl_name = sample[HAUID].split(',')[0].split('_')
        except:
            return
        sample[HA_PROJ] = ha_proj
        sample[HA_FLOWCELL] = ha_flowcell
        sample[SL_NAME] = sl_name


class HARemap:

    def map(self, sample):
        if sample[HA_ID]:
            sample[HA_ID] = clean_ha_id(sample[HA_ID])


class CleanCityName:

    def map(self, sample):
        if sample[CITY]:
            sample.setitem(CITY, '_'.join(sample[CITY].lower().split()), setter='Mapper::CleanCityName')


class FindControls:
    cntrls = {
        'haib17CEM5106_HCCGHCCXY_SL270259',
        'haib17CEM5106_HCCGHCCXY_SL270260',
        'haib17CEM5106_HCCGHCCXY_SL270261',
        'haib17CEM5106_HCCGHCCXY_SL270315',
        'haib17CEM5106_HCCGHCCXY_SL270317',
        'haib17CEM5106_HCCGHCCXY_SL270318',
        'haib17CEM5106_HCCGHCCXY_SL270320',
        'haib17CEM5106_HCCGHCCXY_SL270322',
        'haib17CEM5106_HCCGHCCXY_SL270323',
        'haib17CEM5106_HCCGHCCXY_SL270329',
        'haib17CEM5106_HCCGHCCXY_SL270331',
        'haib17CEM5106_HCCGHCCXY_SL270346',
        'haib17CEM5106_HCCGHCCXY_SL270347',
        'haib17CEM5106_HCCGHCCXY_SL270348',
        'haib17CEM5106_HCCGHCCXY_SL270385',
        'haib17CEM5106_HCCGHCCXY_SL270396',
        'haib17CEM5106_HCCGHCCXY_SL270469',
        'haib17CEM5106_HCCGHCCXY_SL270470',
        'haib17CEM5106_HCCGHCCXY_SL270482',
        'haib17CEM5106_HCCGHCCXY_SL270510',
        'haib17CEM5106_HCCGHCCXY_SL270511',
        'haib17CEM5106_HCCGHCCXY_SL270512',
        'haib17CEM5106_HCCGHCCXY_SL270523',
        'haib17CEM5106_HCCGHCCXY_SL270535',
        'haib17CEM5106_HCCGHCCXY_SL270558',
        'haib17CEM5106_HCCGHCCXY_SL270562',
        'haib17CEM5106_HCCGHCCXY_SL270567',
        'haib17CEM5106_HCV72CCXY_SL269808',
        'haib17CEM5106_HCV72CCXY_SL269809',
        'haib17CEM5106_HCVMTCCXY_SL269616',
        'haib17CEM5106_HCVMTCCXY_SL269617',
        'haib17CEM5106_HCY5HCCXY_SL270995',
        'haib17CEM5106_HCY5HCCXY_SL270996',
        'haib17CEM5106_HCY5HCCXY_SL271131',
        'haib17CEM5106_HCY5HCCXY_SL271132',
        'haib17CEM5106_HCY5HCCXY_SL271138',
        'haib17DB4959_H3MGVCCXY_SL259929',
        'haib17DB4959_H3MGVCCXY_SL259941',
        'haib17DB4959_H3MGVCCXY_SL259983',
        'haib18CEM5453_HMGW3CCXY_SL342291',
        'haib18CEM5526_HMGTJCCXY_SL342622',
        'haib18CEM5526_HMGTJCCXY_SL342623',
        'sossowski_BarcelonaNov2018_C--29786-TCGACGTC-GAGCCTTA',
        'sossowski_BarcelonaNov2018_CSD16-BCN-244-29786-AGGCAGAA-AAGGAGTA',
        'sossowski_BarcelonaNov2018_CSD16-BCN-248-29786-TCCTGAGC-CTCTCTAT',
        'sossowski_BarcelonaNov2018_CSD16-BCN-251-29786-TCCTGAGC-ACTGCATA',
        'sossowski_BarcelonaNov2018_CSD16-BCN-257-29786-GGACTCCT-CTCTCTAT',
        'sossowski_BarcelonaNov2018_MS036-29786-GGACTCCT-TCTCTCCG',
        'sossowski_BarcelonaNov2018_MS037-29786-TAGGCATG-CTCTCTAT',
        'sossowski_BarcelonaNov2018_MS038-29786-TAGGCATG-TATCCTCT',
        'sossowski_BarcelonaNov2018_MS042-29786-TAGGCATG-CTAAGCCT',
        'sossowski_BarcelonaNov2018_MS043-29786-TAGGCATG-CGTCTAAT',
        'sossowski_BarcelonaNov2018_MS044-29786-TAGGCATG-TCTCTCCG',
        'sossowski_BarcelonaNov2018_MS048-29786-CTCTCTAC-ACTGCATA',
        'sossowski_BarcelonaNov2018_MS049-29786-CTCTCTAC-AAGGAGTA',
        'sossowski_BarcelonaNov2018_MS050-29786-CTCTCTAC-CTAAGCCT',
        'sossowski_BarcelonaNov2018_MS058-29786-CGAGGCTG-CTAAGCCT',
        'sossowski_BarcelonaNov2018_MS059-29786-CGAGGCTG-CGTCTAAT',
        'sossowski_BarcelonaNov2018_MS060-29786-CGAGGCTG-TCTCTCCG'
    }

    def map(self, sample):
        if sample[HAUID] and sample[HAUID] in self.cntrls:
            sample.setitem(CONTROL_STATUS, POSITIVE_CONTROL, setter='MAPPER::FindControls')



MAPPERS = [
    CleanCityName(),
    OtherProjToBarcelona(),
    ControlAsCity(),
    CityMetadataMapper(),
    CoreProjMapper(),
    HARemap(),
    HAUIDSplitter(),
    PosToBC(),
    MSubToCity(),
    CityCodeToCity(),
    Handle5106HANames(),
    GuessProjFromMSUBName(),
    SampleType(),
    FindControls(),
    MetaSUBNameToProject(),
    OtherProjUidToMetaSubName(),
    OtherProjUidToCity(),
    GuessProj(),
    AirSamplingProj(),
    MapUUID(),
] + HA_FILENAME_TABLES + SIMPLE_TABLES
