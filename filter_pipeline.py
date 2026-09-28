import osmium


def makeFilteredDataset(source_path, output_path):
    """Filter input dataset to only contain tags of interest that are not private, and their referenced nodes and ways.

    Keyword arguments:
    source_path -- path to the .osm.pbf file that should be filtered.
    output_path -- path to the filtered .osm.pbf file that will be generated.
    """
    fp = osmium.FileProcessor(source_path).with_filter(osmium.filter.KeyFilter('natural', 'addr:street', 'waterway', 'type', 'place', 'landuse', 'amenity', 'man_made', 'leisure', 'historic', 'tourism', 'public_transport', 'sport', 'shop', 'heritage', 'highway', 'barrier'))

    with osmium.BackReferenceWriter(output_path, ref_src=source_path, overwrite=True) as writer:
        for obj in fp:
            if 'access' not in obj.tags or not obj.tags['access'] == 'private':
                if 'highway' not in obj.tags or obj.tags['highway'] not in {'street_lamp', 'crossing', 'turning_circle', 'passing_place', 'give_way', 'traffic signals', 'speed_camera', 'toll_gantry', 'service', 'corridor'}:
                    writer.add(obj)


def makePOIDataset(source_path, output_path):
    """Filter input dataset to only contain points that should be generated as a destination, and their referenced nodes and ways.

    Keyword arguments:
    source_path -- path to the .osm.pbf file that should be filtered.
    output_path -- path to the filtered .osm.pbf file that will be generated.
    """
    fp = osmium.FileProcessor(source_path).with_filter(osmium.filter.KeyFilter('natural', 'highway', 'waterway', 'type', 'place', 'landuse', 'amenity', 'leisure', 'historic', 'tourism', 'sport', 'shop', 'heritage', 'highway'))

    with osmium.BackReferenceWriter(output_path, ref_src=source_path, overwrite=True) as writer:
        for obj in fp:
            write = True
            if 'natural' in obj.tags and obj.tags['natural'] not in {'peak', 'hill', 'water', 'beach'}:
                write = False
            elif 'highway' in obj.tags and obj.tags['highway'] not in {'path', 'footway'}:
                write = False
            elif 'waterway' in obj.tags and obj.tags['waterway'] not in {'river', 'waterfall'}:   
                write = False
            elif 'landuse' in obj.tags and obj.tags['landuse'] not in {'recreation_ground', 'winter_sports'}:   
                write = False
            if write:
                writer.add(obj)
