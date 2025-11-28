class Config():
    DEBUG=False
    SQLALCHEMY_TRACK_MODIFCATIONS=False

class LocalDevelopementConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="sqlite:///parking_lot_V2.sqlite3"  # connect with db instance folder is created with
    # JSON web Token: User gets a token to client and is encrypted
    JWT_SECRET_KEY="rjp23112005" # this is required for encryption using secret key in jwt abt user info
