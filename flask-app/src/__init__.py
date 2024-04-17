# Some set up for the application 

from flask import Flask
from flaskext.mysql import MySQL

# create a MySQL object that we will use in other parts of the API
db = MySQL()

def create_app():
    app = Flask(__name__)
    
    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'

    # these are for the DB object to be able to connect to MySQL. 
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = open('/secrets/db_root_password.txt').readline().strip()
    app.config['MYSQL_DATABASE_HOST'] = 'db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'newHuskyLeagues'  # Change this to your DB name

    # Initialize the database object with the settings above. 
    db.init_app(app)
    
    # Add the default route
    # Can be accessed from a web browser
    # http://ip_address:port/
    # Example: localhost:8001
    @app.route("/")
    def welcome():
        return "<h1>Welcome to the 3200 boilerplate app</h1>"

    # Import the various Beluprint Objects
    from src.team_members.team_members import team_members
    from src.events.events import events
    from src.games.games import games
    from src.fans.fans import fans
    from src.referees.referees import referees
    from src.roles.roles import roles
    from src.sponsors.sponsors import sponsors
    from src.sports.sports import sports
    from src.teams.teams import teams

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.register_blueprint(team_members,url_prefix='/tm')
    app.register_blueprint(events, url_prefix='/e' )
    app.register_blueprint(games, url_prefix='/g' )
    app.register_blueprint(fans, url_prefix='/f' )
    app.register_blueprint(referees, url_prefix='/re' )
    app.register_blueprint(roles, url_prefix='/r' )
    app.register_blueprint(sponsors, url_prefix='/sp' )
    app.register_blueprint(sports, url_prefix='/s' )
    app.register_blueprint(teams, url_prefix='/t' )

    # Don't forget to return the app object
    return app