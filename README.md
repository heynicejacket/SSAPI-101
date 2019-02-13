# Smartsheet API 101

I haven't seen a lot of bite-sized examples (or examples of any size) for interacting with the Smartsheet API. There are surely many people who need to pull data off Smartsheet, but are either not experienced programmers, or don't have the time to futz around with it.

While I'm not quite the former, I have a bit of the latter.

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

...to make things as obvious as posslbe for a complete beginner.

### Getting started with the Smartsheet API

### Using this code
