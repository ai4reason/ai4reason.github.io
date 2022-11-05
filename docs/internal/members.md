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
  github: githabino
```

## ➡️  Required entries

* * * 

### `name` :: string

Member full name as a string.

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

### `homepage` :: url

The URL of the homepage of this member.

* * * 

### `scholar` :: string

The Google Scholar identificator of this member.

* * * 

### `dblp` :: string

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



