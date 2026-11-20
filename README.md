# DataXAPI social & market data for Dify

Public data from Douyin, Xiaohongshu (RedNote), WeChat Official Accounts and Channels, Weibo, Bilibili, Zhihu and Kuaishou, plus Douyin's trend index (Juliang Suanshu), Xiaohongshu PGY (Pugongying), Douyin Xingtu, TikTok, YouTube, X and Reddit, in Dify workflows, chatflows and agents. One [DataXAPI](https://dataxapi.com/?ref=dify) key, 36 ready tools, and all 237 endpoints through *Find an endpoint* and *Call any endpoint*.

- **No sign-in to your own platform account**, no cookies, no QR login.
- **Pay per call; errors are not charged.** Each tool states its price, and every result says what that call cost (`billing.amount`, US dollars).
- **Free trial: up to 333 calls, no card.** Top up from $10; the balance does not expire.

Source: <https://github.com/data-x-api/dify-plugin-dataxapi> · Contact: support@dataxapi.com · Chinese: [readme/README_zh_Hans.md](readme/README_zh_Hans.md)

## Tools

The first 30 are the endpoints DataXAPI's customers called most in the last 30 days, by number of accounts.

<!-- tools:start -->
| Tool | What it returns | Price |
|---|---|---|
| Xiaohongshu note search | Search Xiaohongshu notes by terms: title, text, author, engagement counts, images, and a link that opens. Each says whether it is a brand partnership note on record. By relevance, newest, most liked, most commented or most saved; video or image notes only; published in the last day, week or half year. | $0.02 a call |
| Douyin video search | Search Douyin videos by terms, a page at a time, sorted by relevance, newest or most liked and filtered by time posted: caption, author with follower count, engagement counts. | $0.02 a call |
| WeChat Official Account articles | Get a page of the articles a WeChat Official Account published, newest first: title, digest, link, time published. Each also says whether it was the lead article or one below, its format and cover. The page's articles tab by default; its videos or pictures tab when asked. | $0.02 a call |
| Douyin video comments | Get a page of comments on a Douyin video: text, commenter, likes, reply count, time posted. | $0.002 a call |
| Douyin video play count | Get a Douyin video's counts as of now, by its ID: plays and likes. | $0.002 a call |
| Douyin video detail | Get one Douyin video or image post by ID or link: caption, author, engagement counts, time posted. | $0.002 a call |
| Douyin user videos | Get a page of the videos a Douyin account has posted, newest first: caption, engagement counts, time posted. | $0.002 a call |
| WeChat Official Account article detail | Get one WeChat Official Account article by its link: title, text, time published, the account's name and IDs. It also says whether it was the lead article or one below, its format, cover, digest, byline, "read the original" link and the IP location it was posted from. | $0.02 a call |
| Douyin user profile | Get a Douyin user's profile by account ID or profile link: name, handle, bio, follower, following and post counts, total likes, verification; in the full view also what the badge says, whether it is an organisation's or shop's (blue V), whether the profile has a product showcase, whether the account may sell live, and whether it is live now, with the room's ID. | $0.002 a call |
| Xiaohongshu note detail | Get one Xiaohongshu note by ID or link: title, text, author, engagement counts, images. It also says whether it is a brand partnership note on record. | $0.02 a call |
| Douyin user search | Search Douyin accounts by terms, a page at a time: account ID, display name, avatar, follower count, post count, total likes. | $0.002 a call |
| Douyin trend-index keyword trends | Get the day-by-day search index and composite index of a keyword, or of one to five keywords at once, on Douyin over a date range, from (the Douyin index), with the daily averages of the period, of the one before and of a year earlier. An index is the platform's score of volume, not a count of searches; days are calendar days in China time (UTC+8). | $0.006 a call |
| Douyin hot search board | Get a Douyin hot list: hot searches, rising topics, topic ranking, top search terms or the music chart, with rank and heat. | $0.002 a call |
| WeChat Search articles and videos | Get a page of WeChat Search results for search terms: Official Account articles and Channels videos mixed, each saying in type whether it is an article or a video; by relevance, newest or hottest, filtered by time posted, or articles only or videos only: title or description, the source account's name, time published, an article's link (with a band of reads on some), a video's likes and saves. WeChat Search gives no account ID. | $0.02 a call |
| WeChat Channels video search | Get a page of WeChat Channels videos for search terms through WeChat Search, by relevance, newest or hottest, filtered by time posted: description, the account's name and avatar, time published, likes and saves, length, cover. WeChat Search gives no account ID, and a video's ID is an encrypted one starting with export/: given as export_id to wechat_channels.videos.get it yields the numeric ID, the video file's address and the key that decrypts it; it expires, so use it soon. | $0.02 a call |
| WeChat Official Account live search | Find WeChat Official Accounts and service accounts for search terms through WeChat Search, closest first, possibly followed by less related ones: original ID, WeChat ID, name, bio, avatar, whether verified, owner, number of original articles. Charged per call; no followers or reads, for estimates of those use wechat_mp.accounts.search. | $0.02 a call |
| WeChat Channels video detail | Get one WeChat Channels video by its ID, a search result's export/ ID or its share link: description, author, time published, likes, comments, forwards, saves, and the video file's address with the key that decrypts it. | $0.02 a call |
| Xiaohongshu note comments | Get a page of top-level comments on a Xiaohongshu note by ID or link, newest first or hottest first: text, commenter, likes, reply count, time posted. | $0.02 a call |
| WeChat Channels account videos | Get a page of the videos a WeChat Channels account published, newest first, by the account's ID: description, time published, likes, comments, forwards, saves, length. | $0.02 a call |
| Xiaohongshu user notes | Get a page of the notes a Xiaohongshu account posted, by user ID or profile link: title, text, engagement counts, images, whether pinned. | $0.02 a call |
| Weibo realtime search | Get a page of Weibo posts for search terms, newest first: text (a long post is cut short here), author and follower count, likes, comments, reposts, video plays, pictures, topics. | $0.002 a call |
| Bilibili video search | Get a page of Bilibili videos for search terms, by relevance, newest or most played: title, uploader, views, likes, saves, comments, length. | $0.002 a call |
| Xiaohongshu user profile | Get a Xiaohongshu account by user ID or profile link: name, handle, bio, follower, following and note counts, verification, and the gender and region its profile shows. | $0.02 a call |
| Xiaohongshu PGY keyword search index | Get a keyword's day-by-day search index on Xiaohongshu over about the last three months, from the platform's creator marketplace, with each day's notes about the keyword and how often they were shown, read and engaged with. The platform sets the period; it cannot be chosen. The search index is the platform's index, not a count of searches; days are calendar days in China time (UTC+8). | $0.04 a call |
| WeChat Official Account article stats | Get the current counts of a WeChat Official Account article by its long link: reads, likes, recommends, shares, saves, comments. | $0.02 a call |
| WeChat Channels video comments | Get a page of top-level comments on a WeChat Channels video by its ID: text, commenter, likes, time posted, IP location. | $0.02 a call |
| Douyin trend-index related keywords | Get the keywords related to a keyword on Douyin in one week, from the platform's own keyword tool: those searched together with it and those that appear with it in content, each with its relevance, its place by relevance, its search index and its composite index. An index is the platform's score of volume, not a count of searches. | $0.002 a call |
| Zhihu content search | Get a page of Zhihu answers and articles matching a search; either kind alone, by relevance, newest or most upvoted. | $0.002 a call |
| Kuaishou video search | Search Kuaishou posts by terms, a page at a time, sorted newest or most liked first and filtered by time posted and video length: caption, author, play and engagement counts, time posted, whether it is a video or a photo set, and a video's length. | $0.02 a call |
| Douyin Xingtu creator search | Search Douyin creators on Xingtu by words in their name, filtered by followers, expected CPM (in yuan) and gender, or ordered by expected CPM, lowest first:Xingtu creator ID, name, location, content categories, followers; in the full view also what an integrated and a custom video cost, expected CPMs (in yuan), expected views, the last 30 days' interaction and completion ratios and median views, the e-commerce level, gender and content labels. The creator ID the other Xingtu endpoints take comes from here. | $0.004 a call |
| TikTok video search | Search TikTok videos by keyword, 30 a page; sort by relevance, likes or time posted, and limit how recently they were posted. | $0.002 a call |
| YouTube video transcript | Get the transcript of a YouTube video by ID or link: the whole text and timed segments. lang chooses the language of the captions. | $0.002 a call |
| X post search | Find X posts by search terms, most popular or newest first; the terms may use X's own search operators, such as from:handle. | $0.002 a call |
| Reddit post search | Get a page of Reddit posts matching a search, by relevance, newest or top score, optionally within a period. | $0.002 a call |
| Find an endpoint | Endpoints for a need described in plain words, with price and parameters | free |
| Call any endpoint | Any of the 237 endpoints by its ID | that endpoint's price |
<!-- tools:end -->

