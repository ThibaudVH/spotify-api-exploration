import xml.etree.ElementTree as ET
import pandas as pd
from progressbar import printProgressBar
import datetime


def df_creation(music_lib,cols):
    """
    Parse the XML music library and return the desired data into a pandas dataframe.
    @params:
    music_lib   - Required  : Music library to parse (list of XML objects)
    cols        - Required  : Fields of interest.
    """
    
    dict1={}
    list_values=[]
    # Loop into the XML object to find track information
    for i in range(len(music_lib)):
        values=[]
        for j in range(len(music_lib[i])):
            if music_lib[i][j].tag=='key':
                if music_lib[i][j].text in cols:
                    dict1[music_lib[i][j].text]=music_lib[i][j+1].text
        
        # making sure cols are in the same order
        for c in cols:
            try:
                values.append(dict1[c])
            except:
                values.append('')
        # appending every line one by one is taking too much time as the dataframe gets bigger
        list_values.append(values)
        printProgressBar(iteration = i, total = len(music_lib), printEnd='')
    df = df=pd.DataFrame(data = list_values,columns=cols)
    return df


def get_existing_cols(music_lib):
    """
    Extract the available columns from the music library library
    @params:
    music_lib       - Required  : Music library to parse (list of XML objects)
    """

    cols=[]
    for i in range(len(music_lib)):
        for j in range(len(music_lib[i])):
            if music_lib[i][j].tag=='key':
                cols.append(music_lib[i][j].text)
    return set(cols)


# TODO: more robust way to get the sub_node would be to identify the Key value at j and return the j+1 object
def extract_sub_node(main_dict, keytag):
    """
    Parses the first level of the XML main_dict and returns the sub_node with that XML item tag.
    @params:
    main_dict   - Required  : main node of the iTunes XML Library
    keytag      - Required  : the item tag to look for
    """

    sub_node = None
    for item in list(main_dict[0]):    
        if item.tag==keytag:
            sub_node=item
            break
    return sub_node


def split_music_kind(tracklist):
    """
    Split the Music Library based on the music Kind, and then put extracted songs in list of XML elements.
    Returns a tuple of podacst,  purchased, apples_music and generic_music
    """
    podcast=[] #All podcast elements
    purchased=[] # All purchased music
    apple_music=[] # Music added to lirary through subscription
    generic_music=[]
    for item in tracklist:
        x=list(item)
        for i in range(len(x)):
            if x[i].text=="Genre" and x[i+1].text=="Podcast": #
                #podcast.append(item.getchildren())
                podcast.append(list(item))
                break
            elif x[i].text=="Kind" and x[i+1].text=="Purchased AAC audio file":
                #purchased.append(item.getchildren())
                purchased.append(list(item)) 
                break
            elif x[i].text=="Kind" and x[i+1].text=="Apple Music AAC audio file":
                #apple_music.append(item.getchildren())
                apple_music.append(list(item))
                break
            else :
                #generic_music.append(item.getchildren())
                generic_music.append(list(item))
                break
    return podcast, purchased, apple_music, generic_music


# First import the iTunes Music Library xml and begin to parse it.
# This XML deviates a lot from more classic XML implementation and some of its parsing may seem hacky/unconventional.
# Expects library file in data folder

lib = '../data/iTunes Music Library.xml'
# lib = 'data/iTunes Music Library.xml'

tree = ET.parse(lib)
root = tree.getroot()
main_dict=root.findall('dict')

# Exxtract tracks from the library, which are located into a dict 
tracks_dict = extract_sub_node(main_dict, 'dict')
tracklist=list(tracks_dict.findall('dict'))

# Then split them into relevant kinds
podcast, purchased, apple_music, generic_music = split_music_kind(tracklist)
print ('Number of tracks under Podcast:',str(len(podcast)))
print ('Number of tracks Purchased: ',str(len(purchased)))
print ('Number of Music added thought Apple Music subscription: ',str(len(apple_music)))
print ('Number of Tracks: ',str(len(generic_music)))

#  Extract the existing column names from the different kinds
podcast_cols=get_existing_cols(podcast)
purchased_cols=get_existing_cols(purchased)
apple_music_cols=get_existing_cols(apple_music)
generic_music_cols = get_existing_cols(generic_music)
# Force columns to get more lightweight extract
generic_music_cols = ['Persistent ID', 'Track ID', 'Artist', 'Name', 'Album', 'Track Count','Track Number','Track Type','Total Time','Play Count', 'Year', 'Genre']

# import tracks metadata in pandas dataframes and dump them into csv.
print('Import of AppleMusic')
df_apple_music = df_creation(apple_music,apple_music_cols)
df_apple_music.to_csv('../data/itunes_library_apple_music.csv', index=False)

print('Import of Podcast')
df_podcast = df_creation(podcast,podcast_cols)
df_podcast.to_csv('../data/itunes_library_podcast.csv', index=False)

print('Import of Purchased Music')
df_purchased = df_creation(purchased,purchased_cols)
df_purchased.to_csv('../data/itunes_library_purchased.csv', index=False)

print('Import of General Music')
df_generic = df_creation(generic_music,generic_music_cols)
df_generic.to_csv('../data/itunes_library_generic.csv', index=False)

# #  Get Tracklists
# for item in list(main_dict[0]):
#     # print(item.tag, item.attrib, item.text)    
#     if item.tag=="array":
#         playlists_dict=item
#         tracklist=list(playlists_dict.findall('dict'))
#         # x=list(tracklist[11])
#         # for i in range(len(x)):
#         #     print(x[i].text)


# %%
