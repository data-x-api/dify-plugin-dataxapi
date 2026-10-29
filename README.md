# DataXAPI social & market data for Dify

> Status: not published yet. This repository is a local build; it has not been submitted to the Dify Marketplace.

Source repository: <https://github.com/data-x-api/dify-plugin-dataxapi> · Contact: support@dataxapi.com ·
Chinese guide: [readme/README_zh_Hans.md](readme/README_zh_Hans.md)

[DataXAPI](https://dataxapi.com) returns public data from Douyin, Xiaohongshu (RedNote), WeChat Official Accounts,
WeChat Channels, Kuaishou, TikTok, Bilibili and other platforms in one response shape. This plugin brings it into Dify
workflows, chatflows and agents.

- No sign-in to your own platform account: you only need a DataXAPI API key.
- Charged per call from your DataXAPI balance; a call that errors is not charged. Each endpoint's price is on its page
  at [dataxapi.com/apis](https://dataxapi.com/apis/), and every result states what it cost (`billing.amount`, US dollars).
- One call returns one page. A next page is a new call with `cursor`, charged on its own.

## Tools

| Tool | What it returns | Platforms |
|---|---|---|
| WeChat Official Account articles | The articles an Official Account published, newest first | WeChat Official Accounts (ID starting with `gh_`) |
| Account posts | The posts or videos one account published | Douyin, Xiaohongshu, WeChat Channels, Kuaishou, TikTok, Bilibili |
| Post comments | The comments under one post, video or article | Douyin, Xiaohongshu, WeChat Channels, WeChat Official Accounts, Kuaishou, TikTok, Bilibili |
| Keyword search | Public posts matching search terms | Douyin, Xiaohongshu, WeChat Channels, WeChat Search, Kuaishou, TikTok |
| Call any endpoint | Any DataXAPI endpoint by its ID, with JSON parameters | Every endpoint listed at [dataxapi.com/apis](https://dataxapi.com/apis/) |

Each tool returns JSON with `data` (an `items` list or a single object), `page.next_cursor`, `warnings`, `billing`
(`amount`, `balance_after`) and `request_id`. Posts, comments and accounts use the same fields on every platform; see
[the shared objects](https://dataxapi.com/docs/).

## Setup

1. Create an API key in the DataXAPI console: <https://dataxapi.com/console/keys/?ref=dify>. Free trial: up to 333 calls,
   no card.
2. In Dify, install the plugin (from the Marketplace once it is listed, or from a local `.difypkg` file), open its
   tool settings and paste the key as the credential (it starts with `dx_`).
3. Dify checks the key with `GET /v1/account`, which is free.

## Usage

- In a **workflow**, add a tool node such as *Account posts*, choose the platform, and map the account ID from an
  earlier node. To read more pages, loop on `page.next_cursor`; each page is a charged call.
- In an **agent**, enable the tools you need. The agent picks the platform and fills the identifiers; the tool
  descriptions tell it that each page is a separate charged call.
- *Call any endpoint* example: endpoint `douyin.users.get`, parameters `{"id": "MS4w..."}`. Parameters for every
  endpoint are on its page at [dataxapi.com/apis](https://dataxapi.com/apis/).

Identifiers by platform for *Account posts*: Douyin `sec_uid` (starts with `MS4w`); Xiaohongshu user ID or profile link;
WeChat Channels ID (`v2_...@finder`); Kuaishou numeric user ID; TikTok handle without `@`; Bilibili `mid`.

## Connection requirements

The plugin makes HTTPS requests to one host, `https://api.dataxapi.com`, with the header
`Authorization: Bearer <key>` and the label `X-Source: dify`, so calls from Dify show up separately in your usage.
No other network access is needed. Errors come back as text that names the error code and says whether anything was
charged.

## Privacy

See [PRIVACY.md](PRIVACY.md) and the DataXAPI privacy policy at <https://dataxapi.com/privacy/>.

## Develop and test locally

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt
.venv/bin/python -m pytest
```

The tests mock every HTTP request; they never call the paid API.

To try the plugin against a Dify instance, copy `.env.example` to `.env`, fill in the remote debugging address and key
from the plugin debugging page of your Dify instance, and run `.venv/bin/python -m main`.

## Package and submit to the Dify Marketplace

1. Install the Dify plugin CLI (a separate binary from the
   [dify-plugin-daemon releases](https://github.com/langgenius/dify-plugin-daemon/releases); see the
   [Dify plugin docs](https://docs.dify.ai/en/develop-plugin/getting-started/getting-started-dify-plugin)).
2. From the parent directory: `dify plugin package ./dify-plugin-dataxapi`, then rename the result to
   `dataxapi-0.1.0.difypkg`. `.difyignore` keeps tests, the virtual environment and caches out of the package.
3. With the `data-x-api` GitHub account, fork [langgenius/dify-plugins](https://github.com/langgenius/dify-plugins),
   add only `dataxapi/dataxapi/dataxapi-0.1.0.difypkg`, and open a pull request using the repository's template.
   Risk level: Medium (it sends user-provided identifiers and links to an external API). Sensitive capabilities: none.
4. For a later version, bump `version` in `manifest.yaml`; an update PR adds only the new `.difypkg`.

## License

MIT
