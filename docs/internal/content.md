---
layout: internal
button: ✏️  Content
index: 30
---

# Content update

💡 The links below open a new tab/window.

The content of the web department is stored in the Github repository
[ai4reason.github.io](https://github.com/ai4reason/ai4reason.github.io/){:target="_blank"}.
in 
[/docs](https://github.com/ai4reason/ai4reason.github.io/blob/main/docs/){:target="_blank"} folder.
Group web pages are stored in 
[/docs/groups](https://github.com/ai4reason/ai4reason.github.io/blob/main/docs/groups/){:target="_blank"} subfolders.

Most of the content is in the [Markdown](https://www.markdownguide.org/basic-syntax/){:target="_blank"} format.
New content can be added by updating repository Markdown files, and this can be easily done using the Github web interface.
You can check a basic [Markdown demonstration](https://pages-themes.github.io/leap-day/){:target="_blank"}.

ℹ️  The [kramdown](https://kramdown.gettalong.org/syntax.html/){:target="_blank"} extension is used insted of standard Markdown, and it can be utilized.

## Edit an existing page

1️⃣  Locate the file in the Github web interface for repository
[ai4reason.github.io](https://github.com/ai4reason/ai4reason.github.io/tree/main/docs){:target="_blank"},
most likely inside 
[/docs/groups/](https://github.com/ai4reason/ai4reason.github.io/tree/main/docs/groups){:target="_blank"} directory.

2️⃣  Click on the edit button.  You need to login to Github for this.

3️⃣  Edit the file appropriatelly.  You can use the preview to check your changes.  The rendered Markdown content will apear inside the content part of the web page.

4️⃣  Commit changes and start a pull request.  The web will be updated once the changes are merged.

⚠️  Do not edit the preamble of the file (between `---` lines).

💡 You can add some content even to the pages with auto-generated content (_members_ and _activities_).  Just do not change the 
[Liquid](https://shopify.github.io/liquid/){:target="_blank"}
and 
[Jekyll](https://jekyllrb.com/docs/){:target="_blank"}
directives.

## Add a new page

1️⃣  Locate the directory where to store the file in repository
[ai4reason.github.io](https://github.com/ai4reason/ai4reason.github.io/tree/main/docs){:target="_blank"},
most likely inside 
[/docs/groups/](https://github.com/ai4reason/ai4reason.github.io/tree/main/docs/groups){:target="_blank"} directory.

2️⃣  Add a new file by clicking button _Add file_.  You need to login to Github for this.

3️⃣  The file must start with a header with parameters, at least as follows.

```yaml
---
layout: AR
---
```

Select the `layout` for your group, that is, one of
`AR`, `FAI`, `FM`, `ML`, or `main` for the department-level web.
Put your Markdown content below.

💡 Every page will automatically generate a section button for the appropriate group (left buttons in the top menu).  See below how to [adjust this](#adjust-page-display).

4️⃣  Commit changes and start a pull request.  The web will be updated once the changes are merged.

## Adjust page display

The way a page is displayed can be adjusted by parameters in the page preamble.
The preamble is a YAML record, for example, as follows.

```yaml
---
layout: AR
title: Very long title
button: Long
index: 20
---
```

ℹ️  Use `layout` to select the group of this page (`AR`, `FAI`, `FM`, `ML`, or `main`).

Each page automatically generates a section button in the page menu.
Use `button` to adjust the title of the section button for this page. 
The default value is `title` which, in turn, defaults to the first heading on the page.

ℹ️  To prevent the page button to be generated in the menu, use `hidden: true`.

ℹ️  Buttons are sorted by `index` (defaults to the value of `button`).
For example, set the values of different pages to 1, 2, 3, etc. to sort them.

Other recognized fields are `header` and `subheader` which control the top 
headings of the web page.


## Continue ...

+ [Internal administration](/internal/index.html)
+ [Members update](/internal/members.html)
+ [Publication list](/internal/biblio.html)


