from app.database.database_manager import DatabaseManager


def run_app():
    db_manager = DatabaseManager()
    session = db_manager.get_session()


if __name__ == "__main__":
    run_app()
