"""A script which adds initial rows of user-events to a database.

Usage:
>> python samples/events_api\inject_initial_rows_to_db.py \
--csv-path user_event_example_rows.csv \
--db-user USER --db-password PASS \
--db-name DB_NAME
"""
import argparse
import asyncio
import asyncpg


async def inject_initial_rows_from_csv(csv_path: str, database_url: str) -> None:
    print(database_url)
    pool = await asyncpg.create_pool(dsn=database_url, min_size=1, max_size=5)
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                with open(csv_path, 'rb') as csv_file:
                    await conn.copy_to_table(
                        'user_event',
                        source=csv_file,
                        format='csv',
                        header=True,
                        columns=('user_name', 'event_type', 'data', 'occurred_at')
                    )
    finally:
        await pool.close()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--csv-path', type=str, required=True,
        help='Path to csv file containing user events that we want to inject into the database.'
    )
    arg_parser.add_argument('--db-user', type=str, required=True)
    arg_parser.add_argument('--db-password', type=str, required=True)
    arg_parser.add_argument('--db-name', type=str, required=True)
    arg_parser.add_argument('--db-host', type=str, required=False, default='localhost')
    arg_parser.add_argument('--db-port', type=str, required=False, default='5432')
    args = arg_parser.parse_args()

    print("Starting injecting initial rows of user-events to database...")
    db_url_ = f"postgresql://{args.db_user}:{args.db_password}@{args.db_host}:{args.db_port}/{args.db_name}"
    asyncio.run(inject_initial_rows_from_csv(
        args.csv_path,
        db_url_
    ))
    print("Injection complete!")
