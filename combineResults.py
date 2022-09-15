import pandas as pd
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='Enter filename with csv.')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter filename (including \'.csv\'): ')

result_files = {'internetArchiveResults.csv': 'AI', 'googleBooksResults.csv': 'GB', 'hathiTrustResults.csv': 'HT'}


def make_data_frame(frame_name, name_file):
    all_results = []
    try:
        frame_name = pd.read_csv(name_file)
        abbrev = result_files.get(name_file)
        for index, row in frame_name.iterrows():
            oclc = row[abbrev+'oclc']
            link_name = abbrev+'link'
            title_name = abbrev+'title'
            link = row[link_name]
            result = {link_name: link, 'oclc_id': oclc}
            all_results.append(result)
        frame_name = pd.DataFrame.from_dict(all_results)
        frame_name.drop_duplicates(inplace=True)
        frame_name = pd.pivot_table(frame_name, index=['oclc_id'], values=link_name,
                                    aggfunc=lambda x: '|'.join(str(v) for v in x))
        frames.append(frame_name)
    except pd.errors.EmptyDataError:
        pass


frames = []
for count, filename in enumerate(list(result_files.keys())):
    make_data_frame("df_{}".format(count), filename)

merged = []
for count, frame in enumerate(frames):
    if count == 0:
        new_df = pd.merge(frame, frames[count + 1], how='outer', on='oclc_id')
        merged.append(new_df)
    elif count == 1:
        pass
    else:
        new_df = pd.merge(merged[0], frame, how='outer', on='oclc_id')
        merged[0] = new_df

print(merged[0])
mergedFrame = merged[0]
print(mergedFrame.columns)
print(mergedFrame.head)
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
mergedFrame.to_csv('mergedMultiple_' + dt + '.csv')