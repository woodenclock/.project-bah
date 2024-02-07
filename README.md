# Big At Heart Volunteer Bot

Welcome to the Big At Heart Volunteer Bot! This Telegram bot is designed to streamline the volunteer enrollment process and provide a convenient way for users to explore and register for volunteering opportunities. The bot also facilitates event tracking, feedback collection, and certificate issuance for volunteers.

## Table of Contents

1. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
2. [Usage](#usage)
    - [Enrolling as a Volunteer](#enrolling-as-a-volunteer)
    - [Browsing Volunteer Opportunities](#browsing-volunteer-opportunities)
    - [Viewing Registered, Attended, and Upcoming Events](#viewing-registered-attended-and-upcoming-events)
    - [Providing Feedback](#providing-feedback)
    - [Requesting Certificates](#requesting-certificates)
3. [Data Storage](#data-storage)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- [Telegram](https://telegram.org/) account
- Access to the master Google Spreadsheet for volunteer data storage

### Installation

1. Clone the repository:

   ```bash
   https://github.com/hack4good-awesometeam/.project-bah.git
   ```

2. Configure the bot with your Telegram Bot Token and Google Sheets API credentials.

3. Deploy the bot using your preferred hosting service.

4. Start the bot.

## Usage 

### Enrolling as a Volunteer

`/enroll` initiates the volunteer enrollment process.<br />
Users are prompted to input information such as name, age, gender, work status, immigration status, interests, and skills. Upon submission, a summary of the entered details is displayed. Users can proceed to browse volunteering opportunities after enrollment.

### Browsing Volunteer Opportunities

`/browse` displays a list of available volunteering opportunities.<br />
Users can view a list of opportunities and sign up for events by clicking the provided Registration link. 

### Viewing Registered, Attended, and Upcoming Events

- `/register`: Show events users have registered for.
- `/attended`: Show events users have attended.
- `/upcoming`: Show upcoming events users have registered for.

### Providing Feedback

`/feedback` provides access to a feedback form.<br />
Users can choose an event and submit feedback and reflections through the provided Google Form.

### Requesting Certificates

`/certificate` generates a certificate for attended events.
A PDF certificate will be provided for the event the user has attended.

## Data Storage

All user information, including enrollment details and event registrations, is stored in the master Google Spreadsheet. The data can be used to generate graphs and charts, helping Big At Heart understand the patterns of its volunteer pool.
