from deepmerge import always_merger
from langdetect import detect, detect_langs


def try_name(nlist,record, default=None):
    for name in nlist:
        try:
            return record[name]
        except:
            continue
    else:
        return default
#TODO TESTS
def schema_mapping(existing_record, doi):
    data = {}

    #itemPIDs -required
    always_merger.merge(data, {"itemPIDs": [{"scheme": "DOI", "value": doi}]})


    #itemCreators -required
    authors_array = try_name(nlist=['authors', 'author', 'contributor', 'contributors'], record=existing_record)
    if authors_array == None:
        always_merger.merge(data, {'authors': [{"full_name": "Various authors"}]}) #default
    else:
        if(type(authors_array) is list):
            authors_data = []
            for author in authors_array:
                auth_data = {}
                if 'ORCID' in author:
                    always_merger.merge(auth_data, {"identifiers": [{"scheme": "ORCID", "value": author["ORCID"]}]})
                if 'alternative_names' in author and type(author['alternative_names']) is list:
                    always_merger.merge(auth_data, {"alternative_names": author['alternative_names']})
                if 'roles' in author and type(author['roles']) is list:
                    always_merger.merge(auth_data, {"roles": author['roles']})
                if 'type' in author and type(author['type']) is str:
                    always_merger.merge(auth_data, {"type": author['type']})
                #affiliation /affiliations
                full_name = try_name(nlist=['full_name', 'name', 'fullname', 'literal'], record=author)
                if full_name != None:
                    always_merger.merge(auth_data, {"full_name": full_name})
                    authors_data.append(auth_data)
                    continue
                given = try_name(nlist=['given', 'first', 'first_name'], record=author)
                family = try_name(nlist=['family', 'family_name', 'second_name'], record=author)
                if(given == None or family == None):
                    always_merger.merge(auth_data, {"full_name": "unknown"})
                    authors_data.append(auth_data)
                    continue
                else:
                    full_name = given + " " + family
                    always_merger.merge(auth_data, {"full_name": full_name})
                    authors_data.append(auth_data)
                    continue

            always_merger.merge(data, {'itemCreators': authors_data})

    # document_type
    doctype = try_name(nlist=['document_type', 'type'], record=existing_record)
    if doctype == None:
        always_merger.merge(data, {'document_type': "unknown"})  # default
    else:
        always_merger.merge(data, {'document_type': doctype})

    #publication_year -required
    publication_year = try_name(nlist=['publication_year', 'issued'], record=existing_record)

    if publication_year != None and type(publication_year) is str and len(publication_year['data-part'][0]) == 4:
        always_merger.merge(data, {'publication_year': publication_year})
    elif publication_year != None and type(publication_year) is dict:
        if 'date-parts' in publication_year.keys():
            if len(str(publication_year['date-parts'][0][0])) == 4:
                always_merger.merge(data, {'itemYear': str(publication_year['date-parts'][0][0])})
            else:
                always_merger.merge(data, {'itemYear': "0"})
        else:
            always_merger.merge(data, {'itemYear': "0"})
    else:
        always_merger.merge(data, {'itemYear': "0"})

    # title - required
    title_value = try_name(nlist=['title', 'titles'], record=existing_record)
    if title_value != None:
        if type(title_value) is list:
            title_value= title_value[0]
        title =  title_value
        always_merger.merge(data, {'title': title})
    else:
        always_merger.merge(data, {'title': "unknown"}) #default

    # urls
    urls = try_name(nlist=['url', 'urls', 'URL', 'URLs'], record=existing_record)
    if urls != None and type(urls) is str:
        always_merger.merge(data, {'itemURL': [{"value": urls}]})


    return data
