---
layout: main
hidden: true
subheader: internals
---

# Members update

The list of members of the department is stored in the repository file 
[docs/_data/members.yml](https://github.com/ai4reason/ai4reason.github.io/blob/main/docs/_data/members.yml/){:target="_blank"}
in the 
[YAML](https://en.wikipedia.org/wiki/YAML/){:target="_blank"} 
format.

## Quickstart

To edit the list of department members proceed as follows.

1️⃣  Open the members file [docs/_data/members.yml](https://github.com/ai4reason/ai4reason.github.io/blob/main/docs/_data/members.yml/){:target="_blank"} in the Github web interface.

2️⃣  Click on the edit button.  You need to login to Github for this.

3️⃣  Locate the YAML record to edit or create a new one in the following form.

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

4️⃣  Edit the fields appropriately.  See below for field descriptions.

⚠️  At least the [required fields](#--required-fields) `name`, `dblp`, `role`, and `groups` should be set.

🔴 Make sure the `dblp` [field](#dblp--string) is set correctly.  Otherwise the list of publications will not contain publications of this member. ❗ 

5️⃣  Describe _Commit changes_ and  start a pull request.  Once the pull request is merged, the web page will become updated in a couple of minutes.


## ➡️  Required fields

The required fields should be set for every record.

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


## ➡️  Informal fields

Informal fields provide basic member information to be displayed on the members page.

* * * 

### `image` :: url

A photo of the member, preferably in a 4:3 format (vertical).
The url can be
+ an external link, like `https://my.page/image.png`, or 
+ a local link like `/images/members/user.png`.

The local links are relative to directory
[/docs](https://github.com/ai4reason/ai4reason.github.io/tree/main/docs){:target="_blank"} 
in the repo.
Photos can be uploaded into folder
[/docs/images/members](https://github.com/ai4reason/ai4reason.github.io/tree/main/docs/images/members){:target="_blank"}.


ℹ️  Generic photo `/images/members/user.png` should be used if no photo is available.

* * * 

### `position` :: string

Informal position description as a string, like _Junior Researcher_.

* * *

### `interests` :: [string]

YAML list of strings with the research interests of this member.

⚠️  Keep the interest strings relatively short otherwise the page layout may break.


* * * 

## ➡️  Link fields

Link fields are rendered as linked images next to the member photo.
Additional link fields can be implemented on demand.

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

## Continue ...

+ [Content update](/internal/content.html)
+ [Publication list](/internal/biblio.html)
+ [General pages administration](/internal/index.html)


