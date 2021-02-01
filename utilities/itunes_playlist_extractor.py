#%%
import xml.etree.ElementTree as ET
import pandas as pd
from progressbar import printProgressBar
import datetime

#%%
def music_df_creation(music_lib,cols):
    """
    Parse the XML music library and return the desired data into a pandas dataframe.
    @params:
    music_lib   - Required  : Music library to parse (list of XML objects)
    cols        - Required  : Fields of interest.
    """

    all_track_values=[] # master list to conatain all info for all tracks
    # Loop into the XML object to find track information
    for i in range(len(music_lib)):
        track_specific_dict={} #track specific collector
        track_specific_values=[] #track specific collector
        for j in range(len(music_lib[i])):
            if music_lib[i][j].tag=='key':
                if music_lib[i][j].text in cols:
                    track_specific_dict[music_lib[i][j].text]=music_lib[i][j+1].text #I know this is super retarded, but it's the way Apple implemented it.
        
        # making sure cols are in the same order
        for c in cols:
            try:
                track_specific_values.append(track_specific_dict[c])
            except:
                track_specific_values.append('')
        all_track_values.append(track_specific_values)
        printProgressBar(iteration = i, total = len(music_lib), printEnd='')

    # appending every line one by one is taking too much time as the dataframe gets bigger, hence we dump everything at once at the end of the parsing
    df=pd.DataFrame(data = all_track_values,columns=cols)
    return df

def playlist_df_creation(playlist_lib,cols):
    """
    Parse the XML playlist library and return the desired data into a tuple of pandas dataframe:
    a main one containing the playlists directory and a dictionary of dataframes, containing foreach playlist the track ids in that playlist.
    @params:
    playlist_lib    - Required  : Playlist library to parse (list of XML objects)
    cols            - Required  : Fields of interest, must at least contain 'Playlist ID' 
    """

    # Loop into the XML object to find playlist information
    all_plist_master_info =[]
    all_plist_tracks_df={} # will contain one dataframe (value) for each playlist (key)
    for i in range(len(playlist_lib)):
        master = False
        plist_gen_info_dict={} # playlist gen info container
        plist_gen_info_values=[] # playlist gen info container
        tracks = [] 
        track_ids = [] # get the tracks IDs contained in that plist. 
        for j in range(len(playlist_lib[i])):
            if playlist_lib[i][j].tag=='key': #these contains the general information
                if (playlist_lib[i][j].text == 'Master') & (playlist_lib[i][j+1].tag=='true'):
                    master = True
                if playlist_lib[i][j].text in cols: 
                    plist_gen_info_dict[playlist_lib[i][j].text]=playlist_lib[i][j+1].text
            if playlist_lib[i][j].tag=='array': #tracks composing that plist are contained in this array
                tracks=list(playlist_lib[i][j].findall('dict'))
        if master:
            continue

        # Extract tracks composing that plist
        for j in range(len(tracks)):
            if tracks[j].text == 'Track ID':
                track_ids.append(tracks[j+1].text)
        
        # Extract plist gen info into a general dataframe, making sure cols are in the same order        
        for c in cols:
            try:
                plist_gen_info_values.append(plist_gen_info_dict[c])
            except:
                plist_gen_info_values.append('')
        plist_gen_info_values.append(len(track_ids))
        all_plist_master_info.append(plist_gen_info_values)
        
        plist_tracks_df = pd.DataFrame(data = track_ids, columns=['Track ID'])
        all_plist_tracks_df[plist_gen_info_dict['Playlist ID']] = plist_tracks_df
        
        printProgressBar(iteration = i, total = len(playlist_lib), printEnd='')

    # appending every line one by one is taking too much time as the dataframe gets bigger
    cols.append('Track Count')
    plist_maser_df=pd.DataFrame(data = all_plist_master_info,columns=cols)
    return plist_maser_df, all_plist_tracks_df

def join_plist_tracks(plist_tracks_df):
    """
    Will join that playlist dataframes containing Track IDs with the information contained in the main library dataframe
    """
    pass

def get_existing_cols(lib):
    """
    Extract the available columns from the music library library
    @params:
    lib       - Required  : Library to parse (list of XML objects)
    """

    cols=[]
    for i in range(len(lib)):
        for j in range(len(lib[i])):
            if lib[i][j].tag=='key':
                cols.append(lib[i][j].text)
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
    if not sub_node:
        raise Exception(f'Not able to find {keytag} in iTunes Library file')
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

#%%
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
df_apple_music = music_df_creation(apple_music,apple_music_cols)
df_apple_music.to_csv('../data/itunes_library_apple_music.csv', index=False)

print('Import of Podcast')
df_podcast = music_df_creation(podcast,podcast_cols)
df_podcast.to_csv('../data/itunes_library_podcast.csv', index=False)

print('Import of Purchased Music')
df_purchased = music_df_creation(purchased,purchased_cols)
df_purchased.to_csv('../data/itunes_library_purchased.csv', index=False)

print('Import of General Music')
df_generic = music_df_creation(generic_music,generic_music_cols)
df_generic.to_csv('../data/itunes_library_generic.csv', index=False)


#%%
# Reconstruct Playlists
# Extract playlists from the library, which are located into an array
playlist_array = extract_sub_node(main_dict, 'array')
playlists=list(playlist_array.findall('dict'))
print ('Number of Playlists:',str(len(playlists)))

plist_cols = get_existing_cols(playlists)
#forcing plist columns to get only relevant info
plist_cols = ['Parent Persistent ID', 'Playlist Persistent ID', 'Playlist ID', 'Name']
playlist_master_df, playlist_tracks_dfs = playlist_df_creation(playlists, plist_cols)

# %%
playlist_master_df.head(20)
# playlist_master_df.columns
# %%
