from enum import Enum

URL = 'https://api.stackexchange.com/2.3/search'

class SectionTypes(Enum):
    QA = ('Software Quality Assurance Section', f'{URL}?&site=sqa&order=desc&sort=activity')
    DOp = ('DevOps Section', f'{URL}?&site=devops&order=desc&sort=activity')
    WA = ('Web Applications Section', f'{URL}?&site=webapps&order=desc&sort=activity')
    DS = ('Data Science Section', f'{URL}?&site=datascience&order=desc&sort=activity')
    DB = ('Database Section', f'{URL}?&site=dba&order=desc&sort=activity')
    NS = ('Не уточнять раздел', f'{URL}?&site=webapps&order=desc&sort=activity')

    @staticmethod
    def list():
        return list(map(lambda c: c.value, SectionTypes))
