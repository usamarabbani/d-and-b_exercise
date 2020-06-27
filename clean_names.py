import re

SPECIAL_CHAR_ON_HEAD_TAIL = {'*', ',', '-', '.', '(', ')', ':', '/', ' '}
DBA = ' DBA | d.b.a | dba. | D. B. A. | d-b-a | /D.B.A./ | D.B.A. '


def clean_names(raw_names):
    result = []
    for raw_name in raw_names:
        name = re.sub('[^a-zA-Z./_ -]', '', raw_name)
        name = name.replace('_', ' ')
        name = re.sub(r"^\W+", "", name)
        name = re.sub(r"\W+$|'.'", "", name)
        name = re.sub('- ', '', name)
        name_list = re.split(DBA, name)

        if name_list[0][-1] in SPECIAL_CHAR_ON_HEAD_TAIL:
            name_list[0] = name_list[0][:-1]
        if len(name_list) == 1:
            result.append((name_list[0], None))
            continue
        result.append((name_list[0], name_list[-1]))

    return result


RAW_NAMES = [
    'SPV Inc., DBA: Super Company',
    'Michael Forsky LLC d.b.a F/B Burgers .',
    '*** Youthful You Aesthetics ***',
    'Aruna Indika (dba. NGXess)',
    'Diot SA, - D. B. A. *Diot-Technologies*',
    'PERFECT PRIVACY LLC, d-b-a Perfection,',
    'PostgreSQL DB Analytics',
    '/JAYE INC/',
    ' ETABLISSEMENTS SCHEPENS /D.B.A./ ETS_SCHEPENS',
    'DUIKERSTRAINING OOSTENDE | D.B.A.: D.T.O. '
]
CLEANED_NAME_PAIRS = [
    ('SPV Inc', 'Super Company'),
    ('Michael Forsky LLC', 'F/B Burgers'),
    ('Youthful You Aesthetics', None),
    ('Aruna Indika', 'NGXess'),
    ('Diot SA', 'Diot-Technologies'),
    ('PERFECT PRIVACY LLC', 'Perfection'),
    ('PostgreSQL DB Analytics', None),
    ('JAYE INC', None),
    ('ETABLISSEMENTS SCHEPENS', 'ETS SCHEPENS'),
    ('DUIKERSTRAINING OOSTENDE', 'D.T.O'),
]
assert clean_names(RAW_NAMES) == CLEANED_NAME_PAIRS
