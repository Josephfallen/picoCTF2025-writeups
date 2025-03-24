# **CTF Writeup: WebSocket Exploitation - "Chess Shark"**

## **Challenge Overview**
The challenge presented a WebSocket server at `ws://verbal-sleep.picoctf.net:60291/ws/`. Interacting with this server required using WebSocket clients like `wscat`. 

## **Approach**
I connected to the WebSocket server using `wscat`:

```bash
wscat -c ws://verbal-sleep.picoctf.net:60291/ws/
```

Once connected, I noticed that sending the command `eval -10000` resulted in a response:

```
> eval -10000
< Wow you're quite the chess shark!
```

This hinted that the server might be running some form of evaluation function that interprets the number provided.

## **Exploitation**
By increasing the negative number to `-1000000`, I triggered an unexpected response:

```
> eval -1000000
< Huh???? How can I be losing this badly... I resign... here's your flag: picoCTF{REDACTED}
```

This suggested that the server was handling evaluation results incorrectly and had an unintended condition that caused it to "resign" when the value was too low.

## **Conclusion**
This challenge demonstrated a classic example of **client-side WebSocket interaction exploitation**, where unexpected input values led to an unintended game logic failure, ultimately leaking the flag.
