# wikipedia-client
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/xyzpw/wikipedia-client/total)

A terminal client designed for reading Wikipedia pages.

![wikipedia-client-preview](https://github.com/xyzpw/wikipedia-client/assets/76017734/c119ffe5-a989-48ce-853e-101d2a0338ce)

## Usage
### Arguments
```text
title <title>  title of wikipedia page
related        displays topics related to the current wiki page
infobox        displays the infobox portion of page alone
pager          displays wiki page in paginated format
fullpage       displays full html page
```

#### title
The `title` argument is the specified title for the Wikipedia page to be displayed.

#### related
After displaying the Wikipedia page contents, a list of related pages will be displayed along with a brief description.
```text
Related Topics:
---------------
* Page Title - Brief description of page
----------------------------------------
```

#### infobox
Displays infobox of the Wikipedia page.

#### pager
Displays the Wiki page in paginated format.

#### fullpage
Displays the entirety of the specified Wikipedia page.
> [!NOTE]
> Using pager option is recommended with this parameter.

### Custom Config
A `config.json` file can be edited to set default values:
```json
{
    "hatnotes": true,
    "prettify": true,
    "cites": true
}
```
