
import argparse
import asyncio
import asyncpg


async def inject_initial_rows_from_csv(csv_path: str, database_url: str) -> None:
    pool = asyncpg.create_pool(database_url, minsize=1, maxsize=5)
    async with pool.acquire() as conn:
        async with conn.transaction():
            with open(csv_path) as csv_file:
                await conn.copy_to_table(
                    'user_event',
                    source=csv_file,
                    format='csv',
                    header=True,
                    columns=('user_name', 'event_type', 'data', 'occurred_at')
                )
    await pool.close()



if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--csv_path', type=str, required=True,
        help='Path to csv file containing user events that we want to inject into the database.'
    )
    arg_parser.add_argument('--db-user', type=str, required=True)
    arg_parser.add_argument('--db-password', type=str, required=True)
    arg_parser.add_argument('--db-name', type=str, required=True)
    arg_parser.add_argument('--db-host', type=str, required=False, default='localhost')
    arg_parser.add_argument('--db-port', type=str, required=False, default='5432')
    args = arg_parser.parse_args()

    print("Starting injecting initial rows of user-events to database...")
    asyncio.run(inject_initial_rows_from_csv(
        args.csv_path,
        f"postgresql://{args.db_user}:{args.db_password}@{args.db_host}:{args.db_port}/{args.db_name}"
    ))
    print("Injection complete!")
