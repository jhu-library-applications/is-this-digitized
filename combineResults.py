import pandas as pd
from datetime import datetime

result_files = {'internetArchiveResults.csv': 'AI', 'googleBooksResults.csv': 'GB', 'hathiTrustResults.csv': 'HT'}


def make_data_frame(frame_name, name_file):
    all_results = []
    try:
        frame_name = pd.read_csv(name_file)
        abbrev = result_files.get(name_file)
        for index, row in frame_name.iterrows():
            oclc = row[abbrev+'_oclc']
            oclc = str(oclc)
            link_name = abbrev+'_link'
            title_name = abbrev+'_title'
            link = row[link_name]
            title = row[title_name]
            result = {link_name: link, 'oclc_id': oclc, title_name: title}
            all_results.append(result)
        frame_name = pd.DataFrame.from_dict(all_results)
        frame_name.drop_duplicates(inplace=True)
        df_1 = pd.pivot_table(frame_name, index=['oclc_id'], values=link_name,
                                    aggfunc=lambda x: '|'.join(str(v) for v in x))
        df_2 = pd.pivot_table(frame_name, index=['oclc_id'], values=title_name,
                                    aggfunc=lambda x: '|'.join(str(v) for v in x))
        frame_name = pd.merge(df_1, df_2, how='outer', on='oclc_id')
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
mergedFrame.to_csv('combinedResults_' + dt + '.csv')