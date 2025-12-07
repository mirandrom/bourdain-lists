# Finding Anthony Bourdain's Lost Li.st's in Common Crawl

## Background
On November 26, HN user gregsadetsky [posted a compilation of "Anthony Bourdain's Lost Li.st's"](https://news.ycombinator.com/item?id=46054879), including a table of those that are still lost. A lot of these seem fun and interesting, so I decided to try and find them. Just because they aren't on the Internet Archive, doesn't mean they haven't been saved somewhere else. It turns out that somewhere else is **Common Crawl**.

<table>
  <thead>
    <tr>
      <th>Title</th>
      <th>Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Things I No Longer Have Time or Patience For [link](parsed_html/li.st_Bourdain_things-i-no-longer-have-time-or-patience-for-1UsJAtbmYp0qxlBQSLbl2W)</td>
      <td>4/28/2016</td>
    </tr>
    <tr>
      <td>Nice Views</td>
      <td>3/4/2016</td>
    </tr>
    <tr>
      <td>If I Were Trapped on a Desert Island With Only Three TV Series</td>
      <td>3/2/2016</td>
    </tr>
    <tr>
      <td>The Film Nobody Ever Made</td>
      <td>2/25/2016</td>
    </tr>
    <tr>
      <td>I Want Them Back</td>
      <td>1/23/2016</td>
    </tr>
    <tr>
      <td>Objects of Desire</td>
      <td>1/21/2016</td>
    </tr>
    <tr>
      <td>David Bowie Related</td>
      <td>1/14/2016</td>
    </tr>
    <tr>
      <td>Four Spy Novels by Real Spies and One Not by a Spy</td>
      <td>11/6/2015</td>
    </tr>
    <tr>
      <td>Hotel Slut (That’s Me)</td>
      <td>11/7/2015</td>
    </tr>
    <tr>
      <td>Steaming Hot Porn</td>
      <td>10/18/2015</td>
    </tr>
    <tr>
      <td>5 Photos on My Phone, Chosen at Random</td>
      <td>10/16/2015</td>
    </tr>
    <tr>
      <td>People I’d Like to Be for a Day</td>
      <td>10/15/2015</td>
    </tr>
    <tr>
      <td>I’m Hungry and Would Be Very Happy to Eat Any of This Right Now</td>
      <td>10/2/2015</td>
    </tr>
    <tr>
      <td>Observations From a Beach</td>
      <td>9/27/2015</td>
    </tr>
    <tr>
      <td>Guilty Pleasures</td>
      <td>9/23/2015</td>
    </tr>
    <tr>
      <td>Some New York Sandwiches</td>
      <td>9/5/2015</td>
    </tr>
    <tr>
      <td>Great Dead Bars of New York</td>
      <td>8/19/2015</td>
    </tr>
  </tbody>
</table>

## Finding the lost lists on Common Crawl
Searching Common Crawl through their [web UI](https://index.commoncrawl.org/) is not a great experience. 

Instead I used [cdx_toolkit](https://github.com/cocrawler/cdx_toolkit) which allows us to easily search a range of crawls with `--crawl CC-MAIN-2015,CC-MAIN-2016,CC-MAIN-2017` and see which specific crawls contain which URLs.

```bash
cdxt -v --cc --crawl iter CC-MAIN-2015,CC-MAIN-2016,CC-MAIN-2017 iter "https://li.st/Bourdain/*"

...

INFO:cdx_toolkit:get_more: fetching cdx from https://index.commoncrawl.org/CC-MAIN-2017-51-index
INFO:cdx_toolkit:get_more: fetching cdx from https://index.commoncrawl.org/CC-MAIN-2017-47-index
INFO:cdx_toolkit:get_more: fetching cdx from https://index.commoncrawl.org/CC-MAIN-2017-43-index
INFO:cdx_toolkit:get_more: fetching cdx from https://index.commoncrawl.org/CC-MAIN-2017-39-index
status 200, timestamp 20170923054957, url https://li.st/Bourdain/5-photos-on-my-phone-chosen-at-random-0nsXCpUt69UbZvcMsOh4P3
status 200, timestamp 20170923092731, url https://li.st/Bourdain/caption-the-donald-4ooyAsCr5FSapB1kvlUlpy
status 200, timestamp 20170919134839, url https://li.st/Bourdain/observations-from-a-beach-0X3d0NujKKomnM2HIukguv
...
```

## Downloading and parsing the lost lists from Common Crawl
We can also use `cdx_toolkit` to download from Common Crawl, similarly to how we searched it. 
This will create a `warc.gz` file that we can process with [warcio](https://github.com/webrecorder/warcio). 


```bash
cdxt --cc --crawl CC-MAIN-2017 warc "https://li.st/Bourdain/*" 
python warc_to_html.py bourdain-000000.extracted.warc.gz parsed_html
```

There are some duplicates with the same URL, but there are also lists with different URLs that Anthony edited. 
In "Crimes Against Food" he seems to have had a change of heart, removing the Corn Dog and adding instead:
- The Half-Assed Muffin on an Eggs Benedict:
- Slurry of Soy Sauce and Wasabi
- Chicken Caesar
- "Kobe Meatballs" (ditto "Kobe Burger")

These aren't all the lost lists (I only downloaded `CC-MAIN-2017`), but hopefully the remaining ones are in `CC-MAIN-2015` and/or `CC-MAIN-2016`. 
Just be careful not to get your requests blocked by Common Crawl like I did, it seems the defaults in `cdx_toolkit` are too aggressive. 