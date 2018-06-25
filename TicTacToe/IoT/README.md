# Making a TicTacToe Machine with an AI which players can play against.

Project Plan

Shopping List:

4x4 Button Pad
9.95
https://www.sparkfun.com/products/7835
https://learn.sparkfun.com/tutorials/button-pad-hookup-guide

Button Driver
9.95
https://www.sparkfun.com/products/8033

FeatherWing OLED - 128x32 OLED
14.95
https://www.adafruit.com/product/2900

5mm RGBLED
1.95
https://www.sparkfun.com/products/9264

Raspberry Pie For Broker
36.99
https://www.newegg.com/Product/Product.aspx?Item=N82E16813300007&ignorebbr=1&nm_mc=KNC-GoogleAdwords-PC&cm_mmc=KNC-GoogleAdwords-PC-_-pla-_-Motherboard+%2F+CPU+%2F+VGA+Sets-_-N82E16813300007&gclid=CjwKEAiArvTFBRCLq5-7-MSJ0jMSJABHBvp0aWqcVYCB52ySxVmm9nBN28kGAC-Ti6hxjziASGapNRoCpdvw_wcB&gclsrc=aw.ds

****  Dont Need  ****
Assembled Feather Huzza
18.95
https://www.adafruit.com/products/3046
********

## Build Night 1

#### **Game Programming**

- Develop GameRules
  - Game Start Controls
    - Flash LEDS for game starting
    - How is first player determined
    - _Notes: Remember all controls must be run through the update command_
  - After Start
    - Lock Screen from Issuing new plays until the other user has completed its turn.
      - Prompt for which player turn it is
  - End Game
    - Identify when the game is a draw.
    - Identify when the game is a win / loss and notify appropriate player.

#### **Client -> Broker Programming**

- Each box has a unique ID. _(We should go with an email or Adafruit IO account name)_
- All clients communicate with broker over the same channel.
  - This channel allows clients to request to be game hosts; at which time the broker makes a new a channel based of the clients unique ID.
  - This channel also sends the stream information of game hosts to clients looking for a match.
  - The broker then manages the updating of clients as a game is played out.

#### **Broker Programming**

- Basic Stream that creates a new stream when a TicTacToe Box make itself available for match
