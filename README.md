# scrape_latest_user_agent

Obtain the latest user agent of a browser and operating system.

The user agent is scraped from [whatismybrowser.com](https://www.whatismybrowser.com).

## Usage

```
$ ./scrape_latest_user_agent.py --help
usage: scrape_latest_user_agent.py [-h] [--operating-system {windows,mac_os,linux}] {chrome,firefox}

Obtain the latest user agent of a browser and operating system

positional arguments:
  {chrome,firefox}      The browser for which to obtain the latest user agent.

optional arguments:
  -h, --help            show this help message and exit
  --operating-system {windows,mac_os,linux}

The user agent is scraped from whatismybrowser.com.
```


### Example

```
$ ./scrape_latest_user_agent.py 'chrome' --operating-system 'linux'
```

**Output:**
```
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
```

:thumbsup:
