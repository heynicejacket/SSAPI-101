# Smartsheet API 101

I haven't seen a lot of bite-sized examples (or examples of any size) for interacting with the Smartsheet API. There are surely many people who need to pull data off Smartsheet, but are either not experienced programmers, or don't have the time to futz around with it.

This is intended as a one stop shop, growing repository of simple examples of how to I/O your Smartsheet assets, manipulate the data therein, and push it to other services.

**Please note:** I'm an advocate of tool democratization. These examples are written far more long hand than necessary, and I've opted for spelling out the logic wherever possible (with accompanying comments). These are not examples of Pythonic best practices. For example, I've opted for:

```
p_col = False
if i == 0:
  p_col = True
new_column_dict = {'title': col, 'primary': p_col, ... }
```

...rather than simply:

```
new_column_dict = {'title': col_title, 'primary': i == 0, ... }
```

...to make what's going on as clear as posslbe for a complete beginner.

## Getting started with the Smartsheet API

These examples require you to have a Smartsheet access token (you can find instructions for that <a href="http://smartsheet-platform.github.io/api-docs/#authentication-and-access-tokens">here</a>, and most require you to know the ID of the sheet that you're trying to interact with.

There are a lot of ways to get sheet_id, but in general, if you're new to working with APIs, <a href="https://www.getpostman.com/">Postman</a> is a great tool. They have a <a href="https://www.youtube.com/watch?v=YKalL1rVDOE&list=PLM-7VG-sgbtBsenu0CM-UF3NZj3hQFs7E">series of getting started with APIs videos here</a>, if you are so inclined.

If you want a quick start, <a href="https://www.youtube.com/watch?v=FPXXY_G7eH8&t=646s">this video</a> (queued to exactly what you need to watch) from Smartsheet gets you the basics for how to generate an access token and retrieve a list of your sheets, with:

```
https://api.smartsheet.com/2.0/sheets/?includeAll=true
```

...which will get you a long list that looks like this:

```
{
    "pageNumber": 1,
    "totalPages": 1,
    "totalCount": 333,
    "data": [
        {
            "id": 745780222344261,
            "name": "SODO Happy Hour Spots",
            "accessLevel": "OWNER",
            "permalink": "https://app.smartsheet.com/sheets/6RmVPJrpq34tevgbega9384rth3a4rhh",
            "createdAt": "2019-02-23T17:52:40Z",
            "modifiedAt": "2019-02-29T17:37:13Z"
        },
        {
        ...
```

That "id" is the sheet_id. Everything has an ID - workspaces, reports, sheets, columns, rows, cells.

Lastly, install the smartsheet sdk in the command line with:

```
pip install smartsheet-python-sdk
```

...and you've got enough to be dangerous.


## Using this code
