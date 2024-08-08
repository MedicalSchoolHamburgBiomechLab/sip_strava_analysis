from pathlib import Path

import pandas as pd

from db import init_db, Session
from models import *

PATH_DATA_ROOT = '/Users/dominikfohrmann/data/'


def read_activity_overview() -> pd.DataFrame:
    path_to_file = Path(PATH_DATA_ROOT).joinpath('STRAVA_activities_all.xlsx')
    return pd.read_excel(path_to_file, index_col=0)


def read_stream_file(activity: ActivityModel):
    filename = f'{activity.strava_activity_id}.csv'
    path_to_file = Path(PATH_DATA_ROOT).joinpath('stream_files', filename)
    if not path_to_file.exists():
        return
    df_stream = pd.read_csv(path_to_file, index_col=0)
    # Iterate over the stream types and create a StreamModel for each
    for stream_type in df_stream.columns:
        stream_data = df_stream[stream_type].values
        stream_model = StreamModel(activity_id=activity.id,
                                   stream_type=stream_type,
                                   stream_data=stream_data)
        stream_model.save()


def create_activity(row: pd.Series) -> ActivityModel:
    strava_activity_id = row.get('strava_activity_id')
    activity = ActivityModel.find_by_strava_activity_id(strava_activity_id)
    if activity:
        return activity

    distance = row.get('distance')
    moving_time = row.get('moving_time')
    total_elevation_gain = row.get('total_elevation_gain')
    activity_type = row.get('activity_type')
    start_date = row.get('start_date')
    start_date = pd.to_datetime(start_date)
    start_date_local = row.get('start_date_local')
    start_date_local = pd.to_datetime(start_date_local)
    new_activity = ActivityModel(athlete_id=athlete.id,
                                 strava_activity_id=strava_activity_id,
                                 distance=distance,
                                 moving_time=moving_time,
                                 total_elevation_gain=total_elevation_gain,
                                 activity_type=activity_type,
                                 start_date=start_date,
                                 start_date_local=start_date_local)
    new_activity.save()
    return new_activity


if __name__ == '__main__':
    init_db()  # Initialize the database and create tables

    df = read_activity_overview()

    session = Session()  # Create a new session for bulk operations

    for i, (index, row) in enumerate(df.iterrows()):
        # Check if the athlete already exists
        subject_id = row.get('subject_id')
        athlete = AthleteModel.find_by_subject_id(subject_id)
        if not athlete:
            # If the athlete doesn't exist, create and add them to the session
            athlete = AthleteModel(strava_id=row.get('strava_athlete_id'), subject_id=subject_id)
            athlete.save()
        # Read the activity data
        activity = create_activity(row)
        print(f'Activity: {activity} ({i}/{len(df)})')
        # Read the stream data
        read_stream_file(activity)

    # Commit session after adding all athletes to persist changes
    session.commit()
    session.close()
