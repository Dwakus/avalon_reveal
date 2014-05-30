#!/usr/bin/env python

import web
import random


# Hacky avalon character stuff
characters = {
    5: ['servant', 'Merlin', 'Percival', 'Assassin', 'Morgana'],
    6: ['servant', 'servant', 'Merlin', 'Percival', 'Assassin', 'Morgana'],
    7: ['servant', 'servant', 'Merlin', 'Percival', 'Assassin', 'Morgana', 'minion'],
    8: ['servant', 'servant', 'servant', 'Merlin', 'Percival', 'Assassin', 'Morgana', 'minion'],
    9: ['servant', 'servant', 'servant', 'servant', 'Merlin', 'Percival', 'Assassin', 'Morgana', 'minion'],
    10: ['servant', 'servant', 'servant', 'servant', 'Merlin', 'Percival', 'Assassin', 'Morgana', 'minion', 'minion']
}

identity = {
    'servant': 'a Loyal Servant of Arthur',
    'Merlin': 'Merlin, a Loyal Servant of Arthur',
    'Percival': 'Percival, a Loyal Servant of Arthur',
    'minion': 'an Evil Minion of Mordred',
    'Assassin': 'the Assassin, an Evil Minion of Mordred',
    'Morgana': 'Morgana, an Evil Minion of Mordred'
}

def isEvil(char):
  return char in ['minion', 'Morgana', 'Assassin']

def isGood(char):
  return not isEvil(char)

def assignCharacters(players):
  chars = list(characters[len(players)])
  random.shuffle(chars)
  return chars

def messageForPlayer(player, players, chars):
  assert(len(chars) == len(players))
  assert(player in players)
  playerIdx = players.index(player)
  playerChar = chars[playerIdx]
  msg = "You are " + identity[playerChar]
  if isEvil(playerChar):
    msg += "\n\nOther Minions Are: "
    msg += ", ".join(players[i] for i in range(len(players)) if players[i] != player and isEvil(chars[i]))
  elif playerChar == 'Merlin':
    msg += "\n\nMinions of Mordred Are: "
    msg += ", ".join(players[i] for i in range(len(players)) if isEvil(chars[i]))
  elif playerChar == 'Percival':
    msg += "\n\nMerlin and Morgana are, in no particular order: "
    msg += " and ".join(players[i] for i in range(len(players)) if chars[i] == 'Merlin' or chars[i] == 'Morgana')
  return msg

urls = (
    '/', 'index',
    '/reveal', 'reveal'
)
render = web.template.render('templates/')

class index:
  def GET(self):
    return render.index()

class reveal:
  def POST(self):
    input = web.input()
    players = []
    emails = []
    for i in range(10):
      nameKey = "p{0}Name".format(i)
      emailKey = "p{0}Email".format(i)
      if len(input[nameKey]) > 0 and len(input[emailKey]) > 0:
        players.append(input[nameKey])
        emails.append(input[emailKey])

    chars = assignCharacters(players)
    for i in range(len(players)):
      web.sendmail('avalon@deancode.com', emails[i], "Avalon Reveal!", messageForPlayer(players[i], players, chars))
    
    return "Sent emails for {0} players".format(len(players))

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()

