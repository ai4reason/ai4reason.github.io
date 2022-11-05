---
layout: main
hidden: true
subheader: Internal information system
---

# Members update

## Quickstart

The list of department members is stored in [docs/_data/members.yml](https://github.com/ai4reason/ai4reason.github.io/blob/main/docs/_data/members.yml/){:target="_blank"} in the repository.
Each department member is described by a YAML record with at least the following items.

🔴 Make sure the `dblp` key is set correctly.  Otherwise the list of publications will not contain publications of this member. ❗ 

+ 🔴 `dblp` ⚠️ 

## Member record

```yaml
- name: Jan Z. Rokycan
  dblp: pid/63/5214
  role: staff
  position: Senior researcher
  groups:
    - main
    - AR
  interests:
    - Automated Reasoning
    - Inductive Reasoning
  image: /images/members/user.png
  email: Jan_DOT_Rokycan_AT_gmail_DOT_com
  homepage: http://my.homepage.org/
  scholar: 
  orcid:
  phone: +240-44333-4322
  github: githabino
```

## ➡️  Required entries

* * * 

### `name` :: string

Member full name as a string.

* * * 

### `dblp` :: string


The [DBLP](https://dblp.uni-trier.de/) persistent ID of the member.

⚠️  This is essential for the list of publications to be automatically generated.

ℹ️  To obtain the DBLP persistent ID, click
[here](https://dblp.uni-trier.de/search/author){:target="_blank"} and search for
the member on DBLP.
On the author page, look at the url and extract the part starting with `pid` and ending before `.html`.
Usually it looks like `pid/39/11138` but it can look like `pid/24/5175-1` or `pid/v/RobertVeroff`.

* * * 

### `role` :: enum

Select the member position inside the department from the following values.

|---
| value | description
|-|-|-
| `pi` | principal investigators
| `staff` | general researchers
| `student` | PhD students
| `admin` | administratives
| `alumni` | ex-members

ℹ️  The roles are used to display members under different headings in the members page.

* * * 

### `groups` :: [group]

A YAML list of groups the member belongs to.
At least one group should be specified.
Allowed list items are:

+ `main` 
+ `AR` 
+ `FAI`
+ `FM`
+ `ML`

ℹ️  The members with the `main` group and with the role `pi` or `admin`, are listed
in the department [institution](/institution.html) page (as *main* members).


## ➡️  Informal entries

* * * 

### `position` :: string

Informal position description as a string.

* * *

### `interests` :: [string]

YAML list of strings with the research interests of this member.

⚠️  Keep the interest strings relatively short otherwise the page layout may break.


* * * 

### `image` :: url

* * * 

## ➡️  Link entries

* * *

### `email` :: string

Member email as a string.

* * *

### `phone` :: string

The phone number of this member in the format `+123-55555-4444`.

* * * 

### `homepage` :: url

The URL of the homepage of this member.

* * * 

### `scholar` :: string

The Google Scholar identificator of this member.

ℹ️  To obtain the Google Scholar identificator, search for the member
at [Google Scholar](https://scholar.google.com) and locate his profile.
Then extract the value of the `user` parameter (the text between `user=` and `&` or the end of line). 
Typically, it looks like `4pW-Je4AAAAJ`.

* * *
### `orcid` :: string

The [ORCID](https://orcid.org) ID of the member as a string.

* * * 

### `github` :: string

The [Github](https://github.com/) username of this member.
The link `https://github.com/${github}` with `${github}` substituted by the key value
should point to the Github's user page.

* * * 


## Next

+ [Members update](/internal/members.html)
+ [Content update](/internal/content.html)
+ [Publication list](/internal/biblio.html)


[YAML]: https://en.wikipedia.org/wiki/YAML/
{:target="_blank"} 



