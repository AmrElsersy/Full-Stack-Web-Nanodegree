
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import Column, String, Integer , ForeignKey,Boolean, ARRAY , DateTime 
import datetime
from datetime import datetime

db = SQLAlchemy()
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    seeking_talent = Column(Boolean)
    seeking_description = Column (String)
    website = Column(String)
    genres = Column( ARRAY(String) )
    # xxxxxTODO: implement any missing fields, as a database migration using Flask-Migrate 
    shows = db.relationship('Show',backref='venue',lazy = True)

    def __repr__ (self):
        return 'Venue ' + str(self.id) + ': ' + self.name

    def add(self):
      db.session.add(self)
      db.session.commit()

    def getVenue(self):
      upcoming_shows = Show.query.filter(Show.venue_id == self.id and Show.start_time > datetime.now()).all()
      data = {
        "id" :  self.id,
        "name" : self.name,
        "num_upcoming_shows" : len(upcoming_shows)
      }
      return data

    def getAllInformation(self):
      upcoming_shows = [s.getShow_with_artist() for s in Show.query.filter( Show.venue_id == self.id , Show.start_time > datetime.now() ).all()]
      past_shows = [s.getShow_with_artist() for s in Show.query.filter(Show.venue_id == self.id , Show.start_time <= datetime.now() ).all()]
      my_genres = self.genres if self.genres is not None else []

      print("upcomming ##################")
      for s in upcoming_shows:
        print(s["start_time"],", now:",datetime.now(),",utcnow",datetime.utcnow())
      print("#############################")
      print("past ##################")
      for s in past_shows:
        print(s["start_time"],", now:",datetime.now(),",utcnow",datetime.utcnow())
      print("#############################")
      
      print(my_genres)
      return {
      "id": self.id,
      "name": self.name,
      # "genres": self.genres.split(',') ,
      "genres" : my_genres,
      "address": self.address,
      "city": self.city,
      "state": self.state,
      "phone": self.phone,
      "website": self.website,
      "facebook_link": self.facebook_link,
      "seeking_talent": self.seeking_talent,
      "seeking_description": self.seeking_description,
      "image_link": self.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),      
       }
  
class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    seeking_venue = Column(Boolean)
    seeking_description = Column (String)
    website = Column(String)
    genres = Column(ARRAY(String) )
    # xxxxTODO: implement any missing fields, as a database migration using Flask-Migrate done
    shows = db.relationship('Show',backref='artist',lazy = True)
    def __repr__ (self):
        return 'Artist ' + str(self.id) + ': ' + self.name

    def add(self):
      db.session.add(self)
      db.session.commit()
    def getGeneralInfo(self):
      return {
        "id" : self.id,
        "name" : self.name
      }
    def getAllInformation(self):
      upcoming_shows = [s.getShow_with_venue() for s in Show.query.filter( Show.artist_id == self.id , Show.start_time > datetime.now() ).all()]
      past_shows = [s.getShow_with_venue() for s in Show.query.filter(Show.artist_id == self.id , Show.start_time <= datetime.now() ).all()]
      my_genres = self.genres if self.genres is not None else []
      
      print(my_genres)
      return {
      "id": self.id,
      "name": self.name,
      "genres" : my_genres,
      "city": self.city,
      "state": self.state,
      "phone": self.phone,
      "website": self.website,
      "facebook_link": self.facebook_link,
      "seeking_venue": self.seeking_venue,
      "seeking_description": self.seeking_description,
      "image_link": self.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),      
       }

    def getArtist(self):
      upcoming_shows = Show.query.filter(Show.artist_id == self.id and Show.start_time > datetime.now()).all()
      data = {
        "id" :  self.id,
        "name" : self.name,
        "num_upcoming_shows" : len(upcoming_shows)
      }
      return data


# xxxxTODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = "show"
    id = db.Column(Integer, primary_key = True)

    artist_id = db.Column(Integer, ForeignKey("artist.id"))
    venue_id = db.Column(Integer,ForeignKey("venue.id"))
    start_time = db.Column(DateTime, default=datetime.now())

    def __repr__ (self):
        return 'Show ' + str(self.artist_id) + ',' + str(self.venue_id) 

    def add(self):
      db.session.add(self)
      db.session.commit()

    def getShow_with_artist(self):
      return {
        "artist_id": self.artist_id,
        "artist_name": self.artist.name,
        "artist_image_link": self.artist.image_link,
        "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }
    def getShow_with_venue(self) :
      return {
        "venue_id": self.venue_id,
        "venue_name": self.venue.name,
        "venue_image_link": self.venue.image_link,
        "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }
    def getShow(self):
      return {
        "venue_id": self.venue_id,
        "venue_name": self.venue.name,
        "artist_id": self.artist_id,
        "artist_name": self.artist.name,
        "artist_image_link": self.artist.image_link,
        "start_time": self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      }

