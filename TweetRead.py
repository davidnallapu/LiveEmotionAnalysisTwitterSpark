import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json


# Set up your credentials
consumer_key='NjMPdJl510sXXlqV1ub0RN32m'
consumer_secret='krJtHkcwButxBx7dhNL4KKKD87fFWiDS9J3DpyXIRIAyskJvwR'
access_token ='629349951-zYoZn8C7QdtQpKbF1vy784UeufqN5gbkK3VboIUe'
access_secret='bYJ0cAho8nUEQYbp93oR0boCvaFETMTjFMK5wqiu0lC92'


class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket

  def on_data(self, data):
      try:
          msg = json.loads( data )
          print( msg['text'].encode('utf-8') )
          f = open("tweets.txt", "a")
          f.write(str(msg['text'])+" ")
          f.close()
          self.client_socket.send( msg['text'].encode('utf-8'))
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True

def sendData(c_socket):
  print('start sending data from Twitter to socket')
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)
  # start sending data from the Streaming API 
  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track=['biden'], languages=["en"])

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "127.0.0.1"     # Get local machine name
  port = 1119                 # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )