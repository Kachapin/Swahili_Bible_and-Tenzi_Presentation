# Bible and Tenzi Hymn Presentation System

A browser-based presentation system for displaying hymn lyrics and Bible
verses during live services, presentations, recordings, and online
broadcasts. It includes separate controllers for hymn and Bible content,
corresponding display pages, and a shared Python web server.

The system is designed to work locally on a computer and can be
integrated with OBS Studio through Browser Sources.

## Table of Contents

-   [Features](#features)
-   [How the System Works](#how-the-system-works)
-   [Requirements](#requirements)
-   [Repository Structure](#repository-structure)
-   [Installation and Setup](#installation-and-setup)
-   [Starting and Stopping the
    Server](#starting-and-stopping-the-server)
-   [Shared Python Server](#shared-python-server)
-   [Part I --- Hymn Presentation
    System](#part-i--hymn-presentation-system)
-   [Part II --- Bible Presentation
    System](#part-ii--bible-presentation-system)
-   [OBS Studio Integration](#obs-studio-integration)
-   [Troubleshooting](#troubleshooting)
-   [Backup and Maintenance](#backup-and-maintenance)
-   [Development Notes and
    Limitations](#development-notes-and-limitations)
-   [Credits and Licensing](#credits-and-licensing)

## Features

-   Separate operator interfaces for hymn and Bible presentation.
-   Separate display pages that can be added to OBS Studio as Browser
    Sources.
-   A shared local Python server for passing presentation state from a
    controller to its display.
-   Local JSON files for hymn and Bible content.
-   Keyboard controls for common presentation actions.
-   Multiple Bible display layouts, including full-screen, lower-third,
    and half-screen modes.
-   Local presentation operation without requiring an external hosting
    service.
-   Customizable display appearance where supported by the controller.

## How the System Works

The application has four main parts:

1.  **Controller:** The operator selects content and controls what
    appears on the display.
2.  **Display page:** The page reads the current presentation state and
    renders the content.
3.  **Python server:** The server hosts the local files and provides an
    API for controller-to-display communication.
4.  **Content files:** JSON files store hymn lyrics and Bible text.

The general communication flow is:

``` text
Operator
   |
   v
Controller page
   |
   | POST /api/update
   v
Shared Python server
   |
   | GET /api/state
   v
Display page
   |
   v
OBS Studio Browser Source
```

The controller and display should use the same running server. Keep the
server terminal open while operating the application.

## Requirements

-   Windows, macOS, or Linux computer capable of running Python and a
    modern browser.
-   Python 3.
-   A modern web browser for opening and testing the controller pages.
-   OBS Studio, if the content will be used in a stream or video
    production.
-   The project files, including the Python server and required JSON
    data.
-   A Bible data file in the structure expected by the Bible controller.
-   Hymn data files in the structure expected by the hymn controller.

The instructions below use Windows Command Prompt examples. Adapt the
directory and command syntax for other operating systems.

## Repository Structure

The following is an example layout. Use the actual file and folder names
included in your copy of the repository. If you change the layout,
update any relative paths or URLs in the HTML files as necessary.

``` text
project/
├── README.md
├── server.py
├── Tenzi/
│   ├── Controller.html
│   ├── Display.html
│   └── Hymns/
│       ├── Tenzi_001.json
│       ├── Tenzi_002.json
│       └── ...
└── Bible/
    ├── Controller.html
    ├── bdisplay.html
    └── bible.json
```

The example uses `Tenzi/` for the hymn presentation system. You may
rename this folder to suit your preferred language or terminology. If
the hymn and Bible controllers have the same filename, keep them in
separate folders or rename them carefully and update any links or
instructions that refer to them.

## Installation and Setup

### 1. Obtain the project files

Download or clone the repository, or copy the supplied project files
into a folder on your computer.

Keep the server, controller pages, display pages, and data files in the
intended folder structure. Avoid moving files individually unless you
also check and update their paths.

### 2. Check Python

Open Command Prompt or a terminal and run:

``` bash
python --version
```

If that command is unavailable on Windows, try:

``` bash
py --version
```

Install Python 3 if it is not already installed. The server uses
Python's standard library, so the supplied server does not require
third-party Python packages.

### 3. Start the server from the correct directory

The server serves static files relative to the directory from which it
is launched. Start it from the project directory containing `server.py`,
unless the project instructions specify otherwise.

Example for Windows:

``` bat
cd /d "C:\path\to\project"
python server.py
```

If your system uses the Python launcher, you can use:

``` bat
py server.py
```

Leave the terminal window open while using the application.

### 4. Open the controller pages

Open the relevant controller HTML file in a browser. If a controller
relies on server APIs or browser features that do not work reliably when
opened directly as a local file, open it through the running local
server instead.

For example, if the file is served from the project root, open:

``` text
http://127.0.0.1:8000/Controller.html
```

For a controller inside a subfolder, use its corresponding URL, for
example:

``` text
http://127.0.0.1:8000/Tenzi/Controller.html
```

These are examples; use the actual path and filename in your
installation.

### 5. Test the display

Open the appropriate display page through the same server. Select a hymn
or Bible verse in the controller and confirm that the display updates.
Once this works in a normal browser, configure the display in OBS
Studio.

## Starting and Stopping the Server

### Start

1.  Open a terminal.
2.  Change to the directory containing `server.py`.
3.  Run `python server.py` or `py server.py`.
4.  Keep the terminal open during operation.

### Stop

Return to the terminal running the server and press `Ctrl+C`.

If the server fails to start, check whether another process is already
using port `8000`. If you change the port in `server.py`, update the
URLs used by the controllers, displays, and OBS Browser Sources
accordingly.

## Shared Python Server

The supplied server performs two main functions:

-   Serves the project's HTML, JSON, and other static files.
-   Stores the latest presentation state and makes it available to the
    display pages.

### API endpoints

  -----------------------------------------------------------------------
  Method                  Endpoint                Purpose
  ----------------------- ----------------------- -----------------------
  `GET`                   `/api/state`            Returns the current
                                                  presentation state as
                                                  JSON.

  `POST`                  `/api/update`           Receives a JSON
                                                  presentation state from
                                                  a controller and stores
                                                  it.

  `OPTIONS`               `/api/update`           Handles browser
                                                  preflight requests
                                                  where required.
  -----------------------------------------------------------------------

The display pages poll `/api/state` periodically to check for changes.
The controllers send updates to `/api/update`.

**Important:** The supplied server matches the `/api/state` path
exactly. Keep the display request as `/api/state`; adding a query string
such as `/api/state?x=1` may prevent the existing handler from
recognizing the endpoint unless the server is changed.

### Shared-state behaviour

The server maintains one current presentation state. Both controllers
use that same state endpoint. This means the most recent update from
either controller can replace the state previously sent by the other
controller.

For the unmodified server, operate one presentation system at a time.
For example, finish using the hymn controller before switching to the
Bible controller. If you need both displays to operate independently and
simultaneously, the server and client code must be changed to use
separate state endpoints or channels.

### Local network access

The server may listen on all network interfaces, depending on its
configuration. Use `http://127.0.0.1:8000` when the controller, display,
and OBS Studio are running on the same computer. Access from another
device requires the correct local network address, suitable firewall
rules, and careful consideration of network security.

The basic server is intended for local use and does not provide user
authentication or encrypted connections. Do not expose it directly to
the public internet.

## Part I --- Hymn Presentation System

### Overview

The hymn presentation system loads hymn information from JSON files. The
operator selects a hymn, navigates its stanzas or chorus, and sends the
selected content to the display page.

The exact controls and labels depend on the version of the hymn
controller included in the repository.

### Hymn data files

Hymn files use JSON. The filenames may follow a numbered pattern such as
`Tenzi_001.json`, `Tenzi_002.json`, and so on. Keep filenames consistent
with the naming pattern expected by the controller.

An illustrative data structure is:

``` json
{
  "number": 9,
  "title": "Example hymn title",
  "stanzas": [
    {
      "type": "stanza",
      "index": 1,
      "text": "First line of the stanza\nSecond line of the stanza"
    },
    {
      "type": "chorus",
      "index": 0,
      "text": "First line of the chorus\nSecond line of the chorus"
    }
  ]
}
```

This is an example of the general structure, not a replacement for the
schema required by the included controller. Check the existing sample
files and controller code before creating or editing hymn data.

### Adding or editing hymns

1.  Back up the original JSON file.
2.  Create or edit the file using valid JSON syntax.
3.  Preserve the property names and data types expected by the
    controller.
4.  Use `\n` within JSON strings to represent line breaks.
5.  Save the file using the filename pattern expected by the
    application.
6.  Load the hymn in the controller and check the output on the display.

A JSON validator can help identify missing commas, mismatched quotation
marks, and other syntax errors.

### Typical controls

Depending on the supplied controller version, controls may include:

-   Loading a hymn by number.
-   Moving between stanzas.
-   Displaying the chorus.
-   Moving forward or backward through content.
-   Clearing or blanking the display.
-   Using keyboard shortcuts for common actions.

Use the labels and shortcut hints shown by the actual controller as the
definitive reference for your version.

### Hymn display

Add the hymn display HTML page as an OBS Browser Source. The page must
be served from the same running server that receives updates from the
controller. Confirm that the display is readable at the intended output
resolution and that line breaks are preserved.

## Part II --- Bible Presentation System

### Overview

The Bible presentation system loads Bible text from a JSON data file.
The operator chooses a book, chapter, and verse or range of verses, then
selects how the text should appear on the display.

The documented baseline is **Bible Controller Version 1.4**. Preserve
its existing interface and behaviour when making future changes unless a
deliberate redesign is intended.

### Bible data format

The Bible data file uses a top-level `BIBLEBOOK` array. Each book
contains chapters, and each chapter contains verses.

A simplified example:

``` json
{
  "BIBLEBOOK": [
    {
      "book_number": "1",
      "book_name": "Example Book",
      "CHAPTER": [
        {
          "chapter_number": "1",
          "VERSES": [
            {
              "verse_number": "1",
              "verse_text": "Example verse text."
            },
            {
              "verse_number": "2",
              "verse_text": "Another example verse."
            }
          ]
        }
      ]
    }
  ]
}
```

The example illustrates the data hierarchy. Use the actual field names,
data types, and structure expected by the supplied Bible controller. The
controller's loader converts the source data into an internal
book/chapter/verse structure for navigation.

### Bible controller functions

Version 1.4 includes the following functions:

-   Select a book and chapter.
-   Navigate verses and verse batches.
-   Select a verse or a range of verses.
-   Use Shift-click for range selection in the verse list.
-   Move between chapters using the available controls or keyboard
    shortcuts.
-   Preview selected text before displaying it.
-   Choose a display layout.
-   Adjust supported text and background appearance settings.
-   Hide the displayed text when needed.

The exact appearance of controls may vary by screen size or browser.

### Keyboard controls

The Version 1.4 controller supports these navigation actions:

  Key         Action
  ----------- ---------------------------------------
  `←` / `→`   Move by one verse.
  `↑` / `↓`   Move through verse batches or pages.
  `[` / `]`   Move to the previous or next chapter.
  `Esc`       Hide the display.

If a shortcut does not work, click the controller page first so it has
keyboard focus. Browser or operating-system shortcuts may take priority
in some circumstances.

### Display layouts

The Bible system supports three main layouts:

-   **Full screen:** Displays the selected Bible text in a full-screen
    presentation area.
-   **Lower third:** Places the text in a band near the bottom of the
    output.
-   **Half screen:** Places the text in a half-screen area.

The exact placement and styling are controlled by the included display
page and controller settings. Check each layout in OBS before using it
in a live production.

### Bible display communication

The Bible display page polls the shared server's `/api/state` endpoint
and renders the current Bible presentation state. It should be opened
through the local server and added to OBS as a Browser Source.

If the display remains blank, verify that the server is running, that
the correct display page is loaded, and that the controller is sending a
presentation update.

## OBS Studio Integration

### Add a Browser Source

1.  Start the Python server.
2.  Open OBS Studio.
3.  Select the scene where the content should appear.
4.  Add a **Browser Source**.
5.  Enter the local URL for the relevant display page.
6.  Set the width and height to match the intended canvas or output
    area.
7.  Confirm that the page updates when you operate its controller.

Example URLs, assuming the example folder structure above:

``` text
http://127.0.0.1:8000/Tenzi/Display.html
http://127.0.0.1:8000/Bible/bdisplay.html
```

Use the actual paths in your installation. These example URLs will not
work unless the files are located at those paths and are served by the
running server.

### Recommended checks

-   Keep the Python server running throughout the presentation.
-   Test the controller and display together before going live.
-   Confirm that the OBS Browser Source uses the correct URL.
-   Check the text size, line breaks, contrast, and placement at the
    final output resolution.
-   If you edit HTML or JavaScript, refresh the browser page or refresh
    the Browser Source in OBS.
-   If changes do not appear, check whether the browser is displaying a
    cached copy.

## Troubleshooting

### The server does not start

-   Confirm that Python 3 is installed.
-   Confirm that the terminal is in the directory containing
    `server.py`.
-   Check the error message for a port conflict or syntax error.
-   If port `8000` is already in use, stop the conflicting process or
    change the port consistently across the application.

### The controller opens, but the display does not update

-   Confirm that the server is running.
-   Confirm that the controller and display are using the same server
    address and port.
-   Check the browser developer console for failed requests or
    JavaScript errors.
-   Confirm that the controller is sending updates to `/api/update`.
-   Confirm that the display is polling `/api/state` exactly.
-   Remember that the shared server stores only one current state.

### The display is blank

-   Send content from the controller rather than relying only on the
    initial page view.
-   Check the server terminal for request errors.
-   Verify that the correct display HTML file is loaded.
-   Confirm that the display is not in its blank or hidden state.
-   Refresh the display page or OBS Browser Source after checking the
    server.

### A hymn does not load

-   Confirm that the data file exists in the expected folder.
-   Check the filename and numbering format.
-   Validate the JSON syntax.
-   Compare the file with a known working hymn file.
-   Check the browser console for a failed file request or parsing
    error.

### Bible books or verses are missing

-   Confirm that the Bible JSON file is present and valid.
-   Verify the `BIBLEBOOK`, `CHAPTER`, and `VERSES` structure and the
    required property names.
-   Check that the data uses the expected string or number types.
-   Look for browser console errors during data loading.

### OBS shows an old version

-   Refresh the Browser Source.
-   Reopen the controller or display page.
-   If necessary, close and reopen the browser source after confirming
    that the files have been saved.

### Keyboard shortcuts do not respond

-   Click inside the controller window to give it focus.
-   Check whether another browser or operating-system shortcut is
    intercepting the key.
-   Use the visible controller controls to confirm that the application
    itself is working.

## Backup and Maintenance

Before changing the application:

1.  Back up the full project directory.
2.  Keep a copy of the working server and data files.
3.  Make one change at a time.
4.  Test the controller, display, and OBS Browser Source after each
    change.
5.  Keep a record of the version that is known to work.

Back up both the HTML/JavaScript files and the JSON content files.
Backing up only the controller does not preserve the hymns or Bible
data.

## Development Notes and Limitations

-   The supplied server is a lightweight local server built with
    Python's standard library.
-   The server holds the current state in memory. Restarting it resets
    that state; the controller can send a new state afterward.
-   The server's current state is shared by the hymn and Bible
    controllers, so the unmodified application is intended for
    sequential use of the two systems.
-   The server is not designed as a public-facing, secured web service.
-   File and folder names in this README are examples. The URLs must
    match the actual repository layout.
-   Changes to folder structure can require updates to fetch paths,
    data-file paths, and OBS Browser Source URLs.
-   Keep the Bible Controller Version 1.4 interface and behaviour intact
    when making maintenance changes unless the intended change
    specifically calls for a redesign.
-   The hymn controller's exact shortcuts and data schema should be
    verified against the version distributed with the repository.

## Credits and Licensing

Author: Kelvin Kachapin
special mention to [shemmjunior]([https://github.com](https://github.com/shemmjunior)) whom I used his Swahili Bible Edition for my bible.json file


Permited to use this controller in church and modify to suit your needs, 
This code cannot be sold or used for financial gain including those that have been modified from this code
text, hymn lyrics, fonts, images, and other assets may legally.