Live prices are on each endpoint's page at [dataxapi.com/apis](https://dataxapi.com/apis/?ref=dify). One call returns one page; a next page is a new call with `cursor`, charged on its own.

## What you can build

**A daily brief on competitors' WeChat Official Accounts.** *WeChat Official Account search* finds an account's original ID (starting with `gh_`) by name → *WeChat Official Account articles* gets the latest articles → an Iteration node runs *WeChat Official Account article stats* on each for reads, likes and shares → an LLM node writes the brief. Run it on a schedule.

**Xiaohongshu brand mentions, every day.** *Xiaohongshu note search* for your brand, sort `latest` → *Xiaohongshu note comments* on the most liked notes → an LLM node sorts praise, complaints and questions, with links.

**Check demand before picking a topic.** *Douyin trend-index keyword trends* gives one to five keywords' daily search index with the period before and a year before → *Douyin trend-index related keywords* → *Xiaohongshu PGY keyword search index by day* for the same words → an LLM node says which are rising.

**Let an agent find its own data.** Give the agent *Find an endpoint* (free) and *Call any endpoint*: it describes what it needs ("WeChat Channels comments", "a Bilibili creator's followers"), gets the endpoint and its parameters, then calls it.

## Setup

1. Create a key in the DataXAPI console: <https://dataxapi.com/console/keys/?ref=dify>.
2. Install the plugin from the Dify Marketplace, open its tool settings and paste the key (it starts with `dx_`).
3. Dify checks the key with `GET /v1/account`, which is free.

## What comes back

Each tool returns JSON with `data` (an `items` list or one object), `page.next_cursor`, `warnings`, `billing` (`amount`, `balance_after`) and `request_id`. Posts, comments and accounts have the same fields on every platform, so a workflow can switch platforms without changing the nodes after it. Fields: [dataxapi.com/docs](https://dataxapi.com/docs/?ref=dify). An error comes back as text naming the error code, whether anything was charged and whether to retry.

## Connection requirements

The plugin makes HTTPS requests to one host, `https://api.dataxapi.com`, with `Authorization: Bearer <key>` and `X-Source: dify`. No other network access is needed.

## Privacy

See [PRIVACY.md](PRIVACY.md) and <https://dataxapi.com/privacy/>.

## Develop and test locally

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt
.venv/bin/python -m pytest
```

The tests mock every HTTP request; they never call the paid API. The endpoint tools are written by `scripts/generate_tools.py` from DataXAPI's live catalog; run it again when the catalog or prices change.

## License

MIT
