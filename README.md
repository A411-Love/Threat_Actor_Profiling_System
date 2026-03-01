<!-- The Threat Actor Profiling System is a Python-based OSINT (Open Source Intelligence) tool designed to analyze a username across multiple online platforms and generate a structured risk assessment.

Tool created by : Anush Deshar

The system automates digital footprint analysis by scanning publicly available profiles, detecting suspicious indicators, and calculating a threat score based on predefined logic.

Features

Cross-platform username detection

Detection of known threat actors (manual intelligence database)

Suspicious keyword analysis

Threat score calculation (0–100 scale)

Risk level classification (Low / Medium / High / Critical)

Clickable profile links

Search history tracking

GUI-based interface using Tkinter

Supported Platforms

The tool checks username presence on platforms such as:

GitHub

Twitter

Reddit

Instagram

LinkedIn

Facebook

TikTok

Pinterest

Medium

YouTube

StackOverflow

SoundCloud

HackerOne

TryHackMe

Bugcrowd

Technologies Used

Python 3

Tkinter (GUI Framework)

Requests Library (HTTP handling)

BeautifulSoup (HTML parsing)

How It Works

The user enters a username.

The system constructs profile URLs for each platform.

HTTP requests are sent to check profile existence.

The system checks for known threat actor matches.

Username is scanned for suspicious keywords.

A threat score is calculated.

Risk level is classified and displayed.

Threat Scoring Logic

The risk score is based on:

Number of platforms detected

Presence on cybersecurity platforms

Suspicious keywords in username

Known threat actor match

Threat Scoring Logic

The risk score is based on:

Number of platforms detected

Presence on cybersecurity platforms

Suspicious keywords in username

Known threat actor match 

Ethical Considerations

This tool uses only publicly available information and does not bypass authentication or perform unauthorized access. It is intended for educational and academic purposes only.
-->