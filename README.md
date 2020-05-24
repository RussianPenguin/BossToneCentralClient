# BossToneCentral downloader

Download any patches for any proc from bosstonecentral.
It's very useful when you using fxfloorboard.

![BossToneCentral downloader](app.png)

* Select proc
* Select genre
* Select patch
* Download

File can be found in current application directory.

## Proc settings mapping

```
GT-100 v2/GT-001 => gt.json
GT-1 => gt-1.json
Katana => katana.json
Katana Air => katana-air.json
GT-1000 => gt-1000.json
GP-10 => gp-10.json
ME-80 => me-80.json
ME-25 => me-25.json
```

## Manual download instruction

Download two files
```
define=http://api.roland.com/app/btc/define/ + settings_for_your_proc
apps=define.btc.domain + define.btc.dataapi
```

Your can download any patches with next path

```
define.btc.domain + define.btc.liveset_file + apps.items.basename + '.tsl'
```
